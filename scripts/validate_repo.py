#!/usr/bin/env python3
"""Fail closed when the public repository crosses its text-only privacy boundary.

The validator inspects the files this project actually publishes. Inside a Git
checkout that means the tracked files; in an extracted archive it means every
file except local build and editor state. Either way a virtual environment,
cache, or scratch directory in the working tree can never fail the run.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
MIN_PYTHON = (3, 9)

# Local environment state that is never published. Only consulted when the
# validator runs outside a Git checkout, where tracked-file discovery fails.
UNPUBLISHED_DIRS = {
    ".git",
    ".idea",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    ".vscode",
    ".work",
    "__pycache__",
    "env",
    "node_modules",
    "site-packages",
    "venv",
}

REQUIRED = {
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
    ".github/dependabot.yml",
    ".github/workflows/ci.yml",
    ".github/workflows/release-gate.yml",
    "BOOTSTRAP_PROMPT.md",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "MASTER_PROMPT.md",
    "README.md",
    "SECURITY.md",
    "SESSION_PROMPT.md",
    "START_HERE.md",
    "VERSION",
    "docs/architecture.md",
    "docs/install.md",
    "docs/privacy.md",
    "docs/tool-selection.md",
    "docs/troubleshooting.md",
    "examples/README.md",
    "examples/extracted-source.md",
    "examples/pipeline.mmd",
    "examples/report.md",
    "fixtures/sample.md",
    "patterns/README.md",
    "patterns/extract_insights.md",
    "patterns/extract_tables.md",
    "patterns/generate_d2.md",
    "patterns/synthesize_report.md",
    "scripts/release_gate.py",
    "scripts/smoke_test.py",
    "scripts/validate_repo.py",
    "templates/chart-theme.json",
    "templates/report.typ",
    "templates/slides.md",
    "tests/test_repository.py",
}

ALLOWED_SUFFIXES = {"", ".d2", ".json", ".md", ".mmd", ".py", ".typ", ".txt", ".yaml", ".yml"}

# Files whose whole job is to define the banned vocabulary below. Scanning them
# for their own patterns would always match, so the text-content rules skip
# them. Every other rule, including secrets and machine paths, still applies.
PATTERN_DEFINITION_FILES = {"scripts/validate_repo.py"}

# Assistant-platform and consumer sync-service names. The project stays
# vendor-neutral: prompts describe capabilities, never brands.
FORBIDDEN_PLATFORM_TERMS = re.compile(
    r"\b(?:Claude|ChatGPT|Codex|Cursor|Copilot|Gemini|OneDrive|Dropbox|iCloud|SharePoint|Google Drive)\b",
    re.IGNORECASE,
)
# The owner is already visible in the hosting URL, but publishing it again in
# source files creates an unnecessary account breadcrumb. Documentation should
# use relative links or a repository-URL placeholder instead.
SELF_REPOSITORY_LINK = re.compile(
    r"https?://github\.com/[^/\s)]+/IngestReasonCreate(?:\.git|/|\b)",
    re.IGNORECASE,
)
FORBIDDEN_NAMES = {"AGENTS.md", "CLAUDE.md", "agent.md", ".mcp.json", "reference.docx"}
FORBIDDEN_PARTS = {
    ".agents",
    ".codex",
    ".cursor",
    "cache",
    "dist",
    "downloads",
    "models",
    "outputs",
    "renders",
}

PERSONAL_PATHS = (
    re.compile(r"\b[A-Za-z]:[\\/]"),
    re.compile(r"[A-Za-z]:\\(?:Users|Documents|Desktop|Downloads)\\", re.IGNORECASE),
    re.compile(r"/(?:Users|home|mnt)/[^/\s]+/", re.IGNORECASE),
    re.compile(r"/(?:root|var/" + r"home/[^/\s]+)/", re.IGNORECASE),
    re.compile(r"\bfile://", re.IGNORECASE),
    re.compile(r"(?:^|[\s(\[{'\"])[~][\\/]", re.MULTILINE),
    re.compile(r"(?:\$\{?HOME\}?|%USERPROFILE%|%HOMEPATH%|%HOME%)[\\/]", re.IGNORECASE),
    re.compile(r"\\\\[^\\\s]+\\[^\\\s]+"),
)
# Credential shapes. These run against every published file, including this
# one, so each pattern requires a payload that a pattern definition cannot
# accidentally satisfy. The hosting platform also scans pushes; this check
# exists so a clone, an archive, and a fork all fail the same way offline.
SECRET_PATTERNS = {
    "private key block": re.compile(r"-----BEGIN (?:[A-Z]+ )*PRIVATE KEY(?: BLOCK)?-----"),
    "GitHub token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}\b"),
    "GitHub fine-grained token": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{50,}\b"),
    "model provider key": re.compile(r"\bsk-(?:ant-)?[A-Za-z0-9][A-Za-z0-9\-_]{19,}\b"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA|AGPA|AIDA)[0-9A-Z]{16}\b"),
    "AWS secret access key": re.compile(r"(?i)aws_secret_access_key\s*[=:]\s*[\"']?[A-Za-z0-9/+=]{40}"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b"),
    "Slack token": re.compile(r"\bxox[abprs]-[0-9A-Za-z\-]{10,}\b"),
    "Stripe live key": re.compile(r"\b(?:sk|rk)_live_[0-9A-Za-z]{20,}\b"),
    "JSON web token": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    "credential in connection string": re.compile(
        r"(?i)\b(?:postgres|postgresql|mysql|mongodb(?:\+srv)?|redis|amqp|ftp)://[^\s:@/]+:[^\s:@/]+@"
    ),
    "assigned secret literal": re.compile(
        r"(?i)\b(?:password|passwd|client[_-]?secret|access[_-]?token|auth[_-]?token|api[_-]?key)\b"
        r"\s*[=:]\s*[\"'][^\"'\s]{8,}[\"']"
    ),
}

# Filenames that carry credentials by convention. Extension-based rules already
# reject .pem and .key because they are not allowed text types; these are the
# ones that would otherwise pass on name alone.
FORBIDDEN_CREDENTIAL_NAMES = {
    ".env",
    ".netrc",
    ".npmrc",
    ".pypirc",
    "credentials.json",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "id_rsa",
    "secrets.json",
}
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")

# Upstream project documentation and the project's own host. Anything else is a
# potential account link or private destination and fails the run.
ALLOWED_EXTERNAL_HOSTS = {
    "d2lang.com",
    "docling-project.github.io",
    "github.com",
    "graphviz.org",
    "img.shields.io",
    "marp.app",
    "matplotlib.org",
    "mermaid.js.org",
    "pandoc.org",
    "plotly.com",
    "python-docx.readthedocs.io",
    "python-pptx.readthedocs.io",
    "quarto.org",
    "seaborn.pydata.org",
    "typst.app",
    "www.apache.org",
    "www.python.org",
}
ALLOWED_GITHUB_PATH_PREFIXES = (
    "/microsoft/markitdown",
    "/opendatalab/mineru",
)

LICENSE_SHA256_LF = "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4"
IMPOSSIBLE_CLAIM = re.compile(
    r"\b(?:100%\s+(?:accurate|error[- ]free)|zero hallucination|guaranteed (?:token|context) savings)\b",
    re.IGNORECASE,
)
CLAIM_NEGATION = re.compile(r"\b(?:never|no|not|cannot|without|do not)\b", re.IGNORECASE)


def _git(*args: str) -> str | None:
    """Return stdout for a Git command, or None when Git is unavailable."""
    try:
        completed = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    except OSError:
        return None
    if completed.returncode:
        return None
    return completed.stdout.decode("utf-8", errors="replace")


def published_files() -> tuple[list[Path], str]:
    """Return the files this project publishes and how they were discovered."""
    toplevel = _git("rev-parse", "--show-toplevel")
    if toplevel is not None and Path(toplevel.strip()).resolve() == ROOT:
        listing = _git("ls-files", "-z", "--cached", "--exclude-standard")
        if listing is not None:
            tracked = sorted(ROOT / name for name in listing.split("\0") if name)
            present = [path for path in tracked if path.is_file()]
            if present:
                return present, "tracked"

    found: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in UNPUBLISHED_DIRS for part in path.relative_to(ROOT).parts):
            continue
        found.append(path)
    return sorted(found), "working-tree"


def check_link(rel: str, path: Path, target_text: str, errors: list[str]) -> None:
    if target_text.startswith("#"):
        return
    if target_text.startswith("mailto:"):
        errors.append(f"contact address link in {rel}: {target_text}")
        return
    if target_text.startswith(("http://", "https://")):
        parsed = urlparse(target_text)
        host = parsed.hostname or ""
        if host not in ALLOWED_EXTERNAL_HOSTS:
            errors.append(f"unapproved external link in {rel}: {host or target_text}")
        if host == "github.com" and not parsed.path.lower().startswith(ALLOWED_GITHUB_PATH_PREFIXES):
            errors.append(f"unapproved account-specific link in {rel}: {target_text}")
        return
    resolved = unquote(target_text.split("#", 1)[0])
    if not resolved:
        return
    target = (path.parent / resolved).resolve()
    try:
        target.relative_to(ROOT)
    except ValueError:
        errors.append(f"local link escapes repository in {rel}: {target_text}")
        return
    if not target.exists():
        errors.append(f"broken local link in {rel}: {target_text}")


def main() -> int:
    if sys.version_info < MIN_PYTHON:
        running = ".".join(str(part) for part in sys.version_info[:3])
        wanted = ".".join(str(part) for part in MIN_PYTHON)
        print("VALIDATION FAILED")
        print(f"- Python {wanted} or newer is required; this interpreter is {running}")
        return 1

    errors: list[str] = []
    all_files, discovery = published_files()
    rels = {path.relative_to(ROOT).as_posix() for path in all_files}

    for required in sorted(REQUIRED):
        path = ROOT / required
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing or empty required file: {required}")

    for rel in sorted(rels):
        path = ROOT / rel
        if path.name in FORBIDDEN_NAMES or any(part in FORBIDDEN_PARTS for part in path.parts):
            errors.append(f"forbidden platform, binary-template, or output path: {rel}")
        if path.name.lower() in FORBIDDEN_CREDENTIAL_NAMES or path.name.lower().startswith(".env."):
            errors.append(f"credential-bearing filename is not allowed: {rel}")
        if path.suffix.lower() not in ALLOWED_SUFFIXES:
            errors.append(f"non-text file type is not allowed: {rel}")
        raw = path.read_bytes()
        if b"\x00" in raw:
            errors.append(f"binary NUL byte found: {rel}")
            continue
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"not UTF-8 text: {rel}: {exc}")
            continue

        for pattern in PERSONAL_PATHS:
            if pattern.search(content):
                errors.append(f"personal or machine path found: {rel}")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(content):
                errors.append(f"possible {label} found: {rel}")
        if EMAIL.search(content):
            errors.append(f"email address found: {rel}")

        if rel not in PATTERN_DEFINITION_FILES:
            if FORBIDDEN_PLATFORM_TERMS.search(content):
                errors.append(f"platform or shared-drive reference found: {rel}")
            if SELF_REPOSITORY_LINK.search(content):
                errors.append(f"hardcoded repository-owner link found: {rel}")
            for line in content.splitlines():
                if IMPOSSIBLE_CLAIM.search(line) and not CLAIM_NEGATION.search(line):
                    errors.append(f"unguarded impossible guarantee found: {rel}")
                    break

        if path.suffix.lower() == ".md":
            for match in MARKDOWN_LINK.finditer(content):
                raw_target = match.group(1).strip()
                if raw_target:
                    check_link(rel, path, raw_target.split()[0].strip("<>"), errors)

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").is_file() else ""
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append(f"VERSION is not semantic x.y.z: {version!r}")
    else:
        for name in ("README.md", "CHANGELOG.md"):
            path = ROOT / name
            if path.is_file() and version not in path.read_text(encoding="utf-8"):
                errors.append(f"{name} does not mention VERSION {version}")

    # The README invites readers to audit the whole tree and states how big it
    # is. An unchecked size claim rots on the first commit that adds a file.
    readme_path = ROOT / "README.md"
    if readme_path.is_file():
        expected = f"{len(all_files)} text files"
        if expected not in readme_path.read_text(encoding="utf-8"):
            errors.append(f"README.md must state the published file count as '{expected}'")

    license_path = ROOT / "LICENSE"
    if license_path.is_file():
        normalized = license_path.read_bytes().replace(b"\r\n", b"\n")
        if hashlib.sha256(normalized).hexdigest() != LICENSE_SHA256_LF:
            errors.append("LICENSE does not exactly match the canonical Apache-2.0 text")

    try:
        theme = json.loads((ROOT / "templates/chart-theme.json").read_text(encoding="utf-8"))
        for key in ("primary", "background", "ink"):
            if key not in theme.get("colors", {}):
                errors.append(f"templates/chart-theme.json missing color: {key}")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid templates/chart-theme.json: {exc}")

    for pattern_name in ("extract_insights.md", "extract_tables.md", "synthesize_report.md", "generate_d2.md"):
        path = ROOT / "patterns" / pattern_name
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        for heading in ("## Input contract", "## Security boundary", "## Output contract"):
            if heading not in content:
                errors.append(f"patterns/{pattern_name} missing {heading}")

    if errors:
        print("VALIDATION FAILED")
        for error in sorted(set(errors)):
            print(f"- {error}")
        return 1

    print(f"VALIDATION PASSED: {len(all_files)} published files ({discovery}), version {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
