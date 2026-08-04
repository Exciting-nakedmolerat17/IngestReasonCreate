#!/usr/bin/env python3
"""Bind a vX.Y.Z tag to VERSION and rerun the repository checks."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str]) -> None:
    completed = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=False)
    if completed.returncode:
        raise SystemExit((completed.stdout + completed.stderr).strip())
    if completed.stdout.strip():
        print(completed.stdout.strip())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", required=True)
    args = parser.parse_args()
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    expected = f"v{version}"
    if not re.fullmatch(r"v\d+\.\d+\.\d+", args.tag) or args.tag != expected:
        raise SystemExit(f"RELEASE GATE FAILED: {args.tag!r} does not match {expected!r}")
    run([sys.executable, str(ROOT / "scripts" / "validate_repo.py")])
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])
    run([sys.executable, str(ROOT / "scripts" / "smoke_test.py")])
    print(f"RELEASE GATE PASSED: {expected}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
