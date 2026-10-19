#!/usr/bin/env python3
"""Self-contained source-integrity and packaging validator for this skill."""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'SKILL.md'

# Explicit inventory is intentional; catches accidentally dropped references.
REQUIRED = [
  'README.md', 'SKILL.md',
  'references/human-ai-39.md', 'references/ai-patterns.md',
  'references/ai-test-cases.md', 'references/taste-v2-process.md',
  'references/decision-playbook.md', 'references/visual-craft.md',
  'references/implementation.md', 'references/review.md',
  'references/visual-evidence.md', 'references/sources.md',
  'templates/brief.md', 'templates/audit.md',
  'templates/handoff.md', 'templates/visual-direction.md',
  'templates/state-matrix.md', 'templates/qa-report.md',
  'scripts/static_check.py', 'scripts/validate_skill.py',
]


def validate():
    errors=[]
    for f in REQUIRED:
        if not (ROOT/f).is_file(): errors.append('missing required file: '+f)
    if not SKILL.is_file(): return errors
    s=SKILL.read_text(encoding='utf-8')
    if not s.startswith('---\n') or '\n---\n' not in s[4:]:
        errors.append('invalid YAML-like front matter')
    else:
        header=s.split('\n---\n',1)[0]
        for pat in (r'(?m)^name:\s+human-first-design\s*$',
                    r'(?m)^description:\s+>-?\s*$',
                    r'(?m)^\s+version:\s*["\']1\.1\.0["\']\s*$'):
            if not re.search(pat,header): errors.append('frontmatter mismatch: '+pat)
    # Check relative resource paths mentioned in markdown (with flexible punctuation).
    missing=set()
    for md in sorted(ROOT.rglob('*.md')):
        body=md.read_text(encoding='utf-8')
        matches=re.findall(r'(?<![\w/])((?:references|templates|examples|scripts)/[A-Za-z0-9_./-]+\.(?:md|py))',body)
        for ref in matches:
            if not (ROOT/ref).is_file(): missing.add((str(md.relative_to(ROOT)),ref))
    for source,ref in sorted(missing): errors.append(f'broken reference in {source}: {ref}')
    p=(ROOT/'references/human-ai-39.md').read_text(encoding='utf-8')
    nums=[int(n) for n in re.findall(r'^\|\s*(\d{1,2})\s*\|',p,re.M)]
    if nums != list(range(1,40)):
        errors.append(f'AI principle numbering wrong: expected 1..39, got {nums}')
    fixtures=(ROOT/'references/ai-test-cases.md').read_text(encoding='utf-8')
    for group,num in [('AI',8),('AG',6),('UI',5)]:
        found=[int(n) for n in re.findall(r'^\|\s*'+group+r'-(\d{2})\s*\|',fixtures,re.M)]
        if found != list(range(1,num+1)):
            errors.append(f'fixture set {group} incomplete: {found}')
    return errors

if __name__=='__main__':
    failures=validate()
    for e in failures: print('FAIL',e)
    if failures: sys.exit(1)
    print('PASS: frontmatter, inventory, internal references, 39 ordered AI principles, 19 QA fixtures')
