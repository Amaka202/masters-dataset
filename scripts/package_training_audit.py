"""Select the explicit, hash-bound training audit without modifying source artefacts."""
import hashlib
import json
from pathlib import Path


MANIFEST = 'CATEGORY_AUDIT_CONSOLIDATION_MANIFEST.json'
EXTRAS = (
    'CATEGORY_AUDIT_CONSOLIDATION_BATCH_PLAN_051_059.json',
    'CATEGORY_AUDIT_PROTOCOL.md', 'CATEGORY_AUDIT_COUNTS.csv', 'CATEGORY_AUDIT_PROGRESS.md',
    'EXPERIMENT_PREFLIGHT.py', 'EXPERIMENT_ELIGIBILITY_PREFLIGHT.json',
)


def checked_source(source, name, expected=None):
    if Path(name).name != name or name in ('', '.', '..'):
        raise ValueError(f'Invalid audit source name: {name}')
    raw = (source/name).read_bytes()
    if expected is not None and hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError(f'Audit source digest mismatch: {name}')
    return raw


def audit_files(source):
    path = source/MANIFEST
    if not path.exists():
        return set(), None
    manifest = json.loads(checked_source(source, MANIFEST))
    assert manifest['scope'] == 'training_only'
    assert manifest['training_candidates'] == manifest['consolidation_reviewed_candidates'] == 742
    assert manifest['researcher_approval_ready'] is False
    for collection in ('source_sha256', 'output_sha256'):
        for name, digest in manifest[collection].items():
            checked_source(source, name, digest)
    names = set(manifest['source_sha256']) | set(manifest['output_sha256']) | {MANIFEST} | set(EXTRAS)
    for name in names:
        checked_source(source, name)
    preflight = json.loads(checked_source(source, 'EXPERIMENT_ELIGIBILITY_PREFLIGHT.json'))
    assert preflight['scope'] == 'training_only' and preflight['training_candidates'] == 742
    assert preflight['approved_cases_in_this_preflight'] == 0
    assert all(row['split'] == 'train' and row['ready_for_experiment'] is False
               for row in preflight['rows'])
    for name, digest in preflight['source_sha256'].items():
        checked_source(source, name, digest)
    return names, dict(
        documentation_update_date='2026-11-01', training_reviewed=742,
        training_remaining=0, policy_status='student_selection_principles_approved',
        case_status='assistant_proposals_not_case_approved',
        experiment_protocol_status='draft_not_frozen',
        source_manifest_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        limitation='Complete registered training consolidation audit/provenance and mechanical preflight; '
                   'not a frozen experimental subset or independently adjudicated gold labels.')
