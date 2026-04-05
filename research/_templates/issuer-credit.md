---
ticker: TICKER
name: Full Company Name
sector: sector-slug
sub_sector: sub-sector-slug
rating_sp: BBB-
rating_moodys: Baa3
rating_fitch: BBB-
rating_status: stable
status: ig | hy | crossover | distressed
coverage_priority: core | secondary | monitoring
tags:
  - issuer
  - credit/{ig|hy|crossover}
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
---

# {TICKER} — {Full Name}

> One-sentence description: what this company does and why it's in coverage.

## Snapshot

*Updated every touch. Current state only, no history.*

- **Curves and spreads:** current OAS on representative benchmark bonds; recent move (daily, MTD, YTD).
- **Cap structure snapshot:** total debt, key tranches, leverage ratio, near-term maturities.
- **Fundamentals:** revenue, EBITDA, FCF trajectory. Most recent quarter.
- **Relative value:** where does this trade vs. sector peers? Rich/cheap signal.
- **Catalyst calendar:** earnings date, rating review dates, refinancing maturities.

## Cap structure

*Required for HY / crossover / distressed. Optional for pure IG unless there's something unusual.*

Describe the debt stack by seniority. Note covenants, security packages, guarantees. Call out any unusual features (make-wholes, change-of-control puts, springing liens).

| Tranche | Size | Coupon | Maturity | Seniority | Notes |
|---------|------|--------|----------|-----------|-------|
| ...     | ...  | ...    | ...      | ...       | ...   |

## Business and fundamentals

*Concise. What does the company do, what's the earnings model, what are the key drivers.*

Paragraph or two. Prose, not bullets, unless there's a genuinely list-shaped structure.

## Sector context

Brief — how this name fits in its sector. Link to the sector page for the full relative value treatment.

See [[credit/sectors/sector-slug|Sector Page]] for peers and RV framework.

## Recent developments

*Dated bullets, most recent on top. Every bullet has a raw source citation. This is the append-only activity log for the name.*

- **2026-04-04:** Brief description of development. Citation: `_raw/credit/source-file-YYYY-MM-DD.md`
- **2026-03-28:** ...
- **2026-03-15:** ...

## Open questions

*Things Aayush flagged as unresolved or worth investigating. Agent adds to this when ingesting sources that raise new questions rather than answering old ones.*

- Question 1
- Question 2

## Sources

*All raw files that have contributed to this page. Updated every touch.*

- `_raw/credit/source-file-YYYY-MM-DD.md` — brief description of what it contributed
- `_raw/credit/source-file-YYYY-MM-DD.md` — ...

## Views

*Link out to any view-layer pages for this name. These are separate files living in `credit/situations/` or similar. The facts/views firewall means the thesis never lives on this page.*

- [[situations/YYYY-MM-DD-ticker-thesis-name]] — dated thesis, active
- [[situations/YYYY-MM-DD-ticker-thesis-name]] — dated thesis, closed

---

**Template notes (delete when instantiating):**

1. Every claim on this page needs a raw source citation. No exceptions.
2. Never write views here. "This looks cheap" or "we should be long" belongs in a situation page.
3. When a new source lands, add a dated bullet to Recent developments and update the Snapshot if the source changes any current-state facts. Do not rewrite history.
4. For IG pure-play names, Cap Structure section can be brief (total debt, benchmark maturities). For HY and crossover, it should be thorough.
5. When the rating status changes or a fallen angel trip happens, update the frontmatter AND add a prominent Recent developments entry.
