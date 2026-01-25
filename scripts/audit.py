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


def load_registry() -> List[Dict[str, Any]]:
    """Load the spec registry YAML file."""
    if not REGISTRY_PATH.exists():
        print(f"Warning: Registry not found at {REGISTRY_PATH}")
        return []

    with open(REGISTRY_PATH, 'r') as f:
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
            content = agda_file.read_text()
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
        except Exception as e:
            print(f"Warning: Error parsing {agda_file}: {e}")

    return results


def parse_vault_notes() -> Dict[str, Dict[str, Any]]:
    """
    Scan Vault for canonical notes and extract frontmatter.
    Returns a dict mapping note paths to their metadata.
    """
    results = {}

    if not VAULT_ROOT.exists():
        print(f"Warning: Vault root not found at {VAULT_ROOT}")
        return results

    frontmatter_pattern = re.compile(r'^---\s*\n(.*?)\n---', re.DOTALL)

    for md_file in VAULT_ROOT.rglob("*.md"):
        # Skip inbox drafts and templates
        relative_path = md_file.relative_to(VAULT_ROOT)
        path_str = str(relative_path)
        if path_str.startswith("00_inbox/drafts") or path_str.startswith("_"):
            continue

        try:
            content = md_file.read_text()
            match = frontmatter_pattern.match(content)
            if match:
                try:
                    frontmatter = yaml.safe_load(match.group(1))
                    if frontmatter and frontmatter.get('maturity') == 'canonical':
                        results[path_str] = {
                            'title': frontmatter.get('title', md_file.stem),
                            'type': frontmatter.get('type'),
                            'maturity': frontmatter.get('maturity'),
                            'related': frontmatter.get('related', []),
                            'updated': frontmatter.get('updated')
                        }
                except yaml.YAMLError:
                    pass
        except Exception as e:
            print(f"Warning: Error parsing {md_file}: {e}")

    return results


def analyze_drift(registry: List[Dict], agda_specs: Dict, vault_notes: Dict) -> Dict[str, List]:
    """
    Analyze drift between registry, Agda, and Vault.
    Returns categorized issues.
    """
    issues = {
        'red': [],      # Critical: theory claims theorem but Agda missing/conjecture
        'yellow': [],   # Warning: opportunity or needs attention
        'stale': [],    # Last reviewed > 90 days
        'missing_agda': [],  # Specs with no Agda pointer
        'orphan_agda': [],   # Agda SPEC headers with no registry entry
        'new_knowledge': []  # Agda proved something stronger
    }

    registered_ids = {spec['id'] for spec in registry}
    agda_spec_ids = set(agda_specs.keys())

    # Check each registry entry
    for spec in registry:
        spec_id = spec['id']
        theory = spec.get('theory', {})
        agda = spec.get('agda', {})
        mapping = spec.get('mapping', {})
        gap = spec.get('gap', {})

        # RED: Theory claims theorem but Agda missing/conjecture/refuted
        if theory.get('status') == 'theorem':
            if agda.get('status') in ['missing', 'conjecture']:
                issues['red'].append({
                    'id': spec_id,
                    'title': spec.get('title'),
                    'issue': f"Theory claims theorem but Agda is {agda.get('status')}",
                    'owner': gap.get('owner', 'unknown'),
                    'action': gap.get('action', 'Needs investigation')
                })
            elif agda.get('status') == 'refuted':
                issues['red'].append({
                    'id': spec_id,
                    'title': spec.get('title'),
                    'issue': "Theory claims theorem but Agda REFUTED it",
                    'owner': 'theory',
                    'action': 'Update theory to match Agda refutation'
                })

        # YELLOW: Mapping is different/weakened
        if mapping.get('relation') in ['different', 'weakened']:
            issues['yellow'].append({
                'id': spec_id,
                'title': spec.get('title'),
                'issue': f"Mapping relation is '{mapping.get('relation')}'",
                'rationale': mapping.get('rationale', 'No rationale provided'),
                'owner': gap.get('owner', 'unknown')
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

        # MISSING AGDA: No Agda pointer
        if not agda.get('pointer') or agda.get('status') == 'missing':
            issues['missing_agda'].append({
                'id': spec_id,
                'title': spec.get('title'),
                'tier': spec.get('tier')
            })

    # ORPHAN AGDA: Specs in Agda but not in registry
    for spec_id in agda_spec_ids:
        if spec_id not in registered_ids:
            locations = agda_specs[spec_id]
            issues['orphan_agda'].append({
                'id': spec_id,
                'locations': [f"{loc['file']}:{loc['lemma']}" for loc in locations]
            })

    return issues


def generate_report(registry: List[Dict], agda_specs: Dict, vault_notes: Dict, issues: Dict) -> str:
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

    lines.append(f"| Metric | Count |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total Specs | {total_specs} |")
    for tier in sorted(tier_counts.keys()):
        lines.append(f"| {tier} Specs | {tier_counts[tier]} |")
    lines.append(f"| Agda Verified | {agda_coverage} ({100*agda_coverage//max(total_specs,1)}%) |")
    lines.append(f"| Theory Referenced | {theory_coverage} ({100*theory_coverage//max(total_specs,1)}%) |")
    lines.append(f"| Canonical Vault Notes | {len(vault_notes)} |")
    lines.append(f"| Agda SPEC Headers Found | {len(agda_specs)} unique IDs |")
    lines.append("")

    # Drift Report
    lines.append("## Drift Report")
    lines.append("")

    # RED items
    if issues['red']:
        lines.append("### Critical (RED)")
        lines.append("")
        lines.append("| Spec ID | Title | Issue | Owner | Action |")
        lines.append("|---------|-------|-------|-------|--------|")
        for item in issues['red']:
            lines.append(f"| {item['id']} | {item['title']} | {item['issue']} | {item['owner']} | {item['action']} |")
        lines.append("")
    else:
        lines.append("### Critical (RED)")
        lines.append("")
        lines.append("No critical issues found.")
        lines.append("")

    # YELLOW items
    if issues['yellow']:
        lines.append("### Warnings (YELLOW)")
        lines.append("")
        lines.append("| Spec ID | Title | Issue | Owner |")
        lines.append("|---------|-------|-------|-------|")
        for item in issues['yellow']:
            lines.append(f"| {item['id']} | {item['title']} | {item['issue']} | {item['owner']} |")
        lines.append("")
    else:
        lines.append("### Warnings (YELLOW)")
        lines.append("")
        lines.append("No warnings found.")
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
        lines.append("### Specs Without Agda Verification")
        lines.append("")
        lines.append("| Spec ID | Title | Tier |")
        lines.append("|---------|-------|------|")
        for item in issues['missing_agda']:
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

    # Task List
    lines.append("## Task List")
    lines.append("")
    lines.append("Priority actions based on this audit:")
    lines.append("")

    task_num = 1
    for item in issues['red']:
        lines.append(f"{task_num}. **[{item['owner'].upper()}]** {item['action']} ({item['id']})")
        task_num += 1

    for item in issues['yellow'][:5]:  # Top 5 warnings
        lines.append(f"{task_num}. **[{item['owner'].upper()}]** Address '{item['issue']}' for {item['id']}")
        task_num += 1

    if not issues['red'] and not issues['yellow']:
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

    # Load data sources
    print("Loading registry...")
    registry = load_registry()
    print(f"  Found {len(registry)} specs")

    print("Scanning Agda for SPEC headers...")
    agda_specs = parse_agda_spec_headers()
    print(f"  Found {len(agda_specs)} unique SPEC IDs")

    print("Scanning Vault for canonical notes...")
    vault_notes = parse_vault_notes()
    print(f"  Found {len(vault_notes)} canonical notes")

    # Analyze drift
    print("Analyzing drift...")
    issues = analyze_drift(registry, agda_specs, vault_notes)

    # Summary
    print("\nDrift Summary:")
    print(f"  RED (critical):     {len(issues['red'])}")
    print(f"  YELLOW (warning):   {len(issues['yellow'])}")
    print(f"  Stale entries:      {len(issues['stale'])}")
    print(f"  Missing Agda:       {len(issues['missing_agda'])}")
    print(f"  Orphan Agda:        {len(issues['orphan_agda'])}")
    print(f"  New knowledge:      {len(issues['new_knowledge'])}")

    # Generate report
    print("\nGenerating report...")
    report = generate_report(registry, agda_specs, vault_notes, issues)

    REPORT_PATH.write_text(report)
    print(f"Report written to {REPORT_PATH}")

    # Exit code based on critical issues
    if issues['red']:
        print(f"\n⚠️  {len(issues['red'])} critical issues found!")
        return 1
    else:
        print("\n✓ No critical issues. System is aligned.")
        return 0


if __name__ == '__main__':
    exit(main())
