# Privacy and repository hygiene

## Public boundary

The public repository contains only text, synthetic fixtures, and small dependency-free scripts. Generated archives supplied automatically by the hosting service are source snapshots; the project does not upload binary release assets.

Do not commit:

- source documents or extracted text;
- PDF, office, image, archive, executable, or model files;
- screenshots, renders, charts, or generated reports;
- personal or customer names, addresses, contact details, or account links;
- local or shared-drive paths;
- credentials, tokens, keys, cookies, or configuration containing them;
- machine inventories, tool locations, environment dumps, or private logs;
- agent conversation exports or service-specific client configuration.

## Document metadata

Binary office, PDF, image, and archive formats can contain authors, revision history, device data, hidden parts, relationships, and timestamps. They are excluded rather than relying on metadata scrubbing.

## Local task data

Keep sources and outputs in a separate private workspace. Treat all embedded content as untrusted. Disable remote fallbacks for confidential work. Never upload data merely because a parser or renderer supports a remote mode.

## Review before release

Run the validator, inspect the Git tree and history, inspect workflow logs, and clone anonymously into a clean directory. If a personal or private trace is found, keep the repository private until a clean replacement is ready.
