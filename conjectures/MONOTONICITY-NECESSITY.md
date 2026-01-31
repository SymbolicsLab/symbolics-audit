# Proposition: Monotonicity Necessity for Cycling

**Date**: 2026-01-29
**Status**: Proof sketch + empirical verification (not yet mechanized in Agda)

---

## Statement

If truth support is monotone non-decreasing over time, then switches ≤ 1.

Equivalently: **switches > 1 requires non-monotone truth dynamics.**

---

## Formal Statement

Let τ = (s₀, s₁, ..., sₜ) be a trajectory.

Define:
- `truthSupport(s, u) = (supportsIn(Agg(s)(u)), supportsOut(Agg(s)(u)))`
- `conflictOn(s) = ∃u: truthSupport(s,u) = (true, true)`

**Theorem (Monotonicity Bound)**:
If for all t and all u:
```
truthSupport(sₜ, u) ≤ truthSupport(sₜ₊₁, u)  (componentwise)
```
Then:
```
switches(τ) ≤ 1
```

---

## Proof Sketch

1. `conflictOn(s) = ∃u: truthSupport(s,u) = Both`
2. If truth support is monotone, once Both appears at u, it persists
3. Therefore conflictOn can only transition: false → true (at most once)
4. Cannot go true → false (would require truth support to decrease)
5. Maximum 1 switch (false→true) ∎

---

## Contrapositive (Necessity)

**switches > 1 ⟹ truth support is not monotone**

If a trajectory has more than 1 switch:
- conflictOn must go false→true→false (or true→false→true)
- This requires truth support to decrease at some point
- Therefore some truth-removal mechanism must be active

---

## Empirical Verification

### Phase 3B.2: Additive Evidence (Monotone)
- No truth-removal mechanism
- Result: **switches ≤ 1** for all trajectories (100% verified)

### Phase 3B.3: Evidence TTL (Non-Monotone)
- TTL removes truth support when evidence expires
- Result: **switches > 1** achievable

### Phase 3B.4: Phase Diagram
- k=∞ (baseline, monotone): max switches = 1
- k=3 (short TTL): max switches = 23, mean = 4.05

| TTL | Monotone? | Max Switches | Matches Theory |
|-----|-----------|--------------|----------------|
| ∞   | Yes       | 1            | ✓              |
| 20  | No        | 2            | ✓              |
| 10  | No        | 2            | ✓              |
| 5   | No        | 5            | ✓              |
| 3   | No        | 23           | ✓              |

---

## Consequence: TTL is Necessary for Cycling

This theorem establishes that TTL (or another truth-removal mechanism) is **necessary** for sustained cycling.

Without forgetting:
- Evidence accumulates
- Conflicts persist once formed
- System reaches stable conflict state

With forgetting:
- Old evidence expires
- Conflicts can resolve
- New evidence can create new conflicts
- Cycle continues

---

## Interpretation

**"Metabolism requires forgetting"**

For a symbolic creature to "live" (exhibit sustained cycling):
1. It must receive external evidence (novelty)
2. It must forget old evidence (TTL)
3. The balance determines cycling rate

This is not pathological — it's how bounded rationality works:
- Finite memory horizon
- Rolling evidence window
- Operational rather than accumulated truth

---

## Status

- [x] Informal proof
- [x] Empirical verification (Phase 3B.2, 3B.3, 3B.4)
- [ ] Agda formalization (optional)

---

## See Also

- `ADDITIVE-EVIDENCE-BOUND.md` - switches ≤ 1 under additive evidence
- `spec/EVIDENCE-TTL.md` - TTL specification
- `experiments/phase-diagram/RESULTS.md` - Phase diagram data
