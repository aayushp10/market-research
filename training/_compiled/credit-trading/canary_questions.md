# Canary Questions — credit-trading skill

Each question has one or more required substrings. A compile passes canaries
if, when asked the question using ONLY the newly-compiled skill as context,
the answer contains every required substring (case-insensitive, whitespace-flexible).

Questions are rerun every compile. Failures block `/compile approve`.

Add new canaries sparingly — each one is a commitment that the skill must
continue to encode that specific idea. Tune the required substrings to be
load-bearing phrases, not generic finance vocabulary.

---

## Q1: Core reasoning framework
Q: What are the first three questions you ask when reasoning about any credit move?
Required: "what changed", "who is forced", "why now"

## Q2: Margin of safety in credit
Q: How do you think about margin of safety specifically for credit, not equity?
Required: "upside is capped", "downside", "seniority"

## Q3: Energy decomposition rule
Q: When WTI moves more than 5 percent in a day, why should you refuse to report "Energy IG" as a single spread read?
Required: "sub-", "integrated", "refin"

## Q4: Three-lens framework
Q: What are the three lenses in the individual credit evaluation methodology?
Required: "fundamental", "relative value", "documentation"

## Q5: Total return decomposition
Q: What are the four P&L drivers for a bond position?
Required: "carry", "roll-down", "spread", "rate"

## Q6: Directional causation
Q: Does software sector weakness propagate symmetrically between tech BDCs and hyperscaler capital structure?
Required: "not", "different", "cohort"
