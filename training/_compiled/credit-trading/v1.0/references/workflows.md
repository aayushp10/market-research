# Credit Trading Workflows

Detailed templates for seven core analytical workflows. Each workflow specifies the
analytical steps, required inputs, suggested output format, and common pitfalls.
All workflows integrate the masters' frameworks from `references/masters_frameworks.md`.

## Table of Contents
1. Relative Value / Comp Tables
2. New Issue Analysis
3. Event-Driven Scenarios
4. Capital Structure Analysis
5. Cycle Positioning & Macro-Credit
6. Distressed & Special Situations
7. Flow & Technical Analysis

---

## 1. Relative Value / Comp Tables

### When to Use
User wants to compare spreads across peers, identify rich/cheap opportunities, or screen
a sector for value. Also use when a user asks "where should X trade?" or "is X tight/wide?"

### Analytical Steps

**Step 1: Define the comp universe**
- Start with the IG sector map (`references/ig_sector_map.md`) if the issuer is IG
- For HY/loans, ask the user for the relevant universe or use training knowledge
- Comps should match on: rating bucket, sector, business mix, and ideally size/liquidity
- Be explicit about why each comp was chosen and any weaknesses in the comp set
- Typical comp set: 4-8 names. Fewer is too thin; more dilutes signal

**Step 2: Gather spread data**
- If user provides data: use it directly
- If not: search for recent levels, but caveat staleness clearly
- Key metrics to capture for each name:
  - Spread (OAS or ASW, be consistent across comps)
  - Rating (Moody's / S&P / Fitch — note split ratings)
  - Tenor / maturity
  - Coupon
  - Issue size / liquidity proxy
  - Key credit metrics (leverage, coverage, FCF margin — varies by sector)

**Step 3: Normalize and compare**
- Adjust for tenor differences (interpolate or use matched-maturity where possible)
- Adjust for rating differences (e.g., notch-adjusted comparison)
- Adjust for liquidity (smaller/less liquid issues should trade wider, all else equal)
- Consider the credit curve shape — compare 5s vs 10s vs 30s separately if relevant

**Step 4: Apply Fridson spread decomposition**
- For each comp, estimate: default risk premium + liquidity premium + risk premium
- Identify where the risk premium is highest relative to fundamental risk
- A credit with a high risk premium vs peers may be cheap; low risk premium may be rich
- Cross-check with Altman-style fundamental indicators (leverage trajectory, coverage trend)

**Step 5: Identify rich/cheap with second-level thinking**
- Calculate spread differential vs comp median or mean
- Express as both absolute bp difference and percentile rank
- Flag any names that look mispriced and hypothesize why:
  - Technicals (index inclusion/exclusion, forced selling, new supply)
  - Fundamentals (credit trajectory diverging from peers)
  - Liquidity (smaller issue, off-the-run, orphaned by downsized dealer desks)
  - Event risk (M&A, regulatory, litigation)
- Apply second-level thinking: does the consensus see what you see? If the name is
  "obviously" cheap, why hasn't it already tightened? What do you know that others don't?

**Step 6: Formulate the trade with margin of safety**
- If a rich/cheap opportunity exists, specify the trade: long the cheap name, short the rich
- Quantify carry and roll-down (Gross decomposition)
- Calculate breakeven spread widening — your margin of safety from total return perspective
- Identify the catalyst for convergence
- Size the risk: what's max adverse spread move before you'd cut?
- Suggest hedge: index (CDX/iTraxx), single-name CDS, or paired bond trade
- State what would invalidate the trade

### Output Format
- **Comp table**: xlsx if >5 names (sortable, filterable). Markdown table if ≤5.
- **Scatter plot**: spread vs rating or spread vs leverage — helps visualize outliers
- **Summary prose**: 2-3 paragraph write-up with thesis, margin of safety, and risk/reward

### Common Pitfalls
- Comparing bonds of very different tenors without adjustment
- Ignoring liquidity premium (a 150mm issue should trade wider than a 2bn benchmark)
- Using stale spread data for relative value (anything >1 week old is directional only)
- Comp set too narrow (2 names) or too broad (mixing IG and HY)
- Forgetting to check for upcoming catalysts that explain apparent mispricing
- First-level thinking: calling something "cheap" just because the spread is wider than peers
  without asking why it's wider

---

## 2. New Issue Analysis

### When to Use
User asks about a new bond, loan, or note issuance — pricing, fair value, concession,
whether to participate, or post-pricing assessment.

### Analytical Steps

**Step 1: Understand the deal terms**
Required inputs (ask user if not provided):
- Issuer, rating, sector
- Tranche details: tenor, coupon type (fixed/FRN), benchmark, spread talk/guidance
- Deal size (expected and final)
- Use of proceeds (refinancing, acquisition, general corporate)
- Any structural features (call protection, covenants, collateral)

**Step 2: Establish fair value from secondary**
- Pull the issuer's existing curve (secondary levels across outstanding bonds)
- If new issuer, use closest comps from sector map
- Interpolate to the new issue's maturity point
- This gives the "secondary fair value" — where a fungible bond would trade

**Step 3: Estimate new issue concession (NIC)**
- NIC = new issue spread - secondary fair value
- Typical NIC ranges (these vary with market conditions):
  - IG: 3-10bp in calm markets, 10-25bp in volatile markets
  - HY: 25-50bp normally, wider in stress
  - Loans: 25-50bp OID equivalent
- NIC is compensation for: uncertainty, liquidity risk during distribution, dealer PnL
- If NIC is very tight: deal is priced aggressively, likely strong demand / trophy asset
- If NIC is very wide: credit concern, market weakness, or forced timing

**Step 4: Cycle-adjust your assessment**
- Where are we in the cycle? (Marks/Dalio framework)
- Late cycle with tight spreads → NIC should be higher to compensate; thin NIC = red flag
- Early cycle with wide spreads → NIC may be lower because the base spread already compensates
- Is the issuance trend consistent with late-cycle behavior? (tenor extension, cov-lite, PIK)
- Is the issuer's leverage trajectory consistent with where we are in the cycle?

**Step 5: Assess orderbook dynamics (King flow framework)**
- Book size vs deal size (2x+ is solid, 3x+ is strong, 5x+ is exceptional)
- Did the deal price through talk, in-line, or wide of talk?
- Was the deal upsized? (signals strong demand)
- Who is buying? (real money = sticky, fast money = potential flip risk)
- Are there passive/index flows expected after seasoning?

**Step 6: Total return assessment (Gross decomposition)**
- Calculate expected carry over your holding period
- Estimate roll-down based on credit curve slope
- What breakeven spread widening can you tolerate?
- Factor in the NIC — does it provide enough cushion?

**Step 7: Post-pricing assessment**
- Where does the bond trade in the break? (tightening = successful placement)
- How does the NIC compare to recent deals in the same sector?
- Did the deal change the issuer's curve shape?
- Was there any secondary cheapening in existing bonds (supply indigestion)?

### Output Format
- **Fair value build-up table**: show the math from secondary curve to NIC estimate
- **Prose recommendation**: participate at X spread with Y allocation, or pass because Z
- **Comp table**: if building fair value from peers, show the comp set used

### Common Pitfalls
- Using stale secondary levels as "fair value" in a moving market
- Ignoring curve shape (a 10yr NI when existing curve is inverted is a different analysis)
- Conflating oversubscription with credit quality (momentum buyers inflate books)
- Not considering the use of proceeds (debt-funded M&A vs refinancing are very different signals)
- Forgetting to factor in the issuer's forward supply calendar (more supply coming = less urgency)
- Ignoring cycle context — a deal that looks "fine" in a vacuum may be late-cycle aggressive

---

## 3. Event-Driven Scenarios

### When to Use
User asks about credit impact of: M&A (acquirer or target), LBO, spin-off, restructuring,
rating action, refinancing, regulatory change, or litigation outcome.

### Analytical Steps

**Step 1: Identify the event and affected instruments**
- What is happening? (merger, LBO, spin-off, downgrade, etc.)
- Which entities are affected? (acquirer, target, surviving entity, spun-off entity)
- Which instruments move? (bonds, loans, CDS, equity)
- What is the capital structure before and after?

**Step 2: Map credit impact by scenario**

For **M&A (acquirer is IG)**:
- How much debt is being added? What does pro forma leverage look like?
- Is the acquirer committed to deleveraging? Timeline?
- Rating agency guidance: negative watch, downgrade expected?
- Change of control provisions in target's bonds?
- Spread impact: typically 10-30bp wider for acquirer, target may tighten if being acquired by stronger name

For **LBO (target going from IG to HY)**:
- Pro forma leverage (total debt / EBITDA)
- Typical LBO capital structure: secured TL + unsecured notes + holdco PIK
- Recovery analysis: what do existing bonds recover?
- Change of control puts: which bonds have them, at what price?
- Timing: when does the deal close? What happens between announcement and close?
- Apply Milken's fallen angel framework: forced selling by IG mandates creates dislocation

For **Spin-off**:
- How is debt allocated between parent and spin-off?
- Which entity is stronger? (ratings, cash flow, asset quality)
- Are existing bondholders stuck with the weaker entity?
- Covenant analysis: is there protection against asset stripping?

For **Downgrade / Upgrade**:
- One notch or multi-notch?
- Does it cross the IG/HY boundary? (fallen angel / rising star dynamics)
- Index implications: removal from IG index forces selling; addition to HY index forces buying
- Quantify the flow: how much is in passive/index-constrained mandates? (King framework)
- Apply Milken's insight: fallen angel forced selling typically overshoots fair value

**Step 3: Quantify spread scenarios with distributional thinking**
Build a 3-scenario framework:
- **Bull case**: deal is credit positive or neutral, spreads tighten or hold
- **Base case**: moderate credit impact, spreads widen X bp
- **Bear case**: deal is worse than expected, rating downgrade, spreads widen Y bp
- For each scenario, estimate probability and expected spread move
- Calculate expected value of the position
- Calculate margin of safety: in the bear case, what do you lose? Can you tolerate it?

**Step 4: Identify the trade with second-level thinking**
- Where is the market pricing the event? (implied probability from current spread)
- Is the market over- or under-pricing the risk?
- What is the consensus view? Where might consensus be wrong?
- What is the right instrument? (bonds vs CDS vs equity)
- Carry while you wait: what does the position earn if nothing happens?
- Time decay: does the trade have a shelf life?

### Output Format
- **Scenario table**: 3 scenarios with probability, spread impact, P&L
- **Capital structure visual**: before and after the event (waterfall chart or table)
- **Prose analysis**: 3-5 paragraphs covering thesis, risks, and recommendation
- **Timeline**: key dates (announcement, shareholder vote, regulatory approval, close)

### Common Pitfalls
- Analyzing the acquirer without looking at the target (and vice versa)
- Ignoring change of control provisions (these are money — read the covenants)
- Assuming the rating agencies will act immediately (they lag, sometimes by months)
- Underestimating index rebalancing flows for IG/HY crossover events
- Forgetting that CDS and bonds can react differently (basis moves are the trade)
- Not considering the funding/financing risk if the deal falls apart
- Missing the reflexive loop: M&A funded by cheap debt in late cycle → leverage → downgrades → spread widening → less M&A

---

## 4. Capital Structure Analysis

### When to Use
User asks about an issuer's debt stack, recovery analysis, subordination, relative value
within the cap structure, or basis trading opportunities (bonds vs CDS vs equity).

### Analytical Steps

**Step 1: Map the full capital structure**
From top to bottom (priority of claims):
1. Revolving credit facility (super-senior, typically undrawn or partially drawn)
2. First lien term loans (secured, first priority)
3. Second lien term loans (secured, second priority — common in HY/leveraged)
4. Senior secured bonds
5. Senior unsecured bonds
6. Subordinated / junior bonds
7. Preferred equity / hybrid instruments
8. Common equity

For each tranche capture:
- Outstanding amount
- Coupon / spread
- Maturity
- Call features / make-whole
- Covenants (maintenance vs incurrence, key thresholds)
- Current trading level (price or spread)

**Step 2: Calculate leverage at each level**
- Secured leverage = secured debt / EBITDA
- Total leverage = total debt / EBITDA
- Net leverage = (total debt - cash) / EBITDA
- Interest coverage = EBITDA / interest expense
- FCF to debt service = (EBITDA - capex - tax - working capital) / (interest + mandatory amort)
- Apply Altman Z-Score variable logic: which indicators are deteriorating?

**Step 3: Recovery analysis (Altman + Lasry)**
- Enterprise value estimation (EV/EBITDA multiple approach):
  - Bear case: trough multiple x stressed EBITDA (use cyclically-adjusted, Altman-informed)
  - Base case: average multiple x normalized EBITDA
  - Bull case: peak multiple x current EBITDA
- Use Altman's recovery research: apply cyclically-adjusted recovery rates, not long-run averages
- Waterfall the EV through the capital structure:
  - Administrative claims (DIP, professional fees — typically 3-5% of EV)
  - Secured claims (first lien recovery)
  - Unsecured claims (pro rata distribution of remaining value)
  - Equity (residual, if any)
- Express recovery as cents on the dollar for each tranche
- Identify the fulcrum security (Lasry framework)

**Step 4: Relative value within the capital structure**
- Compare spread per turn of leverage across tranches
- Is the secured/unsecured basis fair? (i.e., is the unsecured bond compensating you enough for being structurally subordinated?)
- Compare bond spread vs CDS spread (basis analysis):
  - Negative basis (CDS < bond): consider buying the bond and buying CDS protection
  - Positive basis (CDS > bond): consider selling CDS protection if you like the credit
- Compare across the curve: is the 5yr/10yr slope appropriate for this credit?

**Step 5: Identify structural risks (Richards/Marathon legal framework)**
- Maturity wall: when do large maturities come due? Can the issuer refinance?
- Covenant headroom: how close is the issuer to tripping maintenance covenants?
- Restricted payments: can the issuer dividend cash upstream to holdco?
- Incremental debt capacity: can they add more debt ahead of you?
- Asset sale provisions: can they sell assets and not apply proceeds to your tranche?
- J.Crew / Chewy / Serta risk: are valuable assets at risk of being moved to unrestricted
  subsidiaries or new first-lien baskets? Read the indenture for trap-door provisions.
- Intercreditor dynamics: who controls the restructuring if it happens?

**Step 6: Margin of safety assessment (Klarman)**
- At current prices, what is your margin of safety?
- If you buy at current spread and the worst case materializes, what's your loss?
- Is the margin of safety coming from price (discount to par), structure (seniority,
  covenants), or business (cash flow durability)?

### Output Format
- **Capital structure table**: always produce this, either markdown or xlsx
- **Waterfall chart**: matplotlib visualization showing claims priority and recovery
- **Recovery sensitivity table**: recovery at different EV/EBITDA multiples
- **Prose summary**: key findings, structural risks, fulcrum identification, and RV observations

### Common Pitfalls
- Missing off-balance-sheet obligations (operating leases, pension, guarantees)
- Using reported EBITDA without adjusting for addbacks (especially in sponsor-backed credits)
- Ignoring the revolver (it's senior to everything and can prime you in a restructuring)
- Treating all "senior unsecured" as equal (holding company vs operating company matters)
- Confusing bond-level recovery with claim-level recovery (accrued interest, make-whole claims)
- Not reading the actual indenture for trap-door covenants
- Using long-run average recovery rates instead of cycle-adjusted rates

---

## 5. Cycle Positioning & Macro-Credit (NEW)

### When to Use
User asks "where are we in the credit cycle?", "should I be adding or reducing risk?",
"what does the macro setup mean for credit?", or any question about broad market positioning.

### Analytical Steps

**Step 1: Cycle phase identification (Marks + Dalio)**
Assess each indicator and map to cycle phase:

| Indicator | Early Expansion | Mid Expansion | Late Expansion | Downturn | Trough |
|-----------|----------------|---------------|----------------|----------|--------|
| Spreads | Wide, compressing | Mid-range | Near tights | Widening | At wides |
| Standards | Tight | Reasonable | Loose (cov-lite) | Tightening fast | Frozen |
| Leverage | Declining | Stable | Rising | Peaking | Deleveraging |
| Default rates | Peaking/declining | Low | Very low | Rising | Peaking |
| Issuance | Low/recovering | Moderate | Record pace | Declining | Near zero |
| Sentiment | Fear/cautious | Neutral/optimistic | Euphoric | Panic | Despair |
| Dispersion | High | Moderate | Low | Rising fast | Very high |

**Step 2: Reflexivity assessment (Soros)**
- Is there a positive reflexive loop operating? (credit availability → asset appreciation → stronger fundamentals → more credit)
- How mature is the loop? (early loops are self-reinforcing; mature loops are fragile)
- What could trigger reversal? (rate shock, geopolitical event, single large default, sector-specific stress)
- How much of current fundamental strength is cycle-dependent vs durable?

**Step 3: Spread adequacy assessment (Fridson decomposition)**
- Current spread vs historical distribution (percentile rank)
- Actuarial default cost at current default rates vs at cycle-average default rates
- Risk premium: are you being compensated for bearing cycle risk?
- Breakeven analysis: how much spread widening can you absorb before losing money?

**Step 4: Flow and technical context (King)**
- Central bank stance and balance sheet trajectory
- ETF flows (LQD, HYG, IGSB, JNK — net inflows/outflows)
- Foreign demand dynamics (FX-hedged yield attractiveness)
- Dealer positioning and balance sheet capacity
- Systematic/quant positioning (are models long or short credit risk?)
- Supply calendar: what's coming in the next 30/60/90 days?

**Step 5: Macro transmission channels**
Map macro variables to credit through specific transmission channels:
- **Rates → Credit:** Higher rates → higher debt service → pressure on leveraged borrowers → wider spreads in HY. But: higher rates with strong growth → IG can tighten.
- **Inflation → Credit:** Moderate inflation helps (nominal growth inflates away leverage). High inflation hurts (input costs, margin compression, tighter policy).
- **Growth → Credit:** Strong growth → lower defaults → tighter spreads. Weak growth → rising defaults → wider spreads. Nuance: sector dispersion increases as growth differentiates winners from losers.
- **Oil/commodities → Credit:** Direct impact on energy credits. Indirect impact on consumer (gas prices → discretionary spending → retail/consumer credit). Geopolitical risk premium affects all credits.
- **FX → Credit:** Strong USD → pressure on EM and USD-funded foreign corporates. Weak USD → capital flows into USD credit from foreign investors.

**Step 6: Positioning recommendation**
Based on the above, recommend:
- Overall risk level: overweight, neutral, or underweight credit risk
- Curve positioning: front end vs belly vs long end (with rationale)
- Quality positioning: up-in-quality vs down-in-quality
- Sector tilts: defensive vs cyclical, and specific sector over/underweights
- Instrument selection: cash vs CDS, IG vs HY, secured vs unsecured
- Hedging: what tail risks are worth hedging and how?

### Output Format
- **Cycle scorecard**: indicator dashboard with current readings and cycle phase
- **Prose analysis**: 3-5 paragraphs on the current environment and positioning
- **Risk/reward matrix**: expected return scenarios at current spread levels
- **Sector heat map**: relative attractiveness across sectors

### Common Pitfalls
- Confusing "fundamentals are strong" with "it's a good time to buy credit" — Marks' insight
  is that strong fundamentals at tight spreads can be a terrible entry point
- Ignoring flows and technicals in a flow-driven market
- Anchoring to recent spreads instead of assessing where fair value is across the cycle
- Not stress-testing your positioning for the scenario where you're wrong
- Treating the credit cycle as perfectly predictable — it's not; you can identify phases
  but not turning points

---

## 6. Distressed & Special Situations (NEW)

### When to Use
User asks about a credit trading at distressed levels (typically <80 cents, or spread >1000bp),
a restructuring, bankruptcy, or special situation where the standard IG/HY framework doesn't apply.

### Analytical Steps

**Step 1: Triage — is this cyclical or structural? (Richards/Marathon)**
The single most important question in distressed:
- **Cyclical distress:** Good business, bad balance sheet. Revenue is depressed by macro
  conditions but will recover. The capital structure needs fixing, but the business survives.
  → Buy at distressed levels, earn recovery premium.
- **Structural distress:** Bad business, regardless of balance sheet. Revenue is in secular
  decline (technology disruption, regulatory change, competitive obsolescence).
  → Avoid or short. No capital structure fix saves a dying business.

**Step 2: Map the capital structure and find the fulcrum (Lasry)**
- Full capital structure mapping (see Workflow 4)
- Build 3 EV scenarios using trough multiples
- Run the waterfall to identify the fulcrum security in each scenario
- The fulcrum is where the most optionality exists — and where you should focus

**Step 3: Legal and document review (Richards/Marathon)**
This step is non-negotiable in distressed:
- Read the credit agreement / indenture — actually read it
- Key provisions to check:
  - Change of control
  - Restricted payments baskets
  - Asset sale / collateral release provisions
  - Unrestricted subsidiary definitions and baskets
  - Incremental facility capacity
  - Cross-default and cross-acceleration provisions
  - Minimum liquidity or leverage maintenance covenants
  - Intercreditor agreement provisions (for multi-lien structures)
- Identify trap doors, J.Crew baskets, uptier exchange mechanics
- Map who controls the process if it goes to restructuring

**Step 4: Recovery analysis (Altman + Moyer framework)**
- **Liquidation analysis:** Sum of parts — what are the assets worth in a fire sale?
  - A/R: 60-80% of book
  - Inventory: 30-60% of book (varies hugely by type)
  - PP&E: 20-50% of book (specialized = low; generic = higher)
  - IP/Intangibles: highly variable, often near zero in liquidation
  - Real estate: independent appraisal value
- **Going concern analysis:** What is the reorganized entity worth?
  - Normalized EBITDA × appropriate multiple
  - Use comparables, but discount for distress friction (legal costs, customer/supplier flight)
  - Account for DIP costs, professional fees, and time value of money through the process
- Apply Altman's cyclical recovery framework: use stressed recovery rates if macro is weak

**Step 5: Catalyst identification (Richards/Marathon)**
No trade without a catalyst. Map the timeline:
- Maturity dates: when does debt come due that forces a reckoning?
- Covenant test dates: when does the next maintenance test occur?
- Litigation milestones: trial dates, settlement deadlines
- Asset sale processes: timeline for 363 sales or private sales
- DIP financing: terms, maturity, conversion features
- Plan confirmation: expected timeline, voting classes, cram-down risk

**Step 6: Scenario-based P&L with margin of safety (Klarman)**
For each scenario (restructuring, liquidation, out-of-court exchange, status quo):
- What is the recovery for each tranche?
- What is the timeline to realization?
- What is the IRR at current price?
- What is the downside if the worst case materializes?
- Is there a margin of safety at current price?

**Step 7: Position sizing and risk management**
Distressed positions require different sizing than performing credit:
- Higher individual position risk → smaller position sizes
- Liquidity is poor → you may not be able to exit
- Binary outcomes are common → size for the worst case
- If you're large enough to be at the table in restructuring → different calculus

### Output Format
- **Capital structure with recovery waterfall**: the centerpiece of any distressed analysis
- **Scenario table**: recovery by tranche across 3+ scenarios
- **Timeline chart**: key dates and catalysts
- **Prose analysis**: thesis, variant perception, margin of safety, risks, exit strategy

### Common Pitfalls
- Buying at 60 cents and thinking you have a "margin of safety" without doing recovery analysis
  (60 cents is not cheap if recovery is 30)
- Ignoring the documents — this is where most distressed investors get burned
- Falling in love with the business without fixing the balance sheet
- Underestimating legal and advisory costs in bankruptcy (can consume 5-10% of EV)
- Ignoring liquidity risk — distressed bonds can gap 10+ points on thin volume
- Not identifying the fulcrum — owning paper above or below it gives you different economics
- Assuming restructuring will be quick (average Chapter 11 takes 12-18 months)

---

## 7. Flow & Technical Analysis (NEW)

### When to Use
User asks about market technicals, fund flows, positioning, supply/demand dynamics,
dealer behavior, index rebalancing, or wants to understand short-term spread drivers
independent of fundamentals.

### Analytical Steps

**Step 1: Supply analysis**
- What is the primary issuance calendar? (next 30/60/90 days)
- How does current supply compare to historical run rate?
- Is supply concentrated in specific sectors or tenors?
- Are issuers extending tenor? (late-cycle signal)
- Net supply = gross issuance - maturities - tenders - calls. Net supply is what matters.
- Current thematic drivers: AI/hyperscaler mega-deals, M&A-related issuance, utility capex

**Step 2: Demand analysis (King framework)**
Map the buyer base and assess each segment:
- **Insurance / pensions:** Structural, price-insensitive demand. Track funded status for
  pensions (higher funded status → more LDI buying), regulatory capital rules for insurers.
- **ETF / passive:** Track daily flows into LQD, HYG, IGSB, JNK, VCSH. Large inflows
  compress spreads indiscriminately; large outflows widen everything.
- **Foreign investors:** FX-hedged yield differential is the key variable. When cross-currency
  basis makes USD credit attractive for Japanese/European buyers → strong demand.
- **CLOs:** Track CLO new issuance and reinvestment capacity. CLOs are the largest buyer
  of leveraged loans and a significant buyer of HY. When CLO creation is strong → loan
  spreads compress. When CLOs trip reinvestment tests → forced selling.
- **Retail:** Track fund flows into mutual funds and ETFs. Retail is a momentum buyer
  (buys after spreads tighten, sells after spreads widen) → amplifies moves.

**Step 3: Positioning analysis**
- Dealer inventory: are dealers long or short credit? (Short inventory = less supply
  overhang; long inventory = potential for dealer selling if markets weaken)
- Systematic/quant positioning: BNP Credit Pulse, JPM positioning indicators. Are systematic
  models long or short credit? These models are momentum-driven and reflexive.
- Hedge fund positioning: net long or short? Tracking through prime brokerage data,
  CFTC positioning reports for credit futures/options.
- Insurance/pension positioning: are they fully allocated or have dry powder?

**Step 4: Technical levels and cross-market signals (Tchir)**
- Key spread levels: previous wides/tights, moving averages, breakout levels
- CDS-bond basis: is the synthetic or cash market leading?
- Credit vs equity divergence: if equity is resilient but credit is widening → pay attention
  to credit (historically a better leading indicator of stress)
- VIX/MOVE vs credit spreads: are vol markets pricing risk that credit isn't?
- iTraxx vs CDX: is European or US credit leading the move?

**Step 5: Index rebalancing mechanics**
Check for upcoming or recent rebalancing events:
- Fallen angels: which names are on negative watch at the IG/HY boundary?
  Estimate forced selling volume = IG AUM × index weight × % of holders that are constrained
- Rising stars: which HY names are on positive outlook for upgrade?
- Index rolls: CDX and iTraxx roll semi-annually (March/September). Roll mechanics create
  predictable spread moves in on-the-run vs off-the-run series.
- Month-end / quarter-end rebalancing: duration extension trades, index tracking adjustments

**Step 6: Synthesis — what the technicals are telling you**
Put it all together:
- Is the supply/demand balance supportive or challenging?
- Is positioning crowded or light?
- Are flows reinforcing or opposing the fundamental direction?
- What is the short-term vs medium-term signal from technicals?
- Where might technicals create opportunities to buy/sell at better levels than fundamentals
  alone would justify?

### Output Format
- **Flow dashboard**: summary of key flow indicators with directional signals
- **Supply calendar**: upcoming issuance with sector/tenor breakdown
- **Positioning summary**: where key investor segments are positioned
- **Prose analysis**: how technicals are affecting current spread levels and near-term outlook

### Common Pitfalls
- Treating technicals as the whole story — they drive short-term moves but fundamentals
  dominate over quarters and years
- Overreacting to one day's ETF flow (look at multi-day/week trends)
- Ignoring positioning when it's at extremes (crowded longs are vulnerable to reversal)
- Not understanding the mechanics of forced selling (index rebal, CLO tests, margin calls)
  and the opportunity it creates for patient capital
- Assuming foreign demand is permanent — it fluctuates with FX hedging costs
- Ignoring dealer balance sheet constraints — they can cause spreads to gap in stress

---

## General Principles Across All Workflows

- **Always state your assumptions.** If you're assuming a specific EBITDA multiple, say so.
  If spread data is from search results and may be stale, flag it.
- **Show your work.** For any quantitative output, the user should be able to trace every
  number back to an input or assumption.
- **Separate fact from opinion.** Label market color, personal assessment, and hard data differently.
- **Time-stamp everything.** Credit is a moving target. Note when data was observed.
- **Think about who is on the other side.** Every trade has a counterparty. Why are they willing
  to take the other side? If you can't answer this, your thesis may be consensus (and therefore
  already priced in).
- **Apply second-level thinking.** Before finalizing any recommendation, ask: what does the
  consensus think, and where might I be wrong?
- **Quantify the margin of safety.** Whether it's breakeven spread widening, recovery in
  the worst case, or carry cushion — know your downside.
- **Decompose expected return.** Carry + roll-down + spread change + rate change. Know which
  component you're betting on and which might work against you.
- **Check cycle positioning.** The same trade at the same spread level can be brilliant
  early in the cycle and catastrophic late in the cycle. Context matters.
