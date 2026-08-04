# Troubleshooting

## Running the repository checks

### `python` is not recognised

Try `python3` instead. On some systems only one of the two names is installed.
If neither resolves, install Python 3.9 or newer from
[python.org](https://www.python.org/downloads/) and open a new terminal so the
command search path is refreshed.

### The validator reports a Python version error

The checks require Python 3.9 or newer. Confirm which interpreter is actually
running with `python -VV` — a shell alias or an activated environment can shadow
the version you expect.

### The validator complains about files I did not add

It should not. The checks read the files this project *publishes*: the tracked
files inside a Git checkout, or everything except known local-state directories
in an extracted archive. A virtual environment, cache, or editor directory in
your working copy is invisible to them.

If you do see errors naming paths like `.venv/` or `node_modules/`, you are
running a version older than 5.5.0. Update, or run the checks from a clean
checkout.

### A check fails on a file that looks harmless

Read the message before changing the file — the rules are narrow on purpose. The
common ones are an unapproved external link host, an assistant or sync-service
brand name, and an address that matches the contact-details pattern. If the rule
is wrong for a reasonable change, that is a bug in the rule; report it rather
than reshaping the contribution around it.

## Running document work

### A command is missing

Check the selected profile, isolated environment, stable command location,
fresh-shell resolution, and an unrelated working directory. Do not assume a tool
is absent from one failed lookup.

### A parser finishes suspiciously fast

Check source page count, output length, headings, tables, warnings, and model
hydration. Run a second selected parser or inspect targeted pages.

### Two parsers disagree

Keep both values and their locators. Inspect the source region. Do not average
or silently choose the more convenient result.

### A file compiles but looks wrong

Render every page or slide. Check fonts, table geometry, clipping, overlap, page
breaks, notes, links, and labels. Fix the source specification and rebuild.

### The output matches the document but the document is wrong

This is not a failure of the pipeline; it is the pipeline working. Report both
values with their locators and say which one is reproducible from the source
data. Do not average them, and do not silently prefer the more convenient one.
[examples/report.md](../examples/report.md) shows the shape of that report.

### A second setup run changes many things

Treat it as an idempotency failure. Stop, compare ownership and state, and
repair the setup logic before continuing.

### Confidential content appears in logs

Stop the run, contain and remove the exposed copy, assess scope, rotate any real
credential, repair the logging boundary, and retest with synthetic data.

### A required route cannot be verified

Report `FAILED` or `REQUIRES HUMAN ACTION`. Do not relabel a mandatory failure
as an optional warning.
