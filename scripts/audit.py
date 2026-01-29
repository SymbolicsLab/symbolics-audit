#!/usr/bin/env python3
"""
Symbolics Audit Script

Parses registry.yaml, Agda SPEC headers, and Vault frontmatter to generate
a compatibility report showing alignment and drift between theory, Agda, and DSL layers.

Usage:
    python scripts/audit.py

Output:
    AUDIT_REPORT.md
"""

import os
import re
import sys

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    print("Or run: pip install -r requirements.txt")
    sys.exit(1)

from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple, Any

# Paths relative to symbolics-audit repo
SCRIPT_DIR = Path(__file__).parent
AUDIT_ROOT = SCRIPT_DIR.parent
REGISTRY_PATH = AUDIT_ROOT / "spec" / "registry.yaml"
REPORT_PATH = AUDIT_ROOT / "AUDIT_REPORT.md"

# Sibling repo paths
SYMBOLICS_LAB = AUDIT_ROOT.parent
AGDA_ROOT = SYMBOLICS_LAB / "symbolics-core" / "src"
VAULT_ROOT = SYMBOLICS_LAB / "symbolics-research" / "Vault"
DSL_ROOT = SYMBOLICS_LAB / "symbolics-dsl"

# Debug mode
DEBUG = os.environ.get('AUDIT_DEBUG', '').lower() in ('1', 'true', 'yes')


def debug(msg: str):
    """Print debug message if DEBUG is enabled."""
    if DEBUG:
        print(f"  [DEBUG] {msg}")


def load_registry() -> List[Dict[str, Any]]:
    """Load the spec registry YAML file."""
    if not REGISTRY_PATH.exists():
        print(f"Warning: Registry not found at {REGISTRY_PATH}")
        return []

    with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    return data.get('specs', [])


def parse_agda_spec_headers() -> Dict[str, List[Dict[str, str]]]:
    """
    Scan Agda files for -- SPEC: headers and extract metadata.
    Returns a dict mapping spec IDs to list of locations where they're found.
    """
    spec_pattern = re.compile(
        r'--\s*SPEC:\s*(SPEC-[A-Z]+-\d+)\s*\n'
        r'(?:--\s*TIER:\s*(\w+)\s*\n)?'
        r'(?:--\s*STATUS:\s*(\w+)\s*\n)?'
        r'(?:--\s*SAFETY:\s*(\w+)\s*\n)?'
    )

    results = defaultdict(list)

    if not AGDA_ROOT.exists():
        print(f"Warning: Agda root not found at {AGDA_ROOT}")
        return results

    for agda_file in AGDA_ROOT.rglob("*.agda"):
        try:
            content = agda_file.read_text(encoding='utf-8')
            relative_path = agda_file.relative_to(AGDA_ROOT)

            for match in spec_pattern.finditer(content):
                spec_id = match.group(1)
                tier = match.group(2)
                status = match.group(3)
                safety = match.group(4)

                # Find the lemma name (next non-comment line after header)
                pos = match.end()
                remaining = content[pos:]
                lines = remaining.split('\n')
                lemma_name = None
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('--'):
                        # Extract function/lemma name
                        name_match = re.match(r'^([a-zA-Z_≈⊓⊔≤][a-zA-Z0-9_≈⊓⊔≤ʳᶜˢ\-]*)', line)
                        if name_match:
                            lemma_name = name_match.group(1)
                        break

                results[spec_id].append({
                    'file': str(relative_path),
                    'tier': tier,
                    'status': status,
                    'safety': safety,
                    'lemma': lemma_name
                })
                debug(f"Found SPEC {spec_id} in {relative_path}: {lemma_name}")
        except Exception as e:
            print(f"Warning: Error parsing {agda_file}: {e}")

    return results


def parse_agda_postulates() -> Dict[str, List[str]]:
    """
    Scan Agda files for postulate blocks.
    Returns a dict mapping file paths to list of postulated names.
    """
    results = defaultdict(list)

    if not AGDA_ROOT.exists():
        return results

    # Pattern to find postulate blocks
    postulate_pattern = re.compile(
        r'postulate\s*\n((?:\s+[^\n]+\n)*)',
        re.MULTILINE
    )
    # Pattern to extract names from postulate block
    name_pattern = re.compile(r'^\s+([a-zA-Z_][a-zA-Z0-9_\-\']*)\s*:', re.MULTILINE)

    for agda_file in AGDA_ROOT.rglob("*.agda"):
        try:
            content = agda_file.read_text(encoding='utf-8')
            relative_path = str(agda_file.relative_to(AGDA_ROOT))

            for match in postulate_pattern.finditer(content):
                block = match.group(1)
                for name_match in name_pattern.finditer(block):
                    name = name_match.group(1)
                    results[relative_path].append(name)
                    debug(f"Found postulate {name} in {relative_path}")
        except Exception as e:
            debug(f"Error scanning postulates in {agda_file}: {e}")

    return results


def preprocess_obsidian_frontmatter(text: str) -> str:
    """
    Pre-process Obsidian frontmatter to make it valid YAML.
    Handles [[wikilink]] syntax in values by quoting them.
    """
    lines = text.split('\n')
    processed = []
    for line in lines:
        # If line contains [[...]] patterns (Obsidian links), quote the value
        if '[[' in line and ':' in line:
            # Split on first colon
            colon_pos = line.index(':')
            key = line[:colon_pos]
            value = line[colon_pos + 1:].strip()
            # Only quote if not already quoted
            if value and not (value.startswith('"') or value.startswith("'")):
                # Use double quotes and escape any internal double quotes
                value = value.replace('"', '\\"')
                line = f'{key}: "{value}"'
        processed.append(line)
    return '\n'.join(processed)


def parse_vault_notes() -> Dict[str, Dict[str, Any]]:
    """
    Scan Vault for canonical notes and extract frontmatter.
    Returns a dict mapping note paths to their metadata.
    """
    results = {}

    if not VAULT_ROOT.exists():
        print(f"Warning: Vault root not found at {VAULT_ROOT}")
        return results

    debug(f"Scanning Vault at: {VAULT_ROOT}")

    # More robust frontmatter pattern - handles various edge cases
    frontmatter_pattern = re.compile(r'^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n', re.DOTALL)

    file_count = 0
    for md_file in VAULT_ROOT.rglob("*.md"):
        file_count += 1
        # Skip inbox drafts, templates, and hidden directories
        relative_path = md_file.relative_to(VAULT_ROOT)
        path_str = str(relative_path)

        # Skip patterns
        if any(part.startswith('_') or part.startswith('.') for part in relative_path.parts):
            debug(f"Skipping (hidden/template): {path_str}")
            continue
        if path_str.startswith("00_inbox/drafts"):
            debug(f"Skipping (draft): {path_str}")
            continue

        try:
            content = md_file.read_text(encoding='utf-8')
            debug(f"Reading: {path_str} ({len(content)} chars)")

            match = frontmatter_pattern.match(content)
            if match:
                frontmatter_text = match.group(1)
                # Pre-process to handle Obsidian [[link]] syntax
                frontmatter_text = preprocess_obsidian_frontmatter(frontmatter_text)
                debug(f"  Frontmatter found: {frontmatter_text[:100]}...")
                try:
                    frontmatter = yaml.safe_load(frontmatter_text)
                    if frontmatter:
                        maturity = frontmatter.get('maturity')
                        debug(f"  maturity={maturity}")
                        if maturity == 'canonical':
                            results[path_str] = {
                                'title': frontmatter.get('title', md_file.stem),
                                'type': frontmatter.get('type'),
                                'maturity': maturity,
                                'related': frontmatter.get('related', []),
                                'updated': frontmatter.get('updated'),
                                'spec_links': frontmatter.get('spec_links', [])
                            }
                            debug(f"  -> CANONICAL: {frontmatter.get('title')}")
                except yaml.YAMLError as e:
                    debug(f"  YAML error: {e}")
            else:
                debug(f"  No frontmatter match")
        except Exception as e:
            print(f"Warning: Error parsing {md_file}: {e}")

    debug(f"Scanned {file_count} files, found {len(results)} canonical notes")
    return results


def analyze_drift(registry: List[Dict], agda_specs: Dict, vault_notes: Dict,
                  postulates: Dict[str, List[str]]) -> Dict[str, List]:
    """
    Analyze drift between registry, Agda, and Vault.
    Returns categorized issues.

    Uses new claim/proof schema:
    - claim: what the spec asserts (theorem | conjecture | definition | bridge | theory-only)
    - proof: what Agda has done (verified | conjecture | refuted | n/a)

    Severity rules:

    RED (critical):
    - claim: theorem + proof: refuted (theory contradicted)
    - claim: theorem + proof: n/a (theorem needs proof)

    YELLOW (warning):
    - claim: theorem + proof: conjecture (work in progress)
    - T1 + claim: conjecture (foundational tier needs certainty)
    - mapping.relation: different WITHOUT (claim: bridge/theory-only OR gap.owner: intentional)
    - mapping.relation: weakened (structural debt)

    GREEN (aligned):
    - claim: theorem + proof: verified
    - claim: conjecture + proof: conjecture (aligned uncertainty)
    - claim: definition + proof: verified/n/a
    - claim: bridge (any proof) - documented translation
    - claim: theory-only (proof: n/a) - intentionally non-formal
    - gap.owner: intentional - documented exception
    """
    issues = {
        'red': [],           # Critical: theorem needs proof or is refuted
        'yellow': [],        # Warning: work in progress or structural debt
        'green': [],         # Aligned or intentional
        'stale': [],         # Last reviewed > 90 days
        'missing_agda': [],  # Specs with no Agda pointer
        'orphan_agda': [],   # Agda SPEC headers with no registry entry
        'orphan_vault': [],  # Canonical notes with no spec linkage
        'new_knowledge': [], # Agda proved something stronger
        'postulates': []     # "Verified" claims that are actually postulates
    }

    registered_ids = {spec['id'] for spec in registry}
    agda_spec_ids = set(agda_specs.keys())

    # Build set of all postulate names for quick lookup
    all_postulates = set()
    for names in postulates.values():
        all_postulates.update(names)

    # Check each registry entry
    for spec in registry:
        spec_id = spec['id']
        tier = spec.get('tier', 'T2')

        # New schema: claim + proof (fall back to old status field for compatibility)
        claim = spec.get('claim', spec.get('status', ''))
        proof = spec.get('proof', '')

        # Legacy support: if proof not set, derive from agda.status
        if not proof:
            agda = spec.get('agda', {})
            agda_status = agda.get('status', 'missing')
            if agda_status == 'verified':
                proof = 'verified'
            elif agda_status == 'conjecture':
                proof = 'conjecture'
            elif agda_status == 'refuted':
                proof = 'refuted'
            else:
                proof = 'n/a'

        theory = spec.get('theory', {})
        agda = spec.get('agda', {})
        mapping = spec.get('mapping', {})
        gap = spec.get('gap', {})

        # Check if "verified" claim is actually a postulate
        agda_pointer = agda.get('pointer', '')
        if proof == 'verified' and agda_pointer:
            lemma_name = agda_pointer.split('.')[-1] if agda_pointer else ''
            if lemma_name in all_postulates:
                issues['postulates'].append({
                    'id': spec_id,
                    'title': spec.get('title'),
                    'pointer': agda_pointer,
                    'issue': 'Marked as verified but is actually a postulate'
                })

        # Severity classification using claim/proof
        gap_owner = gap.get('owner', 'unknown')
        mapping_relation = mapping.get('relation', '')
        design_decision = spec.get('design_decision', 'n/a')

        # Track if we've classified this spec
        classified = False

        # === DESIGN DECISION (check first - always surfaces as YELLOW) ===

        # design_decision: required always YELLOW
        if design_decision == 'required':
            issues['yellow'].append({
                'id': spec_id,
                'title': spec.get('title'),
                'claim': claim,
                'proof': proof,
                'issue': 'Design decision required',
                'owner': gap_owner,
                'action': gap.get('action', 'Resolve design fork')
            })
            classified = True

        # === GREEN conditions (check after design_decision) ===

        # Intentional gaps are GREEN
        elif gap_owner == 'intentional':
            issues['green'].append({
                'id': spec_id,
                'title': spec.get('title'),
                'reason': 'Intentional gap (documented exception)'
            })
            classified = True

        # bridge and theory-only claims are GREEN (explicitly non-formal)
        elif claim in ['theory-only', 'bridge']:
            issues['green'].append({
                'id': spec_id,
                'title': spec.get('title'),
                'reason': f'Claim is {claim} (no Agda required)'
            })
            classified = True

        # === RED conditions ===

        # RED: claim: theorem + proof: refuted
        elif claim == 'theorem' and proof == 'refuted':
            issues['red'].append({
                'id': spec_id,
                'title': spec.get('title'),
                'claim': claim,
                'proof': proof,
                'issue': f"Theorem is refuted by Agda",
                'owner': gap_owner,
                'action': gap.get('action', 'Update theory to match Agda')
            })
            classified = True

        # RED: claim: theorem + proof: n/a (theorem needs proof)
        elif claim == 'theorem' and proof == 'n/a':
            issues['red'].append({
                'id': spec_id,
                'title': spec.get('title'),
                'claim': claim,
                'proof': proof,
                'issue': f"Theorem has no Agda proof",
                'owner': gap_owner,
                'action': gap.get('action', 'Add Agda proof')
            })
            classified = True

        # === YELLOW conditions ===

        # YELLOW: claim: theorem + proof: conjecture (work in progress)
        elif claim == 'theorem' and proof == 'conjecture':
            issues['yellow'].append({
                'id': spec_id,
                'title': spec.get('title'),
                'claim': claim,
                'proof': proof,
                'mapping': mapping_relation,
                'issue': f"Theorem is conjecture in Agda (WIP)",
                'rationale': mapping.get('rationale', ''),
                'owner': gap_owner
            })
            classified = True

        # YELLOW: T1 + claim: conjecture (foundational tier needs certainty)
        elif tier == 'T1' and claim == 'conjecture':
            issues['yellow'].append({
                'id': spec_id,
                'title': spec.get('title'),
                'claim': claim,
                'proof': proof,
                'mapping': mapping_relation,
                'issue': f"T1 conjecture (foundational tier should have certainty)",
                'rationale': mapping.get('rationale', ''),
                'owner': gap_owner
            })
            classified = True

        # YELLOW: Mapping is 'different' without explicit exception
        # Rationale: 'different' means theory and Agda express distinct formalizations -
        # this is structural debt unless explicitly documented as bridge or theory-only
        elif mapping_relation == 'different':
            issues['yellow'].append({
                'id': spec_id,
                'title': spec.get('title'),
                'claim': claim,
                'proof': proof,
                'mapping': mapping_relation,
                'issue': f"Mapping relation is 'different' (structural debt)",
                'rationale': mapping.get('rationale', 'No rationale provided'),
                'owner': gap_owner
            })
            classified = True

        # YELLOW: Mapping is 'weakened' (Agda proves less than theory claims)
        elif mapping_relation == 'weakened':
            issues['yellow'].append({
                'id': spec_id,
                'title': spec.get('title'),
                'claim': claim,
                'proof': proof,
                'mapping': mapping_relation,
                'issue': f"Mapping relation is 'weakened' (Agda proves less than theory)",
                'rationale': mapping.get('rationale', 'No rationale provided'),
                'owner': gap_owner
            })
            classified = True

        # === GREEN (default for aligned specs) ===

        # GREEN: claim: theorem + proof: verified
        elif not classified:
            if claim == 'theorem' and proof == 'verified' and mapping_relation in ['exact', 'strengthened', '']:
                issues['green'].append({
                    'id': spec_id,
                    'title': spec.get('title'),
                    'reason': 'Theorem verified with aligned mapping'
                })
            elif claim == 'definition' and proof in ['verified', 'n/a']:
                # Definitions don't require Agda verification if intentional
                issues['green'].append({
                    'id': spec_id,
                    'title': spec.get('title'),
                    'reason': 'Definition (type alignment or intentionally non-formal)'
                })
            elif claim == 'conjecture' and proof == 'conjecture':
                # Both sides agree it's unproven - aligned state
                issues['green'].append({
                    'id': spec_id,
                    'title': spec.get('title'),
                    'reason': 'Conjecture in both layers (aligned uncertainty)'
                })

        # NEW KNOWLEDGE: Agda proved something stronger
        if mapping.get('relation') == 'strengthened':
            issues['new_knowledge'].append({
                'id': spec_id,
                'title': spec.get('title'),
                'agda_pointer': agda.get('pointer'),
                'rationale': mapping.get('rationale', '')
            })

        # STALE: Last reviewed > 90 days
        last_reviewed = theory.get('last_reviewed')
        if last_reviewed:
            try:
                review_date = datetime.strptime(str(last_reviewed), '%Y-%m-%d')
                if datetime.now() - review_date > timedelta(days=90):
                    issues['stale'].append({
                        'id': spec_id,
                        'title': spec.get('title'),
                        'last_reviewed': str(last_reviewed),
                        'days_ago': (datetime.now() - review_date).days
                    })
            except ValueError:
                pass

        # MISSING AGDA: No Agda pointer (for theorems and definitions that need verification)
        if not agda.get('pointer') and claim in ['theorem', 'definition'] and proof not in ['verified', 'n/a']:
            issues['missing_agda'].append({
                'id': spec_id,
                'title': spec.get('title'),
                'tier': spec.get('tier'),
                'gap_owner': gap_owner
            })
        elif proof in ['conjecture', 'n/a'] and claim == 'theorem':
            issues['missing_agda'].append({
                'id': spec_id,
                'title': spec.get('title'),
                'tier': spec.get('tier'),
                'gap_owner': gap_owner
            })

    # ORPHAN AGDA: Specs in Agda but not in registry
    for spec_id in agda_spec_ids:
        if spec_id not in registered_ids:
            locations = agda_specs[spec_id]
            issues['orphan_agda'].append({
                'id': spec_id,
                'locations': [f"{loc['file']}:{loc['lemma']}" for loc in locations]
            })

    # ORPHAN VAULT: Canonical notes not linked to any spec
    # Build set of referenced note paths from registry
    referenced_notes = set()
    for spec in registry:
        notes_ref = spec.get('theory', {}).get('notes_ref', '')
        if notes_ref:
            referenced_notes.add(notes_ref)

    for note_path, note_data in vault_notes.items():
        if note_path not in referenced_notes:
            issues['orphan_vault'].append({
                'path': note_path,
                'title': note_data.get('title', note_path),
                'type': note_data.get('type')
            })

    return issues


def generate_report(registry: List[Dict], agda_specs: Dict, vault_notes: Dict,
                    issues: Dict, postulates: Dict[str, List[str]]) -> str:
    """Generate the AUDIT_REPORT.md content."""
    lines = []
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Header
    lines.append("# Symbolics Compatibility Audit Report")
    lines.append(f"\n**Generated:** {now}")
    lines.append("")

    # Summary Statistics
    lines.append("## Summary Statistics")
    lines.append("")

    total_specs = len(registry)
    tier_counts = defaultdict(int)
    agda_coverage = 0
    theory_coverage = 0

    for spec in registry:
        tier_counts[spec.get('tier', 'unknown')] += 1
        if spec.get('agda', {}).get('status') == 'verified':
            agda_coverage += 1
        if spec.get('theory', {}).get('notes_ref'):
            theory_coverage += 1

    lines.append("| Metric | Count |")
    lines.append("|--------|-------|")
    lines.append(f"| Total Specs | {total_specs} |")
    for tier in sorted(tier_counts.keys()):
        lines.append(f"| {tier} Specs | {tier_counts[tier]} |")
    lines.append(f"| Agda Verified | {agda_coverage} ({100*agda_coverage//max(total_specs,1)}%) |")
    lines.append(f"| Theory Referenced | {theory_coverage} ({100*theory_coverage//max(total_specs,1)}%) |")
    lines.append(f"| Canonical Vault Notes | {len(vault_notes)} |")
    lines.append(f"| Agda SPEC Headers Found | {len(agda_specs)} unique IDs |")
    lines.append(f"| GREEN (aligned) | {len(issues['green'])} |")
    lines.append(f"| YELLOW (warnings) | {len(issues['yellow'])} |")
    lines.append(f"| RED (critical) | {len(issues['red'])} |")
    lines.append("")

    # Canonical Vault Notes Section
    lines.append("## Canonical Vault Notes")
    lines.append("")
    if vault_notes:
        lines.append("| Path | Title | Type |")
        lines.append("|------|-------|------|")
        for path, data in sorted(vault_notes.items()):
            lines.append(f"| {path} | {data.get('title', '-')} | {data.get('type', '-')} |")
        lines.append("")
    else:
        lines.append("*No canonical vault notes found.*")
        lines.append("")

    # Drift Report
    lines.append("## Drift Report")
    lines.append("")

    # RED items
    lines.append("### Critical (RED)")
    lines.append("")
    if issues['red']:
        lines.append("These specs have theory claiming theorem but Agda status is missing or refuted.")
        lines.append("")
        lines.append("| Spec ID | Title | Issue | Owner | Action |")
        lines.append("|---------|-------|-------|-------|--------|")
        for item in issues['red']:
            action = item.get('action', '').replace('\n', ' ')[:50]
            lines.append(f"| {item['id']} | {item['title']} | {item['issue']} | {item['owner']} | {action} |")
        lines.append("")
    else:
        lines.append("No critical issues found.")
        lines.append("")

    # YELLOW items
    lines.append("### Warnings (YELLOW)")
    lines.append("")
    if issues['yellow']:
        lines.append("These specs have theorem+conjecture status (WIP) or mapping issues.")
        lines.append("")
        lines.append("| Spec ID | Title | Issue | Owner |")
        lines.append("|---------|-------|-------|-------|")
        for item in issues['yellow']:
            lines.append(f"| {item['id']} | {item['title']} | {item['issue']} | {item['owner']} |")
        lines.append("")
    else:
        lines.append("No warnings found.")
        lines.append("")

    # Postulates
    if issues['postulates']:
        lines.append("### Postulate Warnings")
        lines.append("")
        lines.append("These specs are marked as 'verified' but the Agda implementation uses postulates.")
        lines.append("")
        lines.append("| Spec ID | Title | Pointer |")
        lines.append("|---------|-------|---------|")
        for item in issues['postulates']:
            lines.append(f"| {item['id']} | {item['title']} | {item['pointer']} |")
        lines.append("")

    # New Knowledge
    if issues['new_knowledge']:
        lines.append("## New Knowledge from Agda")
        lines.append("")
        lines.append("These specs have strengthened mappings where Agda proved something sharper than theory claimed.")
        lines.append("")
        for item in issues['new_knowledge']:
            lines.append(f"- **{item['id']}** ({item['title']}): {item.get('rationale', 'See Agda pointer')}")
        lines.append("")

    # Stale Entries
    if issues['stale']:
        lines.append("## Stale Entries")
        lines.append("")
        lines.append("These specs have not been reviewed in over 90 days.")
        lines.append("")
        lines.append("| Spec ID | Title | Last Reviewed | Days Ago |")
        lines.append("|---------|-------|---------------|----------|")
        for item in issues['stale']:
            lines.append(f"| {item['id']} | {item['title']} | {item['last_reviewed']} | {item['days_ago']} |")
        lines.append("")

    # Missing Mappings
    lines.append("## Missing Mappings")
    lines.append("")

    if issues['missing_agda']:
        # Filter to show only non-intentional missing
        non_intentional = [i for i in issues['missing_agda'] if i.get('gap_owner') != 'intentional']
        intentional = [i for i in issues['missing_agda'] if i.get('gap_owner') == 'intentional']

        if non_intentional:
            lines.append("### Specs Without Agda Verification (Needs Work)")
            lines.append("")
            lines.append("| Spec ID | Title | Tier | Owner |")
            lines.append("|---------|-------|------|-------|")
            for item in non_intentional:
                lines.append(f"| {item['id']} | {item['title']} | {item['tier']} | {item.get('gap_owner', '-')} |")
            lines.append("")

        if intentional:
            lines.append("### Specs Without Agda Verification (Intentional)")
            lines.append("")
            lines.append("| Spec ID | Title | Tier |")
            lines.append("|---------|-------|------|")
            for item in intentional:
                lines.append(f"| {item['id']} | {item['title']} | {item['tier']} |")
            lines.append("")

    if issues['orphan_agda']:
        lines.append("### Orphan Agda SPEC Headers")
        lines.append("")
        lines.append("These Agda files have SPEC headers pointing to non-existent registry entries.")
        lines.append("")
        for item in issues['orphan_agda']:
            lines.append(f"- **{item['id']}**: {', '.join(item['locations'])}")
        lines.append("")

    if issues['orphan_vault']:
        lines.append("### Orphan Canonical Notes")
        lines.append("")
        lines.append("These canonical Vault notes are not linked to any registry spec.")
        lines.append("")
        lines.append("| Path | Title | Type |")
        lines.append("|------|-------|------|")
        for item in issues['orphan_vault']:
            lines.append(f"| {item['path']} | {item['title']} | {item.get('type', '-')} |")
        lines.append("")

    # Task List
    lines.append("## Task List")
    lines.append("")
    lines.append("Priority actions based on this audit:")
    lines.append("")

    task_num = 1
    for item in issues['red']:
        action = item.get('action', 'Investigate').replace('\n', ' ')[:80]
        lines.append(f"{task_num}. **[{item['owner'].upper()}]** {action} ({item['id']})")
        task_num += 1

    for item in issues['yellow'][:5]:  # Top 5 warnings
        lines.append(f"{task_num}. **[{item['owner'].upper()}]** Address '{item['issue']}' for {item['id']}")
        task_num += 1

    if issues['postulates']:
        lines.append(f"{task_num}. **[AGDA]** Review {len(issues['postulates'])} specs marked verified but using postulates")
        task_num += 1

    if not issues['red'] and not issues['yellow'] and not issues['postulates']:
        lines.append("No immediate actions required. System is in good alignment.")

    lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("*This report was generated by `scripts/audit.py`. Do not edit manually.*")

    return '\n'.join(lines)


def main():
    """Main entry point."""
    print("Symbolics Compatibility Audit")
    print("=" * 40)

    if DEBUG:
        print("DEBUG mode enabled")

    # Load data sources
    print("Loading registry...")
    registry = load_registry()
    print(f"  Found {len(registry)} specs")

    print("Scanning Agda for SPEC headers...")
    agda_specs = parse_agda_spec_headers()
    print(f"  Found {len(agda_specs)} unique SPEC IDs")

    print("Scanning Agda for postulates...")
    postulates = parse_agda_postulates()
    total_postulates = sum(len(v) for v in postulates.values())
    print(f"  Found {total_postulates} postulates in {len(postulates)} files")

    print("Scanning Vault for canonical notes...")
    vault_notes = parse_vault_notes()
    print(f"  Found {len(vault_notes)} canonical notes")

    # Analyze drift
    print("Analyzing drift...")
    issues = analyze_drift(registry, agda_specs, vault_notes, postulates)

    # Summary
    print("\nDrift Summary:")
    print(f"  GREEN (aligned):    {len(issues['green'])}")
    print(f"  YELLOW (warning):   {len(issues['yellow'])}")
    print(f"  RED (critical):     {len(issues['red'])}")
    print(f"  Postulate issues:   {len(issues['postulates'])}")
    print(f"  Stale entries:      {len(issues['stale'])}")
    print(f"  Missing Agda:       {len(issues['missing_agda'])}")
    print(f"  Orphan Agda:        {len(issues['orphan_agda'])}")
    print(f"  Orphan Vault:       {len(issues['orphan_vault'])}")
    print(f"  New knowledge:      {len(issues['new_knowledge'])}")

    # Generate report
    print("\nGenerating report...")
    report = generate_report(registry, agda_specs, vault_notes, issues, postulates)

    REPORT_PATH.write_text(report, encoding='utf-8')
    print(f"Report written to {REPORT_PATH}")

    # Exit code based on critical issues
    if issues['red']:
        print(f"\n!! {len(issues['red'])} critical issues found!")
        return 1
    elif issues['yellow']:
        print(f"\n! {len(issues['yellow'])} warnings found (no critical issues)")
        return 0
    else:
        print("\n OK - No critical issues. System is aligned.")
        return 0


if __name__ == '__main__':
    exit(main())
