# Contributing

Small, evidence-backed changes are welcome.

## What you need

**Python 3.9 or newer, and Git.** That is the whole list. There is nothing to
install, no lockfile, and no network call in any check.

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
python scripts/smoke_test.py
```

If `python` is not found, replace it with `py -3` on Windows or `python3` on
macOS/Linux in all commands.

All three must pass before you open a pull request. Continuous integration runs
the same three commands on Linux, macOS, and Windows against Python 3.9 through
3.13, so a change that only works on your machine will be caught.

A virtual environment in your working copy is fine and is ignored by the checks.

## House rules

1. **Text only, vendor neutral.** No binaries, and no assistant or sync-service
   brand names — prompts describe capabilities so they work with any agent.
2. **Synthetic fixtures only.** Never attach a real document, extract,
   screenshot, credential, host inventory, or private output. Not even a
   redacted one: office and PDF formats carry metadata that redaction misses.
3. **No new runtime dependency** when a standard-library check is enough. The
   zero-dependency property is a feature, not an accident.
4. **Explain the problem, the smallest change that fixes it, and how you tested
   it.** A change to the operating policy needs a reason a reader can check.
5. **Update `CHANGELOG.md`** for anything user-visible.

## If a check fails on something you did not touch

Say so in the pull request rather than working around it. A validator rule that
fires on a reasonable contribution is a bug in the rule, and it is more useful
to fix that than to reshape the contribution around it.

## Branch protection

`main` is protected. Changes land through a pull request with a review and a
passing `validate` check; direct pushes and force pushes are rejected.

## Releasing

Tagging is gated, not ceremonial. `scripts/release_gate.py` refuses any tag that
does not match `VERSION`, then reruns all three checks.

1. Update `VERSION` and add the matching `CHANGELOG.md` entry. The validator
   fails if `README.md` or `CHANGELOG.md` does not mention the new version.
2. Run `python scripts/release_gate.py --tag vX.Y.Z` locally.
3. Confirm release immutability is enabled in the repository host before
   publishing; this protection applies only to future releases.
4. Merge through a pull request, create an annotated tag on the exact `main`
   commit, and push it. The release-gate workflow rejects a tag that points
   anywhere else and reruns the same script against the tagged tree.
5. Create the release as a draft, review all notes and assets, publish it, and
   verify that the host reports the release and tag as immutable.

The checks that protect the public boundary — credential shapes, machine paths,
contact addresses, binary content, forbidden filenames — run on every push, so
there is no separate pre-release secret sweep to remember.

## Licensing

By submitting a contribution, you agree that it is licensed under Apache-2.0 as
described in [LICENSE](LICENSE).
