# Library Phase 3 — Folders 1–3 migrated + pipeline hardened

**Date**: 2026-05-16
**Session scope**: Bulk migration of legacy `Reading/` folders into the Library, with iterative pipeline hardening as Folder N exposed new edge cases.

## State at end of session

- **Library entries**: 85 (Folder 1: 22 / Folder 2: 32 / Folder 3 net new: 31)
- **Quarantine**: 0
- **Status mix**: ~70 verified / ~15 non-canonical (books, book-chapters, pre-DOI papers, preprints with explicit flags)
- **Folders migrated**: 3 of 13 (Synthese Priest, RIFP Post-Cognitivism, Synthese Responsible Beliefs)
- **Folders remaining**: 10 — Inquiry (158), Free Will (68), Phil Psych Imagination (25), Range of Perception (32), Science-Policy (63), Distinction-Emergence-Equity (16), Hannover (7), Madrid (18), Konstanz (21), ENS (13). Total ~421 PDFs remaining.

## Pre-migration v2 design pass (carried over from prior session)

- Verification rename: `user-confirmed` → `non-canonical` across DESIGN.md / CLAUDE.md / PLAN.md. Names the evidence path, not the reviewer.
- Phase 3 scope expanded to include Presentations Readings folders (4 folders / 59 PDFs added). 13 folders / ~511 PDFs total.
- PLAN.md dedup rationale updated post-survey: only 13/511 exact-hash dupes (97.5% unique). The real duplication is canonical-paper-level, caught by Crossref/OpenAlex during ingest as `duplicate-pending-merge`.

## Scripts added (`Library/_scripts/`)

- `dedup_survey.py` — hash-and-group survey across N folders; emits JSON + Markdown report. One-shot.
- `migrate_folder.py` — per-folder migration: parse optional README for hints (priest-format, tier-format, download-report), fall back to filename pattern (`Author_Year_Title.pdf` with multi-author variants), dispatch to `add.ingest`, promote clean, generate `sources.md` migration record.
- `backfill_status.py` — populate `verification.status` field on existing entries. Re-runnable.
- `_migrate_synthese_priest.py` — one-off for Folder 1 retries; can be deleted but kept as a record of pre-tool migration.

## Pipeline fixes accumulated (all in `_scripts/`)

Mostly in `verify.py` and `add.py`. In rough order of discovery:

1. `verify.author_match` — last-token vs last-token fallback ("Williamson" matches "Timothy Williamson")
2. `verify.crossref_search` + `score_match` + `is_strong_match` — ±1 year window for online/print drift
3. `verify.diff_canonical` — fuzzy + substring tolerance for publisher/container display-string variants
4. `add.determine_quarantine_reason` — only substantive (title/year/doi/author) diffs trigger `metadata-mismatch`; publisher/container differences ignored
5. `add.ingest` — when DOI lookup fails (often from truncated PDF-extracted DOIs), fall back to title/author/year hints
6. `verify.title_similarity` — token-set overlap + substring containment (rescues short hint vs long Crossref title)
7. `migrate_folder.camel_to_words` — preserves acronyms (LLMs stays "LLMs", not "LL Ms")
8. `add.ingest --no-resolve` — bypass canonical lookup for books that false-match journal reviews
9. `add.draft_record` — falls back to hints when canonical is None (so records aren't blank)
10. `backfill_status.derive_status_from_record` — anything in entries/ without clean dual-match → non-canonical (was returning unverified)
11. `add.slugify` — transliterate (NFKD + ł/ø/ß table) before slugifying; non-ASCII first authors keep meaningful slugs
12. `verify.author_match` — first-author full credit, co-author 0.7× (prevents Haugeland-as-coauthor matching Dennett-review-of-Haugeland)
13. `migrate_folder.parse_download_report` — line-scoped context (was multi-line lookback, stealing previous row's author/year)
14. `add.draft_record` — `_split_author` helper guards against empty author strings (Crossref org-only entries)
15. `verify._clean_doi` — strip trailing `.,;)]>` from PDF-extracted DOIs

Plus: `add.fill_verification` writes `verification.status` per the v2 design taxonomy.

## sources.md migration records (in submission folders)

- `Submissions/_archived_2026-04-30_Synthese_Priest-Paradoxes/sources.md`
- `Submissions/Sent/2026-04-30_RIFP_Post-Cognitivism/sources.md`
- `Submissions/_archived_2026-05-01_Synthese_Responsible-Beliefs/sources.md`

Each captures: per-PDF disposition, dedups, held-out files, pipeline issues exposed during that folder, gaps still open.

## Folder migration command (current)

```bash
cd ~/Developer/Library
source .venv/bin/activate
python _scripts/migrate_folder.py \
  "<absolute path to source Reading/ folder>" \
  --paper-id <YYYY-MM-DD_Venue_Title> \
  --title "<paper title>"
```

After-run cleanup is typically needed: a few items may need `--no-resolve` re-ingest (books not in Crossref), explicit canonical year for >±1 drift, or held-out for orphan files not in the README.

## Per-folder cost (observed)

| Folder | PDFs | Script time | Cleanup conversation | Outcome |
|---|---:|---:|---|---|
| Synthese Priest | 21 | ~50s + retries | High (first folder; 5 pipeline fixes) | 21/21 |
| RIFP | 32 | ~150s + retries | Medium (4 more pipeline fixes) | 32/32 |
| Responsible Beliefs | 37 | ~80s + retries | Medium-High (3 more pipeline fixes + parser bug) | 34/37 (3 orphans held out) |

Trend: per-PDF script cost roughly constant (~2.5s); per-folder conversation cost dominated by edge-case discovery. Each folder's quirks have been distinct enough that the pipeline is meaningfully more robust after each one. Folder 4 should be substantially smoother.

## Still-open followups (not blocking)

- **Slug collision in `_quarantine/`**: two PDFs that hash to the same generated slug — second silently overwrites first. Surfaced with two Boult drafts in Folder 3. Real fix: `add.py` should detect existing slug in `_quarantine/` and append a disambiguating suffix.
- **`year=None` from caller doesn't suppress PDF year guess**: `q_year = year or guess_year(facts)` treats explicit None as "no hint". Workaround: pass explicit canonical year on retry.
- **Year drift > ±1 not auto-handled**: Friedman 2015/2017, Tanesini 2016/2018. Could widen filter to ±2 but risks false-matching. Currently mitigated by manual retry.
- **First-author weighting could be principled** rather than hard-coded 0.7×.
- **Dewey 1922 needs OCR**: image-only scan in Library. One-off data fix.

## Next-session pickup

1. Read `Library/PLAN.md` Phase 3 task list and scope table.
2. Pick next folder. **Recommended**: Inquiry (158 PDFs, no README, filename-only hints) — biggest stress test for the now-hardened pipeline. Alternative: smaller folders first (Hannover 7 → Distinction-Emergence-Equity 16 → Madrid 18 → Konstanz 21 → Phil Psych Imagination 25 → Range of Perception 32) to build confidence on the tool before the Inquiry behemoth.
3. Run `_scripts/migrate_folder.py` per the command above.
4. After-run cleanup: inspect quarantine, identify books / preprints / >±1-year-drift papers, handle with `--no-resolve` or explicit-year retries.
5. Write `sources.md` (auto-generated draft from migrate_folder; edit to add cleanup notes).
6. Update this record or write a new one for Folders 4+.

The original `Reading/` and `Readings/` folders are still intact on disk for all 3 migrated folders. Renaming to `Sources/` and deleting is the very last step (per DESIGN.md §13); not yet done. User should confirm migration records before bulk deletion.
