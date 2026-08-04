# Report: Meridian Works Q2 service review

> Synthetic example produced from [extracted-source.md](extracted-source.md).
> Note how each section states its evidence class. A reader can tell at a glance
> which lines are quoted from the document, which are arithmetic, and which are
> judgement that the document does not itself support.

## Sourced facts

- Total incidents fell from **107 in Q1 to 102 in Q2** across 43 sites. *(p.3 Table 1)*
- **North** fell 34 to 28; **East** fell 40 to 31. *(p.3 Table 1)*
- **South** rose 21 to 25; **West** rose 12 to 18. *(p.3 Table 1)*
- Counts **exclude planned maintenance events**. *(p.3 caption)*
- Two North sites completed an equipment refresh in Q1. *(p.4 §4.2)*
- South reported a staffing shortfall in weeks 5-9. *(p.4 §4.2)*
- One West site moved to extended operating hours in Q2. *(p.4 §4.2)*

## Calculations

All arithmetic below is derived from p.3 Table 1 and can be recomputed from it.

- Total change: `(102 - 107) / 107 = -4.7%`
- Regions improving: North `-17.6%`, East `-22.5%`
- Regions worsening: South `+19.0%`, West `+50.0%`
- Q2 incidents per site: North `2.33`, South `2.78`, East `2.07`, West `2.57`
- Column check: sites `12+9+15+7 = 43`; Q1 `34+21+40+12 = 107`; Q2 `28+25+31+18 = 102`. All three reconcile with the printed totals.

## Conflict found during verification

**The document contradicts itself, and the narrative is the part that is wrong.**

| Claim | Location | Value |
|---|---|---|
| "incident volume fell by roughly 12%" | p.2 §2.1 | -12% |
| Table 1 totals, recomputed | p.3 | **-4.7%** |

Table 1 is internally consistent: its three columns each sum to their printed
totals. The narrative figure is not reproducible from any table in the document.

**This report uses -4.7% and flags the discrepancy.** The two figures were not
averaged, and the more favourable one was not silently preferred. Resolving it
requires the author's underlying data, which is not in the source.

## Inferences

Marked as inference because the document does not state these causally.

- The reduction is concentrated in two regions rather than being broad-based.
  North and East account for the entire net improvement; the other two regions
  moved against it.
- West's `+50.0%` is the largest relative move but rests on the smallest base
  (12 to 18 incidents across 7 sites). Small-denominator volatility is a
  plausible alternative to any operational explanation.
- The p.4 note about extended operating hours in West is *temporally consistent*
  with West's increase, but the document asserts no causal link and provides no
  exposure-adjusted denominator.

## Recommendations

- Treat "-4.7%" as the reportable figure until the author reconciles p.2 with p.3.
- Ask for an exposure denominator (operating hours or service events per site)
  before drawing conclusions about West.
- Request a written definition of "incident" before comparing to prior periods.

## Unknowns and residual uncertainty

- **Appendix A (p.5) was not used.** Roughly 40% of the page failed OCR
  confidence thresholds. No claim in this report depends on it.
- **"Incident" is undefined in the source** *(p.6)*. Every period comparison
  above assumes the definition did not change between Q1 and Q2.
- **One resolved parser disagreement:** West Q2 was read as both 18 and 13.
  Targeted inspection of p.3 confirmed 18. The report uses 18.
- Two quarters is not a trend. The source's "continuing the improvement trend"
  claim *(p.2)* cannot be checked against this document alone.

---

## Verification record

| Check | Result |
|---|---|
| Every numeric claim traced to a locator | Pass |
| Table columns recomputed against printed totals | Pass — 3 of 3 reconcile |
| Narrative reconciled against tables | **Conflict found and reported** |
| Parser disagreements resolved or disclosed | 1 resolved, 1 disclosed |
| Unreadable regions excluded from claims | Pass |
| Output reopened and read after rendering | Pass |
