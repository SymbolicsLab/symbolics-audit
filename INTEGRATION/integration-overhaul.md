# Integration Overhaul — CI/CD for Theory
**Date**: 2026-03-13

---

## The Problem

When a paper is written — Synthese on risk, EJPS on causality, Estudios on inference — it advances the theory. New framings emerge, existing concepts get refined, connections get made. But those insights stay in the paper's `draft.md`. They don't flow back into:

- The **vault** (the living theory documents)
- The **claims ledger** (which claims are proven, deployed, or conjectural)
- The **book** (which chapters are affected)
- The **Agda** (whether new claims need formalization)
- The **secrecy map** (which ideas are now public)

The previous integration system (symbolics-audit with YAML schemas, severity rules, gap owners) went stale because it required active management as a separate task. Any system that requires context-switching from thinking to tracking will fail.

## The Insight: Theory as Codebase

The project IS a codebase:
- **Papers/presentations** = feature branches (advance the theory in a specific direction)
- **Vault** = main branch (the source of truth for what the theory says)
- **Agda** = test suite (formal verification — does it compile?)
- **Book** = documentation (the architecture document for the system)
- **SDK/benchmark** = production (deployed, running, producing results)
- **Claims ledger** = dependency tracker (what depends on what)

In software, when you merge a feature branch:
1. CI runs tests (does it compile? does it break anything?)
2. Documentation is updated
3. Changes deploy to production

When you "merge" a paper's insights into the vault:
1. Check consistency (does the new insight contradict existing theory?)
2. Update downstream artifacts (vault, book, claims ledger, secrecy map)
3. Flag formalization needs (should this be proven in Agda?)

This overhaul builds that pipeline.

---

## Architecture

### Layer 1: Skills (User-Invoked or Claude-Suggested)

**`/integrate`** — The merge command. After working on a paper, presentation, or any theory-advancing session:

1. Reads the files touched in the session (or a specified submission folder)
2. Reads the relevant vault documents
3. Identifies theoretical advances: new framings, refined concepts, new connections, new claims
4. Proposes specific edits to vault documents (Claude generates, human decides)
5. Updates the claims ledger
6. Flags downstream effects (book chapters, Agda, other papers, secrecy)
7. Writes an integration record

**`/audit`** — The health check. On-demand coherence scan:

1. Scans all submission folders for recent drafts
2. Compares theoretical content against vault
3. Checks Agda coverage (what's claimed but unproven?)
4. Checks book chapter coverage (what's in papers but not in book?)
5. Checks secrecy status (what's public, what's private?)
6. Produces a coherence report with specific action items

**`/claims`** — Quick view/update of the claims ledger. Show current status or update after Agda work.

### Layer 2: Hooks (Automatic)

**Enhanced Stop hook** — After every session, an agent hook:

1. Checks if theory-relevant files were modified (vault, submissions, book, Agda)
2. If so, identifies what changed and what it might affect
3. Writes a brief integration note to `~/Developer/.pending-integrations.md`
4. Updates OVERVIEW.md if deadlines or statuses changed
5. Lightweight — runs in ~30 seconds, not a full integration

**SessionStart enhancement** — At session start, MEMORY.md (already loaded) includes a pointer to check `.pending-integrations.md`. Claude reads it and surfaces any pending integration needs: "Last session advanced the resilience argument in the Synthese Risk paper. Vault 01 and 04 may need updating. Want me to run /integrate?"

### Layer 3: The Claims Ledger (Passive Artifact)

A single markdown file at `symbolics-audit/INTEGRATION/claims-ledger.md`.

Maps every major theoretical claim to its status across all layers:

| Claim | Vault | Agda Status | Papers (deployed) | Book Ch. | Secrecy |
|-------|-------|-------------|-------------------|----------|---------|
| Conservativity | 02, 05 | verified (SPEC-FOLD-*) | EJPS (as "linking rule") | 4 | public |
| T-failure | 05 | verified | — | 4 | private |
| Two-body condition | 01 | structural (3 props) | Synthese Self-Individuation | 2 | public |
| Distinction-preservation | 02 | type-level | Estudios (as "discrimination-preservation") | 4 | public |
| Resilience gradient | 01, 04 | bounded (finite) | Synthese Risk (partial) | 3 | partially public |
| Policy stratification | 02 | type-level | — | 4 | private |
| Entanglement thesis | Nature of Distinction ch. | — | — | 1? | private |
| etc. | | | | | |

Maintained by Claude through `/integrate`, `/audit`, and the Stop hook. The user never touches this file directly.

### Layer 4: Integration Records

Each integration creates a brief record at `symbolics-audit/INTEGRATION/records/YYYYMMDD-description.md`:

```
# Integration: 2026-03-13 — Estudios inference paper
## Source: Submissions/2026-04-01_Estudios_Inferences/
## Advances:
- Constraint-fixity gradient (new framing of policy-fixity in civilian vocabulary)
- Discrimination-preservation (new name for distinction-preservation in civilian vocabulary)
- Maximal resilience explains phenomenology of deductive necessity
## Vault updates: none yet (theoretical content consistent with vault, new vocabulary only)
## Claims ledger: updated (Estudios added to deployed papers for 3 claims)
## Downstream: Book ch. 4 outline updated
```

---

## Implementation Plan

### Step 1: Create the skills

Create three skill files:

- `~/.claude/skills/integrate/SKILL.md`
- `~/.claude/skills/audit/SKILL.md`
- `~/.claude/skills/claims/SKILL.md`

These are user-level (available in all projects, since the integration spans repos).

### Step 2: Create the claims ledger

Create `symbolics-audit/INTEGRATION/claims-ledger.md` with the initial mapping. Populate it by scanning vault, Agda specs, and recent submissions.

### Step 3: Enhance the Stop hook

Replace the current shell-script Stop hook with an agent-type hook that:
- Checks for theory-relevant file modifications
- Writes to `.pending-integrations.md`
- Still outputs the existing checklist

### Step 4: Update MEMORY.md

Add protocol: "At session start, check `~/Developer/.pending-integrations.md` for integration needs from previous sessions."

### Step 5: Create the integration records directory

`symbolics-audit/INTEGRATION/records/` — one file per integration event.

---

## What This Replaces

| Old system | New system |
|---|---|
| spec/registry.yaml (61 specs, YAML schema) | claims-ledger.md (flat markdown, maintained by Claude) |
| Session archive (state.yaml) | MEMORY.md + OVERVIEW.md + integration records |
| AUDIT_REPORT.md (generated) | `/audit` skill (generated on demand, live from repos) |
| Gap tracking (gap owners, severity) | Empty cells in claims ledger |
| Manual session handoffs | Stop hook agent + pending-integrations |

## What This Preserves

- **Agda proofs** — self-maintaining (they compile or they don't)
- **Vault** — remains the source of truth, updated through `/integrate` with user approval
- **Per-repo CLAUDE.md** — entry points for Claude, unchanged
- **OVERVIEW.md** — the human-readable status document
- **Asymmetric authority** — Claude proposes, human decides. No auto-edits to theory.

## Design Principles

1. **Integration is Claude's job, not the user's.** The user thinks and writes. Claude maintains coherence.
2. **No separate management task.** Integration happens as a byproduct of working sessions, not as overhead.
3. **Graceful degradation.** If the system goes untouched for a month, nothing breaks. Claude rebuilds state from the repos next session.
4. **Flat over structured.** Markdown tables over YAML schemas. Readable over machine-parseable.
5. **Asymmetric authority preserved.** Claude proposes vault edits. The user approves, modifies, or rejects.
