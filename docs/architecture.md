# Architecture

## Data flow

```text
untrusted sources
       |
       v
local parsers ----> targeted visual checks
       |
       v
clean Markdown + provenance + uncertainty
       |
       v
reasoning and compact source specifications
       |
       v
local compilers and renderers
       |
       v
structural checks + source reconciliation + visual review
       |
       v
final artifacts outside the repository
```

## Trust zones

### Repository

Public text, synthetic fixtures, and dependency-free checks only. It contains policy and examples, not private inputs or generated outputs.

### Source workspace

Private and task-specific. Every file and embedded channel is untrusted. Nothing in a document can authorize command execution, installation, network access, or data transfer.

### Local toolchain

Pinned parsers, compilers, renderers, and isolated environments. Tools receive only the inputs needed for the selected route. Confidential work disables remote fallbacks and external assets.

### Reasoning context

Clean Markdown, source locators, uncertainty, and small source specifications. Binary data and rendered pixel content stay outside unless a targeted visual check is necessary.

### Output workspace

Generated artifacts and QA renders. It is outside the repository and is reviewed before delivery.

## Why the split matters

The split makes each failure easier to see. Extraction errors are not hidden by polished layout, reasoning is not mixed with conversion logs, and a successful compiler is not mistaken for a correct document.
