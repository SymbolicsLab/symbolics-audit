# CLAUDE.md — Symbolics Audit

## Project Overview

This repository provides cross-layer compatibility tracking for the Symbolics Lab formal theory project. It monitors alignment between:

- **Theory** (Obsidian Vault in `symbolics-research/Vault`)
- **Agda** (Formal proofs in `symbolics-core`)
- **DSL** (Future implementation in `symbolics-dsl`)

## Three-Layer Architecture

### Layer Responsibilities

| Layer | Authority | Format | Location |
|-------|-----------|--------|----------|
| Theory | Conceptual claims | Markdown + YAML frontmatter | `../symbolics-research/Vault/` |
| Agda | Verification | Agda with `-- SPEC:` headers | `../symbolics-core/src/` |
| DSL | Implementation | TBD | `../symbolics-dsl/` |

### Information Flow

```
Theory (claims) ←→ Registry (contract) ←→ Agda (proofs)
                         ↓
                    DSL (implements)
```

## Key Invariants

1. **Every canonical Vault note with `maturity: canonical` should have a registry entry**
2. **Every Agda lemma with `-- SPEC:` must reference a valid registry ID**
3. **Registry IDs are immutable once assigned** (can be deprecated, not reused)
4. **Gap owners must be one of: `theory`, `agda`, `dsl`, `intentional`, `unknown`**

## File Organization

```
symbolics-audit/
├── CLAUDE.md              # This file
├── README.md              # Project overview
├── spec/
│   └── registry.yaml      # Canonical cross-layer contract
├── scripts/
│   └── audit.py           # Audit script
├── AUDIT_REPORT.md        # Generated output (do not edit manually)
└── .github/
    └── workflows/
        └── audit.yml      # CI workflow
```

## Running the Audit

```bash
python scripts/audit.py
```

The script:
1. Parses `spec/registry.yaml`
2. Scans Agda files for `-- SPEC:` headers
3. Scans Vault for canonical notes
4. Generates `AUDIT_REPORT.md`

## Registry Schema

```yaml
- id: SPEC-XXX-NNN
  title: Human-readable name
  statement: Precise claim statement
  tier: T1 | T2 | T3
  claim: theorem | conjecture | definition | bridge | theory-only
  proof: verified | conjecture | refuted | n/a
  theory:
    notes_ref: path/to/note.md
    last_reviewed: YYYY-MM-DD
    confidence: high | medium | low
  agda:
    pointer: Module.Path.lemma-name
    safety: safe | unsafe
  dsl:
    status: implemented | witnessed | missing
    pointer: Module.Path
  mapping:
    relation: exact | weakened | strengthened | different | partial
    rationale: Explanation
  gap:
    owner: theory | agda | dsl | intentional | unknown
    action: Required action or "none"
    justification: Why gap exists
```

## Claim and Proof Fields

Each spec has two top-level fields that separate theory-side assertions from implementation-side verification:

### `claim` — What the spec asserts (theory-side)

| Claim | Meaning |
|-------|---------|
| `theorem` | A proven claim in theory that should have Agda verification |
| `conjecture` | An unproven claim; Agda verification optional/pending |
| `definition` | Establishes terminology; may have Agda type encoding |
| `bridge` | Documents translation between layers; GREEN even with `different` mapping |
| `theory-only` | Philosophical grounding; no Agda formalization expected |

### `proof` — What Agda has actually done (implementation-side)

| Proof | Meaning |
|-------|---------|
| `verified` | Agda has a proof/definition that matches the claim |
| `conjecture` | Agda has a postulate or unproven claim |
| `refuted` | Agda has a counterexample disproving the claim |
| `n/a` | No Agda verification expected (for `bridge`, `theory-only`, some `definition`) |

### Severity Rules

| Claim | Proof | Severity | Rationale |
|-------|-------|----------|-----------|
| `theorem` | `verified` | GREEN | Fully aligned |
| `theorem` | `conjecture` | YELLOW | Work in progress |
| `theorem` | `refuted` | RED | Theory must update |
| `theorem` | `n/a` | RED | Theorem needs proof |
| `conjecture` | `conjecture` | GREEN | Aligned uncertainty |
| `definition` | `verified` | GREEN | Type alignment |
| `definition` | `n/a` | GREEN | Some definitions don't need Agda |
| `bridge` | any | GREEN | Documented translation |
| `theory-only` | `n/a` | GREEN | Intentionally non-formal |
| T1 + `conjecture` | any | YELLOW | Foundational tier needs certainty |

### Bridge Specs

A `bridge` spec explicitly documents the translation between theory concepts and Agda formalization, even when the two don't express identical content. It's not a claim to be proven — it's a documented mapping with a rationale.

**When to use `bridge`:**
- Theory and Agda express the same intuition through different formalizations
- The translation has been deliberately designed and documented
- The `mapping.relation` would otherwise be `different` (causing permanent YELLOW)

**Example:**
- Theory says: "Truth = ineliminable commitment under fold-closure"
- Agda has: property P over admissible states
- Bridge spec documents: "P is the Agda proxy for 'ineliminable commitment'"

A `bridge` spec with `mapping.relation: different` is GREEN because the structural gap is intentionally documented, not unresolved debt.

## Claim Change Policy (Anti-Gaming Rule)

You can only change a spec's `claim` field to reduce severity if you also add an explicit
`rationale` line (1-2 sentences) tied to one of these justifications:

1. **Formal impossibility** — the claim cannot be stated in the type system
2. **Intentional non-formalization** — the claim is philosophical/phenomenological by design
3. **Empirical nature** — the claim is about computational cost, performance, or real-world behavior

This prevents slowly reclassifying everything to `theory-only` or `bridge` to achieve all-green.

**Examples of valid claim changes:**
- `theorem` → `bridge`: "Relates □ semantics to T-failure; translation is documented"
- `theorem` → `theory-only`: "Cost model claim; would require formalizing complexity metric"

**Examples of invalid claim changes:**
- `theorem` → `bridge`: (no rationale given)
- `theorem` → `theory-only`: "Too hard to prove" (laziness is not a valid reason)

## Theorem Narrowing Rule

If a spec is renamed/narrowed because the proved theorem was weaker than the original claim:

1. The old semantic claim MUST become a new spec (as conjecture), OR
2. The old semantic claim MUST be marked `theory-only` with explicit justification

You cannot achieve GREEN by proving a weaker theorem under an old name.
This preserves continuity of intent and prevents semantic drift.

**Example (SPEC-CONTRA-002/004 split):**
- Original SPEC-CONTRA-002 claimed "contradiction preservation"
- Agda proved only "non-explosion" (weaker property)
- Fix: Renamed SPEC-CONTRA-002 to match what was proved, created SPEC-CONTRA-004 for the original claim

## Mapping Relation Rules

The `mapping.relation` field describes how theory and Agda express the same concept:

| Relation | Definition | Example |
|----------|------------|---------|
| `exact` | Layers express identical content | Side trichotomy is identical in both |
| `weakened` | Agda proves less than theory claims | Theory claims universally, Agda proves for subset |
| `strengthened` | Agda proves more than theory claims | Agda includes additional properties |
| `different` | Distinct formalizations of same intuition | Conceptual vs operational definitions |
| `partial` | Partial overlap between layers | Some aspects formalized, others pending |

### When to Use Each Relation

- **exact**: Use when Agda types/proofs directly encode the theory statement
- **weakened**: Use when theory makes stronger claim than Agda has proven
- **strengthened**: Use when Agda proof establishes more than theory asserts
- **different**: Use for philosophical concepts that get operational formalization
- **partial**: Use when some aspects are covered but others are outstanding

## What NOT to Modify Without Confirmation

1. **Registry IDs** — Immutable once assigned
2. **Tier assignments** — Require architectural review
3. **Gap owners** — Should reflect actual responsibility
4. **AUDIT_REPORT.md** — Generated file, do not edit
5. **Status classifications** — Should reflect actual epistemic state

## Canonical Note Requirement

Any new note promoted to `maturity: canonical` MUST include a `spec_links` field
in its frontmatter linking to at least one SPEC entry in the registry.

Even theory-only or philosophical notes should link to a `claim: theory-only` spec.
Notes invisible to the audit system will drift undetected.

Example:
```yaml
---
maturity: canonical
spec_links: [SPEC-MODAL-001, SPEC-MODAL-004]
---
```

## Drift Categories

| Drift Type | Severity | Action |
|------------|----------|--------|
| Theory claims theorem, Agda missing | RED | Add Agda proof or downgrade theory |
| Theory claims theorem, Agda refuted | RED | Update theory to match Agda |
| Agda verified, Theory only conjecture | YELLOW | Opportunity to strengthen theory |
| Mapping is "different" | YELLOW | Document rationale or reconcile |
| `last_reviewed` > 90 days | STALE | Re-review entry |

## Spec ID Conventions

Format: `SPEC-{DOMAIN}-{NNN}`

Domains:
- `DIST` — Distinction-related
- `FOLD` — Fold operator
- `UNFOLD` — Unfold operator
- `DECAY` — Decay/update mechanics
- `RES` — Resolution order
- `AGG` — Aggregation
- `MODAL` — Modal logic (T-failure, etc.)
- `HIER` — Hierarchies (Organizational, Locus)
- `IDENT` — Identity
- `PLAST` — Plasticity
- `METAB` — Metabolism
- `CONTRA` — Contradiction handling
- `MEAN` — Meaning/truth

## Adding New Specs

1. Choose appropriate domain prefix
2. Use next available number in that domain
3. Fill all required fields
4. Set initial `gap.owner` based on which layer is source
5. Run audit to verify consistency
