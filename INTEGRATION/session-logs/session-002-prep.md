# Session 2 Preparation — FDE-Fold Agda Implementation

**Prepared**: 2026-02-02
**Previous Session**: Session 1 (extended, ~6 hours)
**Focus**: Agda implementation of FDE-fold

---

## Context from Session 1

### Key Theoretical Decisions

1. **Atom Ontology (Term B)**: Atoms are fold-stabilized names, not cut-products
2. **Cut-Fold Co-Constitution**: Cut is real at meta-level; fold creates internal witnesses
3. **Remainder = Fiber of Fold**: The multiplicity of Opaque states behind each Config
4. **FDE for Level 2+**: Propositional layer only; pre-propositional remains open

### The Typed Interface (Target)

```agda
World : Set
Opaque : World → Set      -- OPEN: pre-symbolic substrate
Atom : World → Set
Config : (w : World) → Set

cutW : World → World
cut : Opaque w → Opaque (cutW w)
fold : Opaque w → Config w  -- NOT left-invertible
```

### Simpler Entry Point (For Session 2)

```agda
World : Set
World = ℕ

Atom : World → Set
Atom n = Fin n

cutW : World → World
cutW n = suc n

Config : World → Set
fold : {w : World} → Config w → Config w
```

This defers `Opaque` while allowing FDE-fold implementation to proceed.

---

## Session 2 Goals

### Primary: Implement FDE-fold in Agda

1. **Define FDE values**: `data FOUR = Neither | In | Out | Both`
2. **Define Config as world-indexed**: `Config w = Atom w → FOUR` (or pair of finite sets)
3. **Define FDE consequence relation**
4. **Build Setoid on configurations** (equivalence, not equality)
5. **Define fold via Setoid**
6. **Re-prove properties for Setoid**:
   - Idempotence: `fold (fold Φ) ≈ fold Φ`
   - Conservativity: `support (fold Φ) ⊆ support Φ`
   - Contradiction-preservation: `+a ∈ Φ ∧ -a ∈ Φ → +a ∈ fold Φ ∧ -a ∈ fold Φ`

### Secondary: Track Where It Breaks

Where does the implementation hit walls? These breakages constrain `Opaque` specification:
- Does world-indexing cause problems?
- Does Setoid quotient work under `--without-K`?
- What does "conservativity" mean when atoms are world-indexed?

---

## Files to Read at Session Start

### Required
1. `INTEGRATION/state.yaml` — current state
2. `INTEGRATION/decisions/ADR-001-configuration-representation.md` — FDE design decisions
3. `symbolics-core/src/` — existing Agda code structure

### Recommended
4. `Vault/00_inbox/drafts/Cut-Fold Co-Constitution.md` — interface specification
5. `Vault/00_inbox/drafts/Atom Ontology.md` — why atoms are fold-products

---

## Agda Conventions (Reminder)

- **Always**: `--safe --without-K`
- **No**: postulates, `--type-in-type`
- **Header**: `-- SPEC: SPEC-XXX-NNN` linking to audit registry
- **Preference**: Readable over minimal (Core Principle IX)

---

## Questions to Defer (Not for Session 2)

- What is `Opaque`?
- How does remainder formalize?
- What does unfold do?
- How does this connect to DSL?

Focus on: **Does the FDE-fold design actually typecheck?**

---

## Success Criteria

Session 2 is successful if:
1. We have compiling Agda code for FDE values and configurations
2. We have at least one fold property re-proven for Setoid (idempotence is easiest)
3. We've identified where the design breaks (if anywhere)
4. We've NOT spent time on more theory

---

**Ready for Session 2.**
