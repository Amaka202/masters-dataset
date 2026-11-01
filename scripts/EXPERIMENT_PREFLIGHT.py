"""Own training-only size/status preflight; never execute retained dataset programs."""
import argparse
from collections import Counter
import json

import CATEGORY_AUDIT_CONSOLIDATE as consolidation


PROPOSED_CODE_BYTES = 16_384
OUTPUT = 'EXPERIMENT_ELIGIBILITY_PREFLIGHT.json'


def preflight():
    audit = consolidation.audit
    train, families, events, latest = consolidation.training_inputs()
    reviews, active = consolidation.case_reviews(train, families, events, latest)
    assert reviews['remaining_candidates'] == 0 and set(active) == set(train)
    rows = []
    for pid in sorted(train):
        pair, review = train[pid], active[pid]
        assert pair['split'] == 'train'
        before_size = len(pair['before'].encode('utf-8'))
        after_size = len(pair['after'].encode('utf-8'))
        rows.append(dict(
            pair_id=pid, split='train',
            before_utf8_bytes=before_size, after_utf8_bytes=after_size,
            before_fits_proposed_cap=before_size <= PROPOSED_CODE_BYTES,
            both_versions_fit_proposed_cap=max(before_size, after_size) <= PROPOSED_CODE_BYTES,
            current_assistant_proposal=review['experimental_subset_proposal'],
            priority_gate_review=review['experimental_subset_proposal'] == 'conditional_retain',
            decision_status='not_case_approved', ready_for_experiment=False,
            source_batch_file=review['source_batch_file'],
            source_review_revision=review['review_revision'],
            inspected_code_sha256=review['inspected_code_sha256'],
            mechanical_family_id=families[pid], independently_adjudicated_issue_id=None))
    sources = ['EXPERIMENT_PREFLIGHT.py', 'EXPERIMENT_PROTOCOL_DRAFT.md',
               'EXPERIMENT_SELECTION_DECISIONS.md', 'CATEGORY_AUDIT_CONSOLIDATION_MANIFEST.json',
               'CATEGORY_AUDIT_CONSOLIDATION_CASE_REVIEWS.json',
               'HAPY_CVEFIXES_ADMITTED_TRAIN_CANDIDATES.jsonl']
    return dict(
        schema_version='1', scope='training_only', status='mechanical_preflight_not_eligibility_adjudication',
        protocol_status='draft_not_frozen', proposed_code_cap_utf8_bytes=PROPOSED_CODE_BYTES,
        input_policy='Whole function only; no truncation or selective caller context.',
        training_candidates=len(rows),
        before_fits_proposed_cap=sum(r['before_fits_proposed_cap'] for r in rows),
        before_exceeds_proposed_cap=sum(not r['before_fits_proposed_cap'] for r in rows),
        both_versions_fit_proposed_cap=sum(r['both_versions_fit_proposed_cap'] for r in rows),
        maximum_before_utf8_bytes=max(r['before_utf8_bytes'] for r in rows),
        proposal_counts=dict(sorted(Counter(r['current_assistant_proposal'] for r in rows).items())),
        priority_gate_review_ids=[r['pair_id'] for r in rows if r['priority_gate_review']],
        approved_cases_in_this_preflight=0,
        limitation='Size/status bookkeeping cannot establish observability, labels, a valid negative, '
                   'independent roots or dataset adequacy. No held-out substantive review, target execution, '
                   'model calls or automatic case promotion. Original bytes/splits and proposals preserved.',
        source_sha256={name: audit.file_sha(audit.ROOT/name) for name in sources}, rows=rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'check'])
    args = parser.parse_args()
    result = preflight()
    text = json.dumps(result, indent=2, ensure_ascii=False)+'\n'
    path = consolidation.audit.ROOT/OUTPUT
    if args.command == 'check':
        assert path.read_bytes() == text.encode(), 'Stale preflight; rebuild against current source/protocol.'
    else:
        path.write_text(text, encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('rows', 'source_sha256')}, indent=2))
