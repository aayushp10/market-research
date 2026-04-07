# Market Research Vault — Agent Instructions (Root)

You are operating inside Aayush's credit research vault. Your job varies by task — you might be ingesting a source, writing a deep dive, compiling a skill, drafting a briefing, promoting a ledger entry, or something else — but the operating discipline in this file applies to every task, always.

Read this file at the start of every session. Then read the per-folder `CLAUDE.md` for the area you're operating in:

- `training/CLAUDE.md` — when ingesting training sources or running the compile pipeline
- `research/CLAUDE.md` — when ingesting raw research sources, writing deep dives, briefings, or any research artifact
- `journal/CLAUDE.md` — when processing journal entries
- `ledger/CLAUDE.md` — when handling ledger promotions, resolutions, or reviews
- `concepts/CLAUDE.md` — when creating or updating concept stubs

---

## The architecture in one minute

The vault has four content areas plus a shared graph layer:

- **`training/`** — the source corpus the credit-trading skill compiles from. Primers, frameworks, conversations, post-mortems. The skill is a compiled artifact, not a hand-maintained document. You update the skill by dropping new sources into training and triggering a recompile.
- **`research/`** — working research. Raw sources in `_raw/`, work products in `credit/`, `macro/`, `briefings/`. This is where deep dives, situations, themes, and issuer pages live.
- **`journal/`** — Aayush's in-the-moment log. Fast, append-only, Slack-first. Trades, conversations, reading reactions, observations.
- **`ledger/`** — the scoreboard. Predictions graded against reality. Promotion-only (never written directly). Resolutions flow back into training via the monthly review ritual.
- **`concepts/`** — shared graph layer. Thin stub pages (~80 words each) that any content area can wikilink to. Lazily created on first invocation. Never bulk-generated.

The system compounds through four arrows: library → school (research outcomes promoted to training post-mortems), school → skill (training corpus compiled into the skill), skill → library (the skill is used to produce new research), library → library (the concepts graph accumulates backlinks that make future retrieval richer).

---

## The inference-review pattern (meta-rule)

This is the single most important pattern in the vault. It governs every interaction where you need to apply human judgment to content you're producing or processing. Whenever you need to make classification calls, tag assignments, promotion decisions, stub creation choices, or rule changes, you follow this pattern.

**The pattern:**

1. **Do the work, inferring as much as you can.** Read the material, make your best classification decisions, draft the structured output.
2. **Present the result to Aayush with honest confidence markers.** Every field you've determined is marked:
   - `[inferred]` — you're confident, with specific reasoning available on request
   - `[guess]` — you're making an educated guess but could easily be wrong
   - `[needs input]` — you can't reasonably determine this from the available material
3. **Accept freeform prose response.** Aayush can reply with "confirmed" (accept all), with selective corrections ("drop tag X, add tag Y, trust_weight should be medium"), or with a full replacement.
4. **Show a diff of what changed on the user's reply.** Before finalizing, post a brief "updated X, Y; Z unchanged" summary so Aayush has a last-look moment.
5. **Apply and file on confirmation.** Write the final content, commit with a descriptive git message, move to the next task.

**Rules within the pattern:**

- You may ask ONE clarifying follow-up if the user's reply is ambiguous. Not two, not three. If still ambiguous after one follow-up, mark the file as needing manual attention and stop — never guess.
- You MUST provide reasoning for any `[inferred]` or `[guess]` field if asked. "Why did you think this was a primer?" gets a real answer about structural cues, author voice, content density, etc.
- You MUST NOT silently file content. Every decision gets a confirmation step, even when every field is `[inferred]` and highly confident.
- You MUST NOT infer judgment-laden fields (trust_weight, author, origin) dishonestly. If you're not sure, mark it `[guess]` or `[needs input]`. Artificial humility is also wrong — if you can see the Marks signature on a Marks memo, mark the author as `[inferred]` with high confidence.

**Where the pattern applies:**

- Ingestion tagging (training, research, journal)
- Ledger promotion proposals
- Ledger resolution proposals
- Concept stub creation (inline during research writes)
- Post-mortem drafting from ledger reviews
- Skill compile diff approval
- Rule change proposals
- Theme promotion from clustered situations
- Any other place you need Aayush's judgment on content you've produced

This pattern is the contract between you and Aayush. Honor it. Do not invent new shortcuts.

---

## Universal rules

### Provenance is mandatory

Every claim on every research page, every ledger entry, every briefing, every deep dive must be traceable to a specific raw source in `research/_raw/` or a specific training source. No exceptions.

- Research artifacts cite raw sources via wikilinks: `[[research/_raw/credit/issuers/2026-04-02-blue-owl-reuters]]`.
- Training-derived claims (methodology, frameworks) are embedded in the compiled skill and don't need explicit citations — the skill itself is the authority.
- Wiki pages are NEVER evidence for claims on other wiki pages. This is the author-laundering firewall. You may reference other pages for context, but the *evidence* must always trace back to a primary source.
- If you want to make a claim and cannot find a source for it, either find one or don't make the claim. Fabrication is a serious discipline violation.

### Facts and views are separated (the firewall)

- **Facts layer:** issuer pages, sector pages, market pages, raw source citations, concept stubs, macro state snapshots. These are "what the sources say, paraphrased, with citations." They contain no opinions about whether something is cheap, attractive, or actionable.
- **Views layer:** situations, themes, ledger entries, journal entries, briefing Dig/Setups sections. These are "Aayush's thesis, dated, with kill criteria or falsifiability."
- These layers never mix on the same page. If you find yourself writing "this looks cheap" on an issuer page, STOP — that belongs in a situation or theme file.
- When ingesting or updating content, default to the facts layer. View-layer updates require explicit direction from Aayush or come from promotion flows (deep dive → situation, journal entry → ledger).

### Raw sources are immutable

Files in `research/_raw/` and `training/_transcripts/` are never edited, never moved out, never reorganized after filing. They are the audit trail. If a raw source is wrong or outdated, you don't edit it — you file a new raw source alongside it with a newer `as_of_date` and let retrieval handle the recency logic.

### Journal entries are append-only

- No substantive edits to journal entries after 24 hours.
- Typo fixes within 24 hours are permitted.
- If new information changes your view on something a journal entry claims, write a NEW entry that links back to the original. Do not edit history. The honesty of the journal's state-of-mind record is what makes it valuable for calibration.

### Ledger entries are promotion-only

- Never write directly to the ledger. Every entry originates from a journal entry, a research artifact, or a briefing and gets promoted via the inference-review pattern.
- Resolution of open ledger entries also goes through inference-review — an agent proposes the resolution based on current data and Aayush confirms or corrects.
- The only path from ledger to training is the monthly review ritual, which promotes methodological insights to `training/post-mortems/`. Ad-hoc promotions outside the review ritual are strongly discouraged (they skip the calibration step).

### Concept stubs are lazy and thin

- Stubs are created ONLY on first wikilink invocation by an agent writing content in another area. Never bulk-generated, never synthesized from training.
- Each stub is ~80 words maximum. The value is in the backlinks, not the stub text.
- Stub template (use exactly this format):
  ```markdown
  ---
  concept: <slug>
  training_source: training/frameworks/<file>.md
  created: YYYY-MM-DD
  tags: [concept, <domain>]
  ---

  # <Concept Name>

  <One or two sentence definition. Under 80 words total for the stub body.>

  **Why it matters in this framework:** <one sentence, written on stub creation>

  **See training source for full methodology.**

  ---
  *Backlinks below show every invocation across research, journal, and ledger.*
  ```
- Stubs are never hand-edited beyond fixing typos or updating the training source pointer. If a concept needs a 500-word treatment, the expansion belongs in `training/frameworks/` and the stub keeps pointing at it.

### Playbooks and declarative content compile differently

This applies specifically during skill compilation, but you should understand the distinction for any task that touches training sources or the compiled skill.

- **Playbooks** are sequenced procedures (e.g., "to evaluate a BDC: first check mark staleness, then adjust NAV, then compute Price/NAV..."). The compile pipeline PRESERVES playbooks structurally — it does not paraphrase them. Step order and coupling between steps are load-bearing.
- **Declarative content** is everything else — definitions, principles, frameworks, concepts, mental models. The compile pipeline SYNTHESIZES declarative content across sources, with attribution preserved.
- Training files flag playbooks in their frontmatter: `contains_playbooks: [bdc-evaluation, fallen-angel-thesis]`. The compile pipeline uses this flag to find and preserve them.
- Post-mortems that amend playbooks use structured amendment fields: `amends_playbook: bdc-evaluation`, `change_type: refine | reorder | add_step | remove_step`, `new_step_order: [...]`, `rationale: <text>`.
- If you find yourself treating a playbook as prose during synthesis, stop. That's a bug.

### Directional causation

When drawing a thematic link between two things, specify which direction causation runs. "X affects Y" is not enough. State "X → Y because [mechanism]."

Do not assume symmetric links. Example: software weakness → tech-BDC stress is real (tech BDCs lend to software companies). But BDC stress → hyperscaler cap structure does NOT follow — software and hyperscalers are different cohorts.

If you're uncertain about direction, say so and flag it for review.

### Disagreement preservation

When sources disagree, preserve the disagreement explicitly. Never smooth it into a blended statement.

Format: "Source A claims X ([quote, ≤15 words], [citation]). Source B claims Y ([quote, ≤15 words], [citation]). Possible reconciliations: [...]"

Disagreement between sources is often where alpha lives. Document it.

### Energy decomposition

When WTI moves >5% in a day or >15% over a week, any energy reads MUST decompose by sub-industry: Integrated, E&P, Refiners, Gas Pipes, Basic Materials/Chems, Airlines.

Never report "Energy IG" as a single read when oil is moving. The RV trade usually sits inside the complex, not between the complex and rest-of-IG.

### Copyright and quoting

- Direct quotes from any source are ≤15 words.
- One quote per source, maximum. Paraphrase everything else.
- Never reproduce whole paragraphs from articles, research notes, or primers, even if you could fit them under the word limit.
- Song lyrics, poems, haikus: never reproduced in any form.

---

## Wikilinks and file placement

Wikilinks are a promise that the target exists. Speculative linking pollutes the vault with broken references and triggers Obsidian's create-on-click behavior, which produces blank stub files at the vault root. These rules prevent that.

### Linking rules

1. **Only emit `[[wikilinks]]` to pages that currently exist in the vault OR that you are creating in the same operation.** Before writing a wikilink, verify the target path exists on disk.

2. **For mentioned entities without a page yet, use plain text.** Write "OBDC" not "[[OBDC]]" if `research/credit/issuers/OBDC.md` does not exist.

3. **If an unlinked entity deserves a page, propose creating it** in the Dig section of a briefing, or in the scope proposal of a deep dive. Never silently link to a non-existent page.

4. **When you genuinely need to create a new page in the same operation,** create it first with at least template scaffolding filled in, then link to it. Never link first and create later.

### File placement rules

5. **New content pages go in the correct folder per area routing. Never at the vault root.** The vault root is reserved for operational files only: `CLAUDE.md`, `README.md`, top-level `log.md`. Nothing else should be written to the root by you, ever.

6. **Folder assignments** — see each per-folder CLAUDE.md for specifics. The high-level rules:
   - Research work products → `research/credit/*` or `research/macro/*`
   - Research raw sources → `research/_raw/*` (never move out once filed)
   - Training sources → `training/primers/`, `training/frameworks/`, `training/conversations/`, `training/post-mortems/`
   - Training compiled artifacts → `training/_compiled/credit-trading/v<N>/`
   - Journal entries → `journal/entries/` (flat)
   - Ledger open entries → `ledger/open/`
   - Ledger resolved entries → `ledger/resolved/<domain_path>/`
   - Ledger reviews → `ledger/reviews/`
   - Concept stubs → `concepts/<slug>.md` (flat)

7. **If you're uncertain which folder a page belongs in, ask in the current thread rather than guessing.** Misfiled pages are harder to find later than un-created pages.

### File naming rules

Filenames must be descriptive and human-readable. Dates belong in YAML frontmatter (`date_added`, `as_of_date`, `date`), not in filenames.

- **Raw sources** (`research/_raw/`): Descriptive kebab-case slug derived from `source_name`. No date prefix, no timestamp. Example: `crm-q4-fy2026-earnings.md`, `jbi-holdout-trade.md`.
- **Briefings** (`research/briefings/`): `briefing-YYYY-MM-DD.md`. The prefix distinguishes them in the graph.
- **Macro snapshots** (`research/macro/`): `{descriptor}-YYYY-MM-DD.md` where descriptor matches the subfolder purpose. Examples: `rates-2026-04-06.md`, `ig-spreads-2026-04-06.md`, `narrative-2026-04-06.md`, `oil-2026-04-06.md`.
- **Deep dives** (`research/credit/deep-dives/`): Topic slug only. Example: `crm-financial-policy-shift.md`.
- **Issuer/sector pages**: Ticker or sector slug. No dates. Example: `CRM.md`, `enterprise-software.md`.
- **Ledger entries**: Topic slug only. Date is in frontmatter.
- **Never** use bare date-only filenames like `2026-04-06.md`. Never prefix raw sources with timestamps.

---

## Retrieval scoping

Different agents retrieve from different parts of the vault. Honor the scoping rules:

- **Research agents** (deep dive, situation, briefing, issuer/sector page writers) read from `research/`, `concepts/`, and the loaded skill. They do NOT read from `training/` — the loaded skill is the interface to training content. Reaching into `training/` bypasses the compile pipeline's weighting and synthesis.
- **Journal ingestion agent** reads the incoming message and, for context, may read recent entries in `journal/entries/` and the loaded skill. It does not need research content for journal writes.
- **Ledger agents** read `research/`, `journal/`, `ledger/`, and the loaded skill. They're bridging multiple areas.
- **Compile pipeline** reads `training/primers/`, `training/frameworks/`, `training/conversations/`, `training/post-mortems/` to produce a new skill version. It does NOT read `research/`, `journal/`, or `ledger/` — those are downstream of the skill, not inputs to it.
- **Monthly review agent** reads `ledger/resolved/`, `ledger/open/`, and recent `ledger/reviews/`. It proposes promotions into `training/post-mortems/` but does not read other training content.
- **Briefing agent** reads `research/briefing-scope.md`, recent `research/briefings/`, current macro state in `research/macro/*`, and processes files in `research/_raw/inbox/to-file/` that are ready to ingest. It does not read training content directly.

---

## View-laundering defenses

This is the most insidious failure mode in a system like this: a view gets written down, then re-read later as if it were a fact, then cited forward until nobody remembers it started as somebody's take. Every safeguard in this section exists to prevent that.

1. **Prior research artifacts are framed on retrieval as dated hypotheses, not as facts.** When you retrieve a prior deep dive, situation, or theme for context in current work, treat its conclusions as "a dated view to test against current data," not as established truth. Re-derive conclusions from current sources; don't inherit them.

2. **Every generated artifact carries confidence and falsifiability at write time.** Deep dives, situations, themes, ledger entries, and briefing setups must end with a `## Confidence and what would change my mind` section listing confidence level, key assumptions, and specific falsifying conditions. This is what the ledger promotes from and what future retrievals test against.

3. **Facts flow forward, views don't propagate.** If a March briefing OBSERVED that OBDC printed at 95.2, that's a fact — future work can inherit it. If the same briefing CONCLUDED that OBDC looked cheap, that's a view — future work must re-derive the conclusion from current data.

4. **The facts/views firewall is enforced at both write and read.** When writing, don't put views on facts pages. When reading, don't treat views pages as evidence for facts claims.

5. **Self-citation is allowed but must be re-challenged.** A deep dive can reference prior deep dives on the same name — that's how thinking compounds. But the citation must be framed as "prior view as of <date>, current assessment: [re-evaluation]," not as "we already know X."

---

## Rule evolution

CLAUDE.md files are not frozen. They evolve as you and Aayush discover gaps, ambiguities, or cases the current rules don't cover. The evolution mechanism:

1. **During any task**, if you notice a rule is unclear, contradicts another rule, or is missing coverage for a case that came up, complete the current task using the current rules (rules never change mid-task) and then propose an amendment at task end.

2. **Post the proposal to `#agent-ops`** in a new thread with this format:
   ```
   Rule-change proposal
   - File: <path to CLAUDE.md>
   - Current rule: <quoted text>
   - Proposed change: <new text>
   - Reason: <what happened that revealed the gap>
   - Triggered by: <task link or thread reference>
   ```

3. **Wait for Aayush's response.** He may approve as-is, approve with modifications, reject, or defer. On approval, apply the edit and commit with message format: `v2-rules: <file> — <summary>. Triggered by <task reference>`.

4. **Log every approved change** to `_agent/rule_changes.md` with date, file, summary, and the triggering task.

5. **Never silently edit CLAUDE.md files.** Every change requires explicit approval.

6. **Protected rules** — you may NOT propose weakening these:
   - The inference-review pattern (any weakening is a bug)
   - Journal append-only discipline
   - Ledger promotion-only discipline
   - The facts/views firewall
   - Provenance requirements
   - Raw source immutability
   - The concept stub lazy-creation rule
   - The copyright quote limits
   If you find yourself thinking a protected rule should be weakened, it means you've encountered a case the rule wasn't designed for — propose an EXCEPTION or EXTENSION, not a weakening.

Aayush can also propose changes directly via `/rule propose <text>` in any channel. The bot drafts the formal proposal and posts it to `#agent-ops` for confirmation.

---

## Git discipline

Every meaningful edit is committed. Small edits (typo fixes, formatting) can batch. Git is part of the audit trail.

Commit message format: `{action}: {scope} — {detail}`

Examples:
- `v2-ingest: citi-hy-weekly 2026-04-05 — research raw filed`
- `v2-research: deep dive on OBDC — mark staleness focus`
- `v2-ledger: promote OBDC long from 2026-04-07 journal entry`
- `v2-ledger: resolve OBDC target — played out +0.3 over`
- `v2-compile: credit-trading v2.1 published`
- `v2-rules: training/CLAUDE.md — add podcast_transcript to source_type vocabulary`
- `v2-briefings: 2026-04-08 reviewed — iran hormuz update`

Never force-push. Never delete history. The git log is part of the audit trail.

Aayush can `git diff` any change before or after the fact.

---

## Things you must never do

- Cite a wiki page as evidence for a claim on another wiki page.
- Write directly to the ledger. Ledger entries are always promotions.
- Substantively edit a journal entry after the 24-hour window.
- Move or edit files in `research/_raw/` or `training/_transcripts/` after filing.
- Bulk-generate concept stubs from training content.
- Synthesize playbook content as prose during compile.
- Smooth over source disagreement.
- Assume symmetric causation on thematic links.
- Report "Energy IG" as a single read when WTI is moving materially.
- Write views into facts pages.
- Fabricate sources, citations, or quotes. If you can't find a source, say so.
- Write new content pages to the vault root. The root is reserved for operational files only.
- Emit wikilinks to pages that don't exist and that you're not creating in the same operation.
- Silently edit CLAUDE.md files. Rule changes require explicit Slack approval.
- Propose weakening a protected rule.
- File a source from the inbox without completing the inference-review flow.
- Reproduce song lyrics, poems, haikus, or quotes >15 words.
- Retrieve training content during research tasks (use the loaded skill instead).
- Skip the confidence markers in inference-review proposals.
- Guess when you should ask. When uncertain, mark `[needs input]` and wait.

---

## Things you should always do

- Preserve every source, every disagreement, every dated claim.
- Prefer paraphrase over quotation. Direct quotes are rare, short, and in quotation marks.
- State direction of causation explicitly.
- Flag your own uncertainty when it exists.
- Ask for Aayush's judgment when a call is ambiguous rather than guessing.
- Mark inference confidence honestly — `[inferred]`, `[guess]`, `[needs input]`.
- Run ingestion through the full inference-review pattern, even when fields seem obvious.
- Create concept stubs lazily, during the same operation that first wikilinks to them.
- Commit often, with descriptive messages.
- Let artifact density match signal density — don't pad to meet a target length, don't truncate when the material is rich.
- Prefer research from primary sources (filings, rating agency notes, company releases, Bloomberg/Reuters/WSJ/FT) over aggregators.
- Surface rule ambiguities via the rule evolution flow rather than routing around them.
- Trust the structure. If a task doesn't fit cleanly into the vault's shape, that's a signal either the task or the rules need refinement — not that the structure should be bypassed.

---

## Operating reminders by task type

### When ingesting a source

1. Read the file.
2. Infer as many frontmatter fields as possible from content.
3. Mark confidence honestly.
4. Post the inference-review proposal to the appropriate Slack thread.
5. Wait for confirmation, apply corrections, show diff, file, commit.

### When writing a deep dive

1. Read the loaded skill. The methodology is already in your context.
2. Scope the dive in the thread and confirm with Aayush.
3. Check `research/_raw/` for existing sources; propose web search if insufficient.
4. Ingest any web-fetched sources through the full tagging flow before using them.
5. Write the dive. Cite every claim to a raw source. Enforce facts/views firewall.
6. Create concept stubs inline as needed.
7. Add `## Confidence and what would change my mind` at the end.
8. Commit and update indices.

### When drafting a briefing

1. Read `research/briefing-scope.md` and the last 3 briefings.
2. Process files in `research/_raw/inbox/to-file/` (they've been tagged but not yet filed into final locations).
3. Run targeted web searches for current material.
4. Draft the briefing at `research/briefings/YYYY-MM-DD.md` with `status: draft, reviewed: false`.
5. Update relevant `research/macro/*` subfolders with dated snapshots.
6. Propose any ledger promotions in the review thread.
7. STOP. Wait for Aayush's review.

### When promoting to the ledger

1. Detect the falsifiable prediction in the source artifact.
2. Draft the ledger entry with inferred fields, marked for confidence.
3. Post the promotion proposal in `#ledger`.
4. Apply corrections, confirm, file to `ledger/open/`.

### When resolving a ledger entry

1. The revisit-date watcher triggers you or Aayush does manually.
2. Pull current data relevant to the prediction.
3. Draft the resolution with inferred outcome and delta.
4. Post the resolution proposal in `#ledger`.
5. Apply corrections (especially `lessons`, which is always `[needs input]`), confirm, move to `ledger/resolved/<domain>/`.

### When running a compile

1. Read the full training corpus.
2. Two-pass extraction: preserve playbooks, synthesize declarative.
3. Apply post-mortem amendments in order.
4. Write v<N+1> to `training/_compiled/credit-trading/v<N+1>/`.
5. Generate diff and provenance graph.
6. Run canary questions, flag regressions.
7. Post diff + canary results to `#training` for review.
8. On approval, repoint `current`, publish externally, commit.
9. On rejection, preserve v<N+1> as historical but don't publish.

### When doing a monthly review

1. Read `ledger/resolved/` since the last review and any notable `ledger/open/` entries.
2. Compute aggregate stats: outcome breakdown, win rate by domain, confidence calibration.
3. Identify patterns across multiple entries.
4. Draft the review at `ledger/reviews/<YYYY-MM>-review.md`.
5. Propose specific post-mortem promotions for insights that reflect methodological change, not just situational learning.
6. Post to `#ledger` for review.
7. On approval, create each promoted post-mortem via the training ingestion flow (full inference-review for each).

---

## Closing note

This file is long because the system's discipline is load-bearing and every rule prevents a specific failure mode. Re-read it periodically, especially when you notice yourself wanting to take shortcuts. The shortcuts are how these systems degrade.

If a rule contradicts itself, conflicts with a per-folder CLAUDE.md, or doesn't cover a case you've encountered, use the rule evolution flow. Don't improvise.

The goal is a system that compounds over time — where your research gets sharper because real experience flows back into training, where the concepts layer gets denser because the same ideas get invoked across many pieces of work, where the ledger's track record tells Aayush honestly where his edge is. Every rule here serves that goal. Honor them.
