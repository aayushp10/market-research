# Individual Credit Evaluation Framework

A structured, CreditSights-inspired methodology for evaluating any single corporate credit
issuer. This framework produces a complete credit view across three dimensions — fundamental
quality, relative value, and structural/documentation protection — mirroring how the best
independent credit research shops build institutional-grade issuer opinions.

Use this file when:
- The user asks for a full credit analysis on a specific issuer
- Performing a deep dive or "tearsheet" on a name
- Evaluating whether to initiate or exit a position in a specific credit
- Assessing new issue attractiveness for a specific borrower
- The user asks "what do you think of [issuer]?" or "walk me through [ticker]"
- Building a credit opinion that separates fundamentals from relative value
- Any single-name analysis that requires depth beyond quick market color

This framework integrates with the broader credit trading skill. It uses the masters'
frameworks for investment philosophy, the workflows for trade execution, and the IG sector
map for peer identification. Think of this as the "how to think about one name" playbook.

## Table of Contents
1. The Three-Lens Framework
2. Lens 1: Fundamental Quality Assessment (CoreScore)
3. Lens 2: Relative Value Opinion (CS View)
4. Lens 3: Structural & Documentation Assessment
5. Quantitative Risk Overlay
6. Synthesis: Building the Credit Opinion
7. Report Types & Output Templates
8. Sector-Specific Adjustments
9. Common Pitfalls

---

## 1. The Three-Lens Framework

Never conflate fundamental quality with relative value. A strong credit can be an
Underperform if priced too tight. A weak credit can be an Outperform if priced to
compensate. Separating these dimensions is the single most important discipline in
credit research.

**The three lenses, in evaluation order:**

| Lens | Question It Answers | Time Horizon | Output |
|------|---------------------|--------------|--------|
| Fundamental Quality | Is this a durable, well-run credit? | Through-the-cycle (2-5yr) | Quality tier: Core / Strategic / Moderate Risk / Speculative |
| Relative Value | Am I being paid enough for the risks? | 6-12 months | View: Outperform / Market Perform / Underperform |
| Structural Protection | What protections exist if things go wrong? | Life of instrument | Documentation strength score + key risk flags |

**The investment decision stack:**
1. Ground the thesis in fundamentals (Lens 1)
2. Test market compensation against the fundamental view (Lens 2)
3. Set protections, sizing, and instrument selection (Lens 3)

**Key divergence patterns to flag:**
- Fundamentals strong + RV Underperform → Credit solid but pricing rich; patience or curve selection
- Fundamentals weak + RV Outperform → Tactical trade only; tight risk parameters, reassess frequently
- Fundamentals improving + RV Underperform → Monitor for inflection; potential catalyst ahead
- Fundamentals strong + Documentation weak → Beware of structural subordination and leakage risk
- Quant model diverges from analyst view → Triage — investigate why signals conflict

---

## 2. Lens 1: Fundamental Quality Assessment (CoreScore)

This is the through-the-cycle view of issuer durability. It asks: if we hold this credit
for 3-5 years through a full cycle, how confident are we in getting paid back?

### The Six Fundamental Sub-Factors

Evaluate each sub-factor on a 4-point scale (1 = strongest, 4 = weakest), then roll up
into an overall quality tier.

#### Sub-Factor 1: Balance Sheet Strength
**What to assess:**
- Gross and net leverage (Debt/EBITDA, Net Debt/EBITDA) — level and trajectory
- Leverage vs stated targets and rating agency thresholds
- Debt composition: secured vs unsecured, fixed vs floating, maturity profile
- Off-balance-sheet obligations (operating leases capitalized, pension deficits, guarantees)
- Tangible asset coverage — what is the hard asset floor in a liquidation scenario?
- Cash and liquidity position relative to near-term maturities

**Scoring guidance:**
- 1 (Strong): Leverage well below rating thresholds, declining trajectory, strong asset coverage
- 2 (Adequate): Leverage at or near targets, stable, manageable maturity profile
- 3 (Elevated): Leverage above targets or rising, lumpy maturities, limited cushion
- 4 (Weak): Leverage materially above thresholds, rising, near-term refinancing risk

**Key ratios by market segment:**
- IG corporates: Debt/EBITDA, Net Debt/EBITDA, FFO/Debt, Debt/Cap
- HY corporates: Total Leverage, Secured Leverage, Net Leverage
- Financials: CET1, Tier 1, Total Capital, Leverage Ratio, Tangible Common Equity
- REITs: Net Debt/EBITDA, Secured Debt %, Unencumbered Asset Coverage
- Utilities: FFO/Debt, Debt/Rate Base, Regulatory equity thickness

#### Sub-Factor 2: Cash Flow Quality & Resilience
**What to assess:**
- Revenue visibility and predictability (contracted vs spot, recurring vs one-time)
- EBITDA margin level and stability through prior downturns
- Capex intensity: maintenance vs growth — how much FCF survives after maintenance capex?
- Working capital cyclicality and cash conversion
- FCF generation consistency — does this business reliably produce cash?
- Dividend and shareholder return burden on cash flow
- Cash flow sensitivity to key macro variables (commodity prices, rates, FX, volumes)

**Scoring guidance:**
- 1 (Strong): Highly predictable, resilient cash flows; strong FCF conversion; minimal cyclicality
- 2 (Adequate): Moderately predictable; some cyclicality but manageable; decent FCF
- 3 (Elevated): Meaningful cyclicality; FCF volatile or thin after maintenance capex
- 4 (Weak): Highly volatile; negative FCF periods; dependent on market conditions for cash generation

**Stress test the cash flows:**
- What happened to EBITDA in the last recession or industry downturn?
- If revenues dropped 15-20%, can the company still service debt?
- What is the maintenance capex floor — the minimum spend to keep the business running?
- How quickly can costs flex down if demand falls?

#### Sub-Factor 3: Profitability & Competitive Position
**What to assess:**
- Margin trajectory: expanding, stable, or eroding?
- Market position: #1/#2 in core markets, or subscale?
- Pricing power: can the company pass through input cost inflation?
- Barriers to entry: regulatory, capital intensity, network effects, switching costs
- Customer and revenue concentration risk
- Competitive threats: disruption risk, commoditization, substitution
- Management quality: capital allocation track record, strategic clarity, credibility with market

**Scoring guidance:**
- 1 (Strong): Market leader with durable competitive advantages; expanding or stable margins
- 2 (Adequate): Solid market position; margins stable; manageable competitive dynamics
- 3 (Elevated): Subscale or facing intensifying competition; margin pressure visible
- 4 (Weak): Eroding market position; secular headwinds; management credibility questionable

#### Sub-Factor 4: Liquidity & Financial Flexibility
**What to assess:**
- Cash on hand + revolver availability vs near-term obligations (next 12-24 months)
- Revolver maturity and covenants — is the facility truly available under stress?
- Maturity wall: upcoming bond/loan maturities in next 1-3 years
- Access to capital markets: when did they last issue? At what spread? Was it well received?
- Alternative liquidity sources: asset sales, JV interests, subsidiary dividends
- Secured debt capacity remaining (for HY borrowers)
- Rating agency downgrade triggers that could restrict access

**Scoring guidance:**
- 1 (Strong): 2+ years of liquidity runway; no near-term maturities; strong market access
- 2 (Adequate): Comfortable liquidity; maturities manageable; proven market access
- 3 (Elevated): Liquidity adequate but not abundant; approaching maturities need addressing
- 4 (Weak): Liquidity constrained; near-term maturities with uncertain refinancing

**The "2AM test":** If credit markets shut down tonight and didn't reopen for 18 months,
would this company survive without distress? If no, the liquidity score cannot be 1 or 2.

#### Sub-Factor 5: Sector & Industry Risk
**What to assess:**
- Industry cyclicality and current cycle position
- Regulatory risk: is the regulatory framework stable, tightening, or in flux?
- Secular tailwinds or headwinds affecting the sector
- Sector competitive dynamics: consolidating (positive) vs fragmenting, rational vs irrational
- Input cost exposure and pass-through ability
- Technology disruption risk
- ESG-related transition risks (if material to credit — not headline ESG, but credit-impacting ESG)

**Scoring guidance:**
- 1 (Low risk): Stable, defensive sector; favorable regulatory backdrop; secular tailwinds
- 2 (Moderate): Cyclical but manageable; regulatory framework understood; no existential threats
- 3 (Elevated): Highly cyclical or facing regulatory uncertainty; transition risks present
- 4 (High risk): Secular decline; hostile regulatory environment; existential disruption threats

**Cross-reference with cycle analysis:** Where is this specific sector in its own cycle,
independent of the broader credit cycle? A late-cycle sector in a mid-cycle economy
warrants extra caution.

#### Sub-Factor 6: Event Risk
**What to assess:**
- M&A risk: is this an acquirer (potential leverage increase) or target (potential upgrade)?
- LBO risk: attractive to PE? Assess on size, cash flow stability, asset base
- Shareholder activism risk: is there a known activist? Vulnerable to one?
- Litigation/regulatory risk: pending cases, PFAS, opioids, antitrust, etc.
- Management succession risk
- Key-person or key-customer/contract risk
- Spin-off/restructuring risk
- Rating action risk: on watch or outlook? How close to the cliff (IG/HY boundary)?

**Scoring guidance:**
- 1 (Low): Minimal identifiable event risk; stable ownership; no pending triggers
- 2 (Moderate): Some identifiable risks but manageable; stable strategy
- 3 (Elevated): Active M&A program, or known litigation, or rating pressure
- 4 (High): Imminent event risk that could materially alter the credit profile

### Rolling Up to Quality Tier

Aggregate the six sub-factor scores into an overall fundamental quality tier:

| Tier | Typical Average Score | Description |
|------|----------------------|-------------|
| **Core** | 1.0 – 1.7 | Highest quality; resilient through severe stress; sleep-well-at-night credits |
| **Strategic** | 1.8 – 2.5 | Strong credits with identifiable but manageable risk factors; solid long-term holds |
| **Moderate Risk** | 2.6 – 3.3 | Credits requiring active monitoring; fundamentals acceptable but with meaningful vulnerabilities |
| **Speculative** | 3.4 – 4.0 | Credits with significant fundamental challenges; position only with clear catalyst and margin of safety |

**Important:** The roll-up is analyst-judgment weighted, not a simple average. A score of 4
on Liquidity with all other factors at 1 should NOT produce a "Strategic" rating — liquidity
risk is existential and can override all other strengths. Similarly, a 4 on Event Risk when an
LBO is imminent dominates the analysis.

**Judgment overrides to apply:**
- Any sub-factor at 4 → overall tier cannot be better than Moderate Risk
- Liquidity at 4 → overall tier is Speculative regardless of other scores
- Two or more sub-factors at 3+ → overall tier cannot be better than Strategic
- All sub-factors at 1-2 → Core or Strategic, depending on trajectory and cycle position

---

## 3. Lens 2: Relative Value Opinion (CS View)

This is the 6-12 month forward-looking view on spread performance vs the issuer's
sector and peer set. It explicitly separates the trading view from the fundamental quality
assessment.

### Step 1: Establish the Peer Set
- Use the IG sector map for IG names
- For HY: identify 4-8 names matched on rating bucket, sub-sector, and business mix
- For loans: match on leverage, sector, sponsor quality, and documentation type
- Be explicit about the peer set chosen — this anchors the entire RV analysis

### Step 2: Map Current Spread Levels
For the subject issuer and each peer:
- Current spread (OAS, ASW, or G-spread — be consistent)
- Spread percentile vs own 1yr and 3yr range (where in its own history?)
- Spread vs peer median: tight, in-line, or wide — and by how much (bp and %)
- Spread per turn of leverage: normalizes for different capital structures
- Curve shape: does the issuer's credit curve steepen or flatten vs peers?

### Step 3: Assess Spread Drivers
Decompose why the issuer trades where it does vs peers:
- **Fundamental premium/discount:** Do fundamental differences justify the spread gap?
- **Liquidity premium:** Is it a smaller/less liquid issuer trading wide for technical reasons?
- **Technical factors:** Index inclusion/exclusion, recent supply, ETF flows, dealer inventory
- **Event premium:** Is the market pricing in event risk (M&A, downgrade, litigation)?
- **Trajectory premium:** Is the market pricing fundamental improvement/deterioration?

### Step 4: Form the Relative Value Opinion

| Opinion | Criteria |
|---------|----------|
| **Outperform** | Expected excess return greater than sector/peers over 6-12 months. Spread is wide enough to more than compensate for identified risks. Catalyst for tightening exists. |
| **Market Perform** | Spread roughly in line with fair value vs peers. No strong catalyst in either direction. Carry is acceptable but no compelling alpha opportunity. |
| **Underperform** | Spread too tight vs peers relative to identified risks. Or fundamental deterioration not yet reflected in pricing. Negative catalyst approaching. |

### Step 5: Identify Catalysts and Time Horizon
- What specific events could drive spread movement? (earnings, rating action, refinancing, M&A, macro)
- Over what time frame?
- Is this a carry-and-hold recommendation or a tactical spread trade?
- What would change the opinion? (explicit stop-loss levels or invalidation triggers)

### Step 6: Cross-Check with Fundamental Quality
The most valuable signal comes from divergences between Lens 1 and Lens 2:

| Fundamental Quality | RV Opinion | Interpretation |
|--------------------|-----------:|----------------|
| Core/Strategic | Outperform | High-conviction long — fundamentals AND value aligned |
| Core/Strategic | Underperform | Strong credit but rich — reduce, take profits, or wait |
| Moderate Risk/Speculative | Outperform | Spread compensates for risk — tactical position with tight stops |
| Moderate Risk/Speculative | Underperform | Avoid — weak fundamentals AND poor value |
| Improving trajectory | Underperform | Monitor for inflection — potential future opportunity |
| Deteriorating trajectory | Outperform | Fading opportunity — spreads may be wide for good reason |

---

## 4. Lens 3: Structural & Documentation Assessment

For leveraged credits (HY bonds, leveraged loans, private credit), documentation
protection is the third critical dimension. For IG credits, this lens is lighter but still
relevant for event risk assessment.

### For HY Bonds — Key Covenant Provisions to Assess:

**Collateral Protection:**
- Security package: first lien, second lien, unsecured — what assets are pledged?
- Excluded assets and value leakage risk through unrestricted subsidiaries
- J. Crew risk: can IP or valuable assets be transferred beyond creditor reach?
- Lien priority and intercreditor agreement terms

**Default Protection:**
- Financial maintenance covenants (if any): leverage test, coverage test, minimum liquidity
- Incurrence covenants: debt incurrence, restricted payments, asset sales
- Cross-default and cross-acceleration provisions
- Definition of EBITDA — how many and how large are the addbacks?
- Sunset provisions on covenants

**Value Leakage Protection:**
- Restricted payments basket capacity (dividends, buybacks to equity holders)
- Investment baskets: how much can be moved to unrestricted subs or JVs?
- Asset sale proceeds: mandatory offer or reinvestment flexibility?
- Builder basket availability — can retained excess cash flow leave the restricted group?
- Incremental debt capacity: how much additional pari passu debt can be incurred?

**Reporting Protection:**
- Financial reporting frequency and timeliness
- Compliance certificate requirements
- Audited vs unaudited reporting obligations

### For Leveraged Loans — Additional Considerations:
- Maintenance financial covenants: leverage test cushion (headroom)
- EBITDA definition and addback flexibility
- Mandatory prepayment sweep terms (asset sales, excess cash flow, debt issuance)
- MFN sunset provisions
- Repricing protection (call protection, soft call periods)
- Yank-a-bank / replacement provisions

### For IG Credits — Simplified Documentation Focus:
- Change of control put provisions (coupon step-up or put at 101)
- Negative pledge and lien limitations
- Merger/consolidation restrictions
- Restricted subsidiaries vs unrestricted subsidiary structure
- Limitation on sale-leaseback
- Rating triggers on any facilities

### Documentation Strength Rating (1-5 scale):
- 1 (Highly Protective): Strong maintenance covenants, limited baskets, robust reporting
- 2 (Protective): Meaningful protections with standard market flexibility
- 3 (Market Standard): Typical terms for the asset class and rating; some flexibility
- 4 (Issuer Friendly): Wide baskets, generous addbacks, limited maintenance tests
- 5 (Very Issuer Friendly): Cov-lite or near cov-lite; significant flexibility; weak protections

---

## 5. Quantitative Risk Overlay

Layer quantitative signals on top of the qualitative assessment. These should confirm
or challenge the analyst view, not replace it.

### Credit Risk Estimate (Short-term, 1yr horizon)
- Implied default probability from CDS spreads (if available)
- Market-implied PD from bond spreads using recovery assumption
- Compare to: rating-implied historical default rate for the rating bucket
- If market-implied PD >> rating-implied → market sees risk agencies don't (or overliquidity)
- If market-implied PD << rating-implied → market is complacent or credit is upgraded-in-waiting

### Credit Quality Score (Medium-term, through-cycle)
- Altman Z-Score or Z"-Score (for manufacturing / non-manufacturing)
- Distance-to-default (Merton model-inspired): equity vol + leverage → PD estimate
- Rating migration probability: what is the historical probability of downgrade from current rating?
- Fallen Angel Score: for BBB-rated credits, estimate likelihood of falling to HY within 12 months

### Cross-Check: Quant vs Analyst Divergence
- If quant model says "deteriorating" but analyst says "stable" → investigate; something is lagging
- If quant model says "improving" but spreads are wide → potential buy signal
- Track migration over time — are signals converging or diverging?

---

## 6. Synthesis: Building the Credit Opinion

### The One-Page Credit Summary

After completing all three lenses, synthesize into a concise credit opinion:

**Header Block:**
- Issuer name, ticker, sector, sub-sector
- Agency ratings (Moody's / S&P / Fitch) with outlook
- Fundamental Quality Tier: [Core / Strategic / Moderate Risk / Speculative]
- Relative Value Opinion: [Outperform / Market Perform / Underperform]
- Documentation Score: [1-5] (for HY/loans; N/A for most IG)

**Executive Summary (3-5 sentences):**
- State the fundamental quality tier and the key factor driving it
- State the RV opinion and the primary spread driver
- Flag the single most important risk factor
- Note any divergence between fundamental and RV views
- State what would change the opinion

**Key Investment Considerations (ranked by materiality):**
List the 3-5 most important credit considerations, ranked from most to least material.
For each:
- The issue (what is it)
- The analyst view (how will it play out)
- The risk (what if we're wrong)

**Capital Structure Snapshot:**
- Total debt outstanding by instrument (bonds, loans, revolvers)
- Maturity profile: next 1yr, 2-3yr, 3-5yr, 5yr+
- Secured vs unsecured split
- Key financial metrics: leverage, coverage, FCF, liquidity

**Spread Context:**
- Current spread vs 1yr range, 3yr range
- Spread vs peer median
- Curve shape (if multiple maturities outstanding)

**Rating Agency Dynamics:**
- Current ratings with outlook/watch status
- What would trigger an upgrade? Downgrade?
- How close to a threshold (especially IG/HY boundary)?

**Catalysts (next 6-12 months):**
- Upcoming events that could move the credit (earnings, maturities, M&A, regulatory)
- Probability-weight the catalysts — what's the base case vs tail scenarios?

**What Would Change the View:**
- Explicit triggers for upgrading the opinion (e.g., "if leverage falls below 3.0x...")
- Explicit triggers for downgrading the opinion (e.g., "if they pursue a leveraged acquisition...")

---

## 7. Report Types & Output Templates

Match the depth and format to what the user needs:

### Quick Take (desk conversation)
- 2-4 paragraphs, prose format
- Cover: fundamental quality, spread context, and one-line view
- Use when the user asks "what do you think of X?" casually
- No tables or formal structure needed

### Earnings/Event Update
- Focus on what changed and the credit impact
- Key metrics vs prior quarter and expectations
- Spread reaction context
- Updated view (if changed) with specific rationale
- 1-2 pages of prose

### Full Tearsheet (comprehensive deep dive)
- Complete three-lens evaluation as described in Section 6
- Capital structure detail, financial history, peer comparison
- 3-5 pages equivalent
- Use when user asks for a "deep dive," "full analysis," or "tearsheet" on a name

### New Issue Assessment
- Issuer fundamental summary (abbreviated Lens 1)
- Proposed terms and where they should price relative to existing curve and peers
- Fair value estimate with concession analysis (see Workflow 2 in workflows.md)
- Covenant package assessment (Lens 3)
- Subscribe / pass recommendation with rationale

### Relative Value Screen
- Comp table format (see Workflow 1 in workflows.md)
- Spread data, key metrics, and RV opinion for each name in the peer set
- Rich/cheap visualization
- Specific pair trade or sector bet recommendations

---

## 8. Sector-Specific Adjustments

The six-factor framework applies universally, but the key metrics and emphasis shift
by sector. Apply these adjustments:

### Financials (Banks, Insurance, Asset Managers)
- Replace Debt/EBITDA with regulatory capital ratios (CET1, Tier 1, Total Capital)
- Profitability: ROE, ROA, efficiency ratio, NIM (banks), combined ratio (insurance)
- Asset quality replaces general credit quality: NPLs, NCOs, reserve coverage
- Liquidity: LCR, NSFR, deposit stability, wholesale funding reliance
- Regulatory risk is elevated: stress test results, GSIB surcharges, resolution planning
- Event risk: M&A is common; shareholder activism is rare; regulatory action is the key tail

### Utilities & Regulated Industries
- Cash flow quality driven by regulatory framework: constructive vs hostile commissions
- FFO/Debt is the key leverage metric (not Debt/EBITDA)
- Capex is often mandated and recovered through rates — assess regulatory lag
- Event risk: rate case outcomes, political/regulatory shifts, wildfire/environmental liability
- ESG transition risk is material: coal exposure, renewable mandates, stranded asset risk

### Energy (E&P, Midstream, Refining)
- Commodity price sensitivity is the dominant factor
- Hedging profile and hedge tenor matter enormously for cash flow visibility
- Reserve life, finding costs, and decline rates for E&P
- Contract quality, MVCs, and counterparty credit for midstream
- Crack spreads, throughput volumes, and turnaround schedules for refining

### Technology
- Often low or no leverage — focus on cash flow quality and competitive moat
- Revenue visibility: recurring/SaaS vs hardware/license
- Customer concentration and contract renewal risk
- M&A is the primary event risk (often debt-funded acquisitions)
- Rating agency dynamics: many large-cap tech at AA/A with minimal downgrade risk

### Healthcare
- Reimbursement risk (Medicare/Medicaid rate changes)
- Patent cliffs and pipeline optionality for pharma
- Leverage tolerance is high in this sector; focus on FCF-to-debt trajectory
- Litigation risk (opioids, PFAS, product liability) can be existential
- M&A is frequent and often transformative

### Real Estate (REITs)
- Net Debt/EBITDA and Secured Debt % are key metrics
- Unencumbered asset coverage ratio
- Occupancy rates, lease terms, and tenant quality
- Property type exposure (office is challenged; industrial/data center is favored)
- Access to unsecured debt markets is a critical differentiator

### Consumer & Retail
- Same-store sales trends and margin trajectory
- Working capital seasonality (especially for retailers)
- E-commerce disruption exposure
- Brand strength and pricing power
- Lease-adjusted leverage (capitalize operating leases)

---

## 9. Common Pitfalls

### Pitfall 1: Confusing Quality with Value
A BBB-rated credit with improving fundamentals trading at 200bp is not automatically
a buy. It might be perfectly priced. Conversely, a BB credit at 400bp might be cheap
if the market is pricing distress that won't materialize. Always separate the quality
assessment from the pricing assessment.

### Pitfall 2: Anchoring to Agency Ratings
Ratings lag reality, sometimes by quarters or years. A BBB+ credit can have BBB-
fundamentals if the agencies haven't caught up. Use ratings as a starting point, not
the conclusion. The quantitative overlay (Section 5) helps detect misalignment.

### Pitfall 3: Ignoring the Cycle
A credit that looks "Core" quality in mid-cycle may reveal itself as "Moderate Risk" in
a downturn. Stress-test fundamentals against a recession scenario, not just current
conditions. The cycle awareness principle (from the masters' frameworks) is critical here.

### Pitfall 4: Underweighting Liquidity
Liquidity kills credits faster than leverage. A 5x levered company with strong liquidity
and no near-term maturities is safer than a 3x levered company with a revolver expiring
in 6 months during a credit crunch. Always ask the "2AM test."

### Pitfall 5: Treating Documentation as Binary
"Cov-lite" doesn't mean "no protection." Even cov-lite loans have incurrence tests,
reporting requirements, and default triggers. Read the actual provisions — the details
matter enormously, especially in distressed scenarios where basis points of basket
capacity determine who controls the restructuring.

### Pitfall 6: Single-Factor Analysis
Never evaluate a credit on leverage alone, or cash flow alone, or spreads alone. The
three-lens framework exists because each lens captures information the others miss.
A complete credit opinion requires all three perspectives plus the quant overlay.

### Pitfall 7: Ignoring Who Owns the Bonds
The ownership base matters for technical dynamics. If a credit is heavily owned by
ETFs, it faces forced selling risk on downgrades/index exits. If owned by buy-and-hold
insurance accounts, spreads are stickier. If owned by hedge funds, spread moves
can be amplified. Understand the marginal buyer/seller (from the flow awareness principle).

### Pitfall 8: Neglecting the Capital Structure Waterfall
Analyzing the credit without mapping the full capital structure is like reading one chapter
of a book. Senior secured, senior unsecured, sub debt, holdco — each tranche has
different risk, different recovery, and different return characteristics. Always map the
waterfall before forming a view on any specific instrument.
