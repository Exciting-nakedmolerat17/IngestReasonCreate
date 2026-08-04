# Tool selection

Choose the smallest verified route that matches the source and requested output.

## Ingest

| Need | Preferred route | Cross-check or fallback | Main caution |
|---|---|---|---|
| Text-native office, HTML, or simple text | MarkItDown or a native parser | Pandoc or a format library | Weak authority for scans and complex reading order |
| Structured or scanned PDF | Docling with local OCR | Verified local MinerU pipeline | Inspect pages when layout carries meaning |
| Material parser disagreement | Compare outputs to source locators | Targeted page inspection | Never average conflicting values |

## Diagrams

- Mermaid for common flows, sequences, mind maps, and timelines.
- Graphviz for dense graphs, trees, and dependency networks.
- D2 for compact architecture diagrams when its local fixture passes.

The model writes a small definition. The engine performs layout and rendering.

## Charts

Use reviewed Python with Matplotlib, Seaborn, or Plotly when calculations or custom plots are needed. Prefer declarative data and styling. Verify every input, transformation, label, unit, scale, and source note.

## Slides

- Marp for fast Markdown slides where image-backed output is acceptable.
- Quarto for general publishing and editable slide output when the route is verified.
- python-pptx for exact native objects and supplied templates.

Use one engine per deck.

## Documents

- Pandoc for Markdown, DOCX, and multi-format conversion.
- Typst for fast print-ready PDF.
- python-docx for exact native Word objects or programmatic editing.

Compilation is not proof of correctness. Reopen, inspect, and reconcile.
