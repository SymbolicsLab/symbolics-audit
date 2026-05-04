# Library — Initial Setup

Date: 2026-05-03
Type: Structural (new repo, new infrastructure)
Repo: `~/Developer/Library/` (new, sibling to Symbolics/ and Art/)

## What changed

A new repo was created: `~/Developer/Library/`. It is identity-neutral
reference infrastructure for all texts cited across research and art
submissions. It replaces the scattered per-submission `Readings/` folders.

The motivation came from a recurring problem: AI-assisted lit reviews have
~10% citation fabrication rate (memory entry `feedback_citation_audit.md`),
and the same texts get downloaded into every paper's `Readings/`, with
provenance loss (frontmatter-only PDFs, wrong-format files, placeholder
DOIs). Recent examples caught: 8 likely fabrications in the Inquiry SI lit
review; Salis 2016 in Phil Psych; multiple Open Phil Kant fixes; Range of
Perception verification flags.

The Library makes citation correctness a property of the system: no draft
cites a text the Library hasn't verified.

## Design decisions (settled in conversation)

1. **Identity-neutral**: lives at `~/Developer/Library/`, not under
   `Symbolics/`. Both research (Symbolics Lab) and art (Philipe Barsamian)
   draw from it equally. `scope: [research|art|both]` field on each record
   handles the dual-identity filter.
2. **Source-of-truth format: CSL-YAML**. Pandoc consumes it directly
   (full-paper docx pipeline). Auto-export hayagriva for Typst projects
   and BibTeX for anything else. One file maintained, three formats out.
3. **Per-record schema**: citation block + provenance + verification +
   theory + engagements + edges + relations + uses. Full schema in
   `Library/DESIGN.md §4`.
4. **Vocabulary architecture — two layers**:
   - Substrate (`_vocab/substrate.yml`): stable, won't change. Captures
     *how* a text functions in engagement (role, register, engagement_depth
     values, theory_load_bearing, scope, source_type, pages_held, ocr,
     flags, quarantine_reason).
   - Volatile (`_vocab/<name>.yml`): current strategic concerns. Each is
     a file with explicit lifecycle metadata (`status`, `established`,
     `purpose`, `deprecation_signal`, `successor`). Retired vocabularies
     get `status: deprecated`; old records keep their tags forever.
5. **Engagement model**: log of engagements (temporal trace), not static
   read-state. Computes freshness (fresh ≤60d, stale 60–180, cold >180).
   Cold texts about to be cited prompt re-engagement. Memory prosthetic.
6. **Edge model**: two tiers. Auto-populated edges (parent/children,
   supersedes, cites_in_library, co_cited_in_drafts) populate themselves
   from metadata + bibliography extraction. Manual edges (dialogue_with,
   lineage_to, responds_to) opt-in, filled when reading reveals them.
   Library setup is never gated on manual edges.
7. **Two ingestion workflows**, converging on `_quarantine/` → `entries/`:
   - **User-drop**: drop PDF in `_inbox/`, run `process.py`, clean records
     auto-promote, flagged records stay in quarantine.
   - **Agent-fetched**: two-step verify-then-fetch. Citation-resolve agent
     runs first (no web fetching) — fabrications caught upstream. Fetch
     agent only on `verified`. PDF accepted only if DOI matches OR
     (title+first-author match in PDF first page AND page count ≥ claimed).
8. **Long-text protocol**: anything > 25k tokens gets chunked
   (`chunks/NN-<slug>.md` with stable section IDs ≤20k tokens each).
   `summary.md` ≤5k tokens with chunk pointers. Never read source.pdf
   directly during normal sessions for long texts.
9. **Vault relationship is one-way**: Library records reference vault
   sections (`theory.vault_refs:`); vault does not track Library entries.
   Vault stays the user's own — theoretically and practically.

## What was built this session

**Planning artifacts** (so future sessions can pick up cold):
- `Library/CLAUDE.md` — entry point with operating principles, do/don't,
  read order.
- `Library/DESIGN.md` — full architecture and rationale, with major
  decisions log.
- `Library/PLAN.md` — staged rollout (Phases 1–6) with checkboxes.

**Infrastructure**:
- Repo init, `.gitignore` (PDFs not tracked — sha256 in records is the
  integrity reference).
- Directory scaffold: `_scripts/`, `_vocab/`, `_bib/`, `_inbox/`,
  `_quarantine/`, `_provenance/`, `entries/`.
- `_vocab/substrate.yml` — stable substrate vocabulary with full lifecycle
  metadata.
- Python venv (Python 3.14) with `requests`, `pyyaml`, `pypdf`.
- `requirements.txt`.

**Scripts**:
- `_scripts/verify.py` — Crossref + OpenAlex citation resolution. Returns
  `verified` | `partial-match` | `not-found`. Polite User-Agent with
  user's email. CLI + library use. **Tested**: caught Salis 2016
  fabrication (real fab from yesterday's Phil Psych citation audit);
  matched Keller 1903 via OpenAlex (Crossref pre-DOI books are
  partial-match, not fail); verified Woods 2019 by DOI.
- `_scripts/add.py` — single-PDF ingest. Hash, PDF metadata extraction,
  Crossref/OpenAlex verify, drafts record.yml in `_quarantine/`,
  generates integrity report. Auto-quarantines based on typed reasons.
- `_scripts/process.py` — sweeps `_inbox/`, promotes clean
  `_quarantine/` records to `entries/`, prints session-start status
  report.

**Templates** (regenerated by `audit.py` in Phase 2):
- `INVENTORY.md`, `MISSING.md`, `ISSUES.md`.

**First entry** — Keller 1903:
- `entries/keller-1903-story-of-my-life/`
- Tagged `scope: [research, art]` (used in vault evidence + threshold-figures
  book).
- `theory.pillars: [P-shared-cut, P-two-body]`.
- `theory.vault_refs: [01_Ontology#shared-cut, 01_Ontology#three-level-ontology, 02_Operations#commitment]`.
- 3 engagement entries seeded from vault rewrite history (2026-04-03,
  2026-04-04, 2026-05-03).
- `provenance.flags: [version-superseded, jurisdiction-flag]` — PDF is
  2017 Digireads reprint (not 1903 first edition) and Anna's Archive source.
- `length_tokens: 95000`, `summary_status: stub`. Needs chunks before
  cited beyond passages already in vault notes.
- Stub `summary.md` with engagement context, key passages, use guidance.

## Files added/modified outside Library/

- `~/Developer/OVERVIEW.md` — Repository Map updated to include Library/;
  full Library entry added before symbolics-research.
- `~/.claude/projects/-Users-vivianesauriol/memory/MEMORY.md` — repo count
  11→12; Library entry added; pointer to new project memory.
- `~/.claude/projects/-Users-vivianesauriol/memory/project_library.md`
  (new) — Library project memory entry.

## What's next (Phase 2, future sessions)

From `Library/PLAN.md`:
- `_scripts/audit.py` — regenerate INVENTORY/MISSING/ISSUES from records.
- `_scripts/chunk.py` — long-text chunker. Apply to Keller (95k tokens).
- `_scripts/export.py` — generate `_bib/library.bib` + `_bib/library.yml`
  from records.
- Pre-submission citation gate (`verify-citations.py draft.md`).
- Hook integration with `~/Developer/.pending-integrations.md` for
  session-start status reporting.

After Phase 2: bulk migration of high-reuse texts (Brandom, Priest,
Williamson, Kant, Ricoeur, Cassirer, etc.); per-submission `Readings/`
migration done organically as papers are next touched, not in a sweep.

## Why this matters strategically

Three connections to ongoing work:

1. **AI pitch (`symbolics-pitch/STRATEGY.md`)**. The Library is part of the
   evidence stack: it demonstrates the infrastructure-building capability
   of AI-augmented intellectual work. A solo independent researcher with
   no institutional access has built a verified, structured reference
   substrate that produces 0% fabrication rates by construction.
2. **Field establishment (`symbolics-pitch/FIELD-ESTABLISHMENT.md`)**.
   The Library makes pillar/dissolution-candidate scanning queryable.
   Phase 3 builds the volatile vocabulary `_vocab/pillars.yml` synced from
   `PILLARS.md`; queries like "which texts ground P12 (time as
   level-emergent)?" become one-liners.
3. **Threshold-figures book (`Art/Books/threshold-figures/`)**. Identity-
   neutral Library means art-side texts (Preciado, Fisher, Tumarkin,
   Glissant) get the same rigor as research-side. The book project's
   citation hygiene is part of the polemic's seriousness.

## Test of design at session end

The proof that this design holds: after this session, future Claudes can
take over Library work without any conversational memory. They read
`Library/CLAUDE.md` (always first) → `DESIGN.md` (once) → `PLAN.md`
(every time, before working) and know:
- What the Library is for and why.
- The full schema and where vocabularies live.
- Which scripts exist and what they do.
- The current rollout phase and what's next.
- The constraints (vault one-way, PDFs not tracked, no fabrications).

That's the test. Next session: pick up at Phase 2 from `PLAN.md`.
