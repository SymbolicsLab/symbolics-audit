# Symbolics Audit

Cross-layer compatibility tracking for the Symbolics Lab project.

## Purpose

This repository maintains alignment between three layers of the Symbolics formal theory:

1. **Theory (Vault)** — Conceptual/philosophical claims in Obsidian notes
2. **Core (Agda)** — Formal proofs and verified implementations
3. **Language (DSL)** — Practical symbolic manipulation tools (future)

## Architecture

```
SymbolicsLab/
├── symbolics-audit/      # This repo - compatibility tracking
├── symbolics-core/       # Agda formalization
├── symbolics-research/   # Vault with theory notes
└── symbolics-dsl/        # Domain-specific language
```

## Key Files

- `spec/registry.yaml` — Canonical cross-layer contract mapping claims
- `scripts/audit.py` — Generates compatibility report
- `AUDIT_REPORT.md` — Generated output showing drift and alignment

## Running the Audit

```bash
# From this directory
python scripts/audit.py

# Output written to AUDIT_REPORT.md
```

## Registry Schema

Each entry in `spec/registry.yaml` tracks:
- **id**: Unique identifier (e.g., `SPEC-FOLD-001`)
- **tier**: T1 (foundational), T2 (derived), T3 (conjecture)
- **theory**: Status and pointer to Vault note
- **agda**: Status and pointer to lemma
- **dsl**: Status and pointer (when implemented)
- **mapping**: Relationship between layers (exact, weakened, strengthened, different)
- **gap**: Owner and required action when layers disagree

## Principles

1. **Registry is canonical** — Source of truth for what claims exist
2. **Agda is authoritative for verification** — If Agda refutes, theory must update
3. **Gaps must have owners** — No orphan mismatches
4. **"Different" is not failure** — But requires explicit rationale
5. **Audit produces task lists** — Actionable, not just informational

## CI

The GitHub Action runs on PRs to any sibling repo, cloning all repos and running the audit. Critical mismatches fail the build.
