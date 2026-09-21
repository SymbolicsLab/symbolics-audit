# Session handoff — 2026-09-21: the relata-chain's formal checks (Session A prep; ratification NOT run)

**Type:** thinking-partner + repo-side formal checks. **NO vault edits.** Nothing ratified.
**Repos touched:** `developer-meta` (OVERVIEW §7 + banner, `.pending §3`), `claude-memory`, this file.
**Read in full at session start:** OVERVIEW · `.pending-integrations.md` (all five sections) · `00_Theory_Map` · `00_Vault_Map` · `Vault/CLAUDE.md` · `Active/01–05`.

---

## 1. Why the session exists

PB: *"We left the stratification study in a weird state… the whole thing was conducted without one of the main points being fully understood: the stratification is made by one distinction distinguishing over the level below it."*

The study's Phase A/B — marks, contrast class, falsifiers, the 13-cluster survey, Step 12, the five dives — was built on the object stated as **operation-kinds**. PB restated it 2026-08-08 as a **relata-chain**. The restatement was logged and unratified; a re-run decision was pending.

## 2. The gate, raised and held

Session A as scoped (primitive reframe → relata-chain ratification) **is vault work** — it edits `02_Operations §Fold and the hierarchy`, `01_Ontology`, the Theory Map — and §6.4 / `feedback_vault_fresh_session` require a fresh session. The 08-05 stance-axis precedent shows this context load *can* be ruled fresh, but what made that one non-contaminating was an OVERVIEW rotation. **This session's other work was taking — and then correcting — a position on the very claim to be ratified.** So the ratification was deliberately not run. What ran instead: the two tests that are repo-side and mechanical, which feed the fresh session rather than substitute for it.

PB was offered the override and the session closed without it being taken.

## 3. What the checks returned

**★★ `Ascension.agda` already IS the relata-chain — built 2026-07-07, behind the no-other-repos wall, a month before PB stated it.** One constructor; the level rises **iff** the field is a *whole stabilized chain*; the level is **computed** (`m ⊔ n`), never assigned; `levels-self-generate` proves no level ≥ 2 is conferred without an actual ascension in its derivation. Header, verbatim: *"a cut AT A POLE of a prior firing = metabolism — stays at the target's level… a cut over a WHOLE STABILIZED CHAIN = ascension — level + 1"*; *"There is no per-level machinery to build."*

⟹ **The three-formal-homes fork is near-dissolved and the vault is the sole outlier.** The restatement entry's §3 has the Agda "wrong to conclude the kinds are *mere readings*" — it concludes no such thing: it makes the **level structure derived** and layers kind-specific *content* as readings over it, and under a relata-chain **a reading forced by the relatum-type is a derived kind**. Same position, independently arrived at. ⚠ Corroboration, not authority — *the Agda is never the authority, the theory is.*

**★ The defect is real, uniform, and in the READINGS.** Level objects are all typed: `FormIn = LevelIs 2 × MultiPlace`, `RelationIn = LevelIs 3 × MultiPlace`, `VariationIn = LevelIs 4 × MultiPlace`. **Every reading over them is untyped** — `RideOn`, `SeamOn`/`CoLocates`, `TensionWitness`, `tension-grade`, `ElectsContradiction`, `DirectedForeclosure`, `HoldsOpen`, `SettledIn`, `□` all take arbitrary `Event`s at arbitrary levels, and the headers say it is deliberate.

⟹ **Dive 5 was right about the *consequence* and wrong about the *relation*.** "The Agda built a relation without the type constraint" is wrong as written; the relation has the constraint, the consequence does not — and it does not at every rung, by design. Not three-rungs-of-four; one uniform design decision.

**⚠⚠ The live consequence lands on `tension`.** The 08-04 L3-assignment runs *rivalry is constituted by consequence, consequence is L3*. But consequence is `RideOn`, the untyped object, and a pole-take stays at the target's level via `RefLevel`'s `meta` constructor — so **`RideOn` holds between two L1 firings**. Either (a) rivalry is formulable below L3 and the study's spine moves, or (b) `RideOn` owes a relatum-type constraint. **Theory's call, not the code's, and owed before `§Tension` is written** — the level-assignment is part of what gets written. The banked finding *"tension is level-agnostic — a feature"* (checkpoint 6) stops being free under a chain: kind is fixed by relatum-type, and an untyped object has no kind.

**★ Arity: marked in the code, unmarked in the vault.** `MultiPlace`/`BindsTwoWhole` requires **two distinct whole take-ups**, at L2, L3 *and* L4. And the Agda names the arity-1 case: a singleton whole-take-up **raises the level but is not a form** — *"objectification, e.g. index-articulation."* **The vault has no category of level-raising-without-form.** ⟢ Claude, unruled: a candidate reading of **the recursion of index** (taking one chain whole = making its index available as content) — route to Index Studies, do not bank.

*(Claude self-correction recorded: the "unmarked arity parameter" proposed earlier in the session was half wrong. Arity is marked — in the formalization. The finding is a routing, not an invention. Right side of `feedback_explain_from_the_primitive`.)*

**⚠ Guard invoked, matching a standing audit order.** Results proved of an object **before** a relocation do not automatically hold after. The four "surviving" dives were established against the **operation-kind** object and are **transferred, not re-derived**; dive 5's Godfrey-Smith test (*does the dynamic build more of itself?*) is outright **mis-aimed** under a chain, where the dynamic applies to a *new relatum* rather than building more of itself. This is the same unlicensed-transfer audit already ordered for pre-08-04 results.

**Untouched:** the Step-12 driver gap (the ladder says nothing about why anyone climbs) · Luhmann (dive 3's differential stands) · report §8 (PB's).

## 4. The re-run question, shrunk

Phase A/B's marks need restating. The 923-line corpus is worth re-rating **as instrument-diagnostics only** — it was *selected* by the operation-kind filter, so it can be re-scored but not un-selected, and it **cannot answer the chain's own falsifier**. The one genuinely open survey question is narrow: **can anyone name a relatum-type between two of ours, or a missing one?** Do not re-run the dives; do not transfer them either.

## 5. Also logged — a candidate method beat

**The unrun-claim pass** (`.pending §3` head; Claude-proposed, PB approved logging, unratified). Both studies opened back-to-back found the same disease in their own object: **a committed claim carried as a *compression*, never made to constrain anything, with the formalization faithfully encoding the compression rather than the claim.**

- Index: the parameters *are* distinctions — `Primitive/Index.agda` types them as opaque carriers and **names the deferral** in its own header. The bracket was declared and never lifted.
- Stratification: the levels *are* one distinction over the rung below — the vault states operation-kinds, and the ladder/readings split followed.

**The accident rate is the finding**: both were caught by PB in a sentence, neither by anything designed to find them. Three guards travel with it, including one against itself — it is an unrun claim until it produces an instance nobody was already looking at.

## 6. Next session (fresh, small)

1. **Primitive reframe** (§1, 2026-07-05, PB-ratified, still unpropagated) — prerequisite; the chain is stated in its vocabulary.
2. **Relata-chain ratification as its own beat, ahead of `tension`** — it restates what the levels *are*, and `tension`'s destinations write into `02_Operations`. Question: **sharpening or change?** Inputs: `.pending §3` relata-chain entry + its 09-21 formal-check block; the arity/objectification routing; the interpolation test as the stated falsifier.
3. **Then** `tension` — carrying its new prerequisite (rule the `RideOn` level-typing first).
4. **Then** the study's completion, at the reduced size above.

## 7. Owed maintenance, flagged not done

**`OVERVIEW.md` is ~56KB against its own ~40KB cap** and this session added to it. The cap says rotate to `logs/` before exceeding — the breach predates this session, but it is now worse. A rotation pass is owed and was deliberately not taken unilaterally at session end (deciding what is still current is PB's call, not a cleanup task).
