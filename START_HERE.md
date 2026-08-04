# Start here

IngestReasonCreate turns messy source documents into checked reports, slides,
charts, diagrams, and structured Markdown — locally, with tools you already
trust, and with a verification step that is allowed to fail.

**Everything below is a pointer. Pick the line that matches what you are doing.**

| You want to | Open |
|---|---|
| Understand what this is, in 60 seconds | [README.md](README.md) |
| See a real worked pass before spending time | [examples/](examples/) |
| Set up a new machine | [BOOTSTRAP_PROMPT.md](BOOTSTRAP_PROMPT.md) |
| Do a document task on a prepared machine | [SESSION_PROMPT.md](SESSION_PROMPT.md) |
| Read the full operating policy | [MASTER_PROMPT.md](MASTER_PROMPT.md) |
| Decide which tool a job should use | [docs/tool-selection.md](docs/tool-selection.md) |
| Fix something that is behaving oddly | [docs/troubleshooting.md](docs/troubleshooting.md) |
| Contribute a change | [CONTRIBUTING.md](CONTRIBUTING.md) |

## The one rule that matters most

**Keep private source files, extracted text, generated outputs, machine reports,
and credentials outside this repository.** Work on them in a separate folder.

This is not a style preference. `scripts/validate_repo.py` enforces it on every
push, and a pull request that crosses the line fails before anyone reviews it.
