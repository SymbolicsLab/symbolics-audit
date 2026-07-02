# 2026-07-02 — Products work program: R-Q1 + R-Q2 ratified (session "Products Fable 5")

**Type:** strategic/product decisions (not a theory change). **Primary log:** `~/Developer/PRODUCTS-2026-07.md` (read that first; this is the pointer record).

## Context
Fable 5 access confirmed only through ~Jul 7 → decision D-P1: spend it on decision documents/designs, not execution (execution items have complete specs, any model). Motivating frame: products as PhD-pitch arguments (`symbolics-research/PhD/PITCH.md`).

## Decisions ratified by PB this session
- **R-Q1 (RAG):** redesign from per-query stateless conflict detector to **research memory** — persistent position library (S2) + claim-commitment layer (S3); source-landscape = derived report (S1); first deployment = PB's corpus + claims ledger (S4, user #1). The four candidate shapes stack (substrate/report/layer/deployment) rather than compete. Plan: `symbolics-rag/RAG-2.0-PLAN.md` v1 (DR1–5, HR1–7, R0–R4).
- **R-Q2 (Merge):** retrofit to **commitment store**. Code verification falsified the 2026-05-21 memo's "already has persistent state" assumption: metabolism engine + credibility model UNWIRED (dead code beside a Phase-0 live path); **bug: re-merge silently reverts steward resolutions** → fixed as the flagship no-regression invariant. Plan: `symbolics-merge/MERGE-2.0-PLAN.md` v1 (DM1–5, HM1–6, M0–M4).
- **R-ORD (recommendation, PB confirms by acting):** Merge M0+M2.1 first (autonomous, fixes a demo liability), RAG R0 second (needs PB inputs + API budget; schedule its live audit against the next real manuscript, likely TACL).

## Cross-product findings (pitch-grade)
- **HR4 ≡ HM4:** contraction at the commitment level = scope-qualification, on two substrates (claims / source-credibility). Joint pre-registered test of the "one calculus" claim — tested, not asserted.
- Three commitment substrates across the family: rules (Tercet) / records+resolutions (Merge) / positions+claims (RAG).
- Family answers the "inventor-only tool" objection (PB's move): Tercet is publicly try-able.
- PITCH.md feed-ins ×6 banked in the synthesis section of PRODUCTS-2026-07.md.

## Verified state (2026-07-02)
Tercet 404/404 tests, 2.0 complete on disk, deployed API + site pre-2.0, self-assessment frozen at user-gated runtime decision · Merge 107/107, one commit, wiring gaps as above · RAG 174/174, demo preserved as read path + pitch demo.

## Late-session additions (same day)
- **D-P3 EXECUTION MODE:** PB redirected the remaining Fable window from design-only to bringing products toward completion. **D-P4:** Tercet Tier-1 self-assessment **PARKED** (only thermal-risk item; blocks nothing; GitHub-Actions idea considered and dropped; pickup point = `experiments/2026-05_self-assessment/LOG.md`).
- **PITCH.md §4b "The receipts" drafted** (products section for the PhD pitch; six evidence beats; engine-vocabulary only; §6 got a state-check thread).
- **Merge M2.1 SHIPPED:** resolutions survive re-merge (re-apply/confirm/challenge per DM4; `merge/core/commitments.py`); **second bug found+fixed** (resolving one conflict deleted all other entities in the spec); 9 new tests, **116/116 green**; HM1 ACCEPTED.
- PB-input queue: `flyctl auth login` (Tercet deploy) · Stripe keys (commerce) · RAG corpus scope at R0.4.

## Memory/index updates
`project_rag_product` + `project_merge_product` rewritten (+M2.1 note); `project_tercet_self_assessment` PARKED note; MEMORY.md lines updated; worksheet current; OVERVIEW §2 rows (merge/rag) + §11 reference updated.

## Next session pickup
1. Read `~/Developer/PRODUCTS-2026-07.md` (whole file — it is the program's state).
2. Merge: next = **M0.1 benchmark corpus** (gates HM2/HM3 wiring), then M1.1 schema spec before M2.2+. Plan: `symbolics-merge/MERGE-2.0-PLAN.md`.
3. RAG: next = **R0.1 position store** (autonomous); R0.4 needs PB corpus decision. Plan: `symbolics-rag/RAG-2.0-PLAN.md`.
4. Tercet: deploy gated on PB `flyctl auth login`; site settlement story per `docs/settlement-report-spec.md`.
