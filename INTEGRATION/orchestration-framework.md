# Symbolics: Orchestration Framework
**Version**: 0.4.0 | **Date**: 2026-01-31 | **Status**: Active

---

## Architecture Overview

### Primary Orchestrator: Claude Code
Claude Code runs on the user's machine with full filesystem access. It is the primary
orchestrator because it can read and write all repos, run Agda, manage git, and update
state without manual file transfer.

Claude Code operates via three modes defined in `SymbolicsLab/CLAUDE.md`:
- **PROOF mode**: Formal Agda work with enforced XML output structure
- **VAULT-PREP mode**: Note creation with self-check
- **REASON mode**: Free-form thinking that ends with a YAML handoff block

### Deep Reasoning Consultant: Claude Opus
Called in for extended philosophical reasoning, theory synthesis, or cross-domain analysis.

**Claude Desktop with MCP** (preferred): Configure filesystem access to SymbolicsLab/.
Gives Opus-level reasoning with direct file access. See §MCP Setup.

**Claude.ai chat** (fallback): Upload state.yaml and relevant files. Treat as consultant.

### User (Philipe): Final Authority
The user's philosophical intuition is the ultimate authority on what the theory IS.
The user relays prompts/responses for agents without filesystem access (ChatGPT, Gemini, Codex).
The user has veto on all decisions.

### Governing Documents

| Document | Location | Purpose |
|----------|----------|---------|
| CLAUDE.md | `SymbolicsLab/` root | Claude Code operating modes and config |
| state.yaml | `INTEGRATION/` | Current project state (single source of truth) |
| core-principles.md | `INTEGRATION/` | Ten governing principles |
| agent-deliberation-protocols.md | `INTEGRATION/` | Reasoning patterns for Cowork, ChatGPT, Gemini, Codex, cross-agent |
| Vault/CLAUDE.md | `symbolics-research/Vault/` | Vault conventions (AUTHORITATIVE for all vault work) |

---

## Agent Roster

### 1. Claude Code — PRIMARY ORCHESTRATOR
**Access**: Full filesystem, CLI, git, Agda compiler
**Scope**: All repos + INTEGRATION state management + orchestration

**Configuration**: `SymbolicsLab/CLAUDE.md` (reads at session start)
**State**: `INTEGRATION/state.yaml` (reads at start, rewrites at end)

**Duties**:
- Session management (read state → propose plan → execute → update state → commit)
- Agda proof development and verification
- DSL implementation
- Audit registry updates
- Prompt generation for other agents (saved to `INTEGRATION/prompts/`)
- Session logs, git operations

**Deliberation**: Handled by CLAUDE.md operating modes (PROOF, VAULT-PREP, REASON)

---

### 2. Cowork
**Access**: Local filesystem, Obsidian vault
**Scope**: Theory writing, vault maintenance, document creation

**CRITICAL**: Must follow `Vault/CLAUDE.md` for all vault work. That file is authoritative.
The orchestration framework does NOT restate vault conventions.

**Duties**:
- Vault note creation from scattered insights
- Revision drafts for existing canonical notes
- Emergency state.yaml generation (if Claude Code session ended without updating)
- Long-form theory writing (dossier sections, papers, abstracts)

**Deliberation**: See `INTEGRATION/agent-deliberation-protocols.md`
(NEW-NOTE-FROM-INSIGHT, REVISION, STATE-YAML-GENERATION, THEORY-WRITING)

---

### 3. ChatGPT (OpenAI) — Theory Consultant
**Access**: Web/app, extensive conversation memory of theory evolution
**Strengths**: Structural suggestions, lateral connections, recall of past discussions
**Limitations**: Confidence can exceed accuracy. Can be protective of theory.

**CRITICAL**: All prompts written in user's voice. Do NOT mention orchestration
or that another AI is delegating.

**Deliberation**: See agent-deliberation-protocols.md (CHATGPT-CRITIQUE, CHATGPT-CONNECTIONS)

---

### 4. Gemini (Google) — Research Engine
**Access**: Web/app, internet search
**Strengths**: Literature surveys, finding related work, checking novelty

**Deliberation**: See agent-deliberation-protocols.md (GEMINI-SURVEY)

---

### 5. Codex (OpenAI) — Code Reviewer
**Access**: Web/app
**Strengths**: Code review, alternative implementations, testing

**Deliberation**: See agent-deliberation-protocols.md (CODEX-REVIEW)

---

## Information Flow

```
                    ┌─────────────────┐
                    │   Claude Code   │
                    │  (orchestrator  │
                    │  + formal work) │
                    └────────┬────────┘
                             │ filesystem
              ┌──────────────┼───────────────┐
              │              │               │
    ┌─────────┴──┐    ┌─────┴─────┐   ┌────┴─────────┐
    │   Cowork   │    │Claude Opus│   │   ChatGPT    │
    │  (vault)   │    │  (deep    │   │ (consultant) │
    │ filesystem │    │ reasoning)│   │  user-relay  │
    └────────────┘    └───────────┘   └──────────────┘
                                             │
                                    ┌────────┴────────┐
                                    │  Gemini  Codex  │
                                    │  user-relay     │
                                    └─────────────────┘
```

**Direct** (no relay): Claude Code ↔ filesystem ↔ Cowork, Claude Desktop (MCP)
**User-relayed**: Claude Code generates prompts → user copy-pastes to ChatGPT/Gemini/Codex → user relays response

---

## State Management

### state.yaml (replaces HANDOFF.md)

Location: `INTEGRATION/state.yaml`

This is the single source of current project state. Structured YAML that agents
read and write programmatically.

**Rules for all agents:**
- Keep FLAT — no nesting deeper than 2 levels
- When updating: REWRITE the entire section, never patch individual lines
- All dates ISO format

**Fields:**
- `theory_summary` — one paragraph (update only when understanding genuinely changes)
- `verified_agda` / `not_verified` — what's proven vs. what's missing
- `vault_canonical_count` / `vault_draft_count` / `vault_scattered_unrouted`
- `current_context` — what just happened
- `active_threads` — list of active work items with id, summary, status, priority
- `next_actions` — ordered list; Claude Code executes top item
- `agent_status` — last action per agent
- `decisions_pending` — open questions with what they block
- `flags` — anything concerning or surprising

**Update cycle:**
1. Claude Code reads state.yaml at session start
2. Executes top item in `next_actions`
3. Rewrites relevant sections at session end
4. Writes session log to `INTEGRATION/session-logs/session-NNN.md`
5. Git commits both

**Emergency recovery:** If Claude Code session ends without updating state.yaml,
ask Cowork to run the STATE-YAML-GENERATION protocol (see agent-deliberation-protocols.md).

---

## Workflows

### W1: Vault Hygiene (Scattered Insights Integration)
**Goal**: Route 34 scattered insights into vault drafts
**Lead**: Cowork (following NEW-NOTE-FROM-INSIGHT protocol)
1. Claude Code prepares batch of 3-5 insights with context
2. Cowork creates drafts in `00_inbox/drafts/` per Vault/CLAUDE.md
3. User reviews in Obsidian, promotes or returns
4. Claude Code marks insights as "routed" in scattered-insights.md

### W2: Foundational Logic Investigation (F.1)
**Goal**: Determine right logic substrate (LP vs FDE vs topological vs other)
**Agents**: Claude Code (formal), Gemini (literature), ChatGPT (theoretical)
1. Gemini: literature survey on FDE in proof assistants
2. Claude Code (PROOF mode): attempt FDE fold properties in Agda
3. ChatGPT (in user's voice): what does the theory need from a logic?
4. Convergence protocol: synthesize results, user decides

### W3: Unfold Specification (F.3)
**Goal**: Clarify and formalize unfold
**Agents**: ChatGPT (concept), Claude Code (formalization), Claude Opus (deep reasoning)
1. Gather all unfold descriptions across vault and dossier
2. Claude Opus (REASON mode): deep analysis, ends with handoff block
3. Claude Code (PROOF mode): type exploration in Agda

### W4: Critical Audit
**Goal**: Stress-test a specific claim or proof
**Agents**: Codex (review), ChatGPT (objections), Claude Code (counterexamples)
Uses CONVERGENCE protocol from agent-deliberation-protocols.md

### W5: Council Pattern (for foundational questions)
**Goal**: Get independent input from multiple agents on the same question
**Method**: Map-Reduce (see §Council Pattern below)

---

## Council Pattern

For questions like "Is FDE the right logic?" that need multiple perspectives:

**Manual version:**
1. Write one clear question
2. Send independently to 3+ agents (don't share answers between them)
3. Collect responses
4. Synthesize convergence/divergence
5. User decides

**Automated version (future, ~100 lines TypeScript):**
- Script takes a question file from `INTEGRATION/_council/questions/`
- Queries Claude API + OpenAI API with appropriate personas
- Writes responses to `INTEGRATION/_council/Q_NNN_RESOLVED.md`
- Build this when the manual version becomes a bottleneck

---

## Existing Systems (Unchanged)

The orchestration framework extends these. It does NOT replace them.

| System | Location | Governs | Status |
|--------|----------|---------|--------|
| Vault CLAUDE.md | `Vault/CLAUDE.md` | All vault conventions | **Authoritative. Unchanged.** |
| Compatibility Audit | `symbolics-audit/` | Cross-layer alignment | **Unchanged.** |
| Task Scaffolding | `Vault/00_inbox/_tasks/` | Multi-session vault tasks | **Unchanged.** |
| spec_links requirement | Vault frontmatter | Audit integration | **Unchanged and enforced.** |

---

## INTEGRATION Folder

```
symbolics-audit/INTEGRATION/
├── state.yaml                    # Current project state (machine-readable)
├── orchestration-framework.md    # This document
├── core-principles.md            # Ten governing principles
├── agent-deliberation-protocols.md # Protocols for Cowork, ChatGPT, Gemini, Codex, cross-agent
├── completeness-map.md           # Theoretical commitments tracked across layers
├── open-problems.md              # 20 prioritized research problems
├── scattered-insights.md         # 34 unrouted insights from abstracts
├── session-logs/                 # Per-session summaries
│   └── session-NNN.md
├── prompts/                      # Generated prompts for other agents
├── decisions/                    # Architectural Decision Records
│   └── ADR-NNN-title.md
├── _council/                     # Multi-agent convergence (future)
│   ├── questions/
│   └── resolved/
└── red-team/                     # Adversarial review reports
    └── red-team-NNN.md
```

**Session log format:**
```markdown
# Session [N] — [Date]
## Orchestrator: Claude Code
## Goal: [what we set out to do]
## Accomplished: [what was done]
## Agents used: [which agents, what they were asked, key outputs]
## Decisions: [choices made, with rationale]
## Next: [what the next session should address]
## Flags: [anything concerning, surprising, or unresolved]
```

**Architectural Decision Records:**
```markdown
# ADR-NNN: [Title]
## Date: [YYYY-MM-DD]
## Status: [proposed | accepted | superseded]
## Context: [why this decision was needed]
## Decision: [what was chosen]
## Rationale: [why]
## Consequences: [what changes]
```

---

## Hooks and Continuous Verification

### Pre-Commit (Husky)

Install: `npm install husky --save-dev && npx husky init`

`.husky/pre-commit`:
```bash
#!/bin/sh
# Type-check all modified Agda files
agda --safe --without-K src/**/*.agda
```

Optional additions:
- Run `scripts/audit.py` to check spec alignment
- Pipe `git diff` to a lightweight model for quick review

### Post-Proof Workflow
After a successful proof, Claude Code should:
1. Update `INTEGRATION/completeness-map.md`
2. Register new specs in `spec/registry.yaml`
3. Update relevant `active_threads` in state.yaml
4. Git commit with descriptive message

---

## MCP Setup (Claude Desktop with Filesystem Access)

To give Claude Desktop (Opus) direct project access:

1. Open Claude Desktop → Settings → Developer → Edit Config
2. Add filesystem MCP server:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/YOUR_USERNAME/path/to/SymbolicsLab"
      ]
    }
  }
}
```

3. Restart Claude Desktop
4. Verify: hammer icon appears in input box; click to see filesystem tools
5. Test: "Read INTEGRATION/state.yaml and summarize current project state"

**Security**: Only grant access to SymbolicsLab/.

---

## Delegation Principles

| Task | Agent | Mode/Protocol |
|------|-------|---------------|
| Prove in Agda | Claude Code | PROOF mode |
| Write vault note | Cowork | NEW-NOTE-FROM-INSIGHT |
| Revise vault note | Cowork | REVISION |
| Deep theory question | Claude Opus | REASON mode (+ handoff block) |
| "Is this coherent?" | ChatGPT | CHATGPT-CRITIQUE (user's voice) |
| "Who else has done X?" | Gemini | GEMINI-SURVEY |
| "Is this code correct?" | Codex | CODEX-REVIEW |
| Foundational question | Multiple | CONVERGENCE / Council pattern |
| Emergency state recovery | Cowork | STATE-YAML-GENERATION |

### Conflict Resolution
- Formal disagreement → Claude Code runs proof; proof wins
- Theoretical disagreement → present both views; user's intuition breaks tie
- Factual disagreement → Gemini searches; evidence wins

---

## Meta-Review

### Periodic Second Opinions (every 3-5 sessions)
Send status summary to ChatGPT and Gemini independently (in user's voice).
If they converge on a concern the orchestrator hasn't raised, promote it.

### Red Team Sessions (every 5-10 sessions)
Full session dedicated to adversarial review:
- "What is the weakest part of what we've built?"
- "If this theory is wrong, where does it break first?"
Results go in `INTEGRATION/red-team/red-team-NNN.md`.

### Methodology Drift Check
At each framework update: is infrastructure growing faster than theory progress?
The ratio of meta-work to object-level work should decrease over time.
(Principle I: the theory comes first. Principle X: protect the metabolism.)

---

## Quality Gates

Before integrating into canon:
1. **Formal results**: `agda --safe --without-K` passes
2. **Theoretical claims**: Reviewed by ≥2 sources
3. **Vault notes**: Follow Vault/CLAUDE.md, include spec_links, honest maturity
4. **Open Problem updates**: Evidence for status change documented
5. **Architectural decisions**: ADR filed in `INTEGRATION/decisions/`

---

## Repository Structure

```
SymbolicsLab/
├── CLAUDE.md                     # Claude Code orchestrator config
├── symbolics-core/               # Agda proofs
├── symbolics-dsl/                # TypeScript DSL
├── symbolics-audit/              # Audit system
│   ├── spec/registry.yaml
│   ├── scripts/audit.py
│   └── INTEGRATION/              # Research orchestration
│       ├── state.yaml
│       ├── orchestration-framework.md
│       ├── core-principles.md
│       ├── agent-deliberation-protocols.md
│       ├── completeness-map.md
│       ├── open-problems.md
│       ├── scattered-insights.md
│       ├── session-logs/
│       ├── prompts/
│       ├── decisions/
│       ├── _council/
│       └── red-team/
├── symbolics-research/           # Obsidian vault
│   └── Vault/
│       └── CLAUDE.md             # Vault conventions (AUTHORITATIVE)
└── docs/
    └── research-dossier.md
```

---

## Execution Plan

### Session 0 (Complete): Foundation
- [x] Completeness Map, Open Problems, Scattered Insights created
- [x] Orchestration Framework v0.4.0
- [x] Core Principles, Agent Deliberation Protocols
- [x] state.yaml, CLAUDE.md for Claude Code
- [ ] Place all documents in INTEGRATION/
- [ ] Place CLAUDE.md in SymbolicsLab/ root
- [ ] Create subdirectories
- [ ] Set up MCP for Claude Desktop
- [ ] Set up Husky pre-commit hooks
- [ ] Git commit: "Initialize INTEGRATION research orchestration"

### Session 1: System Test + First Object-Level Work
- Claude Code reads state.yaml, proposes plan
- Cowork: 3-5 vault drafts from highest-priority scattered insights
- ChatGPT: review Completeness Map for gaps
- Produce session log + updated state.yaml

### Session 2: Logic Substrate (F.1)
### Session 3: Unfold Specification (F.3)
### Sessions 4+: Determined by results
