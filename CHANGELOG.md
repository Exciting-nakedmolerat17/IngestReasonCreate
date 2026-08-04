# Changelog

## 5.6.0 - 2026-08-04

Presentation and disclosure release. No change to the operating policy.

### Added

- Live repository-validation and release-gate badges, and a clone command that
  runs as written. The owner handle these contain is public by construction:
  it already appears in the address bar, the clone URL, and the owner line of
  every page, so linking to them discloses nothing the page does not. This is
  deliberately separate from the personal contact address that the checks have
  always rejected and still reject.
- A README section stating plainly that nothing installs itself, that the
  verification commands only read files in the folder, and that the setup
  prompt inventories, reuses, records a restore point, and tests its rollback
  before changing a machine. This was the loudest unspoken question and it was
  answered only in the setup prompt.
- An honest note on longevity: with no dependency to rot and no service to shut
  down, abandonment would leave a readable, runnable checklist.

### Changed

- Restored the first-person account of why the project exists. It describes how
  the tools are used, not who uses them.
- The required status check is bound to the continuous-integration application
  rather than accepting any producer of a check with that name.

## 5.5.0 - 2026-08-04

Documentation and robustness release. No change to the operating policy itself.

### Fixed

- First-run verification now gives explicit Windows and macOS/Linux launcher
  fallbacks, plus platform-native audit and reversible negative-test commands.
- The synthetic smoke check now parses and recomputes its fixture rather than
  comparing hardcoded constants, and the tests prove the validator rejects a
  synthetic credential-shaped negative fixture.
- Release tags are now rejected unless they point to the exact protected
  `main` commit; contributor guidance also requires annotated tags, draft-first
  publication, and repository-host immutability verification.
- Machine-path detection now covers generic drive-absolute paths, file URLs,
  home shortcuts and variables, and additional Unix home forms. Hosted-code
  links are restricted to the two documented upstream project paths.
- Removed hardcoded repository-owner URLs and first-person workflow narrative
  from the public documentation. Clone instructions now use the URL supplied by
  the repository host, and issue-template routing no longer embeds an account
  path.
- The validator now rejects future hardcoded self-links that include a hosting
  account name, preserving the account-neutral public boundary.
- `scripts/validate_repo.py` inspects **published** files instead of walking the
  working tree. A local virtual environment, cache, or editor directory used to
  produce a wall of validation errors; creating one is now invisible to the
  checks. Inside a Git checkout the validator reads the tracked files; in an
  extracted archive it skips known local-state directories.
- `tests/test_repository.py` uses the same discovery rule, so the binary-file
  test no longer fails on a developer's own virtual environment.
- The banned-vocabulary patterns are written plainly instead of being split
  across string concatenations to hide them from the validator's own scan. The
  file that defines the patterns is now explicitly exempt from those two
  content rules; every other rule still applies to it.

### Added

- `examples/` — a complete worked pass with invented data, including a source
  document whose own narrative contradicts its own table, to show what the
  verification step is for.
- `CODE_OF_CONDUCT.md`, issue templates, and a pull request template.
- `.github/dependabot.yml` so SHA-pinned workflow actions are re-opened monthly
  rather than silently ageing.
- Continuous integration now runs on Linux, macOS, and Windows against Python
  3.9 through 3.13, replacing a single unpinned interpreter on Linux. An
  aggregate `validate` job fronts the matrix so branch protection needs one
  stable status check.
- A minimum Python version is stated in the documentation and enforced by the
  validator with a readable message instead of a traceback.
- The credential scanner covers more shapes: fine-grained and short-lived
  hosting tokens, model-provider keys, cloud access and secret keys, Slack and
  payment-provider tokens, JSON web tokens, credentials embedded in connection
  strings, and assigned secret literals. Filenames that carry credentials by
  convention are rejected on name alone. This runs offline in every clone,
  archive, and fork rather than relying on the hosting platform's own scan.
- `.gitignore` covers direnv, keystores, private key files, package-manager
  credential files, and editor or operating-system state.
- `.mmd` accepted as a text type, and a curated allowlist of upstream project
  documentation hosts so the docs can link to the tools they name.

### Changed

- `README.md` rewritten to lead with the problem, a rendered pipeline diagram,
  a runnable two-minute check, and the worked example. It opens with a
  side-by-side of the same request answered with and without the playbook, and
  adds an "A new repository with no stars" section that answers the sceptic's
  question directly: what the project does and does not touch, how small the
  audit surface is, and the exact command that checks each claim — including
  one that makes a check fail on purpose.
- The validator asserts that the file count stated in `README.md` matches the
  published tree, so the audit-surface claim cannot quietly rot.
- `START_HERE.md` reduced to a router; the install steps now live in one place
  instead of being restated with small differences.
- `CONTRIBUTING.md`, `docs/install.md`, and `docs/troubleshooting.md` record the
  Python requirement and the two failure modes new users actually hit.

## 5.4.0 - 2026-08-04

- First clean public release.
- Added the Apache License 2.0.
- Added platform-neutral setup and session prompts.
- Added text-only templates, reasoning patterns, synthetic fixtures, and fail-closed repository checks.
- Excluded binary documents, generated artifacts, account links, machine paths, and private operating data from the public boundary.
