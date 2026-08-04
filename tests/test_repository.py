from __future__ import annotations

import subprocess
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_repo  # noqa: E402  (path is set immediately above)


class RepositoryTests(unittest.TestCase):
    def run_script(self, name: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / name)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_validator_passes(self) -> None:
        result = self.run_script("validate_repo.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_smoke_passes(self) -> None:
        result = self.run_script("smoke_test.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_no_binary_files_are_published(self) -> None:
        """Binary formats can carry authorship and revision metadata, so the
        published tree excludes them rather than trying to scrub them."""
        forbidden = {".pdf", ".docx", ".pptx", ".xlsx", ".png", ".jpg", ".zip", ".exe"}
        published, _ = validate_repo.published_files()
        found = sorted(str(path.relative_to(ROOT)) for path in published if path.suffix.lower() in forbidden)
        self.assertEqual(found, [])

    def test_local_environment_does_not_break_discovery(self) -> None:
        """A virtual environment in the working tree is the most common local
        state there is. It must never reach the published-file list."""
        published, _ = validate_repo.published_files()
        offenders = sorted(
            str(path.relative_to(ROOT))
            for path in published
            if set(path.relative_to(ROOT).parts) & validate_repo.UNPUBLISHED_DIRS
        )
        self.assertEqual(offenders, [])

    def test_every_required_file_exists(self) -> None:
        missing = sorted(name for name in validate_repo.REQUIRED if not (ROOT / name).is_file())
        self.assertEqual(missing, [])

    def test_validator_rejects_a_synthetic_secret_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            copied = Path(temp_dir) / "repository"
            shutil.copytree(ROOT, copied, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            unsafe = "pass" + "word: \"" + "not-a-real-secret-000\"\n"
            (copied / "synthetic-negative-test.txt").write_text(unsafe, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(copied / "scripts" / "validate_repo.py")],
                cwd=copied,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("possible assigned secret literal", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
