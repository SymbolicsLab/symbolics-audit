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
  theory:
    status: theorem | conjecture | definition | refuted
    notes_ref: path/to/note.md
    last_reviewed: YYYY-MM-DD
    confidence: high | medium | low
  agda:
    status: verified | conjecture | refuted | missing
    pointer: Module.Path.lemma-name
    safety: safe | unsafe
  dsl:
    status: implemented | witnessed | missing
    pointer: Module.Path
  mapping:
    relation: exact | weakened | strengthened | different
    rationale: Explanation
  gap:
    owner: theory | agda | dsl | intentional | unknown
    action: Required action or "none"
    justification: Why gap exists
```

## What NOT to Modify Without Confirmation

1. **Registry IDs** — Immutable once assigned
2. **Tier assignments** — Require architectural review
3. **Gap owners** — Should reflect actual responsibility
4. **AUDIT_REPORT.md** — Generated file, do not edit

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
