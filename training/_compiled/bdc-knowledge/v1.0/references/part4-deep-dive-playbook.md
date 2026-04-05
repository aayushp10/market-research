# BDC Deep-Dive Analytical Playbook

Source: Synthesized from JunkBondInvestor's OTF analysis (Mar 7, 2026), the 3-part BDC Primer (Feb 2026), and practitioner experience.

---

## Table of Contents

1. The Cardinal Rule
2. The 16-Step Deep-Dive Checklist
3. Step 1: True Sector Reclassification
4. Step 2: Vintage Cohort Analysis
5. Step 3: Mark Validation Against Observable Market Data
6. Step 4: NII Trajectory and Dividend Sustainability Math
7. Step 5: Effective Fee Rate on Equity
8. Step 6: PIK Quantification and Classification
9. Step 7: Unitranche and Structural Subordination
10. Step 8: Unfunded Commitment Risk
11. Step 9: Equity/Preferred Sleeve Analysis
12. Step 10: JV and Specialty Finance Transparency
13. Step 11: Lock-Up and Technical Overhang
14. Step 12: Stress Scenario Modeling (NAV Bridge)
15. Step 13: Earnings-Based Fair Value (NII/Ke)
16. Step 14: What the Market Is Already Pricing
16b. Step 14b: Bottom-Up Mark Staleness Quantification & Adjusted NAV
17. Step 15: Asymmetry Assessment
18. Common Pitfalls to Avoid
19. Web Search Checklist for BDC Analysis

---

## 1. The Cardinal Rule

**Challenge the filing. Don't just extract from it.**

A 10-K tells you what management wants you to see. The sector classifications are chosen by management. The marks are set by management (with third-party valuation input). The NII figure mixes cash and non-cash items. The "diversification" story is constructed by management.

The job of the analyst is to:
- Reclassify what the filing obscures (sector exposure, vintage risk)
- Validate what the filing asserts (marks, credit quality)
- Quantify what the filing describes qualitatively (stress scenarios, implied losses)
- Compute what the filing doesn't disclose (effective fee drag on equity, earnings-based fair value)

If your analysis reaches the same conclusions as the investor presentation, you haven't done the analysis — you've summarized the pitch.

---

## 2. The 16-Step Deep-Dive Checklist

When analyzing a specific BDC from its 10-K/10-Q, work through ALL of these steps. Not every step will surface a material finding, but skipping steps is how you miss the story.

| Step | Question | Output |
|------|----------|--------|
| 1. True Sector Reclassification | What do the borrowers actually do? | Restated sector table (filed vs. true) |
| 2. Vintage Cohort Analysis | When were the loans originated? | Cohort table with stress rates by era |
| 3. Mark Validation | Are the marks stale or aggressive? | Name-level comparisons to market data |
| 4. NII Trajectory | Is NII covering the dividend? Trend? | Quarter-by-quarter NII vs. dividend table |
| 5. Effective Fee Rate on Equity | What is the real fee drag? | Fee as % of NAV, not gross assets |
| 6. PIK Quantification | How much PIK? Originated vs. modified? | PIK $, % of portfolio, % of interest income |
| 7. Unitranche/Subordination | How much hidden subordination? | % unitranche, % "last out" within 1L |
| 8. Unfunded Commitments | How much additional deployment risk? | $ unfunded, % of NAV |
| 9. Equity/Preferred Sleeve | How much NAV depends on equity marks? | Unrealized gain/loss by asset class |
| 10. JV/Specialty Finance | What can't you see? | $ in opaque structures, % of NAV |
| 11. Lock-Up/Technical Overhang | Who is forced to sell? | Release schedule, shares outstanding |
| 12. Stress Scenarios | What does NAV look like in a downturn? | 3-scenario NAV bridge table |
| 13. Earnings-Based Fair Value | What is the stock worth on NII alone? | NII/Ke valuation at multiple cost-of-equity |
| 14. Market-Implied Losses | What is the stock already pricing in? | Implied NAV from stock price × target multiple |
| **14b. Bottom-Up Staleness & Adjusted NAV** | **What should the marks actually be today?** | **Bucket-level staleness bridge, 3-scenario adjusted NAV table, convergence check vs. market price** |
| 15. Asymmetry Assessment | Does the risk/reward favor you? | Bull/base/bear with probabilities |

---

## 3. Step 1: True Sector Reclassification

### Why This Matters
BDCs report portfolio composition using GICS-style industry codes. These codes are notoriously imprecise for private credit borrowers. A healthcare IT SaaS company might file under "Health Care Technology" rather than "Software." A fintech payments processor might be under "Diversified Financial Services." A data infrastructure company might be under "Communications Infrastructure."

The practical effect: **filed sector breakdowns systematically understate the true concentration in a BDC's dominant sector.** For tech-focused BDCs, filed "Software" exposure might show 24% while true tech exposure is 85%.

### How to Do It
1. Pull the full schedule of investments from the 10-K (it's in the financial statements, usually dozens of pages listing every portfolio company).
2. For every major holding (and ideally all of them), look up what the company actually does. Use web search if needed.
3. Reclassify into functional buckets: True Tech (SaaS/fintech/cyber), Tech-Adjacent, Non-Tech, Specialty Finance, Unclear.
4. Build a comparison table: filed classification vs. true economic classification.
5. **State the actual concentration.** "Filed Software & Services = X% | True tech exposure = Y% | Genuinely uncorrelated = Z%."

### Why It Matters for Stress Testing
If 85% of a book is economically correlated to a single sector, a sector credit event is a whole-book event, not a partial headwind. The filed breakdown obscures this, and it matters for every stress scenario you build.

### Key Principle
The question is not "is concentration bad?" — for a thematic lender, concentration is the strategy. The question is: **does the filed breakdown give you an accurate picture of your correlated exposure in a stress scenario?** If not, restate it.

---

## 4. Step 2: Vintage Cohort Analysis

### Why This Matters
Not all loans are created equal. The origination environment determines the underwriting assumptions baked into the loan:
- **ZIRP era (≤2022):** Near-zero rates, peak growth multiples (15-30x EBITDA for software), aggressive growth assumptions, capital structures designed for a different rate environment. Many of these borrowers have not grown into their acquisition valuations.
- **Post-reset (2023+):** Higher base rates already in the cost of capital, more conservative multiples, lenders who watched the 2022 vintage struggle. Not immune to deterioration but starting from a more defensible position.

### How to Do It
1. Segment the portfolio by origination date. Most 10-Ks provide this in the schedule of investments (look at the loan origination/acquisition dates).
2. For each vintage cohort, compute: total FV, number of positions, average spread, % of portfolio.
3. Identify the "stressed" portion within each cohort — positions marked below 95 cents (or 90, depending on threshold).
4. The ZIRP-era cohort (≤2022) deserves special scrutiny. What % of it is stressed? How does it compare to the post-reset book?

### Red Flags
- ZIRP-era second-lien book with 90%+ of positions marked below 95 cents → structural vintage problem, not a bad quarter
- Large first-lien positions from peak-multiple LBOs (2021-2022) still marked at par → validate against market data (Step 3)
- The 2L book from any era showing concentrated stress is a leading indicator for the 1L book from the same vintage

### Key Data Point
If you can compute it: "ZIRP-era book: $XB total | Y% stressed | Avg spread Z bps vs. [post-reset avg spread] bps."

---

## 5. Step 3: Mark Validation Against Observable Market Data

### Why This Matters
BDC marks are set quarterly by the manager (with third-party valuation input). Between mark dates, the market moves but the portfolio doesn't remark. This creates **mark staleness** — the portfolio's reported fair value reflects conditions at the mark date, not today.

Mark staleness is a sector-wide issue, but the magnitude varies by how much the market has moved since the last mark date and how concentrated the portfolio is in the affected sector.

### How to Do It

**Index-level validation:**
1. Identify the BDC's mark date (quarter-end, e.g., December 31).
2. Pull the relevant leveraged loan index (LSTA US Leveraged Loan Index, and sector sub-indices if available — e.g., LSTA Technology) as of the mark date and as of today.
3. Compute the change. If the tech loan index has dropped 6.5 points since the mark date, and the portfolio is 85% tech, the implied staleness is ~5.5 points on the portfolio.
4. State it clearly: "The LSTA tech index has moved X points since the mark date. OTF's book is Y% tech. Implied staleness = Z points, or $W million of unreflected losses."

**Name-level validation:**
1. For the largest positions (top 10-20), check if Bloomberg or other sources have secondary loan pricing available.
2. Compare the BDC's internal mark to the observable market price.
3. Compute the gap in points and dollars.
4. **Example (from JBI's OTF analysis):** OTF carried Barracuda first-lien at 80-88 cents. Bloomberg loan pricing for the same credit was ~59 cents. Gap: 21-29 points on a $76.9M position = $16-22M of potentially unrecognized losses on a single name.

**Cross-BDC validation:**
1. If multiple BDCs hold the same credit, compare their marks. A 22-point gap between one BDC's mark and clearing prices in the secondary market raises a question. If another BDC (e.g., Blackstone Secured Lending) marks the same or similar vintage loan at 78 cents while the target BDC marks it at 100 cents, that's a data point.

### Key Principle
BDC marks can legitimately diverge from secondary market clearing prices — illiquidity premiums, hold-to-maturity perspective, and timing all apply. **But a 20+ point gap on an observable name is not a rounding difference.** It is the most direct data point available on whether the marks reflect current market conditions.

### Output Format
Build a table:
| Name | Instrument | FV ($M) | BDC Mark (¢) | Market Price (¢) | Gap (pts) | Gap ($M) |

---

## 6. Step 4: NII Trajectory and Dividend Sustainability Math

### Why This Matters — CONFIRMED CRITICAL
This was independently flagged by both our analysis and JBI's as the central question for any BDC equity investment. NII coverage below 100% of the dividend is the Primer's "first sign of trouble." But the trajectory matters as much as the level.

### How to Do It
1. Build a quarter-by-quarter table going back at least 4-5 quarters:

| Quarter | NII/sh | Adj NII/sh | Div/sh | Coverage (Rep.) | Coverage (Adj.) | ROE (NII) |

2. **Check the direction.** Monotonically declining NII with a flat or rising dividend is a clear negative signal. Management raising the dividend while NII falls (as in OTF) is an especially aggressive posture.

3. **Annualize the most recent quarter's NII** and compare to the annualized dividend commitment. This is the "can the current run-rate fund the payout" test.

4. **Identify what's filling the gap** if coverage is below 100%: spillover income (finite), fee waivers (discretionary), realized/unrealized gains (volatile), or nothing (dividend cut risk).

5. **SOFR sensitivity:** Pull the BDC's disclosed NII sensitivity per 100bps of SOFR movement. With rates likely continuing to decline, compute how much further NII compresses per cut. Example: "$112M NII sensitivity per 100bps of SOFR → at 465M shares, that's ~$0.24/share per 100bps cut."

### Key Output
"Q4 annualized NII: $X/sh | Annual dividend commitment: $Y/sh | Coverage: Z% | Gap filled by: [source] | SOFR sensitivity: $W/sh per 100bps"

---

## 7. Step 5: Effective Fee Rate on Equity

### Why This Matters
BDC management fees are calculated on gross assets (total assets, not equity). Because BDCs use leverage, gross assets are significantly larger than equity. The effective fee drag on a shareholder's equity is therefore much higher than the stated fee rate.

### How to Do It
1. Compute gross assets (total assets, typically excluding cash per the advisory agreement).
2. Compute NAV (total net assets).
3. **Effective base management fee on equity = (stated fee rate × gross assets) / NAV.**
4. Example (from OTF): Stated fee = 1.5%. Gross assets = $14.3B. NAV = $8.0B. Effective fee on equity = (1.5% × $14.3B) / $8.0B = **2.68%**, or ~$94M/year.

### Why It Matters
The effective fee on equity reveals the true drag. A "1.5% fee" that's actually 2.68% on your equity changes the breakeven math significantly. It also reveals the manager's incentive: the fee grows with gross assets, which means the manager is incentivized to deploy capital and lever up even when spreads are tight or the book is under stress.

### Always Compute This Number
Don't just state the fee rate from the advisory agreement. State the effective rate on equity. This is a consistent gap in surface-level analysis.

---

## 8. Step 6: PIK Quantification and Classification

### Why This Matters — CONFIRMED CRITICAL
PIK (payment-in-kind) inflates reported NII without generating cash. The Primer establishes the framework: originated PIK is different from modified PIK (red flag). But quantifying the total PIK exposure as a % of the portfolio is equally important.

### How to Do It
1. Pull total PIK income from the income statement or footnotes.
2. Compute PIK as % of total interest and dividend income.
3. Pull the aggregate PIK balance outstanding (accrued but unpaid interest added to loan balances) from the schedule of investments or footnotes.
4. Compute PIK balance as % of total portfolio at cost.
5. **Classify:** How much of the PIK was originated with PIK features vs. modified from cash-pay to PIK post-origination? The footnotes or earnings call commentary may disclose this. If not, flag the opacity.

### Sector Benchmarks (from Primer)
- Sector average PIK as % of total interest income: ~8% (as of early 2025 data).
- A name running 15-18%+ PIK is well above average and warrants scrutiny.
- Rising PIK quarter-over-quarter is a trend signal independent of the level.

### Key Output
"PIK income: $X ($Y% of interest income) | PIK balance outstanding: $Z ($W% of portfolio at cost) | Classification: originated vs. modified [if discernible]"

---

## 9. Step 7: Unitranche and Structural Subordination Within First Lien

### Why This Matters
The headline "77% first lien" can mask significant structural subordination. Unitranche loans — especially "last out" positions — have subordination risk within the first-lien bucket that doesn't show up in the asset composition table.

### How to Do It
1. Check the 10-K for disclosure of unitranche composition within first lien. Some BDCs disclose this (OTF: 61% of 1L is unitranche).
2. Within unitranche, determine the % that is "last out" vs. "first out."
3. "Last out" first-lien has a secondary priority behind super-senior "first out" in certain scenarios. In a recovery, last-out holders get paid after first-out holders — the recovery rate is structurally lower.

### Key Principle
A portfolio that is "77% first lien, 61% of which is unitranche, and some portion of that is last-out" has a very different risk profile than a portfolio that is "77% standalone first lien." The headline number is the same; the subordination risk is not.

---

## 10. Step 8: Unfunded Commitment Risk

### Why This Matters
Unfunded commitments are contractual obligations to fund additional capital to existing portfolio companies. In stress, borrowers draw on committed facilities — this means the BDC is deploying additional capital into potentially deteriorating credits at exactly the wrong time.

### How to Do It
1. Pull unfunded commitments from the 10-K footnotes.
2. Compute unfunded commitments as % of NAV.
3. Consider: if borrowers draw 50-100% of unfunded commitments in a stress scenario, how much additional capital is being deployed? Where does the funding come from — available revolver capacity, cash, or asset sales?

### The Primer's Early Warning Signal
"When portfolio companies start pulling heavily on committed credit facilities, it often signals cash flow stress before it shows up in payment defaults. If you hear a manager mention 'elevated revolver utilization' across the portfolio, pay attention."

---

## 11. Step 9: Equity/Preferred Sleeve Analysis

### Why This Matters — CONFIRMED CRITICAL
Some BDCs carry meaningful equity and preferred equity exposure (10-20% of portfolio). This sleeve behaves very differently from the senior secured loan book:
- It's the first-loss position in the capital structure.
- It generates unrealized gains/losses that directly hit NAV.
- It can prop up NAV in good times (masking NII deterioration) and crater NAV in bad times.

### How to Do It
1. Pull the equity/preferred sleeve from the investment table: amortized cost vs. fair value.
2. Compute unrealized gain/loss by asset class.
3. **Ask: how much of the NAV trend is driven by the equity sleeve vs. the core loan book?**
4. If NAV is rising because of equity marks while NII is falling, the "NAV growth" story is fragile — it's dependent on volatile marks, not stable income.

### Key Principle (from Primer)
"A BDC with 20% equity exposure has a very different risk profile than one with 95% first lien debt. The equity component adds volatility to NAV in both directions."

---

## 12. Step 10: JV and Specialty Finance Transparency

### Why This Matters
Some BDCs run joint ventures or specialty finance subsidiaries alongside the core loan book. These structures are consolidated at equity method — you don't see the underlying assets.

### How to Do It
1. List every JV and specialty finance entity disclosed in the 10-K.
2. For each: what does it invest in? How much capital is committed? What % of NAV?
3. **Flag anything that doesn't match the BDC's stated strategy.** A tech-focused BDC holding railcar leases, life settlements, and pharmaceutical royalties through specialty subsidiaries is not "diversified" — it's running side strategies you can't diligence.

### Key Principle (from Primer)
"If a BDC has 15% of its NAV in a JV, you're trusting management's marks on assets you can't see."

---

## 13. Step 11: Lock-Up and Technical Overhang

### Why This Matters
Recently listed BDCs (especially conversions from non-traded vehicles) often have lock-up provisions that create persistent selling pressure. This is a technical factor, not a fundamental one, but it can dominate price action for 6-12 months post-listing.

### How to Do It
1. Pull the lock-up release schedule from the 10-K or 8-K filings.
2. Compute: what % of shares are still locked? When are the release dates? How much comes free each month?
3. **Consider the behavioral angle:** Pre-listing shareholders bought at or near NAV. If the stock trades at 0.68x NAV, they're sitting on 30%+ losses with no liquidity. The incentive to sell on any release date is strong, especially for retail investors in former non-traded vehicles.

---

## 14. Step 12: Stress Scenario Modeling (NAV Bridge)

### Why This Matters
Qualitative risk descriptions ("the portfolio could decline in a downturn") are not analysis. **Quantified stress scenarios are.** The question isn't "could NAV decline?" — of course it could. The question is "by how much, under what assumptions, and does the current stock price already embed that decline?"

### How to Build a Stress Model

**Step 1: Segment the portfolio into risk buckets.**
Use your vintage cohort and sector reclassification work. Example buckets:
- ZIRP-era first lien (≤2022)
- Non-ZIRP first lien (2023+)
- ZIRP-era second lien / subordinated
- Non-ZIRP second lien / other
- Equity / preferred sleeve

**Step 2: Assign haircut assumptions to each bucket.**
Calibrate to **observable market data**, not arbitrary round numbers:
- For the non-ZIRP first-lien book: use the actual LSTA tech index decline since the mark date (e.g., 6.5 points) as the base case. This is conservative — it assumes no further deterioration, just catching up to where the market already is.
- For the ZIRP-era first-lien book: apply a larger haircut reflecting the additional vintage risk. 20-30 points is a defensible range based on cross-BDC mark comparisons and observable secondary loan pricing.
- For second lien: ZIRP vintage with 92% of positions already stressed → 60+ point haircuts are not aggressive.
- For equity/preferred: include in the non-ZIRP bucket or apply a conservative 15-20% haircut.

**Step 3: Build the NAV bridge.**
| Bucket | FV ($M) | Haircut | MTM Loss ($M) | % of NAV |
Start from reported NAV/sh, subtract each bucket's haircut contribution, arrive at stressed NAV/sh.

**Step 4: Build three scenarios.**
1. **Base case:** Observable market moves only. No additional deterioration assumed. This is the "what's already happened" scenario.
2. **Tail case:** Additional sector-specific stress (e.g., AI disruption compressing borrower revenues, broader tech credit event). Haircuts 2-3x the base case.
3. **Armageddon:** 2008-style liquidity freeze + severe credit deterioration. Not a central case but worth naming because it calibrates the true downside.

**Step 5: Apply a steady-state multiple to each stressed NAV.**
For BDCs, the right target multiple is NOT 1.0x NAV. Per JBI:
- ARCC (best-in-class, 21+ year track record): 0.90-1.05x in normal conditions
- Average well-managed BDC: ~0.90x
- Newly listed, unproven, or stressed name: 0.80-0.90x

Apply the appropriate multiple to get fair value per share under each scenario.

### Output Table
| Scenario | MTM Loss ($M) | % of NAV | Stressed NAV/sh | @ 0.90x | vs. Stock Price |

---

## 15. Step 13: Earnings-Based Fair Value (NII/Ke)

### Why This Matters
Most BDC analysis focuses on P/NAV. But P/NAV only tells you something useful if NAV is stable. If NII is declining and the income stream doesn't support the current payout, a NAV-based framework misses the story.

### How to Do It
Run a parallel valuation capitalizing the earnings stream:

**Fair Value = Annualized NII per share / Cost of Equity (Ke)**

Run it at multiple Ke assumptions (9%, 10%, 11%, 12%) and at multiple NII assumptions (reported GAAP, adjusted, recovery scenario).

| NII Basis | Ann. NII/sh | Ke = 9% | Ke = 10% | Ke = 11% | vs. Stock Price |

### Key Insight
If the earnings-based fair value is *below* the stock price at reasonable Ke assumptions, the stock is pricing in an NII recovery that hasn't happened yet. That's a bet on the future, not a margin of safety.

### When This Framework Dominates
The earnings-based framework is more important than P/NAV when:
- NII is declining and the trend hasn't stabilized
- The dividend is not covered by NII
- NAV is being supported by unrealized gains rather than income
- The book has significant mark staleness risk

---

## 16. Step 14: What the Market Is Already Pricing

### How to Do It
1. Take the current stock price.
2. Divide by a reasonable steady-state multiple (0.90x for a typical BDC, adjust up for premium names, down for unproven ones).
3. The result is the implied fair NAV the market is pricing.
4. Subtract reported NAV to get the implied mark-to-market loss.
5. Compare this to your stress scenario output. Is the market pricing the base case? More than the base case? Less?

### Example (from JBI's OTF analysis)
Stock: $11.82. At 0.90x, implied fair NAV = $13.13. Reported NAV = $17.33. Implied MTM loss = ~$1.9B. JBI's base case stress produced ~$2.0B of losses and stressed NAV of $12.92. At 0.90x → $11.63. **The market and the stress model converged within $100M.** That's not a coincidence — it suggests the market has done the math.

---

## 16b. Step 14b: Bottom-Up Mark Staleness Quantification & Adjusted NAV

Step 14 gives you the **top-down** view: what the stock is pricing in aggregate. This step gives you the **bottom-up** view: what the marks should actually be, bucket by bucket, producing an independent adjusted NAV estimate. **Then you converge the two.** If they align, the market has done the math. If they diverge, you've found either a mispricing or a flaw in your model.

### Why This Step Exists

Most BDC analysis describes mark risk qualitatively ("the marks could be stale"). That is not analysis. This step forces **quantification**: "the implied staleness is $X million, or $Y per share, producing an adjusted NAV of $Z under three scenarios." The output is a table, not a paragraph.

### Prerequisites

Before starting this step, you must have completed:
- **Step 1 (True Sector Reclassification)** — you need the real sector exposure map, not the filed one
- **Step 3 (Mark Validation)** — you need the index-level and name-level data
- **Step 12 (Stress Scenarios)** — you need the risk bucket segmentation
- **Step 14 (Market-Implied Losses)** — you need the top-down cross-check to converge against

### Phase 1: Establish the Staleness Window

1. Identify the BDC's mark date (quarter-end from the 10-K/10-Q).
2. Compute the number of calendar days between the mark date and today.
3. Characterize the interim market: calm (<1 point index move), volatile (1-3 point move), or crisis (>3 point move).
4. **Rule of thumb:** If gap <30 days and markets calm, staleness is likely <$0.10/sh. If gap >45 days OR markets have been volatile, staleness analysis is essential and likely material.

**Output:** "Mark date: [date]. Days since mark: [N]. Market regime since mark: [calm/volatile/crisis]."

### Phase 2: Pull the Observable Market Moves

Use web search to find the following data points:

1. **Morningstar LSTA US Leveraged Loan Index** — weighted average bid as of mark date vs. today. Compute the change in points.
2. **LSTA Software/Technology sub-index** — performing software loan average bid as of mark date vs. today. This is the critical sub-index for any BDC with tech exposure.
3. **Non-Software performing loans** — compute the ex-Software index move (total index move adjusted for Software drag).
4. **Distressed share** — % of loans priced below 80 cents as of mark date vs. today. Rising distressed share = rising tail risk.
5. **Name-level secondary pricing** — for the BDC's top 10-20 positions, check Bloomberg or LCD for observable secondary loan prices. Compute gaps vs. the BDC's internal marks.

**Search queries to use:**
- `LSTA leveraged loan index price [month] [year]`
- `leveraged loan software sector performance [year]`
- `PitchBook LCD loan market monthly wrap [month] [year]`
- `[portfolio company name] loan secondary pricing`
- `JPMorgan private credit software loan marks` (for bank-level mark data)

**Output:** A table of index moves:

| Index / Sub-Index | Level at Mark Date | Level Today | Change (pts) |
|---|---|---|---|
| LSTA US Leveraged Loan (broad) | | | |
| LSTA Software (performing) | | | |
| LSTA ex-Software (performing) | | | |
| Distressed share (% <80¢) | | | |

### Phase 3: Segment the Portfolio into Mark-Staleness Risk Buckets

This is the core analytical work. Segment the entire portfolio into buckets based on (a) asset class, (b) sector exposure, and (c) current mark level. Use the BDC's filed portfolio data (schedule of investments, earnings presentation) cross-referenced with your sector reclassification work from Step 1.

**Standard bucket template (adjust based on the specific BDC):**

| Bucket | Description | How to Size It |
|--------|-------------|---------------|
| A. Sector-exposed 1L (performing) | First-lien loans in the sector(s) under stress, currently marked >90¢ | True sector reclassification × 1L allocation × % marked above 90 |
| B. Sector-exposed 1L (stressed) | First-lien loans in stressed sector(s), currently marked <90¢ | Same sector × 1L allocation × % marked below 90 |
| C. Non-exposed 1L (performing) | First-lien loans outside stressed sector(s), marked >90¢ | Remaining 1L after removing sector-exposed |
| D. Non-exposed 1L (stressed) | First-lien loans outside stressed sector(s), marked <90¢ | Check shadow non-accrual data |
| E. Second lien (all) | All second-lien positions | From asset composition table |
| F. Unsecured debt | All unsecured/mezzanine positions | From asset composition table |
| G. Specialty finance + JVs | Opaque structures (equity method, non-observable marks) | From asset composition table |
| H. Preferred equity | Preferred equity sleeve | From asset composition table |
| I. Common equity | Common equity sleeve | Compare cost basis vs. FV for unrealized gain/loss |

**Key data to pull for each bucket:**
- Fair value ($M)
- % of total portfolio
- Amortized cost ($M) — to compute existing unrealized gain/loss
- Average mark (FV as % of par, if debt) or FV vs. cost (if equity)

### Phase 4: Assign Staleness Haircuts by Bucket

For each bucket, estimate the mark-to-market move since the mark date. **Calibrate to observable data, not arbitrary numbers.**

**Haircut calibration principles:**

1. **Sector-exposed performing 1L (Bucket A):** Apply a beta-adjusted version of the relevant sector sub-index move. Private credit loans don't reprice tick-for-tick with the syndicated index because they're illiquid and held-to-maturity. **Use a 50-75% beta** to the observable index move. Example: if the LSTA Software sub-index fell 8 points, apply 4-6 points to the private credit software 1L book.

2. **Sector-exposed stressed 1L (Bucket B):** Stressed names have higher beta to market moves. Apply **75-100% of the index move** or more if names are approaching distress thresholds.

3. **Non-exposed performing 1L (Bucket C):** Apply the ex-sector index move. If the broad index ex-Software fell 75 bps, apply **0.5-2 points** depending on credit quality mix.

4. **Non-exposed stressed 1L (Bucket D):** Higher beta. Apply **1-3 points** above the performing move.

5. **Second lien (Bucket E):** Second lien has structurally higher beta to market moves than first lien (lower recovery, higher loss-given-default sensitivity). Apply **1.5-2x** the first-lien haircut for the same sector.

6. **Unsecured debt (Bucket F):** Similar to second lien but smaller exposure typically. Apply **1-3 points.**

7. **Specialty finance + JVs (Bucket G):** These marks are hardest to validate externally. If the underlying assets are senior secured loans (like in a credit SLF), apply a modest haircut reflecting the broad loan index move levered by the JV's internal leverage. If the underlying assets are non-correlated (life settlements, railcar leasing), **assume flat** unless you have specific reason to haircut. Flag the opacity explicitly.

8. **Preferred equity (Bucket H):** First-loss-like characteristics. Apply **2-6 points** haircut in a risk-off environment, more if the underlying companies are in stressed sectors.

9. **Common equity (Bucket I):** The most volatile bucket. If the equity sleeve is sitting on unrealized gains, ask: how much of that gain would survive in the current market? **Haircut the unrealized gain by 30-50%** in a moderate stress; by 50-75% in a severe stress. Enterprise value multiples for PE-backed companies compress in risk-off environments.

**Output:** A table:

| Bucket | Est. FV ($M) | % of Portfolio | Mark-Date Avg Mark | Current Market Proxy | Implied Move (pts) | Staleness ($M) |
|--------|-------------|---------------|-------------------|---------------------|-------------------|---------------|
| A | | | | | | |
| B | | | | | | |
| ... | | | | | | |
| **Total** | | | | | | **$XXX** |

### Phase 5: Build Three Scenarios

Don't produce a single point estimate. Build three scenarios reflecting different assumptions about (a) the magnitude of further market moves and (b) the beta between observable index moves and private credit marks.

| Scenario | Methodology |
|----------|------------|
| **Conservative** | Low end of each haircut range. Assumes private credit marks have lower beta to the syndicated selloff. Assumes no further deterioration beyond what's already happened. |
| **Moderate** | Midpoint of each haircut range. Assumes moderate beta and current market levels persist through next mark date. |
| **Aggressive** | High end of each haircut range. Assumes continued market deterioration into next mark date, higher beta on stressed names, equity sleeve gives back more gains. |

### Phase 6: Build the Adjusted NAV Table

Starting from reported NAV/sh, subtract the per-share staleness impact and add back any accretive items (buybacks, NII earned since mark date).

| | Reported | Conservative | Moderate | Aggressive |
|--|---------|-------------|----------|-----------|
| **Reported NAV/sh** | $X.XX | $X.XX | $X.XX | $X.XX |
| **Less: Mark Staleness** | — | ($A.AA) | ($B.BB) | ($C.CC) |
| **Less: NII shortfall vs dividend (if any)** | — | ($D.DD) | ($D.DD) | ($D.DD) |
| **Plus: Accretive share buybacks (if any)** | — | +$E.EE | +$E.EE | +$E.EE |
| **Adjusted NAV/sh** | $X.XX | **$F.FF** | **$G.GG** | **$H.HH** |
| **@ 0.90x multiple** | — | | | |
| **@ 0.85x multiple** | — | | | |
| **@ 0.80x multiple** | — | | | |
| **@ 0.75x multiple** | — | | | |

**Multiple selection guidance (from JBI):**
- Best-in-class, 20+ year track record (ARCC): 0.90-1.05x
- Well-managed, scaled, mid-track-record: 0.85-0.95x
- Average, externally managed: 0.80-0.90x
- Newly listed, unproven, or under stress: 0.70-0.85x
- Apply at the *adjusted* NAV, not reported NAV

### Phase 7: Convergence Check Against Market Pricing

This is where the top-down (Step 14) and bottom-up (this step) meet.

1. Take the current stock price.
2. For each scenario in your adjusted NAV table, compute: **Stock Price ÷ Adjusted NAV/sh = Implied Multiple.**
3. Ask: **Is that implied multiple reasonable for this BDC's quality tier?**
   - If the implied multiple at your moderate scenario is 0.80-0.90x for a mid-quality BDC, the market and your model are converging. The stock is approximately fairly priced on stressed NAV.
   - If the implied multiple at your moderate scenario is <0.75x, the market is pricing in more than your staleness estimate — either you're underestimating the mark problem, or there's an additional risk (dividend cut, NII spiral, credit event) the market is pricing that you haven't quantified.
   - If the implied multiple at your moderate scenario is >0.95x, the stock may be cheap — either the market hasn't fully priced in the staleness, or there's a positive catalyst the market is discounting.

4. **State the convergence explicitly:** "The market at $XX.XX is pricing my [conservative/moderate/aggressive] scenario at a [X.XX]x multiple. This implies the market [has/has not] fully incorporated the mark staleness and [is/is not] pricing additional risks beyond mark moves."

### Phase 8: Quantify Specific Structural Mark Risks

Beyond the index-level staleness bridge, flag and quantify these structural issues that can cause reported marks to overstate true value:

#### The Unitranche Mark Problem
If the BDC discloses a meaningful unitranche allocation within first lien:
1. Identify the % of first lien that is unitranche.
2. Estimate the % of unitranche that is "last out" (if disclosed).
3. **"Last out" first-lien recovers materially less than standalone first-lien in a default.** Current marks may not fully reflect this subordination because marks are typically based on income/yield approaches, not liquidation recovery analysis.
4. Apply a **2-3 point additional haircut** to the estimated "last out" exposure as a structural risk premium. This doesn't show up as daily staleness — it crystallizes in a default scenario.
5. **Report separately:** "Unitranche structural subordination risk: $X million, not included in the staleness bridge but relevant to stress NAV."

#### Specialty Finance / JV Opacity
1. Total the FV of all specialty finance and JV positions.
2. Compute as % of NAV.
3. **If >10% of NAV is in opaque structures, flag it.** You cannot validate these marks from the outside.
4. Ask: do the underlying assets in these vehicles correlate with the stressed sector? A credit SLF holding software loans has the same staleness problem as the direct loan book. A life settlement vehicle does not.
5. **Don't haircut blindly** — but state the opacity clearly and note what you're trusting management on.

#### The Equity Sleeve — Fragile NAV Support
1. Pull the equity/preferred sleeve: amortized cost vs. fair value.
2. Compute unrealized gain/loss.
3. **If NAV is being supported by unrealized equity gains while NII is declining, the NAV story is fragile.** The equity gains depend on enterprise value multiples holding up. In a credit stress environment, EV multiples compress.
4. Quantify: "The equity sleeve contributes $X million of unrealized gains to NAV. A 30-50% reversal of these gains would reduce NAV/sh by $Y.YY."
5. Include this in the aggressive staleness scenario.

### Output Checklist

When you complete this step, your output should include ALL of the following:

- [ ] Observable index moves table (Phase 2)
- [ ] Portfolio segmented into risk buckets with FV, %, and avg mark (Phase 3)
- [ ] Haircut table with staleness $ by bucket (Phase 4)
- [ ] Three-scenario aggregate staleness (conservative, moderate, aggressive) in $ and $/sh (Phase 5)
- [ ] Adjusted NAV table with multiple tiers (Phase 6)
- [ ] Convergence statement vs. current stock price (Phase 7)
- [ ] Structural risk flags: unitranche, specialty/JV opacity, equity sleeve fragility (Phase 8)
- [ ] A clear statement of what the stock is pricing and whether it's cheap, fair, or rich on your adjusted NAV

---

## 17. Step 15: Asymmetry Assessment

### The Final Question
After all the work above, the question is: **does the risk/reward favor the investor?**

Frame it clearly:
- **Bull case:** What needs to go right? (NII stabilizes, leverage ramps accretively, marks hold, lock-up clears, multiple re-rates). Probability? Target price?
- **Base case:** What does "nothing changes" look like? Market-implied value is roughly where it trades. The stock isn't cheap; it's approximately fairly priced on stressed NAV.
- **Bear case:** What goes wrong? (AI disruption hits borrower revenues, marks catch down 30-50 points on ZIRP book, NII continues declining, dividend cut, equity sleeve reverses). Probability? Downside target?

**Assess the asymmetry.** For the upside to materialize, multiple things must go right simultaneously (marks hold, NII recovers, overhang clears). For the downside to materialize, only one thing needs to disappoint (marks catch up to market, NII keeps declining, or equity gains reverse). **When the upside requires everything to go right and the downside requires only one thing to go wrong, the asymmetry does not favor you** — even if the headline discount looks attractive.

---

## 18. Common Pitfalls to Avoid

1. **Accepting filed sector classifications at face value.** Always reclassify. GICS codes for private credit borrowers systematically understate concentration.

2. **Treating P/NAV discount as inherently attractive.** A 32% discount to NAV is only attractive if the NAV is real. If the book needs a 25% haircut and the right multiple is 0.90x, the stock is fairly priced at 0.68x reported NAV.

3. **Ignoring mark staleness.** If the last mark date was Dec 31 and you're analyzing in March, three months of market moves are not reflected in the portfolio. Check the relevant loan indices.

4. **Describing risks qualitatively instead of quantifying them.** "The portfolio could be impacted by a tech downturn" is not analysis. "$2.0B of implied MTM losses producing stressed NAV of $12.92" is analysis.

5. **Computing fees on the stated rate.** Always compute the effective fee rate on equity. A "1.5% fee" that's 2.68% on equity is a different animal.

6. **Ignoring the dividend math.** If NII doesn't cover the dividend and the trend is deteriorating, it doesn't matter how cheap the P/NAV looks — a dividend cut resets the stock lower and compresses the multiple simultaneously.

7. **Treating the equity sleeve as free upside.** Equity co-investments are first-loss positions. In a downturn, they get wiped out before debt takes a haircut. If the equity sleeve is propping up NAV, that NAV is fragile.

8. **Forgetting to check lock-up schedules.** For recently listed BDCs, the lock-up release schedule can dominate price action for 6-12 months.

---

## 19. Web Search Checklist for BDC Analysis

When analyzing a specific BDC, use web search to supplement the 10-K. Here's what to look for:

1. **Current stock price** → compute P/NAV, dividend yield on market price
2. **Most recent earnings press release** → may have updated data not yet in the 10-K
3. **LSTA leveraged loan index levels** (overall and sector-specific) → mark staleness check
4. **Bloomberg or other secondary loan pricing** for the BDC's largest positions → name-level mark validation
5. **Peer BDC marks** on the same credits (check other BDC 10-Ks/10-Qs for shared portfolio companies)
6. **Analyst consensus estimates** for NII → is the market expecting recovery or further decline?
7. **Lock-up release schedule** updates (8-K filings) → technical overhang timeline
8. **Recent earnings call transcripts** → management commentary on amendment activity, PIK trends, deployment pace
9. **Credit rating agency actions** (Moody's, S&P, Fitch) on the BDC itself → rating watch or outlook changes
10. **JunkBondInvestor or other independent research** on the specific name → practitioner-grade analysis to cross-reference
