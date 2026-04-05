# BDC Primer Part 3: The Liability Stack, Funding, Maturity Wall, and Fallen Angel Risk

Source: JunkBondInvestor (Feb 21, 2026)

---

## Table of Contents

1. Why BDC Debt Exists
2. The Liability Stack
3. Secured Credit Facilities
4. Unsecured Notes
5. SBIC Debentures
6. Convertible Notes
7. Liability Stack Framework Summary
8. Asset Coverage — The Tripwire
9. How to Read a BDC's Funding Profile
10. The 2026 Maturity Wall
11. The Refinancing Math
12. Spread Framework and Relative Value
13. Fallen Angel Risk
14. The TCPC Case Study
15. The Feedback Loop
16. Who's At Risk Today
17. The Equity Investor's Takeaway

---

## 1. Why BDC Debt Exists

- BDCs need leverage to generate competitive returns.
- A portfolio yielding 10-11% on assets doesn't get you to a double-digit ROE without debt.
- **Example math:** At 1.0x leverage, a BDC earning 10.5% on assets and paying 5.5% on debt generates roughly 15.5% on gross assets, minus fees and expenses, leaving 10-11% ROE.
- Without leverage, you're stuck at single-digit returns that aren't as appealing.
- **The regulatory cap is 2.0x debt-to-equity** (raised from 1.0x by the Small Business Credit Availability Act in 2018). Most BDCs operate in the 0.9x to 1.2x range. The average across the sector is currently around 1.2x regulatory leverage.

## 2. The Liability Stack

Not all BDC debt is created equal. Understanding the stack is the first step to credit analysis.

Most debt comes from three main sources: secured bank credit facilities, unsecured bonds, and SBIC debentures. Each has different characteristics, different costs, and different implications for stress tolerance.

**For fixed income investors, BDC unsecured notes offer:**
- **Yield pickup:** BDC bonds typically trade wider than comparably rated financials. The highest-quality issuers like ARCC, BXSL, and TSLX trade tighter, in the 180-200bps range over treasuries. Smaller or weaker credits trade wider, sometimes 250bps+. The sector carries a complexity premium and a private credit stigma that keeps some institutional buyers away.
- **Structural seniority over equity.** Unsecured bonds sit above equity but below the secured facilities. The relevant question for bondholders is less about ultimate recovery and more about whether the structure forces deleveraging before the cycle turns.
- **Diversification.** BDC credit risk is tied to middle-market corporate health, not mortgage credit or consumer lending. The underlying exposure is to PE-backed middle-market borrowers across sectors like software, healthcare, and business services.

**The catch:** BDCs are essentially levered portfolios of below-investment-grade loans. The underlying assets are non-investment grade even if the BDC itself carries a BBB- rating. A BDC rated BBB- is holding loans that would individually be rated B. That mismatch is what makes BDC credit analysis interesting, and why spreads are wider than typical IG financials.

**Representative bond pricing:**

| Issuer | Rating | Coupon | Px | YTW | STW |
|--------|--------|--------|----|-----|-----|
| ARCC 5.25 31 | Baa2/BBB | 5.250% | 98.4 | 5.6% | 196 bps |
| BXSL 5.125 31 | Baa2/BBB- | 5.125% | 97.7 | 5.7% | 203 bps |
| TSLX 5.625 30 | Baa2/BBB- | 5.625% | 100.4 | 5.5% | 187 bps |
| BBB Index (Bloomberg) | — | 4.750% | n/a | 4.9% | 96 bps |

**Who's buying BDC bonds:**
- Insurance companies seeking yield pickup over core IG
- Total return bond funds with flexibility to own BBB- credits
- Credit-focused hedge funds playing relative value
- Passive ownership is lighter than in vanilla IG financials because BDCs sit in an idiosyncratic corner of "financials" with various index and mandate constraints.
- The buyer base is more specialized, which contributes to wider spreads and more volatility in risk-off environments.

## 3. Secured Credit Facilities (Revolvers and Term Loans)

- Most BDCs have a secured revolving credit facility with a syndicate of banks.
- The facility is secured by the BDC's loan portfolio, with the banks taking a first-priority lien on the assets. Think of it as a margin loan against the portfolio.
- **Cheapest funding source.** But it comes with borrowing base risk.
- Banks set an **advance rate** against eligible collateral (typically 50-70%).
- If marks decline or assets move to non-accrual, the borrowing base shrinks.
- The BDC may be forced to pay down the facility even if it has ample liquidity otherwise.

**Example:** A BDC with $1 billion of collateral at a 60% advance rate has $600 million of borrowing capacity. If marks decline 10% and some loans move to non-accrual, the eligible collateral might drop to $850 million. Suddenly the borrowing base is $510 million. If the BDC had $580 million drawn, it needs to pay down $70 million or pledge additional collateral.

**Dispersion of secured/unsecured mix varies widely by issuer.**

## 4. Unsecured Notes

- Typically 5-7 year fixed-rate notes issued in the institutional market.
- **No borrowing base. No mark-to-market triggers. No margin calls.** The debt just sits there until maturity (or early redemption).
- That stability comes at a cost: unsecured notes price wider because bondholders are structurally subordinate to the secured lenders. In a liquidation, secured creditors get paid first from the pledged collateral. Unsecured bondholders have a claim on what's left.

**Current unsecured bond pricing (representative issues):**

| Issuer | Coupon | Maturity | Px | YTW | STW |
|--------|--------|----------|----|-----|-----|
| CGBD | 5.75% | 2/15/2031 | 97.5 | 6.2% | 253 bps |
| TCPC | 6.95% | 5/30/2029 | 99.3 | 6.9% | 310 bps |
| BCSF | 5.95% | 3/1/2031 | 97.4 | 6.4% | 268 bps |
| ARCC | 5.25% | 4/12/2031 | 98.3 | 5.6% | 196 bps |
| MAIN | 6.95% | 3/1/2029 | 103.7 | 5.4% | 202 bps |
| OBDC | 6.20% | 7/15/2030 | 100.1 | 6.1% | 247 bps |
| Average | 6.18% | — | 99.4 | 6.1% | 246 bps |
| Median | 6.08% | — | 98.8 | 6.2% | 250 bps |

**Note the dispersion.** ARCC funds at +196bps. TCPC (now high yield) funds at +310bps. That's over 100bps of spread difference that flows straight through to the income statement.

**BDCs with more unsecured funding have more flexibility.** They're not facing borrowing base pressure when marks decline. That's worth something in a stress scenario.

## 5. SBIC Debentures

- Some BDCs have Small Business Investment Company (SBIC) subsidiaries that can borrow from the SBA at favorable rates.
- **Key feature: SBIC debentures are typically excluded from the regulatory leverage calculation.**
- A BDC can run 1.0x "regulatory" leverage and 1.2x "total" leverage if the difference is SBIC debt.
- **Example:** MAIN: Total leverage is 0.73x, but regulatory leverage (excluding SBIC) is only 0.62x. FDUS: Total leverage 0.75x, regulatory leverage 0.49x.
- For the BDCs that have it, SBIC funding is a meaningful advantage: cheap, long-dated, non-recourse to the parent, and doesn't count against the regulatory cap.

**BDCs with meaningful SBIC usage (% of liabilities):**
- SCM: 47%, FDUS: 35%, SAR: 21%, CSWC: 17%, MAIN: 16%, NMFC: 11%, TCPC: 11%

## 6. Convertible Notes

- A handful of BDCs have convertible notes outstanding (e.g., GLAD has issued convertible notes).
- Treat converts as unsecured debt first. Conversion is optional and terms-driven, and only becomes a deleveraging path if the equity performs and the notes actually convert.

## 7. Liability Stack Framework Summary

| Funding Type | Typical Cost | Flexibility | Borrowing Base Risk |
|-------------|-------------|-------------|---------------------|
| Secured revolver | Lowest | Lowest | Yes |
| Unsecured notes | Higher (fixed) | Highest | No |
| SBIC debentures | Low (SBA rates) | High | No |

## 8. Asset Coverage — The Tripwire

- BDCs are subject to an **asset coverage requirement** under the 1940 Act.
- In practice, that can mean distribution restrictions and forced deleveraging, even if the portfolio is still "money-good" over time.
- If asset values fall, leverage mechanically rises, and at some point the BDC may stop paying distributions and delever (and/or issue equity) to get back into compliance.
- **The practical point: you don't need "ultimate loss" to create stress.** Marks down 5-10% plus a borrowing base haircut can force paydowns, dividend pressure, and defensive behavior long before any bondholder impairment is on the table.

## 9. How to Read a BDC's Funding Profile

### 1. Secured vs. Unsecured Mix
- Higher unsecured = more flexibility.
- A BDC with 70% unsecured funding is less likely to face forced deleveraging from borrowing base mechanics when marks move.
- A BDC with 80% secured is one bad quarter away from forced deleveraging.
- **Quick screen:** If secured funding exceeds 60% of total liabilities, dig deeper into the borrowing base mechanics.

### 2. Fixed vs. Floating Mix
- BDC assets are almost entirely floating-rate (SOFR + spread).
- If liabilities are also floating, the net interest margin is relatively stable regardless of where rates go.
- If liabilities are fixed, the BDC benefits when rates rise (asset yields go up, funding costs stay flat) but suffers when rates fall (asset yields compress, funding costs are locked in).
- Some BDCs use swaps to change their fixed/floating mix. Converting fixed liabilities to floating increases sensitivity to falling rates (and reduces the "locked-in" cost disadvantage if base rates decline). That's positioning, not a pure hedge.

**Mostly Floating liabilities:** CGBD 100%, TSLX 100%, NCDL 100%, PFLT 90%
**Mostly Fixed liabilities:** FDUS 95%, CSWC 93%, BBDC 78%, BCSF 63%

### 3. Maturity Profile
- Staggered maturities across multiple years is better than a concentrated wall.
- Check what percentage of debt matures in the next 12-18 months.
- **Quick screen:**
  - Less than 15% of debt maturing in next 12 months: Low refinancing risk
  - 15-25% maturing: Moderate risk, check the credit rating
  - More than 25% maturing: High risk, especially if on negative watch

### 4. Headroom to Regulatory Cap

| Leverage Level | Interpretation |
|---------------|---------------|
| Below 1.0x | Very conservative, room to grow |
| 1.0x – 1.2x | Normal operating range |
| 1.2x – 1.4x | Getting tight, less cushion |
| Above 1.4x | Close to stress territory |

- A BDC at 1.1x leverage can absorb roughly a 45% decline in NAV before hitting the 2.0x cap.
- A BDC at 1.4x can only absorb about 30%. That cushion matters.
- **Example:** If NAV drops 15% from writedowns, leverage mechanically increases. A BDC at 1.2x becomes roughly 1.4x. Suddenly management is worried about headroom rather than opportunity.

### 5. Cost of Debt vs. Asset Yield

**Net Interest Margin by BDC (weighted avg portfolio yield at FV, cost of debt, NIM):**

| Ticker | Wtd Avg Portfolio Yield at FV (%) | Cost of Debt (%) | NIM (%) |
|--------|----------------------------------|-------------------|---------|
| MAIN | 11.8% | 5.8% | 6.0% |
| MSIF | 11.7% | 6.1% | 5.6% |
| ARCC | 10.3% | 4.9% | 5.4% |
| FSK | 10.5% | 5.3% | 5.2% |
| BXSL | 10.0% | 5.0% | 5.0% |
| TSLX | 11.1% | 6.0% | 5.1% |
| OBDC | 10.0% | 5.6% | 4.4% |
| MSDL | 9.9% | 5.9% | 4.1% |
| MFIC | 10.3% | 6.4% | 3.9% |
| PSBD | 10.1% | 6.2% | 3.9% |
| OTF | 9.6% | 6.1% | 3.5% |
| KBDC | 10.6% | 7.1% | 3.5% |

- Note that KBDC has the highest cost of debt (7.1%) and the thinnest margin (3.5%). That's partly because it's newer and doesn't have the funding relationships of the established players.
- Net investment spreads are near trough levels. Expect them to stay roughly flat through 2026 as declining asset yields (from lower base rates) are offset by declining funding costs (as floating-rate facilities adjust). But any refinancing of the back book, where older deals were done at wider spreads, is a headwind.

### 6. Unencumbered Assets
- BDCs with significant unsecured funding have unencumbered assets — assets not pledged to secured lenders.
- This is a source of contingent liquidity.
- If a BDC with $2 billion of assets has $800 million pledged to a secured facility and $1.2 billion unencumbered, it has flexibility to pledge more collateral, raise additional secured debt, or sell assets without lender consent.
- **BDCs that are 80%+ secured-funded may have limited unencumbered assets.** That constrains optionality in a stress scenario.

## 10. The 2026 Maturity Wall

- Approximately **$12 billion** of index-eligible BDC debt matures in 2026. In aggregate, that's manageable. But the distribution matters.
- **BDC Debt Maturing in 2026 ($ in millions, % of total investments):**
  - ARCC: $2,150 (7.3%)
  - BBDC: $430 (17.9%)
  - BCSF: $600 (23.7%)
  - BXSL: $1,500 (10.9%)
  - FSK: $1,000 (7.5%)
  - GBDC: $600 (6.9%)
  - GSBD: $500 (15.6%)
  - MAIN: $500 (9.7%)
  - OBDC: $1,495 (9.1%)
  - TCPC: $347 (20.2%)
  - TSLX: $300 (9.0%)
  - HTGC: $425 (9.5%)

- ARCC has the largest absolute maturity wall, but $2.2 billion on a $25+ billion portfolio is manageable.
- BCSF has less debt coming due, but 24% of its portfolio is more concentrated.
- **The maturity wall doesn't end in 2026** — it extends through 2027-2029 for many issuers. BDCs that termed out debt opportunistically in 2020-2021 are facing larger walls in 2028-2029.

**BDC Debt Maturities by Year ($ in billions):**
- 2026: $12.0
- 2027: $10.0
- 2028: $12.0
- 2029: $16.0
- 2030: $14.0

## 11. The Refinancing Math

- Much of the 2026 maturity stack was issued in 2020-2021 with coupons in the low-3% area. That's paper issued when rates were near zero.
- **Replacement debt is pricing at 5.5-6.5% for investment-grade issuers.** For weaker credits or those on negative watch, it's 6.5-7.5%.
- That's 200-350bp of incremental interest expense.

**Example calculation:**
- A BDC refinancing $500 million of 3.0% notes at 5.5%:
  - Old annual interest: $15 million
  - New annual interest: $27.5 million
  - Incremental expense: $12.5 million
- On a $2 billion equity base, that's approximately 60bps of ROE compression. Purely from refinancing, before any credit issues.

- For the entire sector, if $12 billion refinances at 250bp higher rates, that's $300 million of incremental annual interest expense. That's real money.

## 12. Spread Framework and Relative Value

- BDC unsecured spreads sit roughly around the ~200bp area for stronger issuers, wider for stressed credits. The sector often trades wider than vanilla IG financials.
- The sector trades about 40-50bps wide of the broader IG financials index.

**Spread dispersion across tickers:**

| Tier | Representative Spreads (bp) |
|------|---------------------------|
| Tightest (ARCC, BXSL) | +140–190 |
| Middle (OBDC, TSLX) | +190–220 |
| Wider (BCSF, CGBD, NMFC) | +240–280 |
| High Yield (TCPC) | 300+ |

### Where BDCs Trade Relative to Their Own Secured Debt
- Within the same issuer, unsecured bonds often trade only modestly wider than the implied cost of the secured bank facility, despite being structurally junior.
- In other words, the subordination premium can look thin. You're not getting paid much for being junior in the capital structure.

### Where BDCs Trade Relative to the Underlying Loans
- BDC unsecured bonds yield 5.5-7.0%. The loans they're making yield 10-11%.
- The 400-500bp differential is the equity return plus the risk premium for subordination.
- As long as realized losses stay modest in normal conditions, the math works.
- But if credit deteriorates meaningfully, you're relying on that equity cushion to absorb losses before they reach the bonds.

### Relative Value Framework:

| Metric | Interpretation |
|--------|---------------|
| BDC spread vs IG fincos | Currently +40–50bp; if >+75bp, potentially attractive |
| BDC spread vs own secured | Should be +50–75bp for subordination; if tighter, potentially rich |
| BDC spread vs HY index | BDCs at BBB- should be tighter than BB index; if not, credit concerns |

### The High-Beta Dynamic
- BDCs trade like levered credit. When risk appetite is strong, spreads compress quickly. When sentiment sours, BDCs widen more than the broader market.
- BDC bonds are high-beta IG. Buying them means making a bet on private credit sentiment as much as individual company fundamentals.
- In a risk-off tape, BDCs will underperform.
- **The setup for 2026 favors caution.** BDCs are high-beta credit, and sentiment around private credit remains fragile. BDC spreads widen faster than the broader market. Positioning defensively at the ticker level makes sense here.

### Year-to-Date Performance (as of publication)
- BDC index has returned approximately +0.10% YTD vs +1.34% for US corporates broadly.
- The underperformance reflects lingering concerns about private credit asset quality.

## 13. Fallen Angel Risk

- This is the dynamic that both bond and equity investors should understand.

### Historical Context
- For years, BDC credit ratings were remarkably uniform. Nearly every public BDC was rated BBB- by at least one agency.
- The rating agencies treated BDCs as a relatively homogeneous group, differentiated mainly by size and manager quality.
- **That changed in 2025.** Rating dispersion increased meaningfully.

### Rating Actions (Upgrades / Positive Outlook):
| Ticker | Agency | Old | New | Date |
|--------|--------|-----|-----|------|
| GBDC | Moody's | Baa3 | Baa2 | Jan-25 |
| TSLX | Moody's | Baa3 | Baa2 | Feb-25 |
| ARCC | Fitch | BBB | Positive Outlook | May-25 |
| HTGC | Moody's | Baa3 | Baa2 | Sep-25 |
| HLEND | Moody's | Baa3 | Baa2 | Nov-25 |
| TSLX | S&P | BBB- | Positive Outlook | Dec-25 |
| OBDC | Moody's | Baa3 | Baa2 | Jan-26 |

### Rating Actions (Downgrades / Negative Outlook):
| Ticker | Agency | Old | New | Date |
|--------|--------|-----|-----|------|
| TCPC | Moody's | Baa3 | Ba1 | Mar-25 |
| OCSL | Fitch | BBB- | Negative Outlook | Apr-25 |
| FSK | Fitch | BBB- | Negative Outlook | Aug-25 |
| TCPC | Fitch | BB+ | BB (Watch Negative) | Jan-26 |

### The Agencies Are Now Differentiating Based On:
- Asset quality trends (non-accruals, internal ratings migration)
- NII coverage and earnings stability
- Leverage and funding flexibility
- Manager quality and track record

### What Happens When a BDC Falls to High Yield (The TCPC Case Study)

TCPC is the case study. When it was downgraded from BBB- to BB+ in 2025, several things happened:

**1. Cost of capital spiked immediately.**
- TCPC's 2029 notes went from trading around +200bp (IG context) to +310bps (HY context).
- That's over 100bps of spread widening, or roughly $3 million of additional annual interest cost per $300 million of debt.

**2. Index exclusion triggered forced selling.**
- Many IG index funds and IG-only mandates can't hold high-yield paper. When TCPC fell from IG to HY, those holders had to sell.
- The technical pressure compounded the fundamental weakness.

**3. Refinancing options narrowed.**
- IG BDCs can access the investment-grade bond market with $300-500 million deals at reasonable spreads.
- HY issuers face a smaller buyer base, smaller deal sizes, and wider pricing.
- TCPC can still fund through its bank facilities, but unsecured issuance is materially more expensive. That constrains growth and flexibility.

**4. The equity multiple compressed.**
- Higher funding costs compress NII. Lower NII means lower ROE. Lower ROE means the stock de-rates.
- TCPC trades at 0.60x NAV, versus 0.90x for the sector average.
- The P/NAV discount reflects both asset quality concerns and the cost-of-capital disadvantage.

### The Feedback Loop (Vicious Cycle):
1. Credit problems emerge (rising non-accruals, PIK, mark deterioration)
2. Rating agencies put the BDC on negative watch
3. Bond spreads widen in anticipation of downgrade
4. Downgrade happens; cost of capital spikes
5. Higher funding costs pressure NII coverage
6. Weaker coverage raises further credit concerns
7. Equity de-rates on lower forward earnings
8. At a discount to NAV, the BDC can't issue equity accretively
9. Growth stalls, competitive position weakens
10. → Cycle feeds back to step 1

**The BDCs with clean portfolios and stable ratings avoid this loop entirely.** They fund cheaply, grow accretively, and compound. The BDCs that enter the loop have a hard time escaping.

## 14. Who's At Risk Today

- **FSK and OCSL are the names to watch.** Both are on negative outlook at multiple agencies.
- If asset quality deteriorates further or NII coverage slips, they could follow TCPC to high yield.

### What Would Trigger More Fallen Angels?
- Non-accruals rising above 4-5%
- NII coverage falling below 100% for multiple quarters
- Leverage creeping above 1.4x
- Concentrated exposure to sectors under stress (software, healthcare)
- Loss of confidence in fair value marks

## 15. The Equity Investor's Takeaway

If you own BDC equity, here's why the liability stack matters:

### 1. Funding Mix Determines Stress Tolerance
- A BDC running mostly secured with a revolver renewal coming up faces forced deleveraging risk if marks move. One with 70% unsecured and staggered maturities has time.

### 2. The Maturity Wall is a Margin Headwind
- Every dollar refinanced at higher rates compresses NII. Even the best-managed portfolios will see earnings pressure from the liability side.

### 3. Rating Matters More Than Investors Think
- The gap between BBB- and BB+ isn't just a letter. It's the difference between accessing $300-500 million bond deals at 200bps and struggling to place smaller deals at 300bps+.

### 4. The Bond Market Often Leads the Equity
- Bond spreads often lead equity prices. If a BDC's bonds are widening while the stock is stable, the bond market is telling you something.
- Bond investors do deep credit work. They're looking at portfolio details, mark trends, and covenant cushions. When they start selling, equity investors should pay attention.

### 5. Watch the Unsecured Bond Spreads
- The spread between equity dividend yields and bond YTM tells you how much extra compensation the market demands for equity risk.
- When that spread compresses, either the equity is getting expensive or the bonds are getting cheap.
- When it widens, the market is getting more cautious on the equity.
