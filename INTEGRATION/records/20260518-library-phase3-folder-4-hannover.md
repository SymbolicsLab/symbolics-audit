# Library Phase 3 — Folder 4 (Hannover) migrated + pipeline polish

**Date**: 2026-05-18
**Session scope**: First post-hardening folder. Tests whether the pipeline
holds up on a presentation folder with no README. Outcome: 7/7 PDFs
migrated, two new pipeline issues surfaced, one CLI fix landed.

## State at end of session

- **Library entries**: 92 (Folder 4 net new: 7)
- **Quarantine**: 0
- **Status mix**: ~74 verified / ~18 non-canonical (books, chapters, image-only scans, pre-DOI papers)
- **Folders migrated**: 4 of 13 (Synthese Priest, RIFP, Responsible Beliefs, Hannover)
- **Folders remaining**: 9 — Inquiry (158), Free Will (68), Phil Psych Imagination (25), Range of Perception (32), Science-Policy (63), Distinction-Emergence-Equity (16), Madrid (18), Konstanz (21), ENS (13). Total ~414 PDFs remaining.

## Hannover specifics

The folder had no README and the filename patterns were inconsistent with
`migrate_folder.py`'s regex set (e.g.
`Herfeld_Model-transfer-in-science_2024.pdf` has year *after* title, not
the expected `Author_Year_Title` order; `Charbonneau&Bourrat_…` uses `&`
not in any pattern). All 7 would have fallen back to PDF-metadata-only
hints — too lossy for the journal-article + book-chapter mix in this
folder.

Cheapest fix: author a one-shot README in priest-format from the existing
`reading-list.md`, then run the migrator. README sits in `Readings/`
permanently as a side effect.

Result of the bulk pass: 5/7 auto-promoted (4 journal articles +
1 incorrectly attributed handbook record — see issue 1 below);
2/7 quarantined (Boumans chapter not found in Crossref/OpenAlex; Woodward
book matched with year drift + image-only scan blocking OpenAlex
cross-verify).

## Issues surfaced this folder

1. **Crossref title-search overreach to parent book.** Herfeld's chapter
   "Model transfer in science" doesn't have a chapter-level DOI in
   Crossref. The title query returned the parent handbook record
   (`10.4324/9781003205647`, Knuuttila et al. eds.), so the chapter PDF
   got filed under `knuuttila-2024-the-routledge-handbook-of-philosophy`
   as if it were the handbook itself. Auto-promote did not catch this
   because dual-DB match held — both databases happily matched the
   handbook record; the mismatch was at the record-vs-PDF level, not at
   the canonical-resolution level.

   **Fix**: deleted the bogus entry, re-ingested with
   `add.py --no-resolve --copy --title "Model transfer in science"
   --author Herfeld --year 2024`. Manually set `status: non-canonical`
   on the resulting quarantine record before promotion.

   **Root cause / followup**: the verifier should refuse to match a query
   title against a canonical record whose type is `book` when the query
   title is short and the canonical title is much longer (or contains the
   query title as a substring). Specifically, an entry-level title like
   "Model transfer in science" matching a book titled "The Routledge
   Handbook of Philosophy of Scientific Modeling" should fail
   `is_strong_match` even if author + year align — because the parent
   book is presumably edited by someone other than the chapter author.
   Worth a hardening pass in `verify.score_match` before Folder 5
   (Inquiry, 158 PDFs, will almost certainly contain similar shapes).

2. **`--no-resolve` doesn't suppress PDF-extracted DOI guessing.** After
   re-ingesting Herfeld with `--no-resolve`, the resulting record still
   carried `doi: 10.4324/9781003205647` — the *parent* book's DOI,
   extracted from PDF metadata by `guess_doi(facts)`. Per the existing
   verify→draft flow, `q_doi = doi or guess_doi(facts)`: the user-supplied
   hint for DOI was None, so PDF metadata won. Chapter PDFs commonly
   embed the parent book's DOI in their metadata, so this is a
   recurring shape.

   **Fix applied**: manually set DOI to null in the record before
   promotion.

   **Followup** (next session): in `add.ingest`, when `no_resolve=True`,
   skip `guess_doi(facts)` (and arguably also `guess_title`,
   `guess_author`, `guess_year` if not user-supplied — `--no-resolve`
   should mean "use only what I told you").

3. **Year-on-slug drift for Crossref online-edition registration.**
   Woodward's *Making Things Happen* — print 2003, OUP online registration
   2004. Crossref returned year 2004; slug became
   `woodward-2004-making-things-happen`. The DOI is correct and points to
   the same work; only the bibliographic year shifted.

   **Fix applied**: renamed quarantine dir, updated `citation.date`,
   logged the discrepancy in `verification.diffs`. The OUP DOI stayed.

   **Note**: this is structurally identical to the Friedman 2015/2017 and
   Tanesini 2016/2018 cases from prior session (`year drift > ±1
   not auto-handled`). The "±1 window" tolerance covers it for *matching*
   but doesn't normalize the slug after the fact. Slug should be derived
   from the *user hint year* when available, with the Crossref year only
   used as fallback. Followup.

## Pipeline change landed this session (improvement #16)

`add.py`: `--no-resolve` exposed as a CLI flag. Previously only available
as a Python kwarg on `ingest()`, which forced manual-retry cases to
either drop into `python -c` or be edited inline. Used twice in this
folder alone (Herfeld chapter, would have been used for Boumans too if
the workflow had been linear); will be used in every book-heavy folder
going forward.

## sources.md migration record (in presentation folder)

`Symbolics/symbolics-research/Presentations/2026-04_Hannover_Model-Transfer/sources.md`
— full per-PDF disposition, cleanup notes, and the seven Library IDs
that will be cited from any post-presentation paper drafted from this
talk's material.

## Per-folder cost (running)

| Folder | PDFs | Script time | Cleanup conversation | Outcome |
|---|---:|---:|---|---|
| Synthese Priest | 21 | ~50s + retries | High (first folder; 5 pipeline fixes) | 21/21 |
| RIFP | 32 | ~150s + retries | Medium (4 more pipeline fixes) | 32/32 |
| Responsible Beliefs | 37 | ~80s + retries | Medium-High (3 more pipeline fixes + parser bug) | 34/37 (3 orphans held out) |
| Hannover | 7 | ~65s + retries | Medium (1 silent mismatch + 2 quarantine retries; 1 CLI flag, 2 followups) | 7/7 |

Cost reset somewhat with Hannover — Crossref-overreach (issue 1 above)
is a new shape the prior three folders didn't surface because their
PDFs were almost entirely journal articles with chapter-level DOIs.
Presentation folders (which lean book-chapter / monograph heavier) will
likely keep exposing this kind of issue.

## Still-open followups (in priority order for next session)

**New from this folder:**

- **`verify.score_match` should reject title-substring-of-canonical-title
  matches when the canonical is type `book` or `edited-book` and the
  chapter author is not in the canonical's author list.** This is the
  highest-leverage fix before Folder 5 (Inquiry, 158 PDFs).
- **`--no-resolve` should disable PDF-extracted metadata fallbacks.**
  When the user says "use only what I told you", the script should not
  fill in DOI / title / author / year from `guess_*(facts)`.
- **Slug derivation should prefer user hint year over Crossref year**
  when both are present, to avoid online-registration drift on the slug.

**Carried over from 2026-05-16:**

- Slug collision in `_quarantine/` (Boult drafts in Folder 3)
- `year=None` from caller doesn't suppress PDF year guess
- Year drift > ±1 not auto-handled (Friedman, Tanesini; Woodward this
  folder is in-window at exactly ±1)
- First-author weighting could be principled rather than hard-coded 0.7×
- Dewey 1922 needs OCR

## Next-session pickup

1. Read `Library/PLAN.md` Phase 3 task list and updated scope table.
2. **Recommended next folder**: tackle the `verify.score_match` hardening
   *first*, then take on **Inquiry (158 PDFs)** — by far the largest
   remaining folder, with filename-only hints and a wide author/venue
   mix that will exercise the hardened pipeline thoroughly.
   Alternative low-risk path: keep tightening on smaller folders
   (Distinction-Emergence-Equity 16 → Madrid 18 → Konstanz 21 → Phil Psych
   Imagination 25 → Range of Perception 32) before Inquiry, then deal
   with Free Will 68, Science-Policy 63, Inquiry 158 in escalating order.
3. Run `_scripts/migrate_folder.py` per the standard invocation; check
   for missing README in the target folder *before* running and seed
   one from any available reading-list / DOWNLOAD-REPORT artifact if
   absent.
4. Inspect quarantine; retry books and chapters with
   `add.py --no-resolve --copy …`; manually finalize records that need
   container titles, second authors, etc.
5. Run `audit.py`; write `sources.md`; update PLAN.md; write a new
   session record for the next folder.

Original Hannover `Readings/` folder is still intact on disk. Renaming
to `Sources/` and deleting is the very last step (per DESIGN.md §13);
not yet done.
