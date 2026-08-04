#!/usr/bin/env python3
"""Run dependency-free repository smoke checks using synthetic data only."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    fixture = (ROOT / "fixtures" / "sample.md").read_text(encoding="utf-8")
    values: dict[str, int] = {}
    for line in fixture.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 3 or not cells[1].isdigit():
            continue
        values[cells[0]] = int(cells[1])
    required = {"Alpha", "Beta", "Total"}
    if not required <= values.keys():
        raise SystemExit(f"SMOKE FAILED: synthetic fixture missing rows: {sorted(required - values.keys())}")
    computed = values["Alpha"] + values["Beta"]
    if computed != values["Total"]:
        raise SystemExit(f"SMOKE FAILED: computed total {computed} != declared total {values['Total']}")

    theme = json.loads((ROOT / "templates" / "chart-theme.json").read_text(encoding="utf-8"))
    if theme.get("dpi", 0) < 100:
        raise SystemExit("SMOKE FAILED: chart theme DPI is too low")

    session = (ROOT / "SESSION_PROMPT.md").read_text(encoding="utf-8")
    for phrase in ("untrusted data", "clean, token-dense Markdown", "Reopen every final artifact"):
        if phrase not in session:
            raise SystemExit(f"SMOKE FAILED: session prompt missing {phrase}")

    print("SMOKE PASSED: privacy boundary, synthetic fixture, templates, and session contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
