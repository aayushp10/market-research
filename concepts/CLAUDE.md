# Concepts — Folder Rules

Read the root `CLAUDE.md` first; this file extends it with folder-specific rules for the concepts graph layer.

---

## Purpose

`concepts/` is a shared graph layer of thin stub pages. Any content area — research, journal, ledger — can wikilink to a concept stub. The value is in the backlinks: over time, each concept accumulates references from across the vault, making it a retrieval hub for a specific idea.

---

## Folder structure

```
concepts/
├── CLAUDE.md              ← this file
├── mark-staleness.md      ← concept stub
├── price-nav.md           ← concept stub
├── nii-coverage.md        ← concept stub
└── ...                    ← flat, one file per concept
```

Flat structure. No subfolders. One file per concept, named by slug.

---

## Lazy creation only

This is a protected rule (see root CLAUDE.md). Stubs are created ONLY on first wikilink invocation by an agent writing content in another area. They are:

- **Never bulk-generated** from training content
- **Never synthesized** by scanning the skill for concept candidates
- **Never pre-populated** during setup or migration phases
- **Only created** when an agent writing a research artifact, journal entry, or ledger entry invokes a concept that doesn't yet have a stub

The creation path is always: agent writes `[[concepts/mark-staleness]]` → checks if `concepts/mark-staleness.md` exists → if not, creates the stub inline → then writes the wikilink.

**Why this matters:** bulk generation produces generic stubs disconnected from real use. Lazy creation ensures every stub was born because someone actually needed the concept, and the first backlink is always the creating context.

---

## Stub template

Agents MUST use exactly this format when creating a concept stub:

```markdown
---
concept: <slug>
training_source: training/frameworks/<file>.md  # or primers/ or conversations/
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

### Template rules

- **~80 words maximum** for the stub body (definition + "why it matters" sentence). The value is in backlinks, not stub text.
- **`training_source`** MUST point to the training file that contains the full methodology for this concept. If the concept comes from the loaded skill and you can identify the source file, point there. If the source file is unknown (e.g., the concept is in the v1.0 frozen skill with pending provenance backfill), use `training_source: unknown-pending-backfill`.
- **`tags`** MUST include `concept` plus at least one domain tag (e.g., `bdc`, `credit`, `macro`, `risk`, `valuation`).

---

## Stub lifecycle

1. **Created** during a research write, inline, as described above.
2. **Notification** posted to the relevant channel: "Created new concept stub: `[[concept-name]]` (linked from <artifact>). Review at any time."
3. **Accumulates backlinks** as other artifacts reference the same concept.
4. **Never substantively edited.** Typo fixes and `training_source` pointer updates are permitted. Nothing else.
5. **If a concept outgrows its stub** — needs a 500-word definition, detailed methodology, worked examples — the expansion belongs in `training/frameworks/` as a proper training source. The stub updates its `training_source` pointer and keeps its ~80-word summary.

---

## Concept stub creation does NOT go through inference-review

Stubs created during research writes are part of a larger task that's already in review (the deep dive, situation, etc.). The stub is committed as part of the same operation.

However, the first time an agent creates a concept stub, it MUST post a brief notification so Aayush is aware. He can review the stub definition at any time and push back if the definition needs fixing.

---

## Things specific to this folder you must never do

- Bulk-generate stubs from training content or the compiled skill.
- Create stubs outside the context of writing a real artifact that needs the concept.
- Write stubs longer than ~80 words in the body.
- Substantively edit stubs beyond typo fixes and `training_source` updates.
- Create subfolders. Concepts is flat.
- Create a stub without posting a notification to the relevant channel.
