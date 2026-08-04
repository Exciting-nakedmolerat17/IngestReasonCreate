# Extracted source: Meridian Works quarterly service review

> Synthetic example. Every name, number, and finding below is invented for
> demonstration. This file shows what the ingest stage is supposed to hand to
> the reasoning stage: compact Markdown, a locator on every fact, and an
> explicit record of what the parser was unsure about.

**Source:** `quarterly-service-review.pdf` (6 pages, text-native with one scanned appendix)
**Parser:** layout-aware local extraction, OCR enabled for pages 4-6
**Extracted:** 6 of 6 pages, 1 page partially unreadable

---

## p.1 — Cover

Title: Quarterly Service Review, Q2
Prepared for: Operations Committee
Classification: Internal

## p.2 §2.1 — Summary narrative

> "Across all regions, incident volume fell by roughly 12% quarter on quarter,
> continuing the improvement trend established last year."

> "The North and East regions drove the reduction. South and West saw modest
> increases attributable to seasonal demand."

## p.3 Table 1 — Incidents by region

| Region | Sites | Incidents Q1 | Incidents Q2 |
|---|---:|---:|---:|
| North | 12 | 34 | 28 |
| South | 9 | 21 | 25 |
| East | 15 | 40 | 31 |
| West | 7 | 12 | 18 |
| **Total** | **43** | **107** | **102** |

Caption (p.3): "Incident counts exclude planned maintenance events."

## p.4 §4.2 — Regional notes

North: two sites completed the equipment refresh in Q1.
South: staffing shortfall reported in weeks 5 through 9.
East: no material change to operating pattern.
West: one site transitioned to extended operating hours in Q2.

## p.5 Appendix A — Scanned incident log

Partially unreadable. Approximately 40% of the page failed OCR confidence
thresholds due to a skewed scan and a stamp overlapping the table body.

## p.6 — Definitions

No definition of "incident" is given anywhere in the document.

---

## Uncertainty and parser disagreements

| Item | Locator | Status |
|---|---|---|
| West Q2 incident count | p.3 Table 1 | Two local parsers disagreed: 18 and 13. Targeted page inspection of p.3 confirmed **18**. Resolved. |
| Appendix A totals | p.5 | **Unresolved.** OCR confidence below threshold across ~40% of the page. Not used in any downstream claim. |
| Narrative reduction figure | p.2 §2.1 | Narrative states ~12%; Table 1 supports a different figure. **Conflict passed downstream unresolved — not averaged.** |
| Definition of "incident" | p.6 | Absent from source. Comparisons across periods assume a stable definition. |
