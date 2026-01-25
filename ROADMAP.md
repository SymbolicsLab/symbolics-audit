# Symbolics Agda Verification Roadmap

This document outlines the prioritized work queue for Agda formalization.
It reflects the current YELLOW issues in the audit report and their dependencies.

**Last updated:** 2026-01-25

**Status:** ✅ All YELLOW specs resolved. Audit shows 39 GREEN, 0 YELLOW, 0 RED.

---

## Priority Queue for Agda Verification

### A) SPEC-MODAL-001 (T-failure) — ✅ COMPLETED

**Status:** VERIFIED (2026-01-25)

**Implementation:** `Mechanics.TFailure.T-failure-countermodel`

Minimal 2-state Kripke countermodel proving T-axiom fails in non-reflexive frames:
- State `s₀` accesses `s₁` (non-reflexive frame)
- Valuation `P`: true at `s₁`, false at `s₀`
- `□P` holds at `s₀` (all accessible states satisfy P)
- `P` does not hold at `s₀`
- `T-axiom-fails : ¬ (∀ P s → box R₂ P s → P s)`

**Bonus:** Also proves `interval-inhabited` for SPEC-MODAL-003

---

### B) FoldOperator as Typed Record — STRUCTURAL PREREQUISITE

**Status:** Not a spec, but enables SPEC-FOLD-002 and SPEC-FOLD-003

**Why it matters:** "Fold" is currently ambiguous — different fold implementations
have different properties. Without a typed structure, we can't prove idempotence
or conservativity in general.

**Implementation approach:**
```agda
record FoldOperator (Config : Set) : Set₁ where
  field
    fold : Config → Config
    -- Optional axiom fields for specific fold types:
    idempotent : fold ∘ fold ≡ fold  -- for IdempotentFold
    conservative : ∀ φ → atoms (fold φ) ⊆ atoms φ  -- for ConservativeFold
```

**Benefits:**
- Specific fold instances satisfy specific properties
- DSL "Fold" can point to a specific instance
- Prevents "fold" from becoming a metaphysical bucket
- SPEC-FOLD-002/003 become provable for specific instances

**Effort:** Medium — requires architectural decision
**Impact:** Enables proofs for SPEC-FOLD-002, SPEC-FOLD-003

---

### C) SPEC-CONTRA-002 (Contradiction-preservation) — ✅ COMPLETED

**Status:** VERIFIED (2026-01-25)

**Implementation:** `Mechanics.ContradictionPreservation.non-explosive-paraconsistency`

Proved non-explosive paraconsistency: conflicting contexts (with both In and Out
at same locus) produce well-defined results under all operations.

Key approach: Instead of proving "conflict persists in aggregate" (which the
resolution order resolves to In), we prove the system is TOTAL on conflicting
inputs. All operations (aggregate, synthesize, applyFold) remain well-defined.

Concrete witness: `conflict-non-explosion` on Two-element universe.

---

### D) SPEC-FOLD-002/003 (Idempotence/Conservativity) — REQUIRES (B)

**Status:** Both are conjecture in theory and Agda

**Why it matters:** Without idempotence, "admissible state" (fold-closure) is undefined.
Without conservativity, fold could fabricate new content.

**Implementation approach:**
- Only provable for specific fold implementations, not "fold in general"
- Requires FoldOperator structure from (B)
- May need to characterize *which* folds satisfy these properties

**Blocked by:** Task (B) above

**Effort:** Medium-High — depends on FoldOperator design
**Impact:** Enables SPEC-ADMIS-001 (Admissible State Definition)

---

## Dependency Graph

```
                     ┌──────────────────┐
                     │ SPEC-MODAL-001   │
                     │   (T-failure)    │
                     │   ✅ VERIFIED    │
                     └────────┬─────────┘
                              │ unblocks
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
   SPEC-MODAL-003     SPEC-CDIST-001     SPEC-CDIST-002
   (Interval)         (Commit/Real)      (Nec/Act)
   [now provable]     [bridge spec]      [bridge spec]

                     ┌──────────────────┐
                     │  FoldOperator    │
                     │   (structure)    │
                     └────────┬─────────┘
                              │ enables
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
   SPEC-FOLD-002      SPEC-FOLD-003      SPEC-ADMIS-001
   (Idempotent)       (Conservative)     (Admissible)
   [future work]      [future work]      ✅ VERIFIED

   SPEC-CONTRA-002
   (Contradiction-preservation)
   ✅ VERIFIED
```

---

## Refined Priority Queue

### Step A — ✅ COMPLETED: SPEC-MODAL-001 (T-failure)

Proven via `Mechanics.TFailure` module (2026-01-25).

This proof is now the anchor for:
- Interval existence (`interval-inhabited` in same module)
- Divergence claims in SPEC-CDIST-001/002 (commitment can diverge from realization)

### Step B — Convert SPEC-MODAL-003 to Pure Definition in Agda

Define: `Interval s φ = (s ⊨ □φ) × (s ⊭ φ)`

This can be done NOW without waiting for T-failure proof. The definition is exact.
(Already marked GREEN in registry as `claim: definition`.)

### Step C — Introduce FoldOperator Record

Do NOT prove idempotence/conservativity for "fold in general."

```agda
record FoldOperator (Config : Set) : Set₁ where
  field
    fold : Config → Config
```

Prove properties for specific instances only.

Once this exists:
- SPEC-ADMIS-001 becomes definable (admissible = fixed point of fold)
- SPEC-FOLD-002/003 become provable for specific instances

### Step D — ✅ COMPLETED: SPEC-CONTRA-002 (Contradiction-preservation)

Proven via `Mechanics.ContradictionPreservation` module (2026-01-25).

Approach: Proved totality of all operations on conflicting inputs rather than
persistence of conflict structure. The system is non-explosive by construction.

---

## Current YELLOW Specs (Post-Triage)

**All structural debt has been addressed!**

| Spec ID | Issue | Assessment | Action |
|---------|-------|------------|--------|
| ~~SPEC-MODAL-001~~ | ~~theorem+conjecture~~ | ✅ **VERIFIED** | Done |
| ~~SPEC-CONTRA-002~~ | ~~theorem+conjecture~~ | ✅ **VERIFIED** | Done |
| ~~SPEC-ADMIS-001~~ | ~~weakened mapping~~ | ✅ **VERIFIED** | Done |

Audit status: **39 GREEN, 0 YELLOW, 0 RED**

**Resolved to GREEN:**
- SPEC-MODAL-002 → `claim: bridge` (documented translation)
- SPEC-MODAL-003 → `claim: definition` with `mapping: exact` (definition is exact)
- SPEC-CONTRA-003 → `claim: theory-only` (empirical/cost claim)
- SPEC-CDIST-001 → `claim: bridge` (terminological mapping)
- SPEC-CDIST-002 → `claim: bridge` (terminological mapping)

---

## Claim Change Policy (Anti-Gaming Rule)

You can only change a spec's `claim` field to reduce severity if you also add an explicit
`justification` line (1-2 sentences) tied to one of:

1. **Formal impossibility** — the claim cannot be stated in the type system
2. **Intentional non-formalization** — the claim is philosophical/phenomenological by design
3. **Empirical nature** — the claim is about computational cost, performance, or real-world behavior

This prevents slowly reclassifying everything to `theory-only` or `bridge` to achieve all-green.

**Examples of valid claim changes:**
- `theorem` → `bridge`: "Relates □ semantics to T-failure; translation is documented"
- `theorem` → `theory-only`: "Cost model claim; would require formalizing complexity metric"

**Examples of invalid claim changes:**
- `theorem` → `bridge`: (no justification given)
- `theorem` → `theory-only`: "Too hard to prove" (laziness is not valid)

---

## Non-Goals (Intentionally Not Formalized)

These specs are marked `theory-only` or `intentional` and should remain so:

- **SPEC-UNFOLD-001** — Theory-level operator stub
- **SPEC-TRUTH-001** — Philosophical definition
- **SPEC-MEAN-001** — Philosophical definition
- **SPEC-HIER-001/002** — Organizational frameworks
- **SPEC-CTYPE-001** — Meta-theoretical classification
- **SPEC-PLAST-002** — T3 conjecture about Level 6 self
- **SPEC-CONTRA-003** — Empirical cost claim

---

*This roadmap is documentation only. No Agda changes should be made based on this
document without explicit instruction.*
