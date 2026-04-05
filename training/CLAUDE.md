# Training — Folder Rules

Read the root `CLAUDE.md` first; this file extends it with folder-specific rules for the training corpus.

---

## Purpose

`training/` holds the source corpus from which the credit-trading skill is compiled. Content here is NOT used directly during research tasks — it flows through the compile pipeline into a versioned skill artifact. Agents doing research read the loaded skill, not raw training content.

---

## Folder structure

```
training/
├── CLAUDE.md              ← this file
├── inbox/
│   ├── to-tag/            ← files dropped via #training, awaiting inference-review
│   └── to-file/           ← tagged files awaiting filing to a content folder
├── primers/               ← foundational texts: books, book chapters, long-form primers
├── frameworks/            ← analytical frameworks, mental models, decision rubrics
├── conversations/         ← Claude conversation distillations, chat logs with insights
├── post-mortems/          ← trade/prediction reviews that amend methodology
├── _transcripts/          ← raw transcripts (immutable archive, never edited)
├── _compiled/
│   ├── credit-trading/    ← versioned compiled skill artifacts
│   │   ├── v1.0/
│   │   ├── v<N>/
│   │   └── current        ← copy pointing to latest published version
│   └── bdc-knowledge/     ← archived, absorbed into credit-trading at next compile
├── _provenance/           ← per-version provenance graphs (which sources shaped which sections)
```

---

## Frontmatter requirements

Every training source MUST have these fields:

```yaml
source_type: primer           # REQUIRED — closed vocabulary, see below
author: Howard Marks           # REQUIRED
date_added: 2026-04-05         # REQUIRED — when added to training corpus
origin: book                   # REQUIRED — where Aayush got it (book, conversation, podcast, paper, etc.)
tags: [cycles, risk, distressed]  # REQUIRED — topical tags for filtering
```

Optional fields:

```yaml
date_published: 2018-01-15     # when the source was originally published
trust_weight: high             # high | medium | low — defaults below
supersedes: primers/old-file.md  # if this replaces an earlier version
contains_playbooks: [bdc-evaluation, fallen-angel-thesis]  # procedural content flags
amends_playbook: bdc-evaluation  # post-mortem amendment target
change_type: refine            # refine | reorder | add_step | remove_step
new_step_order: [...]          # required if change_type is reorder
rationale: "text"              # required on post-mortems that amend playbooks
```

### Source type vocabulary (closed)

`primer`, `framework`, `memo`, `paper`, `book`, `book_chapter`, `transcript`, `podcast_notes`, `call_notes`, `claude_conversation`, `post_mortem`

No other values are permitted. If a source doesn't fit, propose a vocabulary extension via the rule evolution flow.

### Trust weight defaults

- **Primers, frameworks, post-mortems:** default `high` (grounded in real track record or established expertise)
- **Conversations:** default `medium` (insight-dense but less rigorous than published work)

Override the default in frontmatter when the content warrants it. A casual chat that yielded a key insight can be `high`; a primer from an author Aayush doesn't respect can be `low`.

---

## Ingestion rules

1. Files arrive in `training/inbox/to-tag/` via file drops in `#training`.
2. Every file MUST go through the inference-review pattern (see root CLAUDE.md) before moving to a content folder.
3. The inference-review flow tags frontmatter fields with `[inferred]`/`[guess]`/`[needs input]` confidence markers.
4. On confirmation, the file moves from `to-tag/` → `to-file/` → final content folder (e.g., `primers/`).
5. No file leaves the inbox without the inference-review flow completing successfully.

### Content folder rules

- **Flat structure.** No nesting by author or publisher within `primers/`, `frameworks/`, `conversations/`, or `post-mortems/`. Use frontmatter tags for filtering.
- **Naming convention:** `<author-or-source>-<topic-slug>.md` (e.g., `marks-risk-memo.md`, `klarman-margin-of-safety-ch3.md`, `fridson-distressed-framework.md`).

### Playbook flagging

Files with procedural content MUST declare `contains_playbooks: [list]` in frontmatter. This is how the compile pipeline finds playbooks to preserve structurally. Missing this flag means the compile pipeline treats the content as declarative and may paraphrase procedure into prose — a serious failure mode.

### Post-mortem amendment format

Post-mortems that amend existing playbooks MUST use structured amendment fields:

```yaml
amends_playbook: bdc-evaluation
change_type: refine              # refine | reorder | add_step | remove_step
new_step_order: [...]            # required if change_type is reorder
rationale: "After the Blue Owl situation, mark staleness should be checked BEFORE computing Price/NAV, not after"
```

This structured format is what the compile pipeline reads when applying amendments. Freeform amendment text without these fields will not be picked up.

### Transcript archiving

When a Claude conversation distillation is filed to `conversations/`, check whether the raw transcript should be archived to `_transcripts/`. If yes, Aayush provides the transcript. Both files are filed with cross-references in frontmatter:
- Conversation file: `transcript: _transcripts/<filename>.md`
- Transcript file: `distillation: conversations/<filename>.md`

---

## System-managed folders

These folders are written by automated pipelines. Never hand-edit their contents.

- **`_compiled/`** — versioned skill artifacts produced by the compile pipeline.
- **`_provenance/`** — provenance graphs mapping source contributions to each skill version.
- **`_transcripts/`** — raw conversation transcripts. Immutable once filed.

---

## Compile trigger discipline

The compile pipeline is triggered manually via `/compile` in `#training`. It is NOT triggered per-file.

New training files accumulate until a compile is triggered. The bot posts a reminder in `#training` when:
- 5 or more new training files have been ingested since the last compile, OR
- 14 days have passed since the last compile

whichever comes first. The reminder is a nudge, not an auto-trigger. Aayush decides when to compile.

---

## Things specific to this folder you must never do

- Hand-edit files in `_compiled/`, `_provenance/`, or `_transcripts/`.
- Nest content inside `primers/`, `frameworks/`, `conversations/`, or `post-mortems/` (flat only).
- Skip the `contains_playbooks` flag on files with procedural content.
- Auto-trigger compiles without Aayush's explicit command.
- Use source types not in the closed vocabulary without a rule evolution proposal.
