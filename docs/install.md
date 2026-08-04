# Install, verify, and remove

## Before changing anything

Inventory first. Record existing versions, resolved command paths, relevant command-search state, free disk, selected capabilities, and conflicts. Do not reinstall a healthy tool.

Create a scoped restore record that distinguishes pre-existing items from files and environments owned by the new installation.

## Install rules

- Use reviewed official sources and stable pinned versions.
- Prefer isolated environments for Python and JavaScript tools.
- Install heavyweight OCR or acceleration components only after a workload and resource review.
- Keep one stable command entry per selected tool rather than exposing every environment executable.
- Never weaken shell policy or wait invisibly for a password.
- Stop on source, integrity, licence, or ownership ambiguity.

## Verification

For each selected capability, run a small synthetic end-to-end fixture. A useful fixture proves that the tool can accept an input, produce the expected kind of output, and fail when a mandatory condition is missing.

Repeat command-resolution checks from a fresh shell and an unrelated directory. Then run the repository checks:

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
python scripts/smoke_test.py
```

These three commands need **Python 3.9 or newer and nothing else** — no
packages, no lockfile, no network access. If `python` is not found, replace it
with `py -3` on Windows or `python3` on macOS/Linux, and use that launcher for
all three commands.

They validate the repository itself. They do **not** certify any external
document tool on a particular machine; only the per-capability fixtures above
do that, and a machine is not ready until those pass.

## Upgrade

Upgrade deliberately. Record a new restore point, inspect upstream changes and licences, update pins, rerun the affected fixtures, and keep the previous known-good environment until promotion succeeds.

## Remove or roll back

Show the proposed changes first. Remove only installation-owned environments, shims, caches, and managed configuration. Preserve source data, unrelated software, and later human edits. Rerun the previous known-good fixtures after recovery.
