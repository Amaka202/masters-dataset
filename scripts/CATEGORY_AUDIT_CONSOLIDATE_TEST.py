"""Tests of own evidence/proposal validation; retained dataset source stays inert."""
from copy import deepcopy
import json
import unittest
from unittest.mock import patch

import CATEGORY_AUDIT_CONSOLIDATE as consolidation


class ConsolidationReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.train, cls.families, cls.events, cls.latest = consolidation.training_inputs()
        cls.batch_name = consolidation.REVIEW_BATCHES[0]
        cls.batch = consolidation.audit.load(cls.batch_name)

    def reviews(self, batch=None, latest=None, batch_name=None):
        load = consolidation.audit.load
        batch_name = self.batch_name if batch_name is None else batch_name
        with patch.object(consolidation.audit, 'load', side_effect=lambda name:
                          batch if batch is not None and name == batch_name else load(name)):
            return consolidation.case_reviews(self.train, self.families, self.events,
                                              self.latest if latest is None else latest)

    def test_current_proposals_and_verified_both_side_proofs(self):
        result, active = self.reviews()
        self.assertEqual(result['current_reviewed_candidates'], 742)
        self.assertEqual(result['remaining_candidates'], 0)
        self.assertEqual(result['proposal_counts'], {
            'conditional_retain': 6, 'defer_missing_context': 318,
            'defer_security_boundary': 80, 'defer_existing_contract': 80,
            'defer_selected_attribution': 134, 'propose_feature_exclusion': 25,
            'defer_task_scope': 4, 'defer_paired_negative': 70,
            'propose_nonrepair_exclusion': 25,
        })
        broad_categories = {'CORR-INCOMPLETE-CASE-HANDLING', 'CORR-STATE-TRANSITION',
                            'CORR-CONTEXT-PROPAGATION'}
        self.assertEqual(set(active), {pid for pid, event in self.latest.items()
                                       if event['category_id'] in broad_categories
                                         or self.train[pid]['repository'] in {
                                              'github.com/pandas-dev/pandas', 'github.com/keras-team/keras',
                                              'github.com/scrapy/scrapy', 'github.com/psf/black',
                                               'github.com/nitely/spirit', 'github.com/nvbn/thefuck',
                                                'github.com/matrix-org/synapse', 'github.com/ansible/ansible',
                                                 'github.com/pylons/waitress', 'github.com/unrud/radicale',
                                                  'github.com/openstack/glance', 'github.com/vyperlang/vyper',
                                                    'github.com/nautobot/nautobot',
                                                     'github.com/triaxtec/openapi-python-client',
                                                       'github.com/tlsfuzzer/tlslite-ng',
                                                        'github.com/openstack/nova',
                                                          'github.com/zulip/zulip',
                                                            'github.com/shuup/shuup',
                                                             'github.com/yt-dlp/yt-dlp',
                                                               'github.com/cookiecutter/cookiecutter',
                                                               'github.com/openstack/swift',
                                                               'github.com/rohe/pysaml2',
                                                                'github.com/matrix-org/sydent',
                                                                'github.com/pyload/pyload',
                                                                'github.com/executablebooks/markdown-it-py',
                                                                'github.com/langchain-ai/langchain',
                                                                 'github.com/tensorflow/tensorflow',
                                                                 'github.com/twisted/twisted',
                                                                 'github.com/saleor/saleor',
                                                                 'github.com/openstack/keystone',
                                                                  'github.com/openidc/pyoidc',
                                                                  'github.com/urllib3/urllib3',
                                                                  'github.com/solj/bcfg2',
                                                                  'github.com/openstack/swauth',
                                                                   'github.com/qutebrowser/qutebrowser',
                                                                   'github.com/canonical/cloud-init',
                                                                    'github.com/ikus060/rdiffweb',
                                                                    'github.com/mlflow/mlflow',
                                                                    'github.com/encode/starlette',
                                                                    'github.com/openstack/horizon',
                                                                     'github.com/open-mss/mss',
                                                                     'github.com/getsentry/sentry',
                                                                     'github.com/netease-youdao/qanything',
                                                                     'github.com/scipy/scipy',
                                                                     'github.com/canonical/operator',
                                                                     'github.com/codingjoe/django-s3file',
                                                                     'github.com/encode/django-rest-framework',
                                                                     'github.com/felixschwarz/mjml-python',
                                                                      'github.com/gerapy/gerapy',
                                                                      'github.com/jdennis/keycloak-httpd-client-install',
                                                                      'github.com/pinterest/querybook',
                                                                      'github.com/spiral-project/ihatemoney',
                                                                      'github.com/zenml-io/zenml',
                                                                       'github.com/zopefoundation/zope',
                                                                       'github.com/nyuccl/psiturk',
                                                                       'gitlab.com/mayan-edms/mayan-edms',
                                                                       'github.com/aaugustin/websockets',
                                                                       'github.com/askbot/askbot-devel',
                                                                       'github.com/bbengfort/confire',
                                                                       'github.com/bit-team/backintime',
                                                                       'github.com/bmaltais/kohya_ss',
                                                                       'github.com/cvandeplas/pystemon',
                                                                       'github.com/django-wiki/django-wiki',
                                                                       'github.com/goauthentik/authentik',
                                                                       'github.com/horazont/xmpp-http-upload',
                                                                       'github.com/inveniosoftware/invenio-drafts-resources',
                                                                       'github.com/john5223/bottle-auth',
                                                                       'github.com/jupyter/jupyter_core',
                                                                       'github.com/jupyter/notebook',
                                                                       'github.com/jupyterhub/oauthenticator',
                                                                       'github.com/kozea/cairosvg',
                                                                       'github.com/lxml/lxml',
                                                                       'github.com/mansuf/mangadex-downloader',
                                                                       'github.com/mindsdb/mindsdb',
                                                                       'github.com/miurahr/py7zr',
                                                                       'github.com/mnbikeways/database',
                                                                       'github.com/mongodb/mongo-python-driver',
                                                                       'github.com/mozilla/pollbot',
                                                                       'github.com/naparuba/shinken',
                                                                       'github.com/oppia/oppia',
                                                                        'github.com/peering-manager/peering-manager',
                                                                        'github.com/ractf/core',
                                                                        'github.com/rasahq/rasa',
                                                                        'github.com/pyeve/eve',
                                                                        'github.com/wichert/pyrad',
                                                                        'github.com/widgetti/solara',
                                                                        'github.com/pyca/cryptography',
                                                                        'github.com/sehmaschine/django-grappelli',
                                                                        'github.com/python-social-auth/social-app-django',
                                                                        'github.com/python/cpython',
                                                                        'github.com/python-discord/bot',
                                                                        'github.com/yogeshojha/rengine'}})
        self.assertEqual(sum(self.train[pid]['repository'] == 'github.com/pandas-dev/pandas'
                              for pid in active), 174)
        self.assertEqual(sum(self.train[pid]['repository'] == 'github.com/keras-team/keras'
                              for pid in active), 73)
        self.assertEqual(sum(self.train[pid]['repository'] == 'github.com/scrapy/scrapy'
                              for pid in active), 48)
        self.assertEqual(sum(self.train[pid]['repository'] == 'github.com/psf/black'
                              for pid in active), 50)
        self.assertEqual(sum(self.train[pid]['repository'] == 'github.com/nitely/spirit'
                              for pid in active), 29)
        self.assertEqual(sum(self.train[pid]['repository'] == 'github.com/nvbn/thefuck'
                               for pid in active), 30)
        self.assertEqual(sum(self.train[pid]['repository'] == 'github.com/matrix-org/synapse'
                                for pid in active), 21)
        self.assertEqual(sum(self.train[pid]['repository'] == 'github.com/ansible/ansible'
                                for pid in active), 25)
        self.assertEqual(sum(self.train[pid]['repository'] == 'github.com/pylons/waitress'
                                 for pid in active), 18)
        self.assertEqual(sum(self.train[pid]['repository'] == 'github.com/unrud/radicale'
                                 for pid in active), 17)
        self.assertEqual(sum(self.train[pid]['repository'] == 'github.com/openstack/glance'
                                  for pid in active), 16)
        self.assertEqual(sum(self.train[pid]['repository'] == 'github.com/vyperlang/vyper'
                                  for pid in active), 11)
        self.assertEqual(sum(self.train[pid]['repository'] == 'github.com/nautobot/nautobot'
                                   for pid in active), 9)
        self.assertEqual(sum(self.train[pid]['repository'] == 'github.com/triaxtec/openapi-python-client'
                                   for pid in active), 8)
        self.assertEqual(sum(self.train[pid]['repository'] == 'github.com/tlsfuzzer/tlslite-ng'
                                    for pid in active), 8)
        self.assertEqual(sum(self.train[pid]['repository'] == 'github.com/openstack/nova'
                                    for pid in active), 7)
        self.assertEqual(sum(self.train[pid]['repository'] == 'github.com/zulip/zulip'
                                     for pid in active), 7)
        self.assertEqual(sum(self.train[pid]['repository'] == 'github.com/shuup/shuup'
                                     for pid in active), 7)
        for record in active.values():
            self.assertEqual(record['researcher_status'], 'pending')
            self.assertIsNone(record['audited_independent_issue_count'])
            self.assertEqual(set(record['selected_source_proofs']), {'before', 'after'})

    def test_changed_ledger_checkpoint_is_rejected(self):
        batch = deepcopy(self.batch)
        batch['discovery_ledger_checkpoint']['sha256'] = '0'*64
        with self.assertRaisesRegex(AssertionError, 'checkpoint changed'):
            self.reviews(batch=batch)

    def test_nontraining_case_cannot_enter_the_review_batch(self):
        batch = deepcopy(self.batch)
        batch['reviews'][0]['pair_id'] = 'held-out-not-a-training-id'
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch)

    def test_missing_context_cannot_be_silently_promoted_to_retain(self):
        batch = deepcopy(self.batch)
        record = next(item for item in batch['reviews']
                      if item['function_only_context'] == 'requires_missing_project_contract')
        record['experimental_subset_proposal'] = 'conditional_retain'
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch)

    def test_later_discovery_revision_makes_old_proposal_stale(self):
        latest = deepcopy(self.latest)
        pid = self.batch['reviews'][0]['pair_id']
        latest[pid]['revision'] += 1
        result, active = self.reviews(latest=latest)
        self.assertEqual(result['stale_review_candidates'], [pid])
        self.assertNotIn(pid, active)
        self.assertEqual(result['current_reviewed_candidates'], 741)
        self.assertEqual(result['remaining_candidates'], 1)
        self.assertEqual(len(result['records']), 749)

    def test_mutable_issue_proofs_preserve_snapshot_limits(self):
        _, active = self.reviews()
        record = next(item for item in active.values() if 'bugs-in-py_ansible-15:' in item['pair_id'])
        proofs = [proof for proof in record['verified_evidence_anchors']
                  if proof.get('source_kind') == 'mutable_issue_body_snapshot']
        self.assertEqual(len(proofs), 2)
        for proof in proofs:
            self.assertEqual(proof['updated_at'], '2019-11-21T14:40:59Z')
            self.assertIn('not an immutable commit', proof['limitation'])
            self.assertEqual(len(proof['api_response_sha256']), 64)

    def test_issue_body_must_match_its_retained_api_response(self):
        name = 'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_003.json'
        evidence = deepcopy(consolidation.audit.load(name))
        source = next(item for item in evidence['sources'] if item['source_kind'] == 'mutable_issue_body_snapshot')
        api = json.loads(source['api_response_text'])
        api['body'] += ' changed reported body'
        source['api_response_text'] = json.dumps(api)
        source['api_response_sha256'] = consolidation.audit.sha(source['api_response_text'])
        load = consolidation.audit.load
        with patch.object(consolidation.audit, 'load', side_effect=lambda value:
                          evidence if value == name else load(value)):
            with self.assertRaises(AssertionError):
                consolidation.verify_supplemental_evidence()

    def test_discussion_proofs_keep_comment_and_pull_snapshot_qualifications(self):
        _, active = self.reviews()
        proofs = [proof for item in active.values() if 'bugs-in-py_cookiecutter-' in item['pair_id']
                  for proof in item['verified_evidence_anchors']
                  if proof.get('source_kind') == 'mutable_discussion_body_snapshot']
        self.assertEqual(len(proofs), 8)
        for proof in proofs:
            self.assertIn('not a prior contract', proof['limitation'])
            self.assertEqual(proof['collected'], '2026-10-25')
            self.assertTrue(proof['html_url'].startswith('https://github.com/cookiecutter/cookiecutter/'))
            self.assertTrue(proof['created_at'])
            self.assertTrue(proof['updated_at'])
            self.assertEqual(len(proof['api_response_sha256']), 64)

    def test_pull_and_comment_metadata_cannot_disagree_with_full_response(self):
        name = 'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_004.json'
        load = consolidation.audit.load
        for path, field, replacement in [
                ('pulls/974', 'text', 'An invented prior contract'),
                ('pulls/974', 'title', 'An invented historical guarantee'),
                ('pulls/974', 'labels', ['bug']),
                ('issues/comments/149006905', 'updated_at', '2014-01-01T00:00:00Z'),
                ('issues/comments/149006905', 'html_url', 'https://github.com/unrelated/comment')]:
            with self.subTest(path=path, field=field):
                evidence = deepcopy(load(name))
                source = next(s for s in evidence['sources'] if s['path'] == path)
                source[field] = replacement
                if field == 'text':
                    source['sha256'] = consolidation.audit.sha(source['text'])
                with patch.object(consolidation.audit, 'load', side_effect=lambda value:
                                  evidence if value == name else load(value)):
                    with self.assertRaises(AssertionError):
                        consolidation.verify_supplemental_evidence()

    def test_mutable_discussion_requires_full_response_and_qualifications(self):
        name = 'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_004.json'
        load = consolidation.audit.load
        for field in ('api_response_text', 'limitation', 'collected'):
            with self.subTest(field=field):
                evidence = deepcopy(load(name))
                source = next(s for s in evidence['sources'] if s['path'] == 'issues/comments/149006905')
                source.pop(field)
                with patch.object(consolidation.audit, 'load', side_effect=lambda value:
                                  evidence if value == name else load(value)):
                    with self.assertRaises(AssertionError):
                        consolidation.verify_supplemental_evidence()

    def test_feature_exclusion_needs_consistent_contract_and_no_repair_negative(self):
        name = consolidation.REVIEW_BATCHES[3]
        for field, replacement in [
                ('existing_contract', 'supported_under_retained_contract'),
                ('selected_relevance', 'local_repair_supported'),
                ('paired_negative_scope', 'mechanism_local_only'),
                ('experimental_subset_proposal', 'defer_missing_context')]:
            with self.subTest(field=field):
                batch = deepcopy(consolidation.audit.load(name))
                record = next(r for r in batch['reviews'] if r['pair_id'].endswith(':find_hook'))
                record[field] = replacement
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_retain_cannot_bypass_a_discovery_exclusion_by_relabelling_dimensions(self):
        name = consolidation.REVIEW_BATCHES[3]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if r['pair_id'].endswith(':find_hook'))
        record.update(existing_contract='supported_under_retained_contract',
                      selected_relevance='local_repair_supported',
                      function_only_context='conditional_on_ordinary_api_semantics',
                      paired_negative_scope='mechanism_local_only',
                      experimental_subset_proposal='conditional_retain')
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_existing_control_contract_and_unresolved_task_scope_stay_separate(self):
        _, active = self.reviews()
        record = next(r for r in active.values() if r['pair_id'].endswith(':generate_ignored_nodes'))
        self.assertEqual(record['existing_contract'], 'supported_under_retained_contract')
        self.assertEqual(record['task_scope'], 'unresolved_nonstyle_eligibility')
        self.assertEqual(record['experimental_subset_proposal'], 'defer_task_scope')
        self.assertTrue(record['task_scope_reason'])
        self.assertEqual(record['function_only_context'], 'requires_missing_project_contract')

    def test_scope_deferral_cannot_lose_its_reason_or_hide_as_context_only(self):
        name = consolidation.REVIEW_BATCHES[4]
        for field, value in [('task_scope_reason', ''), ('task_scope', 'approved'),
                             ('existing_contract', 'unresolved_existing_contract'),
                             ('experimental_subset_proposal', 'defer_missing_context')]:
            with self.subTest(field=field):
                batch = deepcopy(consolidation.audit.load(name))
                record = next(r for r in batch['reviews'] if r['pair_id'].endswith(':generate_ignored_nodes'))
                record[field] = value
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_repository_batch_cannot_silently_omit_an_awkward_candidate(self):
        name = consolidation.REVIEW_BATCHES[4]
        batch = deepcopy(consolidation.audit.load(name))
        batch['reviews'].pop()
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_after_contract_regression_preserves_supported_old_contract(self):
        _, active = self.reviews()
        record = next(r for r in active.values() if 'bugs-in-py_keras-35:' in r['pair_id'])
        self.assertEqual(record['existing_contract'], 'supported_under_retained_contract')
        self.assertEqual(record['paired_negative_scope'], 'not_established_for_selected_component')
        self.assertEqual(record['experimental_subset_proposal'], 'defer_paired_negative')
        self.assertEqual(record['paired_negative_assessment'], 'unresolved_contract_regression')
        self.assertTrue(record['paired_negative_assessment_reason'])

    def test_after_contract_regression_cannot_hide_as_missing_context_or_retain(self):
        name = consolidation.REVIEW_BATCHES[5]
        for field, value in [('paired_negative_assessment_reason', ''),
                             ('paired_negative_assessment', 'approved'),
                             ('paired_negative_scope', 'mechanism_local_only'),
                             ('existing_contract', 'unresolved_existing_contract'),
                             ('experimental_subset_proposal', 'defer_missing_context'),
                             ('experimental_subset_proposal', 'conditional_retain')]:
            with self.subTest(field=field, value=value):
                batch = deepcopy(consolidation.audit.load(name))
                record = next(r for r in batch['reviews'] if 'bugs-in-py_keras-35:' in r['pair_id'])
                record[field] = value
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_pandas_after_failure_does_not_assert_it_was_newly_introduced(self):
        _, active = self.reviews()
        records = [r for r in active.values() if 'bugs-in-py_pandas-44:' in r['pair_id']]
        self.assertEqual(len(records), 2)
        for record in records:
            self.assertEqual(record['paired_negative_assessment'], 'unresolved_contract_failure')
            self.assertEqual(record['experimental_subset_proposal'], 'defer_paired_negative')
            self.assertEqual(record['existing_contract'], 'supported_under_retained_contract')
            self.assertIn('already existed', record['paired_negative_assessment_reason'])

    def test_pandas_after_failure_cannot_hide_as_context_or_lose_its_reason(self):
        name = consolidation.REVIEW_BATCHES[7]
        for field, value in [('paired_negative_assessment_reason', ''),
                             ('paired_negative_assessment', 'approved'),
                             ('experimental_subset_proposal', 'defer_missing_context'),
                             ('existing_contract', 'unresolved_existing_contract')]:
            with self.subTest(field=field):
                batch = deepcopy(consolidation.audit.load(name))
                record = next(r for r in batch['reviews'] if 'bugs-in-py_pandas-44:' in r['pair_id'])
                record[field] = value
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_pandas_corrections_keep_prior_supported_events_as_history(self):
        name = consolidation.REVIEW_BATCHES[7]
        revised = [r for r in consolidation.audit.load(name)['reviews']
                   if r['source_discovery_revision'] == 2]
        self.assertEqual(len(revised), 4)
        for record in revised:
            pid = record['pair_id']
            history = [e for e in self.events if e['pair_id'] == pid]
            self.assertEqual([e['revision'] for e in history], [1, 2])
            self.assertEqual(history[0]['review_status'], 'assistant_supported')
            self.assertEqual(history[1]['review_status'], 'assistant_ambiguous')
            self.assertEqual(history[0]['inspected_code_sha256'], history[1]['inspected_code_sha256'])

    def test_pandas_dtype_batch_cannot_omit_a_failed_after_candidate(self):
        name = consolidation.REVIEW_BATCHES[7]
        batch = deepcopy(consolidation.audit.load(name))
        batch['reviews'] = [r for r in batch['reviews']
                            if not r['pair_id'].endswith(':DataFrame.transpose')]
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_batch009_after_failures_keep_old_duty_and_uncertain_chronology(self):
        _, active = self.reviews()
        records = [r for r in active.values() if r['batch_id'] == 'consolidation-009'
                   and r['experimental_subset_proposal'] == 'defer_paired_negative']
        self.assertEqual(len(records), 2)
        for record in records:
            self.assertEqual(record['existing_contract'], 'supported_under_retained_contract')
            self.assertEqual(record['paired_negative_assessment'], 'unresolved_contract_failure')
            self.assertEqual(record['paired_negative_scope'], 'not_established_for_selected_component')

    def test_batch009_after_failure_cannot_be_relabelled_context_only(self):
        name = consolidation.REVIEW_BATCHES[8]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if r['pair_id'].endswith(':_normalize'))
        record['experimental_subset_proposal'] = 'defer_missing_context'
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_batch009_corrections_preserve_seven_supported_prior_events(self):
        batch = consolidation.audit.load(consolidation.REVIEW_BATCHES[8])
        revised = [r for r in batch['reviews'] if r['source_discovery_revision'] == 2]
        self.assertEqual(len(revised), 7)
        for record in revised:
            history = [e for e in self.events if e['pair_id'] == record['pair_id']]
            self.assertEqual([e['review_status'] for e in history],
                             ['assistant_supported', 'assistant_ambiguous'])
            self.assertEqual(history[0]['inspected_code_sha256'], history[1]['inspected_code_sha256'])
        prefix = (consolidation.audit.ROOT/'CATEGORY_AUDIT_LEDGER.jsonl').read_bytes().splitlines(keepends=True)[:767]
        self.assertEqual(consolidation.audit.sha(b''.join(prefix)),
                         'eea3f5e60a1bbd7403498a5ef32a87d10a3ec2c535573181f7d671d0e3759e77')

    def test_batch009_cannot_omit_a_prior_policy_conflict(self):
        name = consolidation.REVIEW_BATCHES[8]
        batch = deepcopy(consolidation.audit.load(name))
        batch['reviews'] = [r for r in batch['reviews'] if not r['pair_id'].endswith(':nanvar')]
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_batch010_corrections_preserve_old_acceptance_and_feature_history(self):
        batch = consolidation.audit.load(consolidation.REVIEW_BATCHES[9])
        revised = [r for r in batch['reviews'] if r['source_discovery_revision'] == 2]
        self.assertEqual(len(revised), 3)
        for record in revised:
            history = [e for e in self.events if e['pair_id'] == record['pair_id']]
            expected = (['assistant_supported', 'assistant_ambiguous']
                        if record['pair_id'].endswith(':Series._get_with') else
                        ['assistant_ambiguous', 'assistant_proposed_exclusion'])
            self.assertEqual([e['review_status'] for e in history], expected)
            self.assertEqual(history[0]['inspected_code_sha256'], history[1]['inspected_code_sha256'])
        prefix = (consolidation.audit.ROOT/'CATEGORY_AUDIT_LEDGER.jsonl').read_bytes().splitlines(keepends=True)[:774]
        self.assertEqual(consolidation.audit.sha(b''.join(prefix)),
                         'ce2e46f82dd898d4a274ad2e5e928f7f0b74e32b58de6f51f2122da6afe7fab1')

    def test_batch010_cannot_omit_an_unclassified_selected_component(self):
        name = consolidation.REVIEW_BATCHES[9]
        batch = deepcopy(consolidation.audit.load(name))
        batch['reviews'] = [r for r in batch['reviews'] if not r['pair_id'].endswith(':TimelikeOps._round')]
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_batch010_capacity_regression_cannot_be_hidden_as_context_only(self):
        name = consolidation.REVIEW_BATCHES[9]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if r['pair_id'].endswith(':Block.to_native_types'))
        self.assertEqual(record['existing_contract'], 'supported_under_retained_contract')
        self.assertEqual(record['paired_negative_assessment'], 'unresolved_contract_regression')
        record['experimental_subset_proposal'] = 'defer_missing_context'
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_keras_repository_batch_cannot_silently_drop_a_contract_ambiguity(self):
        name = consolidation.REVIEW_BATCHES[5]
        batch = deepcopy(consolidation.audit.load(name))
        batch['reviews'] = [r for r in batch['reviews'] if not r['pair_id'].endswith(':TFOptimizer.get_updates')]
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_batch011_corrections_preserve_contract_history_and_prefix(self):
        batch = consolidation.audit.load(consolidation.REVIEW_BATCHES[10])
        revised = [r for r in batch['reviews'] if r['source_discovery_revision'] == 2]
        self.assertEqual(len(revised), 19)
        for record in revised:
            history = [e for e in self.events if e['pair_id'] == record['pair_id']]
            expected = (['assistant_ambiguous', 'assistant_proposed_exclusion']
                        if record['experimental_subset_proposal'] == 'propose_feature_exclusion'
                        else ['assistant_supported', 'assistant_ambiguous'])
            self.assertEqual([e['review_status'] for e in history], expected)
            self.assertEqual(history[0]['inspected_code_sha256'], history[1]['inspected_code_sha256'])
        prefix = (consolidation.audit.ROOT/'CATEGORY_AUDIT_LEDGER.jsonl').read_bytes().splitlines(keepends=True)[:777]
        self.assertEqual(consolidation.audit.sha(b''.join(prefix)),
                         '88b984675aacade9e41696e6577c4dd7d3deaad9a38f65d2ae6f336b8a63167b')

    def test_batch011_cannot_omit_unclassified_coordinated_cleanup(self):
        name = consolidation.REVIEW_BATCHES[10]
        batch = deepcopy(consolidation.audit.load(name))
        batch['reviews'] = [r for r in batch['reviews'] if not r['pair_id'].endswith(':GeneratorEnqueuer.stop')]
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_batch011_new_api_cannot_be_promoted_to_retained_old_defect(self):
        name = consolidation.REVIEW_BATCHES[10]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if r['pair_id'].endswith(':EarlyStopping.__init__'))
        record['experimental_subset_proposal'] = 'conditional_retain'
        with self.assertRaisesRegex(AssertionError, 'Feature expansion'):
            self.reviews(batch=batch, batch_name=name)

    def test_batch012_corrections_preserve_contract_history_and_prefix(self):
        batch = consolidation.audit.load(consolidation.REVIEW_BATCHES[11])
        revised = [r for r in batch['reviews'] if r['source_discovery_revision'] == 2]
        self.assertEqual(len(revised), 9)
        for record in revised:
            history = [e for e in self.events if e['pair_id'] == record['pair_id']]
            self.assertEqual([e['review_status'] for e in history],
                             ['assistant_supported', 'assistant_ambiguous'])
            self.assertEqual(record['experimental_subset_proposal'], 'defer_existing_contract')
            self.assertEqual(history[0]['inspected_code_sha256'], history[1]['inspected_code_sha256'])
        prefix = (consolidation.audit.ROOT/'CATEGORY_AUDIT_LEDGER.jsonl').read_bytes().splitlines(keepends=True)[:796]
        self.assertEqual(consolidation.audit.sha(b''.join(prefix)),
                         '8b01d57c1114ecc51f49d8c2b5ef38de9a02c50e4aff46ffe41150b0f8860388')

    def test_batch012_cannot_omit_a_logging_component(self):
        name = consolidation.REVIEW_BATCHES[11]
        batch = deepcopy(consolidation.audit.load(name))
        batch['reviews'] = [r for r in batch['reviews'] if not r['pair_id'].endswith(':Scraper.handle_spider_error')]
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_batch012_residual_recovery_failure_cannot_be_hidden_as_context_only(self):
        name = consolidation.REVIEW_BATCHES[11]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if r['pair_id'].endswith(':gunzip'))
        self.assertEqual(record['paired_negative_assessment'], 'unresolved_contract_failure')
        record['experimental_subset_proposal'] = 'defer_missing_context'
        with self.assertRaisesRegex(AssertionError, 'after-contract failure'):
            self.reviews(batch=batch, batch_name=name)

    def test_security_screen_correction_preserves_history_and_context_deferral(self):
        result, active = self.reviews()
        pid = next(p for p in active if p.endswith(':HttpAuthMiddleware.process_request'))
        history = [r for r in result['records'] if r['pair_id'] == pid]
        self.assertEqual([r['review_revision'] for r in history], [1, 2])
        self.assertEqual(active[pid]['security_screen'], 'demonstrated_security_boundary')
        self.assertEqual(active[pid]['experimental_subset_proposal'], 'defer_missing_context')
        name = consolidation.REVIEW_BATCHES[12]
        batch = deepcopy(consolidation.audit.load(name))
        batch['reviews'][0]['experimental_subset_proposal'] = 'conditional_retain'
        batch['reviews'][0]['function_only_context'] = 'conditional_on_ordinary_api_semantics'
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_batch014_corrections_preserve_policy_history_and_prefix(self):
        batch = consolidation.audit.load(consolidation.REVIEW_BATCHES[13])
        changed = {e['pair_id'] for e in self.events[805:807]}
        revised = [r for r in batch['reviews'] if r['pair_id'] in changed]
        self.assertEqual(len(revised), 2)
        for record in revised:
            history = [e for e in self.events if e['pair_id'] == record['pair_id']]
            self.assertEqual([e['review_status'] for e in history],
                             ['assistant_supported', 'assistant_ambiguous'])
            self.assertEqual(record['experimental_subset_proposal'], 'defer_existing_contract')
            self.assertEqual(history[0]['inspected_code_sha256'], history[1]['inspected_code_sha256'])
        prefix = (consolidation.audit.ROOT/'CATEGORY_AUDIT_LEDGER.jsonl').read_bytes().splitlines(keepends=True)[:805]
        self.assertEqual(consolidation.audit.sha(b''.join(prefix)),
                         '01d082abd0bde3518a4bc6ce51e94593afae71533c1fc02592869171d946c2f6')

    def test_batch014_cannot_omit_an_annotation_only_exclusion(self):
        name = consolidation.REVIEW_BATCHES[13]
        batch = deepcopy(consolidation.audit.load(name))
        batch['reviews'] = [r for r in batch['reviews'] if not r['pair_id'].endswith(':schedule_formatting')]
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_nonrepair_exclusion_cannot_be_silently_recast_as_feature_or_retain(self):
        name = consolidation.REVIEW_BATCHES[13]
        for proposal in ('conditional_retain', 'propose_feature_exclusion'):
            with self.subTest(proposal=proposal):
                batch = deepcopy(consolidation.audit.load(name))
                record = next(r for r in batch['reviews'] if r['pair_id'].endswith(':schedule_formatting'))
                record['experimental_subset_proposal'] = proposal
                with self.assertRaisesRegex(AssertionError, 'explicit nonrepair exclusion'):
                    self.reviews(batch=batch, batch_name=name)

    def test_cvefixes_proofs_do_not_borrow_hapy_fix_metadata(self):
        _, active = self.reviews()
        record = active['CVEfixes:139435414054923:11275476978704']
        self.assertEqual(record['security_screen'], 'demonstrated_security_boundary')
        for proof in record['selected_source_proofs'].values():
            self.assertEqual(proof['archive'], 'SECURITY_ADMISSION_UPSTREAM_SNAPSHOTS.zip')
        name = consolidation.REVIEW_BATCHES[13]
        batch = deepcopy(consolidation.audit.load(name))
        item = next(r for r in batch['reviews'] if r['pair_id'] == record['pair_id'])
        item['anchors'].append({'kind': 'fix', 'needle': 'unverified unrelated fix'})
        with self.assertRaisesRegex(AssertionError, 'Fix anchors require retained HaPy'):
            self.reviews(batch=batch, batch_name=name)

    def test_newline_policy_deferral_does_not_certify_known_after_empty_input_failure(self):
        name = consolidation.REVIEW_BATCHES[13]
        for function in ('format_file_in_place', 'format_stdin_to_stdout'):
            with self.subTest(function=function):
                batch = deepcopy(consolidation.audit.load(name))
                record = next(r for r in batch['reviews'] if 'bugs-in-py_black-18:' in r['pair_id']
                              and r['pair_id'].endswith(':'+function))
                self.assertTrue(record['additional_after_concerns'])
                self.assertEqual(record['experimental_subset_proposal'], 'defer_existing_contract')
                record['paired_negative_scope'] = 'mechanism_local_only'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_batch015_cannot_drop_a_boundary_deferred_wrapper(self):
        name = consolidation.REVIEW_BATCHES[14]
        batch = deepcopy(consolidation.audit.load(name))
        batch['reviews'] = [r for r in batch['reviews'] if r['pair_id'] != 'CVEfixes:114250776010152:260344157106406']
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_spirit_get_parameter_does_not_erase_post_operation_gate(self):
        _, active = self.reviews()
        records = [r for p, r in active.items() if self.train[p]['repository'] == 'github.com/nitely/spirit']
        self.assertEqual(sum(r['redirect_analysis']['parameter_source'] == 'POST' for r in records), 19)
        query_post = [r for r in records if r['redirect_analysis']['parameter_source'] == 'GET'
                      and r['redirect_analysis']['operation_gate'] == 'POST_required']
        self.assertEqual(len(query_post), 4)
        self.assertTrue(all(r['experimental_subset_proposal'] == 'defer_security_boundary' for r in query_post))
        name = consolidation.REVIEW_BATCHES[14]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if r['pair_id'] == query_post[0]['pair_id'])
        record['redirect_analysis']['parameter_source'] = 'POST'
        with self.assertRaisesRegex(AssertionError, 'parameter mapping must match'):
            self.reviews(batch=batch, batch_name=name)

    def test_spirit_nested_spans_share_family_without_new_ledger_events(self):
        _, active = self.reviews()
        records = [r for p, r in active.items() if self.train[p]['repository'] == 'github.com/nitely/spirit']
        self.assertEqual(len({r['mechanical_family_id'] for r in records}), 1)
        outer = active['CVEfixes:114250776010152:11935636564556']
        inner = active['CVEfixes:114250776010152:260344157106406']
        for side in ('before', 'after'):
            parent, child = outer['selected_source_proofs'][side], inner['selected_source_proofs'][side]
            self.assertEqual(parent['member'], child['member'])
            self.assertLess(parent['start'], child['start'])
            self.assertGreaterEqual(parent['end'], child['end'])
        checkpoint = consolidation.audit.load(consolidation.REVIEW_BATCHES[14])['discovery_ledger_checkpoint']
        self.assertEqual(checkpoint['events'], 807)
        prefix = (consolidation.audit.ROOT/'CATEGORY_AUDIT_LEDGER.jsonl').read_bytes().splitlines(keepends=True)[:807]
        self.assertEqual(consolidation.audit.sha(b''.join(prefix)),
                          '7a3bae6bdb33eccbbb4d19dc40f1e2f6f2a99f15dd94827f6fc607a72e57bf65')
        spirit_events = [e for e in self.events if e['pair_id'] in {r['pair_id'] for r in records}]
        self.assertEqual(len(spirit_events), 29)

    def test_batch016_cannot_omit_a_null_category_nonrepair(self):
        name = consolidation.REVIEW_BATCHES[15]
        batch = deepcopy(consolidation.audit.load(name))
        pid = next(r['pair_id'] for r in batch['reviews'] if r['pair_id'].endswith(':SortedCorrectedCommandsSequence._remove_duplicates'))
        self.assertIsNone(self.latest[pid]['category_id'])
        batch['reviews'] = [r for r in batch['reviews'] if r['pair_id'] != pid]
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_batch016_settings_correction_preserves_old_api_and_prefix(self):
        batch = consolidation.audit.load(consolidation.REVIEW_BATCHES[15])
        record = next(r for r in batch['reviews'] if r['pair_id'].endswith(':Settings.update'))
        history = [e for e in self.events if e['pair_id'] == record['pair_id']]
        self.assertEqual([e['review_status'] for e in history], ['assistant_supported', 'assistant_ambiguous'])
        self.assertEqual(history[0]['inspected_code_sha256'], history[1]['inspected_code_sha256'])
        self.assertEqual(record['experimental_subset_proposal'], 'defer_selected_attribution')
        self.assertEqual(record['source_discovery_revision'], 2)
        prefix = (consolidation.audit.ROOT/'CATEGORY_AUDIT_LEDGER.jsonl').read_bytes().splitlines(keepends=True)[:808]
        self.assertEqual(consolidation.audit.sha(b''.join(prefix)),
                          '590e37fbe1828b68634fccc089589b9abba27a909946a53f7a789a0a72410642')
        prefix = (consolidation.audit.ROOT/'CATEGORY_AUDIT_LEDGER.jsonl').read_bytes().splitlines(keepends=True)[:807]
        self.assertEqual(consolidation.audit.sha(b''.join(prefix)),
                         '7a3bae6bdb33eccbbb4d19dc40f1e2f6f2a99f15dd94827f6fc607a72e57bf65')

    def test_thefuck_quoting_failure_chronology_cannot_be_hidden_as_context_only(self):
        name = consolidation.REVIEW_BATCHES[15]
        for case, assessment in [('thefuck-11:', 'unresolved_contract_regression'),
                                 ('thefuck-9:', 'unresolved_contract_failure')]:
            with self.subTest(case=case):
                batch = deepcopy(consolidation.audit.load(name))
                record = next(r for r in batch['reviews'] if case in r['pair_id'])
                self.assertEqual(record['paired_negative_assessment'], assessment)
                record['experimental_subset_proposal'] = 'defer_missing_context'
                with self.assertRaisesRegex(AssertionError, 'after-contract failure'):
                    self.reviews(batch=batch, batch_name=name)

    def test_thefuck_old_uniqueness_equivalence_is_nonrepair_not_feature(self):
        name = consolidation.REVIEW_BATCHES[15]
        for function in ('_get_first_two_unique', '_remove_duplicates'):
            with self.subTest(function=function):
                batch = deepcopy(consolidation.audit.load(name))
                record = next(r for r in batch['reviews'] if r['pair_id'].endswith('.'+function))
                self.assertEqual(record['existing_contract'], 'no_selected_runtime_repair')
                record['experimental_subset_proposal'] = 'propose_feature_exclusion'
                with self.assertRaisesRegex(AssertionError, 'explicit nonrepair exclusion'):
                    self.reviews(batch=batch, batch_name=name)

    def test_git_boolean_flag_correction_preserves_authored_history_and_proposals(self):
        result, active = self.reviews()
        pid = 'HaPy-Bug:bugs-in-py_thefuck-11:0:thefuck/rules/git_push.py:get_new_command'
        history = [r for r in result['records'] if r['pair_id'] == pid]
        self.assertEqual([r['review_revision'] for r in history], [1, 2])
        self.assertEqual(history[0]['source_discovery_revision'], history[1]['source_discovery_revision'])
        self.assertEqual(history[0]['experimental_subset_proposal'], history[1]['experimental_subset_proposal'])
        self.assertEqual(active[pid]['batch_id'], 'consolidation-017')
        self.assertIn('Boolean flag', active[pid]['contract_reason'])
        self.assertTrue(any(p.get('path') == 'parse-options.h' for p in active[pid]['verified_evidence_anchors']))
        self.assertEqual(consolidation.audit.file_sha(consolidation.audit.ROOT/'CATEGORY_AUDIT_CONSOLIDATION_BATCH_016.json'),
                         '153301634ff350389f79929aac6664d2a21a0435cacde018bfdeab062050866a')

    def test_batch017_metadata_leaf_revalidation_cannot_omit_unchanged_companion(self):
        name = consolidation.REVIEW_BATCHES[16]
        batch = deepcopy(consolidation.audit.load(name))
        self.assertEqual(len(batch['reviews']), 3)
        batch['reviews'] = [r for r in batch['reviews'] if 'thefuck-25:' not in r['pair_id']]
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_batch018_cannot_omit_a_null_category_downloader(self):
        name = consolidation.REVIEW_BATCHES[17]
        batch = deepcopy(consolidation.audit.load(name))
        pid = next(r['pair_id'] for r in batch['reviews'] if r['pair_id'].endswith(':SimpleHttpClient.get_file'))
        self.assertIsNone(self.latest[pid]['category_id'])
        batch['reviews'] = [r for r in batch['reviews'] if r['pair_id'] != pid]
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_synapse_downloader_after_failures_cannot_receive_mechanism_negative(self):
        name = consolidation.REVIEW_BATCHES[17]
        for function in ('SimpleHttpClient.get_file', 'MatrixFederationHttpClient.get_file'):
            with self.subTest(function=function):
                batch = deepcopy(consolidation.audit.load(name))
                record = next(r for r in batch['reviews'] if r['pair_id'].endswith(':'+function))
                self.assertTrue(record['additional_after_concerns'])
                self.assertEqual(record['experimental_subset_proposal'], 'propose_nonrepair_exclusion')
                record['paired_negative_scope'] = 'mechanism_local_only'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_synapse_glob_feature_loss_cannot_be_hidden_as_context_only(self):
        name = consolidation.REVIEW_BATCHES[17]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if r['pair_id'].endswith(':_glob_matches'))
        self.assertEqual(record['paired_negative_assessment'], 'unresolved_contract_regression')
        record['experimental_subset_proposal'] = 'defer_missing_context'
        with self.assertRaisesRegex(AssertionError, 'after-contract failure'):
            self.reviews(batch=batch, batch_name=name)

    def test_spirit_victim_delivery_deferral_cannot_be_promoted_to_retain(self):
        name = consolidation.REVIEW_BATCHES[14]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if r['experimental_subset_proposal'] == 'defer_security_boundary')
        record['experimental_subset_proposal'] = 'conditional_retain'
        record['function_only_context'] = 'conditional_on_ordinary_api_semantics'
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_batch019_cannot_omit_either_null_category_case(self):
        name = consolidation.REVIEW_BATCHES[18]
        original = consolidation.audit.load(name)
        null_ids = [r['pair_id'] for r in original['reviews'] if self.latest[r['pair_id']]['category_id'] is None]
        self.assertEqual(len(null_ids), 2)
        for pid in null_ids:
            with self.subTest(pair_id=pid):
                batch = deepcopy(original)
                batch['reviews'] = [r for r in batch['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_ansible_transfer_pam_banner_after_failures_require_explicit_deferrals(self):
        name = consolidation.REVIEW_BATCHES[18]
        original = consolidation.audit.load(name)
        failures = [r for r in original['reviews'] if 'paired_negative_assessment' in r]
        self.assertEqual(len(failures), 8)
        self.assertEqual(sum(r['paired_negative_assessment'] == 'unresolved_contract_failure' for r in failures), 1)
        self.assertEqual(sum(r['security_screen'] == 'demonstrated_security_boundary' for r in failures), 6)
        for record in failures:
            with self.subTest(pair_id=record['pair_id']):
                batch = deepcopy(original)
                item = next(r for r in batch['reviews'] if r['pair_id'] == record['pair_id'])
                item['experimental_subset_proposal'] = 'defer_missing_context'
                with self.assertRaisesRegex(AssertionError, 'after-contract failure'):
                    self.reviews(batch=batch, batch_name=name)

    def test_batch019_contract_revisions_preserve_history_code_and_ledger_prefix(self):
        prefix811 = (consolidation.audit.ROOT/'CATEGORY_AUDIT_LEDGER.jsonl').read_bytes().splitlines(keepends=True)[:811]
        self.assertEqual(consolidation.audit.sha(b''.join(prefix811)),
                          'a8458c2712f92ddee97ecf55a8c85c861a310552b024ceb487949d2f4e3cfb11')
        batch = consolidation.audit.load(consolidation.REVIEW_BATCHES[18])
        revised = [r for r in batch['reviews'] if r['source_discovery_revision'] == 2]
        self.assertEqual(len(revised), 3)
        expected = {'bugs-in-py_ansible-12:': ('assistant_ambiguous', 'assistant_supported'),
                    'bugs-in-py_ansible-13:': ('assistant_supported', 'assistant_supported'),
                    'bugs-in-py_ansible-6:': ('assistant_supported', 'assistant_ambiguous')}
        for fragment, statuses in expected.items():
            record = next(r for r in revised if fragment in r['pair_id'])
            history = [e for e in self.events if e['pair_id'] == record['pair_id']]
            self.assertEqual(tuple(e['review_status'] for e in history), statuses)
            self.assertEqual([e['revision'] for e in history], [1, 2])
            self.assertEqual(history[0]['inspected_code_sha256'], history[1]['inspected_code_sha256'])
            self.assertEqual(history[0]['category_id'], history[1]['category_id'])
        prefix = (consolidation.audit.ROOT/'CATEGORY_AUDIT_LEDGER.jsonl').read_bytes().splitlines(keepends=True)[:808]
        self.assertEqual(consolidation.audit.sha(b''.join(prefix)),
                         '590e37fbe1828b68634fccc089589b9abba27a909946a53f7a789a0a72410642')

    def test_batch020_cannot_omit_any_null_category_component(self):
        name = consolidation.REVIEW_BATCHES[19]
        original = consolidation.audit.load(name)
        null_ids = [r['pair_id'] for r in original['reviews'] if self.latest[r['pair_id']]['category_id'] is None]
        self.assertEqual(len(null_ids), 8)
        for pid in null_ids:
            with self.subTest(pair_id=pid):
                batch = deepcopy(original)
                batch['reviews'] = [r for r in batch['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_waitress_partial_repairs_cannot_hide_after_contract_failures(self):
        name = consolidation.REVIEW_BATCHES[19]
        original = consolidation.audit.load(name)
        failures = [r for r in original['reviews'] if 'paired_negative_assessment' in r]
        self.assertEqual(len(failures), 3)
        self.assertEqual(sum(r['paired_negative_assessment'] == 'unresolved_contract_regression' for r in failures), 1)
        self.assertEqual(sum(r['paired_negative_assessment'] == 'unresolved_contract_failure' for r in failures), 2)
        for record in failures:
            with self.subTest(pair_id=record['pair_id']):
                batch = deepcopy(original)
                item = next(r for r in batch['reviews'] if r['pair_id'] == record['pair_id'])
                item['experimental_subset_proposal'] = 'defer_missing_context'
                with self.assertRaisesRegex(AssertionError, 'after-contract failure'):
                    self.reviews(batch=batch, batch_name=name)

    def test_waitress_chunk_hardening_cannot_receive_a_clean_negative(self):
        name = consolidation.REVIEW_BATCHES[19]
        for cve in ('CVE-2019-16785', 'CVE-2019-16786'):
            with self.subTest(cve=cve):
                batch = deepcopy(consolidation.audit.load(name))
                record = next(r for r in batch['reviews'] if cve in r['pair_id'] and r['pair_id'].endswith(':ChunkedReceiver.received'))
                self.assertEqual(record['security_screen'], 'unresolved_boundary')
                self.assertEqual(record['experimental_subset_proposal'], 'defer_security_boundary')
                self.assertTrue(record['additional_after_concerns'])
                record['paired_negative_scope'] = 'mechanism_local_only'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_waitress_deferred_continue_residual_preserves_authored_history(self):
        result, active = self.reviews()
        pid = 'HaPy-Bug:cve_CVE-2022-31015:0:src/waitress/wasyncore.py:dispatcher.send'
        history = [r for r in result['records'] if r['pair_id'] == pid]
        self.assertEqual([r['review_revision'] for r in history], [1, 2])
        self.assertEqual(history[0]['source_discovery_revision'], history[1]['source_discovery_revision'])
        self.assertEqual(history[0]['experimental_subset_proposal'], 'defer_missing_context')
        self.assertEqual(active[pid]['experimental_subset_proposal'], 'defer_paired_negative')
        self.assertEqual(active[pid]['paired_negative_assessment'], 'unresolved_contract_failure')
        self.assertEqual(consolidation.audit.file_sha(consolidation.audit.ROOT/'CATEGORY_AUDIT_CONSOLIDATION_BATCH_020.json'),
                         '83efd9d9de1ad79d6d8c48c513c266110ad6c84e2e723e2f909e71df059d7bf6')
        name = consolidation.REVIEW_BATCHES[20]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if r['pair_id'] == pid)
        record['experimental_subset_proposal'] = 'defer_missing_context'
        with self.assertRaisesRegex(AssertionError, 'after-contract failure'):
            self.reviews(batch=batch, batch_name=name)

    def test_batch021_socket_leaf_revalidation_cannot_omit_unchanged_worker(self):
        name = consolidation.REVIEW_BATCHES[20]
        batch = deepcopy(consolidation.audit.load(name))
        self.assertEqual(len(batch['reviews']), 3)
        batch['reviews'] = [r for r in batch['reviews'] if not r['pair_id'].endswith(':HTTPChannel.write_soon')]
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_radicale_selection_cannot_omit_policy_converter_or_consumer(self):
        name = consolidation.REVIEW_BATCHES[21]
        original = consolidation.audit.load(name)
        self.assertEqual(len(original['reviews']), 17)
        self.assertEqual(len({self.families[r['pair_id']] for r in original['reviews']}), 2)
        for suffix in ('193597207056014:180205556361792',
                       '277049986640473:253680698316502',
                       '7561542198959:23186523446072'):
            with self.subTest(suffix=suffix):
                batch = deepcopy(original)
                batch['reviews'] = [r for r in batch['reviews'] if not r['pair_id'].endswith(suffix)]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_radicale_sidecar_regression_cannot_be_only_a_context_deferral(self):
        name = consolidation.REVIEW_BATCHES[21]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if r['pair_id'].endswith(':253680698316502'))
        self.assertEqual(record['paired_negative_assessment'], 'unresolved_contract_regression')
        record['experimental_subset_proposal'] = 'defer_missing_context'
        with self.assertRaisesRegex(AssertionError, 'after-contract failure'):
            self.reviews(batch=batch, batch_name=name)

    def test_radicale_cvefixes_records_cannot_borrow_hapy_fix_evidence(self):
        name = consolidation.REVIEW_BATCHES[21]
        batch = deepcopy(consolidation.audit.load(name))
        batch['reviews'][0]['anchors'].append({'kind': 'fix', 'needle': 'borrowed patch'})
        with self.assertRaisesRegex(AssertionError, 'Fix anchors require retained HaPy'):
            self.reviews(batch=batch, batch_name=name)

    def test_radicale_revisions_preserve_selected_bytes_categories_and_811_event_prefix(self):
        self.assertGreaterEqual(len(self.events), 827)
        ledger = consolidation.audit.ROOT/'CATEGORY_AUDIT_LEDGER.jsonl'
        self.assertEqual(consolidation.audit.sha(b''.join(ledger.read_bytes().splitlines(keepends=True)[:825])),
                         '82a7ed0370f99633102502587bb7f84cfd867aee911c754570fb24bfffa40229')
        self.assertEqual(consolidation.audit.sha(b''.join(ledger.read_bytes().splitlines(keepends=True)[:811])),
                         'a8458c2712f92ddee97ecf55a8c85c861a310552b024ceb487949d2f4e3cfb11')
        batch = consolidation.audit.load(consolidation.REVIEW_BATCHES[21])
        revised = [r for r in batch['reviews'] if r['source_discovery_revision'] == 2]
        self.assertEqual(len(revised), 14)
        changes = []
        for record in revised:
            history = [e for e in self.events if e['pair_id'] == record['pair_id']]
            self.assertEqual([e['revision'] for e in history], [1, 2])
            self.assertEqual(history[0]['category_id'], history[1]['category_id'])
            self.assertEqual(history[0]['issue_family_id'], history[1]['issue_family_id'])
            self.assertEqual(history[0]['inspected_code_sha256'], history[1]['inspected_code_sha256'])
            changes.append(tuple(e['review_status'] for e in history))
        self.assertEqual(changes.count(('assistant_ambiguous', 'assistant_supported')), 5)
        self.assertEqual(changes.count(('assistant_supported', 'assistant_ambiguous')), 9)
        self.assertEqual(consolidation.audit.file_sha(consolidation.audit.ROOT/consolidation.REVIEW_BATCHES[21]),
                         '682db03073182664483cd5a5d08a00b99948bb7adb660c4c89b445d311c0d856')

    def test_radicale_residual_consumer_concerns_cannot_receive_clean_negatives(self):
        name = consolidation.REVIEW_BATCHES[21]
        original = consolidation.audit.load(name)
        for suffix in (':185969555792679', ':29633273842125'):
            with self.subTest(suffix=suffix):
                batch = deepcopy(original)
                record = next(r for r in batch['reviews'] if r['pair_id'].endswith(suffix))
                self.assertEqual(record['security_screen'], 'unresolved_boundary')
                self.assertEqual(record['selected_relevance'], 'coordinated_component_not_isolated')
                self.assertTrue(record['additional_after_concerns'])
                record['paired_negative_scope'] = 'mechanism_local_only'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_glance_selection_cannot_omit_authorization_acl_or_validation(self):
        name = consolidation.REVIEW_BATCHES[22]
        original = consolidation.audit.load(name)
        for fragment in ('CVE-2012-5482:', 'MultiTenantStore.set_acls', ':2:glance/store/swift.py:StoreLocation.parse_uri'):
            with self.subTest(fragment=fragment):
                batch = deepcopy(original)
                batch['reviews'] = [r for r in batch['reviews'] if fragment not in r['pair_id']]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_glance_v2_delayed_delete_residual_requires_explicit_negative_deferral(self):
        name = consolidation.REVIEW_BATCHES[22]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if 'CVE-2012-5482:' in r['pair_id'])
        self.assertEqual(record['paired_negative_assessment'], 'unresolved_contract_failure')
        self.assertEqual(record['security_screen'], 'demonstrated_security_boundary')
        record['experimental_subset_proposal'] = 'defer_missing_context'
        with self.assertRaisesRegex(AssertionError, 'after-contract failure'):
            self.reviews(batch=batch, batch_name=name)

    def test_glance_unknown_log_audience_cannot_be_promoted_by_api_context(self):
        name = consolidation.REVIEW_BATCHES[22]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if ':2:glance/store/swift.py:StoreLocation.parse_uri' in r['pair_id'])
        self.assertEqual(record['security_screen'], 'unresolved_boundary')
        record['experimental_subset_proposal'] = 'conditional_retain'
        record['function_only_context'] = 'conditional_on_ordinary_api_semantics'
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_glance_delete_redaction_cannot_hide_after_caller_raw_uri_concerns(self):
        name = consolidation.REVIEW_BATCHES[22]
        original = consolidation.audit.load(name)
        deletes = [r for r in original['reviews'] if r['pair_id'].endswith(('BaseStore.delete', 'Store.delete'))]
        self.assertEqual(len(deletes), 3)
        for record in deletes:
            with self.subTest(pair_id=record['pair_id']):
                self.assertEqual(record['experimental_subset_proposal'], 'defer_security_boundary')
                self.assertTrue(record['additional_after_concerns'])
                batch = deepcopy(original)
                item = next(r for r in batch['reviews'] if r['pair_id'] == record['pair_id'])
                item['paired_negative_scope'] = 'mechanism_local_only'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_vyper_selection_cannot_omit_cvefixes_or_null_category_rows(self):
        name = consolidation.REVIEW_BATCHES[23]
        original = consolidation.audit.load(name)
        excluded = [r for r in original['reviews']
                    if self.latest[r['pair_id']]['category_id'] is None]
        self.assertEqual(len(excluded), 6)
        for record in [original['reviews'][0], excluded[0], excluded[-1]]:
            with self.subTest(pair_id=record['pair_id']):
                batch = deepcopy(original)
                batch['reviews'] = [r for r in batch['reviews'] if r['pair_id'] != record['pair_id']]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_vyper_raw_capacity_after_failure_requires_explicit_negative_deferral(self):
        name = consolidation.REVIEW_BATCHES[23]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if r['pair_id'].endswith(':_unpack_returndata'))
        self.assertEqual(record['paired_negative_assessment'], 'unresolved_contract_failure')
        self.assertIn('allocation including method-id padding is128', record['paired_negative_assessment_reason'])
        self.assertIn('New ABI ret_len is160', record['paired_negative_assessment_reason'])
        record['experimental_subset_proposal'] = 'defer_missing_context'
        with self.assertRaisesRegex(AssertionError, 'after-contract failure'):
            self.reviews(batch=batch, batch_name=name)

    def test_vyper_equivalent_refactors_cannot_be_promoted_to_positive_pairs(self):
        name = consolidation.REVIEW_BATCHES[23]
        original = consolidation.audit.load(name)
        refactors = [r for r in original['reviews'] if r['experimental_subset_proposal'] == 'propose_nonrepair_exclusion']
        self.assertEqual(len(refactors), 5)
        for record in refactors:
            with self.subTest(pair_id=record['pair_id']):
                batch = deepcopy(original)
                item = next(r for r in batch['reviews'] if r['pair_id'] == record['pair_id'])
                item['experimental_subset_proposal'] = 'defer_missing_context'
                with self.assertRaisesRegex(AssertionError, 'nonrepair exclusion'):
                    self.reviews(batch=batch, batch_name=name)

    def test_vyper_tuple_conversion_cannot_borrow_sibling_security_delivery(self):
        name = consolidation.REVIEW_BATCHES[23]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if r['pair_id'].endswith(':new_type_to_old_type'))
        self.assertIsNone(self.latest[record['pair_id']]['category_id'])
        self.assertEqual(record['selected_relevance'], 'conditional_runtime_repair')
        self.assertEqual(record['security_screen'], 'unresolved_boundary')
        record['experimental_subset_proposal'] = 'conditional_retain'
        record['function_only_context'] = 'conditional_on_ordinary_api_semantics'
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_nautobot_selection_cannot_omit_either_family_or_ambiguous_helpers(self):
        name = consolidation.REVIEW_BATCHES[24]
        original = consolidation.audit.load(name)
        for fragment in ('CVEfixes:236838846013906:', 'CVEfixes:44778668750512:', 'CVEfixes:902395637795:'):
            with self.subTest(fragment=fragment):
                batch = deepcopy(original)
                batch['reviews'] = [r for r in batch['reviews'] if fragment not in r['pair_id']]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_nautobot_introduced_after_contract_failures_need_explicit_deferrals(self):
        name = consolidation.REVIEW_BATCHES[24]
        original = consolidation.audit.load(name)
        failed = [r for r in original['reviews'] if r.get('paired_negative_assessment') == 'unresolved_contract_regression']
        self.assertEqual(len(failed), 2)
        for record in failed:
            with self.subTest(pair_id=record['pair_id']):
                batch = deepcopy(original)
                item = next(r for r in batch['reviews'] if r['pair_id'] == record['pair_id'])
                item['experimental_subset_proposal'] = 'defer_missing_context'
                with self.assertRaisesRegex(AssertionError, 'after-contract failure'):
                    self.reviews(batch=batch, batch_name=name)

    def test_nautobot_already_escaped_or_coordinated_paths_cannot_be_promoted(self):
        name = consolidation.REVIEW_BATCHES[24]
        original = consolidation.audit.load(name)
        deferred = [r for r in original['reviews'] if r['experimental_subset_proposal'] == 'defer_selected_attribution']
        self.assertEqual(len(deferred), 4)
        for record in deferred:
            with self.subTest(pair_id=record['pair_id']):
                batch = deepcopy(original)
                item = next(r for r in batch['reviews'] if r['pair_id'] == record['pair_id'])
                item['experimental_subset_proposal'] = 'conditional_retain'
                item['function_only_context'] = 'conditional_on_ordinary_api_semantics'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_nautobot_revisions_preserve_825_event_prefix_and_selected_identity(self):
        ledger = consolidation.audit.ROOT/'CATEGORY_AUDIT_LEDGER.jsonl'
        self.assertEqual(consolidation.audit.sha(b''.join(ledger.read_bytes().splitlines(keepends=True)[:827])),
                         '8b0f0e74c6a9a96b62ac9ca15164b9eeaceb87d10e5b070fc1d8c52fa3a6f359')
        self.assertEqual(consolidation.audit.sha(b''.join(ledger.read_bytes().splitlines(keepends=True)[:825])),
                         '82a7ed0370f99633102502587bb7f84cfd867aee911c754570fb24bfffa40229')
        self.assertGreaterEqual(len(self.events), 827)
        changes = []
        for event in self.events[825:827]:
            history = [e for e in self.events if e['pair_id'] == event['pair_id']]
            self.assertEqual([e['revision'] for e in history], [1, 2])
            for field in ('category_id', 'issue_family_id', 'inspected_code_sha256'):
                self.assertEqual(history[0][field], history[1][field])
            self.assertEqual(self.train[event['pair_id']]['repository'], 'github.com/nautobot/nautobot')
            changes.append(tuple(e['review_status'] for e in history))
        self.assertCountEqual(changes, [('assistant_supported', 'assistant_ambiguous'),
                                        ('assistant_ambiguous', 'assistant_supported')])

    def test_nautobot_import_delivery_keeps_file_owner_and_operator_distinct(self):
        name = consolidation.REVIEW_BATCHES[24]
        original = consolidation.audit.load(name)
        record = next(r for r in original['reviews'] if r['pair_id'] == 'CVEfixes:902395637795:240653218551071')
        self.assertEqual(record['source_discovery_revision'], 2)
        self.assertEqual(record['security_screen'], 'demonstrated_security_boundary')
        self.assertIn('file/catalog author versus operator/browser', record['security_reason'])
        self.assertIn('not automatically other users', record['security_reason'])
        self.assertTrue(any(a.get('path') == 'django/contrib/messages/storage/cookie.py' for a in record['anchors']))
        batch = deepcopy(original)
        item = next(r for r in batch['reviews'] if r['pair_id'] == record['pair_id'])
        item['experimental_subset_proposal'] = 'conditional_retain'
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_openapi_selection_includes_both_families_and_all_six_null_categories(self):
        name = consolidation.REVIEW_BATCHES[25]
        original = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items()
               if row['repository'] == 'github.com/triaxtec/openapi-python-client'}
        self.assertEqual({r['pair_id'] for r in original['reviews']}, ids)
        self.assertEqual(len(ids), 8)
        self.assertEqual(sum(self.latest[pid]['category_id'] is None for pid in ids), 6)
        self.assertEqual(len({self.families[pid] for pid in ids}), 2)
        for fragment in (':Project.__init__', ':EnumProperty.__post_init__', ':DateTimeProperty.get_imports'):
            with self.subTest(fragment=fragment):
                batch = deepcopy(original)
                batch['reviews'] = [r for r in batch['reviews'] if not r['pair_id'].endswith(fragment)]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_openapi_enum_after_regression_cannot_be_reclassified_as_context_only(self):
        name = consolidation.REVIEW_BATCHES[25]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if r['pair_id'].endswith(':EnumProperty.values_from_list'))
        self.assertEqual(record['paired_negative_assessment'], 'unresolved_contract_regression')
        self.assertTrue(record['additional_after_concerns'])
        self.assertIn('combining', record['paired_negative_assessment_reason'])
        self.assertIn('subsequent developer/application import/use', record['security_reason'])
        record['experimental_subset_proposal'] = 'defer_missing_context'
        with self.assertRaisesRegex(AssertionError, 'after-contract failure'):
            self.reviews(batch=batch, batch_name=name)

    def test_openapi_nonrepairs_and_coordinated_initializer_cannot_be_promoted(self):
        name = consolidation.REVIEW_BATCHES[25]
        original = consolidation.audit.load(name)
        nonrepairs = [r for r in original['reviews'] if r['existing_contract'] == 'no_selected_runtime_repair']
        self.assertEqual(len(nonrepairs), 5)
        initializer = next(r for r in original['reviews'] if r['pair_id'].endswith(':EnumProperty.__post_init__'))
        self.assertEqual(initializer['experimental_subset_proposal'], 'defer_selected_attribution')
        for record in nonrepairs + [initializer]:
            with self.subTest(pair_id=record['pair_id']):
                batch = deepcopy(original)
                item = next(r for r in batch['reviews'] if r['pair_id'] == record['pair_id'])
                item['experimental_subset_proposal'] = 'conditional_retain'
                item['function_only_context'] = 'conditional_on_ordinary_api_semantics'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_openapi_preserves_discovery_and_matches_shared_helper_versions(self):
        self.assertGreaterEqual(len(self.events), 827)
        ledger = consolidation.audit.ROOT/'CATEGORY_AUDIT_LEDGER.jsonl'
        self.assertEqual(consolidation.audit.sha(b''.join(ledger.read_bytes().splitlines(keepends=True)[:827])),
                         '8b0f0e74c6a9a96b62ac9ca15164b9eeaceb87d10e5b070fc1d8c52fa3a6f359')
        batch = consolidation.audit.load(consolidation.REVIEW_BATCHES[25])
        for record in batch['reviews']:
            self.assertEqual(record['source_discovery_revision'], self.latest[record['pair_id']]['revision'])
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_026.json')['sources']
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_026_PEERS.json')['sources']
        self.assertEqual(context[1]['text'], peers[4]['text'])
        self.assertEqual(context[1]['sha256'], peers[4]['sha256'])
        self.assertNotEqual(context[1]['ref'], peers[4]['ref'])

    def test_openapi_identical_old_new_enum_templates_still_require_explicit_refs(self):
        name = consolidation.REVIEW_BATCHES[25]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if r['pair_id'].endswith(':EnumProperty.values_from_list'))
        anchor = next(a for a in record['anchors'] if a.get('path') == 'openapi_python_client/templates/enum.pyi')
        anchor.pop('ref')
        with self.assertRaisesRegex(AssertionError, 'unambiguous path/ref'):
            self.reviews(batch=batch, batch_name=name)

    def test_tlslite_selection_cannot_omit_null_or_revised_oracle_siblings(self):
        name = consolidation.REVIEW_BATCHES[26]
        original = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items() if row['repository'] == 'github.com/tlsfuzzer/tlslite-ng'}
        self.assertEqual({r['pair_id'] for r in original['reviews']}, ids)
        self.assertEqual(len(ids), 8)
        self.assertEqual(sum(self.latest[pid]['category_id'] is None for pid in ids), 7)
        self.assertEqual(len({self.families[pid] for pid in ids}), 1)
        for fragment in (':Python_RSAKey.parsePEM', ':RSAKey.decrypt', ':RSAKey._raw_pkcs1_verify'):
            with self.subTest(fragment=fragment):
                batch = deepcopy(original)
                batch['reviews'] = [r for r in batch['reviews'] if not r['pair_id'].endswith(fragment)]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_tlslite_four_after_regressions_require_explicit_negative_deferral(self):
        name = consolidation.REVIEW_BATCHES[26]
        original = consolidation.audit.load(name)
        failed = [r for r in original['reviews'] if r.get('paired_negative_assessment') == 'unresolved_contract_regression']
        self.assertEqual(len(failed), 4)
        for record in failed:
            with self.subTest(pair_id=record['pair_id']):
                batch = deepcopy(original)
                item = next(r for r in batch['reviews'] if r['pair_id'] == record['pair_id'])
                item['experimental_subset_proposal'] = 'defer_missing_context'
                with self.assertRaisesRegex(AssertionError, 'after-contract failure'):
                    self.reviews(batch=batch, batch_name=name)

    def test_tlslite_uncertain_old_contracts_and_new_state_adapter_cannot_be_retained(self):
        name = consolidation.REVIEW_BATCHES[26]
        original = consolidation.audit.load(name)
        deferred = [r for r in original['reviews'] if r['experimental_subset_proposal'] == 'defer_existing_contract']
        self.assertEqual(len(deferred), 3)
        helper = next(r for r in original['reviews'] if r['pair_id'].endswith(':_parseKeyHelper'))
        self.assertEqual(helper['existing_contract'], 'no_selected_runtime_repair')
        for record in deferred + [helper]:
            with self.subTest(pair_id=record['pair_id']):
                batch = deepcopy(original)
                item = next(r for r in batch['reviews'] if r['pair_id'] == record['pair_id'])
                item['experimental_subset_proposal'] = 'conditional_retain'
                item['function_only_context'] = 'conditional_on_ordinary_api_semantics'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_tlslite_revisions_preserve_827_event_prefix_and_unclassified_identity(self):
        ledger = consolidation.audit.ROOT/'CATEGORY_AUDIT_LEDGER.jsonl'
        self.assertGreaterEqual(len(self.events), 831)
        self.assertEqual(consolidation.audit.sha(b''.join(ledger.read_bytes().splitlines(keepends=True)[:831])),
                         '9ca57ede950e4495ca81ef3c279a6ff7d312196473e270b47ad37fb68886c5c3')
        self.assertEqual(consolidation.audit.sha(b''.join(ledger.read_bytes().splitlines(keepends=True)[:827])),
                         '8b0f0e74c6a9a96b62ac9ca15164b9eeaceb87d10e5b070fc1d8c52fa3a6f359')
        self.assertEqual(len(self.events[827:831]), 4)
        for event in self.events[827:831]:
            history = [e for e in self.events if e['pair_id'] == event['pair_id']]
            self.assertEqual([e['revision'] for e in history], [1, 2])
            self.assertEqual([e['review_status'] for e in history],
                             ['assistant_proposed_exclusion', 'assistant_ambiguous'])
            self.assertIsNone(event['category_id'])
            self.assertEqual(self.train[event['pair_id']]['repository'], 'github.com/tlsfuzzer/tlslite-ng')
            for field in ('category_id', 'issue_family_id', 'inspected_code_sha256'):
                self.assertEqual(history[0][field], history[1][field])

    def test_tlslite_native_override_evidence_requires_matched_ref(self):
        name = consolidation.REVIEW_BATCHES[26]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if r['pair_id'].endswith(':RSAKey._raw_pkcs1_verify'))
        anchor = next(a for a in record['anchors'] if a.get('path') == 'tlslite/utils/openssl_rsakey.py')
        anchor.pop('ref')
        with self.assertRaisesRegex(AssertionError, 'unambiguous path/ref'):
            self.reviews(batch=batch, batch_name=name)

    def test_tlslite_advisory_retains_full_snapshot_and_tls_randomization_limit(self):
        evidence = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_027_CONTRACTS.json')
        source = next(s for s in evidence['sources'] if s['source_kind'] == 'mutable_advisory_api_snapshot')
        response = json.loads(source['api_response_text'])
        self.assertEqual(source['text'], source['api_response_text'])
        self.assertEqual(response['cve_id'], 'CVE-2020-26263')
        self.assertEqual(response['updated_at'], source['updated_at'])
        self.assertIn('this is known to not be the case', response['description'])
        batch = consolidation.audit.load(consolidation.REVIEW_BATCHES[26])
        record = next(r for r in batch['reviews'] if r['pair_id'].endswith(':RSAKey.decrypt'))
        self.assertIn('already randomizes', record['contract_reason'])
        self.assertIn('not a reproduced remotely exploitable oracle', record['security_reason'])
        self.assertTrue(any(a.get('path') == 'tlslite/keyexchange.py' for a in record['anchors']))

    def test_nova_selection_includes_all_five_families_and_three_case_components(self):
        name = consolidation.REVIEW_BATCHES[27]
        original = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items() if row['repository'] == 'github.com/openstack/nova'}
        self.assertEqual({r['pair_id'] for r in original['reviews']}, ids)
        self.assertEqual(len(ids), 7)
        self.assertEqual(len({self.families[pid] for pid in ids}), 5)
        case_ids = {pid for pid in ids if self.latest[pid]['category_id'] == 'SEC-POLICY-CASE-NORMALIZATION'}
        self.assertEqual(len(case_ids), 3)
        for pid in sorted(case_ids):
            with self.subTest(pair_id=pid):
                batch = deepcopy(original)
                batch['reviews'] = [r for r in batch['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_nova_residual_and_introduced_failures_cannot_lose_negative_deferral(self):
        name = consolidation.REVIEW_BATCHES[27]
        original = consolidation.audit.load(name)
        failed = [r for r in original['reviews'] if 'paired_negative_assessment' in r]
        self.assertEqual(len(failed), 4)
        self.assertEqual(sum(r['paired_negative_assessment'] == 'unresolved_contract_failure' for r in failed), 1)
        self.assertEqual(sum(r['paired_negative_assessment'] == 'unresolved_contract_regression' for r in failed), 3)
        for record in failed:
            with self.subTest(pair_id=record['pair_id']):
                batch = deepcopy(original)
                item = next(r for r in batch['reviews'] if r['pair_id'] == record['pair_id'])
                item['experimental_subset_proposal'] = 'defer_missing_context'
                with self.assertRaisesRegex(AssertionError, 'after-contract failure'):
                    self.reviews(batch=batch, batch_name=name)

    def test_nova_helper_history_does_not_relabel_selected_pairs_or_families(self):
        ids = sorted(pid for pid, row in self.train.items() if row['repository'] == 'github.com/openstack/nova')
        injector, helper = self.train[ids[0]], self.train[ids[3]]
        after_lines, _ = consolidation.audit.source(injector, 'after')
        self.assertIn(helper['before'].strip(), ''.join(after_lines))
        self.assertNotEqual(injector['after_sha256'], helper['before_sha256'])
        self.assertNotEqual(self.families[ids[0]], self.families[ids[3]])
        batch = consolidation.audit.load(consolidation.REVIEW_BATCHES[27])
        self.assertEqual(batch['discovery_ledger_checkpoint'], {
            'events': 831, 'sha256': '9ca57ede950e4495ca81ef3c279a6ff7d312196473e270b47ad37fb68886c5c3'})
        ledger = consolidation.audit.ROOT/'CATEGORY_AUDIT_LEDGER.jsonl'
        self.assertEqual(consolidation.audit.sha(b''.join(ledger.read_bytes().splitlines(keepends=True)[:831])),
                         batch['discovery_ledger_checkpoint']['sha256'])

    def test_nova_same_path_delivery_evidence_needs_explicit_historical_ref(self):
        name = consolidation.REVIEW_BATCHES[27]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if r['pair_id'] == 'CVEfixes:132813494207412:155029054060270')
        anchor = next(a for a in record['anchors'] if a.get('path') == 'nova/virt/libvirt/driver.py')
        anchor.pop('ref')
        with self.assertRaisesRegex(AssertionError, 'unambiguous path/ref'):
            self.reviews(batch=batch, batch_name=name)

    def test_nova_archive_peer_origin_rejects_changed_proof_or_ref(self):
        evidence = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_028_PEERS.json')
        source = evidence['sources'][0]
        origin = consolidation.supplemental_origin(source, self.train, {})
        self.assertEqual(origin['url'], self.train[source['training_case']]['upstream_snapshots']['before']['url'])
        for field, value in (('ref', 'wrong-historical-ref'), ('archive_proof', {}),
                             ('training_case', 'held-out-not-in-training')):
            with self.subTest(field=field):
                altered = deepcopy(source)
                altered[field] = value
                with self.assertRaises(AssertionError):
                    consolidation.supplemental_origin(altered, self.train, {})

    def test_url_less_supplement_needs_a_verified_archive_peer_identity(self):
        source = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_028_PEERS.json')['sources'][0]
        altered = deepcopy(source)
        altered['source_kind'] = 'retained_source_text'
        with self.assertRaises(KeyError):
            consolidation.supplemental_origin(altered, self.train, {})

    def test_zulip_selection_cannot_drop_an_overlapping_upload_component(self):
        name = consolidation.REVIEW_BATCHES[28]
        original = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items() if row['repository'] == 'github.com/zulip/zulip'}
        self.assertEqual({r['pair_id'] for r in original['reviews']}, ids)
        self.assertEqual(len(ids), 7)
        self.assertEqual(len({self.families[pid] for pid in ids}), 4)
        uploads = {pid for pid in ids if self.train[pid]['path'] == 'zerver/views/upload.py'}
        self.assertEqual(len(uploads), 3)
        for pid in sorted(uploads):
            with self.subTest(pair_id=pid):
                batch = deepcopy(original)
                batch['reviews'] = [r for r in batch['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_zulip_unresolved_s3_delivery_cannot_be_promoted_to_retain(self):
        name = consolidation.REVIEW_BATCHES[28]
        original = consolidation.audit.load(name)
        deferred = [r for r in original['reviews'] if r['experimental_subset_proposal'] == 'defer_security_boundary']
        self.assertEqual(len(deferred), 3)
        for record in deferred:
            with self.subTest(pair_id=record['pair_id']):
                batch = deepcopy(original)
                item = next(r for r in batch['reviews'] if r['pair_id'] == record['pair_id'])
                item['experimental_subset_proposal'] = 'conditional_retain'
                item['function_only_context'] = 'conditional_on_ordinary_api_semantics'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_zulip_proxy_config_requires_exact_historical_ref(self):
        name = consolidation.REVIEW_BATCHES[28]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if r['pair_id'] == 'CVEfixes:138361432817692:139264948810741')
        anchor = next(a for a in record['anchors'] if a.get('path', '').endswith('uploads-internal.conf'))
        anchor.pop('ref')
        with self.assertRaisesRegex(AssertionError, 'unambiguous path/ref'):
            self.reviews(batch=batch, batch_name=name)

    def test_zulip_config_and_mime_evidence_matches_retained_admission_hashes(self):
        row = self.train['CVEfixes:138361432817692:139264948810741']
        sources = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_029_DELIVERY.json')['sources']
        for expected in row['admission_review']['context_files']:
            with self.subTest(path=expected['path']):
                matches = [s for s in sources if s['path'] == expected['path'] and s['ref'] == row['fixing_commit']]
                self.assertEqual(len(matches), 1)
                self.assertEqual(matches[0]['sha256'], expected['sha256'])
                self.assertEqual(consolidation.audit.sha(matches[0]['text']), expected['sha256'])

    def test_shuup_selection_preserves_both_ambiguous_and_supported_discovery(self):
        name = consolidation.REVIEW_BATCHES[29]
        original = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items() if row['repository'] == 'github.com/shuup/shuup'}
        self.assertEqual({r['pair_id'] for r in original['reviews']}, ids)
        self.assertEqual(len(ids), 7)
        self.assertEqual(len({self.families[pid] for pid in ids}), 1)
        self.assertEqual(sum(self.latest[pid]['review_status'] == 'assistant_ambiguous' for pid in ids), 6)
        for status in ('assistant_ambiguous', 'assistant_supported'):
            with self.subTest(discovery_status=status):
                pid = next(pid for pid in sorted(ids) if self.latest[pid]['review_status'] == status)
                batch = deepcopy(original)
                batch['reviews'] = [r for r in batch['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_shuup_retrieved_corpus_and_peers_match_immutable_training_sources(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_030_PEERS.json')['sources']
        self.assertEqual(len(peers), 14)
        corpora = [consolidation.audit.load(f'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_030_{suffix}.json')
                   for suffix in ('SEARCH', 'CONTEXT')]
        self.assertEqual(corpora[0]['archive_url'], corpora[1]['archive_url'])
        self.assertEqual(corpora[0]['archive_sha256'], corpora[1]['archive_sha256'])
        for peer in peers:
            row = self.train[peer['training_case']]
            side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
            lines, proof = consolidation.audit.source(row, side)
            self.assertEqual(peer['archive_proof'], proof)
            self.assertEqual(peer['text'], ''.join(lines))
            self.assertEqual(peer['sha256'], row['upstream_snapshots'][side]['sha256'])
            for corpus in corpora:
                for source in corpus['sources']:
                    if (source['path'], source['ref']) == (peer['path'], peer['ref']):
                        self.assertEqual(source['text'], peer['text'])
                        self.assertEqual(source['sha256'], peer['sha256'])

    def test_shuup_identical_old_after_template_still_requires_explicit_ref(self):
        name = consolidation.REVIEW_BATCHES[29]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if r['pair_id'] == 'CVEfixes:225114817513454:76918662907619')
        anchor = next(a for a in record['anchors'] if a.get('path') == 'shuup/front/templates/shuup/front/problem.jinja')
        sources = [s for s in consolidation.audit.load(anchor['file'])['sources'] if s['path'] == anchor['path']]
        self.assertEqual(len(sources), 2)
        self.assertEqual(sources[0]['sha256'], sources[1]['sha256'])
        anchor.pop('ref')
        with self.assertRaisesRegex(AssertionError, 'unambiguous path/ref'):
            self.reviews(batch=batch, batch_name=name)

    def test_ytdlp_selection_preserves_nested_and_successive_cookie_representations(self):
        name = consolidation.REVIEW_BATCHES[30]
        original = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items() if row['repository'] == 'github.com/yt-dlp/yt-dlp'}
        self.assertEqual({r['pair_id'] for r in original['reviews']}, ids)
        self.assertEqual(len(ids), 7)
        self.assertEqual(len({self.families[pid] for pid in ids}), 3)
        self.assertEqual(sum(self.latest[pid]['review_status'] == 'assistant_ambiguous' for pid in ids), 1)
        for pid in ('CVEfixes:1244687962110:150148805336597',
                    'CVEfixes:1244687962110:245376085224988',
                    'CVEfixes:65969548864427:34066104510263',
                    'CVEfixes:71516930378917:28977003986818'):
            with self.subTest(pair_id=pid):
                batch = deepcopy(original)
                batch['reviews'] = [r for r in batch['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_ytdlp_peers_match_training_spans_and_retrieved_context(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_031_PEERS.json')['sources']
        self.assertEqual(len(peers), 12)
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_031_CONTEXT.json')['sources']
        for peer in peers:
            row = self.train[peer['training_case']]
            side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
            lines, proof = consolidation.audit.source(row, side)
            self.assertEqual(peer['archive_proof'], proof)
            self.assertEqual(peer['text'], ''.join(lines))
            self.assertEqual(peer['sha256'], row['upstream_snapshots'][side]['sha256'])
            for source in context:
                if (source['path'], source['ref']) == (peer['path'], peer['ref']):
                    self.assertEqual(source['text'], peer['text'])
                    self.assertEqual(source['sha256'], peer['sha256'])

    def test_ytdlp_quoting_modes_require_explicit_versioned_evidence(self):
        name = consolidation.REVIEW_BATCHES[30]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews'] if r['pair_id'] == 'CVEfixes:1244687962110:150148805336597')
        anchor = next(a for a in record['anchors'] if a.get('path') == 'yt_dlp/utils/_utils.py')
        anchor.pop('ref')
        with self.assertRaisesRegex(AssertionError, 'unambiguous path/ref'):
            self.reviews(batch=batch, batch_name=name)

    def test_cookiecutter_remaining_selection_includes_all_null_components(self):
        name = consolidation.REVIEW_BATCHES[31]
        batch = consolidation.audit.load(name)
        prior = {r['pair_id'] for r in consolidation.audit.load(consolidation.REVIEW_BATCHES[3])['reviews']}
        all_ids = {pid for pid, row in self.train.items() if row['repository'] == 'github.com/cookiecutter/cookiecutter'}
        self.assertEqual(len(all_ids), 9)
        self.assertEqual({r['pair_id'] for r in batch['reviews']}, all_ids - prior)
        self.assertEqual(len({self.families[pid] for pid in all_ids}), 5)
        unclassified = [pid for pid in all_ids - prior if self.latest[pid]['category_id'] is None]
        self.assertEqual(len(unclassified), 4)
        for pid in sorted(unclassified):
            with self.subTest(pair_id=pid):
                altered = deepcopy(batch)
                altered['reviews'] = [r for r in altered['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=altered, batch_name=name)

    def test_cookiecutter_prompt_revision_preserves_prior_identity_and_831_prefix(self):
        ledger = consolidation.audit.ROOT/'CATEGORY_AUDIT_LEDGER.jsonl'
        self.assertGreaterEqual(len(self.events), 832)
        self.assertEqual(consolidation.audit.sha(b''.join(ledger.read_bytes().splitlines(keepends=True)[:832])),
                         '77d3003fbedadf6b27134179e2da0b0164693a1eb7ee572a1850a8d9ba10771c')
        self.assertEqual(consolidation.audit.sha(b''.join(ledger.read_bytes().splitlines(keepends=True)[:831])),
                         '9ca57ede950e4495ca81ef3c279a6ff7d312196473e270b47ad37fb68886c5c3')
        pid = 'HaPy-Bug:bugs-in-py_cookiecutter-3:0:cookiecutter/prompt.py:read_user_choice'
        history = [e for e in self.events if e['pair_id'] == pid]
        self.assertEqual([e['revision'] for e in history], [1, 2])
        self.assertEqual([e['review_status'] for e in history],
                         ['assistant_proposed_exclusion', 'assistant_ambiguous'])
        for field in ('category_id', 'issue_family_id', 'inspected_code_sha256'):
            self.assertEqual(history[0][field], history[1][field])
        self.assertIsNone(history[1]['category_id'])

    def test_cookiecutter_after_compatibility_failure_cannot_be_silently_retained(self):
        name = consolidation.REVIEW_BATCHES[31]
        for mutation in ('proposal', 'scope'):
            with self.subTest(mutation=mutation):
                batch = deepcopy(consolidation.audit.load(name))
                record = next(r for r in batch['reviews'] if r.get('paired_negative_assessment') == 'unresolved_contract_regression')
                if mutation == 'proposal':
                    record['experimental_subset_proposal'] = 'defer_missing_context'
                else:
                    record['paired_negative_scope'] = 'mechanism_local_only'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_cookiecutter_peers_match_archive_proofs_and_resolved_parent_context(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_032_PEERS.json')['sources']
        self.assertEqual(len(peers), 8)
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_032_CONTEXT.json')['sources']
        for peer in peers:
            row = self.train[peer['training_case']]
            side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
            lines, proof = consolidation.audit.source(row, side)
            self.assertEqual(peer['archive_proof'], proof)
            self.assertEqual(peer['text'], ''.join(lines))
            self.assertEqual(peer['sha256'], row['full_file_sha256'][side])
            for source in context:
                if (source['path'], source['ref']) == (peer['path'], peer['ref']):
                    self.assertEqual(source['text'], peer['text'])
                    self.assertEqual(source['sha256'], peer['sha256'])

    def test_swift_complete_family_cannot_omit_ambiguous_policy_components(self):
        name = consolidation.REVIEW_BATCHES[32]
        batch = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items() if row['repository'] == 'github.com/openstack/swift'}
        self.assertEqual(len(ids), 6)
        self.assertEqual({r['pair_id'] for r in batch['reviews']}, ids)
        self.assertEqual(len({self.families[pid] for pid in ids}), 1)
        ambiguous = [pid for pid in ids if self.latest[pid]['review_status'] == 'assistant_ambiguous']
        self.assertEqual(len(ambiguous), 4)
        for pid in sorted(ambiguous):
            with self.subTest(pair_id=pid):
                altered = deepcopy(batch)
                altered['reviews'] = [r for r in altered['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=altered, batch_name=name)

    def test_swift_legacy_mode_failure_cannot_be_silently_retained(self):
        name = consolidation.REVIEW_BATCHES[32]
        for mutation in ('proposal', 'scope'):
            with self.subTest(mutation=mutation):
                batch = deepcopy(consolidation.audit.load(name))
                record = next(r for r in batch['reviews'] if r.get('paired_negative_assessment') == 'unresolved_contract_regression')
                self.assertIn('middleware/memcache.py', record['pair_id'])
                if mutation == 'proposal':
                    record['experimental_subset_proposal'] = 'defer_selected_attribution'
                else:
                    record['paired_negative_scope'] = 'mechanism_local_only'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_swift_deduplicated_peers_match_both_selected_files_and_parent_context(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_033_PEERS.json')['sources']
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_033_CONTEXT.json')['sources']
        self.assertEqual(len(peers), 4)
        self.assertEqual(len({p['path'] for p in peers}), 2)
        for peer in peers:
            row = self.train[peer['training_case']]
            side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
            lines, proof = consolidation.audit.source(row, side)
            self.assertEqual(peer['archive_proof'], proof)
            self.assertEqual(peer['text'], ''.join(lines))
            self.assertEqual(peer['sha256'], row['full_file_sha256'][side])
            matches = [s for s in context if (s['path'], s['ref']) == (peer['path'], peer['ref'])]
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]['text'], peer['text'])
            self.assertEqual(matches[0]['sha256'], peer['sha256'])

    def test_pysaml2_complete_family_cannot_omit_a_selected_parser(self):
        name = consolidation.REVIEW_BATCHES[33]
        batch = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items() if row['repository'] == 'github.com/rohe/pysaml2'}
        self.assertEqual(len(ids), 6)
        self.assertEqual({r['pair_id'] for r in batch['reviews']}, ids)
        self.assertEqual(len({self.families[pid] for pid in ids}), 1)
        for pid in sorted(ids):
            with self.subTest(pair_id=pid):
                altered = deepcopy(batch)
                altered['reviews'] = [r for r in altered['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=altered, batch_name=name)

    def test_pysaml2_unresolved_delivery_blocks_retain_even_with_ordinary_context(self):
        name = consolidation.REVIEW_BATCHES[33]
        original = consolidation.audit.load(name)
        unresolved = [r['pair_id'] for r in original['reviews'] if r['security_screen'] == 'unresolved_boundary']
        self.assertEqual(len(unresolved), 3)
        for pid in unresolved:
            with self.subTest(pair_id=pid):
                batch = deepcopy(original)
                record = next(r for r in batch['reviews'] if r['pair_id'] == pid)
                record['experimental_subset_proposal'] = 'conditional_retain'
                record['function_only_context'] = 'conditional_on_ordinary_api_semantics'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_pysaml2_six_peers_match_all_three_selected_files_and_parent_context(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_034_PEERS.json')['sources']
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_034_CONTEXT.json')['sources']
        self.assertEqual(len(peers), 6)
        self.assertEqual(len({p['path'] for p in peers}), 3)
        for peer in peers:
            row = self.train[peer['training_case']]
            side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
            lines, proof = consolidation.audit.source(row, side)
            self.assertEqual(peer['archive_proof'], proof)
            self.assertEqual(peer['text'], ''.join(lines))
            self.assertEqual(peer['sha256'], row['full_file_sha256'][side])
            matches = [s for s in context if (s['path'], s['ref']) == (peer['path'], peer['ref'])]
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]['text'], peer['text'])
            self.assertEqual(matches[0]['sha256'], peer['sha256'])

    def test_sydent_complete_repository_includes_previously_ambiguous_address(self):
        name = consolidation.REVIEW_BATCHES[34]
        batch = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items() if row['repository'] == 'github.com/matrix-org/sydent'}
        self.assertEqual(len(ids), 6)
        self.assertEqual({r['pair_id'] for r in batch['reviews']}, ids)
        self.assertEqual(len({self.families[pid] for pid in ids}), 5)
        for pid in sorted(ids):
            with self.subTest(pair_id=pid):
                altered = deepcopy(batch)
                altered['reviews'] = [r for r in altered['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=altered, batch_name=name)

    def test_sydent_address_revision_preserves_identity_and_832_prefix(self):
        ledger = consolidation.audit.ROOT/'CATEGORY_AUDIT_LEDGER.jsonl'
        self.assertEqual(len(self.events), 833)
        self.assertEqual(consolidation.audit.file_sha(ledger),
                         'e9d9086397f5b960af9df2784a0e0073bf7afeaa9b5edceca61b382bc9e8744a')
        self.assertEqual(consolidation.audit.sha(b''.join(ledger.read_bytes().splitlines(keepends=True)[:832])),
                         '77d3003fbedadf6b27134179e2da0b0164693a1eb7ee572a1850a8d9ba10771c')
        pid = 'HaPy-Bug:cve_CVE-2019-11340:0:sydent/util/emailutils.py:sendEmail'
        history = [e for e in self.events if e['pair_id'] == pid]
        self.assertEqual([e['revision'] for e in history], [1, 2])
        self.assertEqual([e['review_status'] for e in history], ['assistant_ambiguous', 'assistant_supported'])
        for field in ('category_id', 'issue_family_id', 'inspected_code_sha256'):
            self.assertEqual(history[0][field], history[1][field])

    def test_sydent_introduced_and_residual_after_failures_cannot_be_silently_retained(self):
        name = consolidation.REVIEW_BATCHES[34]
        original = consolidation.audit.load(name)
        unresolved = [r for r in original['reviews'] if r.get('paired_negative_assessment')]
        self.assertEqual({r['paired_negative_assessment'] for r in unresolved},
                         {'unresolved_contract_regression', 'unresolved_contract_failure'})
        for item in unresolved:
            for mutation in ('proposal', 'scope'):
                with self.subTest(pair_id=item['pair_id'], mutation=mutation):
                    batch = deepcopy(original)
                    record = next(r for r in batch['reviews'] if r['pair_id'] == item['pair_id'])
                    if mutation == 'proposal':
                        record['experimental_subset_proposal'] = 'defer_missing_context'
                    else:
                        record['paired_negative_scope'] = 'mechanism_local_only'
                    with self.assertRaises(AssertionError):
                        self.reviews(batch=batch, batch_name=name)

    def test_sydent_mixed_origin_peers_match_resolved_parent_context(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_035_PEERS.json')['sources']
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_035_CONTEXT.json')['sources']
        self.assertEqual(len(peers), 10)
        self.assertEqual({self.train[p['training_case']]['source'] for p in peers}, {'CVEfixes', 'HaPy-Bug'})
        for peer in peers:
            row = self.train[peer['training_case']]
            side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
            lines, proof = consolidation.audit.source(row, side)
            self.assertEqual(peer['archive_proof'], proof)
            self.assertEqual(peer['text'], ''.join(lines))
            self.assertEqual(peer['sha256'], proof['sha256'])
            matches = [s for s in context if (s['path'], s['ref']) == (peer['path'], peer['ref'])]
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]['text'], peer['text'])
            self.assertEqual(matches[0]['sha256'], peer['sha256'])

    def test_pyload_exhaustive_repository_selection_rejects_missing_case(self):
        name = consolidation.REVIEW_BATCHES[35]
        batch = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items() if row['repository'] == 'github.com/pyload/pyload'}
        self.assertEqual(len(ids), 6)
        self.assertEqual({r['pair_id'] for r in batch['reviews']}, ids)
        self.assertEqual(len({self.families[pid] for pid in ids}), 5)
        for pid in sorted(ids):
            with self.subTest(pair_id=pid):
                altered = deepcopy(batch)
                altered['reviews'] = [r for r in altered['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=altered, batch_name=name)

    def test_pyload_supported_after_regression_cannot_be_downgraded_to_context_only(self):
        name = consolidation.REVIEW_BATCHES[35]
        original = consolidation.audit.load(name)
        for mutation in ('proposal', 'scope'):
            with self.subTest(mutation=mutation):
                batch = deepcopy(original)
                record = next(r for r in batch['reviews'] if r.get('paired_negative_assessment'))
                self.assertEqual(record['paired_negative_assessment'], 'unresolved_contract_regression')
                if mutation == 'proposal':
                    record['experimental_subset_proposal'] = 'defer_missing_context'
                else:
                    record['paired_negative_scope'] = 'mechanism_local_only'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_pyload_peers_match_each_resolved_before_after_source(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_036_PEERS.json')['sources']
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_036_CONTEXT.json')
        self.assertEqual(len(peers), 12)
        for peer in peers:
            row = self.train[peer['training_case']]
            side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
            expected_ref = row['fixing_commit'] if side == 'after' else context['parents'][row['fixing_commit']]
            self.assertEqual(peer['ref'], expected_ref)
            lines, proof = consolidation.audit.source(row, side)
            self.assertEqual(peer['archive_proof'], proof)
            self.assertEqual(peer['text'], ''.join(lines))
            self.assertEqual(peer['sha256'], proof['sha256'])
            matches = [s for s in context['sources'] if (s['path'], s['ref']) == (peer['path'], peer['ref'])]
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]['text'], peer['text'])

    def test_markdown_complete_selection_preserves_all_discovery_statuses(self):
        name = consolidation.REVIEW_BATCHES[36]
        batch = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items()
               if row['repository'] == 'github.com/executablebooks/markdown-it-py'}
        self.assertEqual(len(ids), 6)
        self.assertEqual({r['pair_id'] for r in batch['reviews']}, ids)
        self.assertEqual(len({self.families[pid] for pid in ids}), 2)
        self.assertEqual({self.latest[pid]['review_status'] for pid in ids},
                         {'assistant_supported', 'assistant_ambiguous'})
        for pid in sorted(ids):
            with self.subTest(pair_id=pid):
                altered = deepcopy(batch)
                altered['reviews'] = [r for r in altered['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=altered, batch_name=name)

    def test_markdown_cli_after_regression_cannot_be_silently_retained(self):
        name = consolidation.REVIEW_BATCHES[36]
        original = consolidation.audit.load(name)
        for mutation in ('proposal', 'scope'):
            with self.subTest(mutation=mutation):
                batch = deepcopy(original)
                record = next(r for r in batch['reviews'] if r.get('paired_negative_assessment'))
                self.assertEqual(record['paired_negative_assessment'], 'unresolved_contract_regression')
                if mutation == 'proposal':
                    record['experimental_subset_proposal'] = 'defer_missing_context'
                else:
                    record['paired_negative_scope'] = 'mechanism_local_only'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_markdown_shared_file_peers_match_resolved_before_after_archives(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_037_PEERS.json')['sources']
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_037_CONTEXT.json')
        self.assertEqual(len(peers), 8)
        for peer in peers:
            row = self.train[peer['training_case']]
            side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
            expected_ref = row['fixing_commit'] if side == 'after' else context['parents'][row['fixing_commit']]
            self.assertEqual(peer['ref'], expected_ref)
            lines, proof = consolidation.audit.source(row, side)
            self.assertEqual(peer['archive_proof'], proof)
            self.assertEqual(peer['text'], ''.join(lines))
            self.assertEqual(peer['sha256'], proof['sha256'])
            matches = [s for s in context['sources'] if (s['path'], s['ref']) == (peer['path'], peer['ref'])]
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]['text'], peer['text'])

    def test_langchain_complete_selection_preserves_all_discovery_statuses(self):
        name = consolidation.REVIEW_BATCHES[37]
        batch = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items()
               if row['repository'] == 'github.com/langchain-ai/langchain'}
        self.assertEqual(len(ids), 6)
        self.assertEqual({r['pair_id'] for r in batch['reviews']}, ids)
        self.assertEqual(len({self.families[pid] for pid in ids}), 4)
        self.assertEqual({self.latest[pid]['review_status'] for pid in ids},
                         {'assistant_supported', 'assistant_ambiguous'})
        for pid in sorted(ids):
            with self.subTest(pair_id=pid):
                altered = deepcopy(batch)
                altered['reviews'] = [r for r in altered['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=altered, batch_name=name)

    def test_langchain_after_regressions_cannot_be_silently_retained(self):
        name = consolidation.REVIEW_BATCHES[37]
        original = consolidation.audit.load(name)
        ids = [r['pair_id'] for r in original['reviews'] if r.get('paired_negative_assessment')]
        self.assertEqual(len(ids), 3)
        for pid in ids:
            for mutation in ('proposal', 'scope'):
                with self.subTest(pair_id=pid, mutation=mutation):
                    batch = deepcopy(original)
                    record = next(r for r in batch['reviews'] if r['pair_id'] == pid)
                    self.assertEqual(record['paired_negative_assessment'], 'unresolved_contract_regression')
                    if mutation == 'proposal':
                        record['experimental_subset_proposal'] = 'defer_missing_context'
                    else:
                        record['paired_negative_scope'] = 'mechanism_local_only'
                    with self.assertRaises(AssertionError):
                        self.reviews(batch=batch, batch_name=name)

    def test_langchain_shared_file_peers_match_resolved_before_after_archives(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_038_PEERS.json')['sources']
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_038_CONTEXT.json')
        self.assertEqual(len(peers), 8)
        for peer in peers:
            row = self.train[peer['training_case']]
            side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
            expected_ref = row['fixing_commit'] if side == 'after' else context['parents'][row['fixing_commit']]
            self.assertEqual(peer['ref'], expected_ref)
            lines, proof = consolidation.audit.source(row, side)
            self.assertEqual(peer['archive_proof'], proof)
            self.assertEqual(peer['text'], ''.join(lines))
            self.assertEqual(peer['sha256'], proof['sha256'])
            matches = [s for s in context['sources'] if (s['path'], s['ref']) == (peer['path'], peer['ref'])]
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]['text'], peer['text'])

    def test_tensorflow_complete_selection_includes_null_producer_exclusion(self):
        name = consolidation.REVIEW_BATCHES[38]
        batch = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items()
               if row['repository'] == 'github.com/tensorflow/tensorflow'}
        self.assertEqual(len(ids), 5)
        self.assertEqual({r['pair_id'] for r in batch['reviews']}, ids)
        self.assertEqual(len({self.families[pid] for pid in ids}), 2)
        self.assertEqual({self.latest[pid]['review_status'] for pid in ids},
                         {'assistant_supported', 'assistant_proposed_exclusion'})
        self.assertEqual(sum(self.latest[pid]['category_id'] is None for pid in ids), 1)
        for pid in sorted(ids):
            with self.subTest(pair_id=pid):
                altered = deepcopy(batch)
                altered['reviews'] = [r for r in altered['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=altered, batch_name=name)

    def test_tensorflow_retirement_and_security_deferrals_cannot_be_bypassed(self):
        name = consolidation.REVIEW_BATCHES[38]
        original = consolidation.audit.load(name)
        scoped = [r['pair_id'] for r in original['reviews']
                  if r['experimental_subset_proposal'] == 'defer_task_scope']
        security = [r['pair_id'] for r in original['reviews']
                    if r['experimental_subset_proposal'] == 'defer_security_boundary']
        self.assertEqual(len(scoped), 1)
        self.assertEqual(len(security), 3)
        for pid in scoped + security:
            with self.subTest(pair_id=pid):
                batch = deepcopy(original)
                record = next(r for r in batch['reviews'] if r['pair_id'] == pid)
                record['experimental_subset_proposal'] = (
                    'defer_missing_context' if pid in scoped else 'conditional_retain')
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_tensorflow_shared_file_peers_match_resolved_before_after_sources(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_039_PEERS.json')['sources']
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_039_CONTEXT.json')
        self.assertEqual(len(peers), 8)
        for peer in peers:
            row = self.train[peer['training_case']]
            side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
            expected_ref = row['fixing_commit'] if side == 'after' else context['parents'][row['fixing_commit']]
            self.assertEqual(peer['ref'], expected_ref)
            lines, proof = consolidation.audit.source(row, side)
            self.assertEqual(peer['archive_proof'], proof)
            self.assertEqual(peer['text'], ''.join(lines))
            self.assertEqual(peer['sha256'], proof['sha256'])
            matches = [s for s in context['sources'] if (s['path'], s['ref']) == (peer['path'], peer['ref'])]
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]['text'], peer['text'])

    def test_twisted_complete_selection_preserves_all_discovery_statuses(self):
        name = consolidation.REVIEW_BATCHES[39]
        batch = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items()
               if row['repository'] == 'github.com/twisted/twisted'}
        self.assertEqual(len(ids), 5)
        self.assertEqual({r['pair_id'] for r in batch['reviews']}, ids)
        self.assertEqual(len({self.families[pid] for pid in ids}), 2)
        self.assertEqual(sum(self.latest[pid]['category_id'] is None for pid in ids), 0)
        for pid in sorted(ids):
            with self.subTest(pair_id=pid):
                altered = deepcopy(batch)
                altered['reviews'] = [r for r in altered['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=altered, batch_name=name)

    def test_saleor_complete_selection_includes_null_cleaner_and_ambiguous_catch(self):
        name = consolidation.REVIEW_BATCHES[40]
        batch = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items()
               if row['repository'] == 'github.com/saleor/saleor'}
        self.assertEqual(len(ids), 5)
        self.assertEqual({r['pair_id'] for r in batch['reviews']}, ids)
        self.assertEqual(len({self.families[pid] for pid in ids}), 3)
        self.assertEqual({self.latest[pid]['review_status'] for pid in ids},
                         {'assistant_supported', 'assistant_ambiguous', 'assistant_proposed_exclusion'})
        self.assertEqual(sum(self.latest[pid]['category_id'] is None for pid in ids), 2)
        for pid in sorted(ids):
            with self.subTest(pair_id=pid):
                altered = deepcopy(batch)
                altered['reviews'] = [r for r in altered['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=altered, batch_name=name)

    def test_twisted_saleor_security_attribution_and_nonrepair_cannot_be_promoted(self):
        for name in consolidation.REVIEW_BATCHES[39:41]:
            original = consolidation.audit.load(name)
            for item in original['reviews']:
                with self.subTest(batch=name, pair_id=item['pair_id']):
                    batch = deepcopy(original)
                    record = next(r for r in batch['reviews'] if r['pair_id'] == item['pair_id'])
                    record['experimental_subset_proposal'] = 'conditional_retain'
                    with self.assertRaises(AssertionError):
                        self.reviews(batch=batch, batch_name=name)

    def test_twisted_saleor_shared_peers_match_resolved_before_after_archives(self):
        for number, count in (('040', 4), ('041', 6)):
            peers = consolidation.audit.load(f'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_{number}_PEERS.json')['sources']
            context = consolidation.audit.load(f'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_{number}_CONTEXT.json')
            self.assertEqual(len(peers), count)
            for peer in peers:
                with self.subTest(batch=number, ref=peer['ref'], path=peer['path']):
                    row = self.train[peer['training_case']]
                    side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
                    expected_ref = row['fixing_commit'] if side == 'after' else context['parents'][row['fixing_commit']]
                    self.assertEqual(peer['ref'], expected_ref)
                    lines, proof = consolidation.audit.source(row, side)
                    self.assertEqual(peer['archive_proof'], proof)
                    self.assertEqual(peer['text'], ''.join(lines))
                    self.assertEqual(peer['sha256'], proof['sha256'])
                    matches = [s for s in context['sources'] if (s['path'], s['ref']) == (peer['path'], peer['ref'])]
                    self.assertEqual(len(matches), 1)
                    self.assertEqual(matches[0]['text'], peer['text'])

    def test_keystone_complete_selection_preserves_both_token_revisions(self):
        name = consolidation.REVIEW_BATCHES[41]
        batch = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items()
               if row['repository'] == 'github.com/openstack/keystone'}
        self.assertEqual(len(ids), 4)
        self.assertEqual({r['pair_id'] for r in batch['reviews']}, ids)
        self.assertEqual(len({self.families[pid] for pid in ids}), 3)
        self.assertEqual({self.latest[pid]['review_status'] for pid in ids}, {'assistant_supported'})
        self.assertEqual(sum(self.latest[pid]['category_id'] is None for pid in ids), 0)
        for pid in sorted(ids):
            with self.subTest(pair_id=pid):
                altered = deepcopy(batch)
                altered['reviews'] = [r for r in altered['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=altered, batch_name=name)

    def test_keystone_expiry_positive_after_cannot_be_silently_retained(self):
        name = consolidation.REVIEW_BATCHES[41]
        original = consolidation.audit.load(name)
        records = sorted(original['reviews'], key=lambda r: r['pair_id'])
        earlier, later = records[:2]
        self.assertEqual(self.train[earlier['pair_id']]['after'], self.train[later['pair_id']]['before'])
        self.assertEqual(earlier['paired_negative_assessment'], 'unresolved_contract_failure')
        for mutation in ('proposal', 'scope'):
            with self.subTest(mutation=mutation):
                batch = deepcopy(original)
                record = next(r for r in batch['reviews'] if r['pair_id'] == earlier['pair_id'])
                if mutation == 'proposal':
                    record['experimental_subset_proposal'] = 'defer_missing_context'
                else:
                    record['paired_negative_scope'] = 'mechanism_local_only'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_keystone_log_security_delivery_cannot_be_silently_promoted(self):
        name = consolidation.REVIEW_BATCHES[41]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(r for r in batch['reviews']
                      if r['experimental_subset_proposal'] == 'defer_security_boundary')
        self.assertEqual(record['security_screen'], 'unresolved_boundary')
        record['experimental_subset_proposal'] = 'conditional_retain'
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_keystone_shared_peers_match_resolved_before_after_archives(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_042_PEERS.json')['sources']
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_042_CONTEXT.json')
        self.assertEqual(len(peers), 8)
        for peer in peers:
            with self.subTest(ref=peer['ref'], path=peer['path']):
                row = self.train[peer['training_case']]
                side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
                expected_ref = row['fixing_commit'] if side == 'after' else context['parents'][row['fixing_commit']]
                self.assertEqual(peer['ref'], expected_ref)
                lines, proof = consolidation.audit.source(row, side)
                self.assertEqual(peer['archive_proof'], proof)
                self.assertEqual(peer['text'], ''.join(lines))
                self.assertEqual(peer['sha256'], proof['sha256'])
                matches = [s for s in context['sources'] if (s['path'], s['ref']) == (peer['path'], peer['ref'])]
                self.assertEqual(len(matches), 1)
                self.assertEqual(matches[0]['text'], peer['text'])

    def test_pyoidc_complete_selection_includes_null_hash_exclusion(self):
        name = consolidation.REVIEW_BATCHES[42]
        batch = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items()
               if row['repository'] == 'github.com/openidc/pyoidc'}
        self.assertEqual(len(ids), 4)
        self.assertEqual({r['pair_id'] for r in batch['reviews']}, ids)
        self.assertEqual(len({self.families[pid] for pid in ids}), 1)
        self.assertEqual({self.latest[pid]['review_status'] for pid in ids},
                         {'assistant_supported', 'assistant_ambiguous', 'assistant_proposed_exclusion'})
        self.assertEqual(sum(self.latest[pid]['category_id'] is None for pid in ids), 1)
        for pid in sorted(ids):
            with self.subTest(pair_id=pid):
                altered = deepcopy(batch)
                altered['reviews'] = [r for r in altered['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=altered, batch_name=name)

    def test_pyoidc_code_callback_residual_cannot_be_silently_retained(self):
        name = consolidation.REVIEW_BATCHES[42]
        original = consolidation.audit.load(name)
        for mutation in ('proposal', 'scope'):
            with self.subTest(mutation=mutation):
                batch = deepcopy(original)
                record = next(r for r in batch['reviews'] if r.get('paired_negative_assessment'))
                self.assertEqual(record['paired_negative_assessment'], 'unresolved_contract_failure')
                if mutation == 'proposal':
                    record['experimental_subset_proposal'] = 'defer_missing_context'
                else:
                    record['paired_negative_scope'] = 'mechanism_local_only'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_pyoidc_security_attribution_and_nonrepair_cannot_be_promoted(self):
        name = consolidation.REVIEW_BATCHES[42]
        original = consolidation.audit.load(name)
        for item in original['reviews']:
            with self.subTest(pair_id=item['pair_id']):
                batch = deepcopy(original)
                record = next(r for r in batch['reviews'] if r['pair_id'] == item['pair_id'])
                record['experimental_subset_proposal'] = 'conditional_retain'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_pyoidc_shared_peers_match_resolved_before_after_archives(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_043_PEERS.json')['sources']
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_043_CONTEXT.json')
        self.assertEqual(len(peers), 6)
        for peer in peers:
            with self.subTest(ref=peer['ref'], path=peer['path']):
                row = self.train[peer['training_case']]
                side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
                expected_ref = row['fixing_commit'] if side == 'after' else context['parents'][row['fixing_commit']]
                self.assertEqual(peer['ref'], expected_ref)
                lines, proof = consolidation.audit.source(row, side)
                self.assertEqual(peer['archive_proof'], proof)
                self.assertEqual(peer['text'], ''.join(lines))
                self.assertEqual(peer['sha256'], proof['sha256'])
                matches = [s for s in context['sources'] if (s['path'], s['ref']) == (peer['path'], peer['ref'])]
                self.assertEqual(len(matches), 1)
                self.assertEqual(matches[0]['text'], peer['text'])

    def test_urllib3_complete_selection_includes_null_mislinked_percent_pair(self):
        name = consolidation.REVIEW_BATCHES[43]
        batch = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items()
               if row['repository'] == 'github.com/urllib3/urllib3'}
        self.assertEqual(len(ids), 4)
        self.assertEqual({r['pair_id'] for r in batch['reviews']}, ids)
        self.assertEqual(len({self.families[pid] for pid in ids}), 4)
        self.assertEqual({self.latest[pid]['review_status'] for pid in ids},
                         {'assistant_supported', 'assistant_proposed_exclusion'})
        self.assertEqual(sum(self.latest[pid]['category_id'] is None for pid in ids), 1)
        for pid in sorted(ids):
            with self.subTest(pair_id=pid):
                altered = deepcopy(batch)
                altered['reviews'] = [r for r in altered['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=altered, batch_name=name)

    def test_urllib3_casing_after_body_residual_cannot_be_silently_retained(self):
        name = consolidation.REVIEW_BATCHES[43]
        original = consolidation.audit.load(name)
        for mutation in ('proposal', 'scope'):
            with self.subTest(mutation=mutation):
                batch = deepcopy(original)
                record = next(r for r in batch['reviews'] if r.get('paired_negative_assessment'))
                self.assertEqual(record['paired_negative_assessment'], 'unresolved_contract_failure')
                if mutation == 'proposal':
                    record['experimental_subset_proposal'] = 'defer_missing_context'
                else:
                    record['paired_negative_scope'] = 'mechanism_local_only'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_urllib3_context_and_mislinked_nonrepair_cannot_be_promoted(self):
        name = consolidation.REVIEW_BATCHES[43]
        original = consolidation.audit.load(name)
        for item in original['reviews']:
            with self.subTest(pair_id=item['pair_id']):
                batch = deepcopy(original)
                record = next(r for r in batch['reviews'] if r['pair_id'] == item['pair_id'])
                record['experimental_subset_proposal'] = 'conditional_retain'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_urllib3_shared_peers_match_resolved_before_after_archives(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_044_PEERS.json')['sources']
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_044_CONTEXT.json')
        self.assertEqual(len(peers), 8)
        self.assertEqual(len(context['parents']), 4)
        self.assertEqual(len(context['archives']), 8)
        for peer in peers:
            with self.subTest(ref=peer['ref'], path=peer['path']):
                row = self.train[peer['training_case']]
                side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
                expected_ref = row['fixing_commit'] if side == 'after' else context['parents'][row['fixing_commit']]
                self.assertEqual(peer['ref'], expected_ref)
                lines, proof = consolidation.audit.source(row, side)
                self.assertEqual(peer['archive_proof'], proof)
                self.assertEqual(peer['text'], ''.join(lines))
                self.assertEqual(peer['sha256'], proof['sha256'])
                matches = [s for s in context['sources'] if (s['path'], s['ref']) == (peer['path'], peer['ref'])]
                self.assertEqual(len(matches), 1)
                self.assertEqual(matches[0]['text'], peer['text'])

    def test_bcfg2_complete_selection_preserves_ambiguous_signing_and_shared_family(self):
        name = consolidation.REVIEW_BATCHES[44]
        batch = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items()
               if row['repository'] == 'github.com/solj/bcfg2'}
        self.assertEqual(len(ids), 4)
        self.assertEqual({r['pair_id'] for r in batch['reviews']}, ids)
        self.assertEqual(len({self.families[pid] for pid in ids}), 1)
        self.assertEqual({self.latest[pid]['review_status'] for pid in ids},
                         {'assistant_supported', 'assistant_ambiguous'})
        self.assertEqual(sum(self.latest[pid]['category_id'] is None for pid in ids), 0)
        for pid in sorted(ids):
            with self.subTest(pair_id=pid):
                altered = deepcopy(batch)
                altered['reviews'] = [r for r in altered['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=altered, batch_name=name)

    def test_bcfg2_introduced_and_residual_after_failures_need_paired_deferral(self):
        name = consolidation.REVIEW_BATCHES[44]
        original = consolidation.audit.load(name)
        assessed = [r for r in original['reviews'] if r.get('paired_negative_assessment')]
        self.assertEqual({r['paired_negative_assessment'] for r in assessed},
                         {'unresolved_contract_regression', 'unresolved_contract_failure'})
        for item in assessed:
            for mutation in ('proposal', 'scope'):
                with self.subTest(pair_id=item['pair_id'], mutation=mutation):
                    batch = deepcopy(original)
                    record = next(r for r in batch['reviews'] if r['pair_id'] == item['pair_id'])
                    if mutation == 'proposal':
                        record['experimental_subset_proposal'] = 'defer_missing_context'
                    else:
                        record['paired_negative_scope'] = 'mechanism_local_only'
                    with self.assertRaises(AssertionError):
                        self.reviews(batch=batch, batch_name=name)

    def test_bcfg2_context_security_and_signing_ambiguity_cannot_be_promoted(self):
        name = consolidation.REVIEW_BATCHES[44]
        original = consolidation.audit.load(name)
        for item in original['reviews']:
            with self.subTest(pair_id=item['pair_id']):
                batch = deepcopy(original)
                record = next(r for r in batch['reviews'] if r['pair_id'] == item['pair_id'])
                record['experimental_subset_proposal'] = 'conditional_retain'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_bcfg2_shared_peers_match_resolved_before_after_archives(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_045_PEERS.json')['sources']
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_045_CONTEXT.json')
        self.assertEqual(len(peers), 4)
        self.assertEqual(len(context['parents']), 1)
        self.assertEqual(len(context['archives']), 2)
        for peer in peers:
            with self.subTest(ref=peer['ref'], path=peer['path']):
                row = self.train[peer['training_case']]
                side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
                expected_ref = row['fixing_commit'] if side == 'after' else context['parents'][row['fixing_commit']]
                self.assertEqual(peer['ref'], expected_ref)
                lines, proof = consolidation.audit.source(row, side)
                self.assertEqual(peer['archive_proof'], proof)
                self.assertEqual(peer['text'], ''.join(lines))
                self.assertEqual(peer['sha256'], proof['sha256'])
                matches = [s for s in context['sources'] if (s['path'], s['ref']) == (peer['path'], peer['ref'])]
                self.assertEqual(len(matches), 1)
                self.assertEqual(matches[0]['text'], peer['text'])

    def test_swauth_complete_selection_preserves_ambiguous_deletion_and_shared_family(self):
        name = consolidation.REVIEW_BATCHES[45]
        batch = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items()
               if row['repository'] == 'github.com/openstack/swauth'}
        self.assertEqual(len(ids), 4)
        self.assertEqual({r['pair_id'] for r in batch['reviews']}, ids)
        self.assertEqual(len({self.families[pid] for pid in ids}), 1)
        self.assertEqual({self.latest[pid]['review_status'] for pid in ids},
                         {'assistant_supported', 'assistant_ambiguous'})
        self.assertEqual(sum(self.latest[pid]['category_id'] is None for pid in ids), 0)
        for pid in sorted(ids):
            with self.subTest(pair_id=pid):
                altered = deepcopy(batch)
                altered['reviews'] = [r for r in altered['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=altered, batch_name=name)

    def test_swauth_cached_token_deletion_residual_requires_paired_deferral(self):
        name = consolidation.REVIEW_BATCHES[45]
        original = consolidation.audit.load(name)
        for mutation in ('proposal', 'scope'):
            with self.subTest(mutation=mutation):
                batch = deepcopy(original)
                record = next(r for r in batch['reviews'] if r.get('paired_negative_assessment'))
                self.assertEqual(record['pair_id'], 'CVEfixes:88203329489273:6394449417396')
                self.assertEqual(record['paired_negative_assessment'], 'unresolved_contract_failure')
                if mutation == 'proposal':
                    record['experimental_subset_proposal'] = 'defer_missing_context'
                else:
                    record['paired_negative_scope'] = 'mechanism_local_only'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_swauth_context_and_cached_revocation_deferrals_cannot_be_promoted(self):
        name = consolidation.REVIEW_BATCHES[45]
        original = consolidation.audit.load(name)
        for item in original['reviews']:
            with self.subTest(pair_id=item['pair_id']):
                batch = deepcopy(original)
                record = next(r for r in batch['reviews'] if r['pair_id'] == item['pair_id'])
                record['experimental_subset_proposal'] = 'conditional_retain'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_swauth_shared_peers_match_all_four_selected_archives_and_parent(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_046_PEERS.json')['sources']
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_046_CONTEXT.json')
        self.assertEqual(len(peers), 2)
        self.assertEqual(len(context['parents']), 1)
        self.assertEqual(len(context['archives']), 2)
        ids = [pid for pid, row in self.train.items()
               if row['repository'] == 'github.com/openstack/swauth']
        for pid in ids:
            for side in ('before', 'after'):
                row = self.train[pid]
                ref = row['fixing_commit'] if side == 'after' else context['parents'][row['fixing_commit']]
                with self.subTest(pair_id=pid, side=side):
                    peer = next(s for s in peers if (s['path'], s['ref']) == (row['path'], ref))
                    lines, proof = consolidation.audit.source(row, side)
                    self.assertEqual(peer['archive_proof']['sha256'], proof['sha256'])
                    self.assertEqual(peer['text'], ''.join(lines))
                    self.assertEqual(peer['sha256'], proof['sha256'])
                    matches = [s for s in context['sources'] if (s['path'], s['ref']) == (peer['path'], peer['ref'])]
                    self.assertEqual(len(matches), 1)
                    self.assertEqual(matches[0]['text'], peer['text'])

    def test_qutebrowser_complete_selection_preserves_shared_settings_family(self):
        name = consolidation.REVIEW_BATCHES[46]
        batch = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items()
               if row['repository'] == 'github.com/qutebrowser/qutebrowser'}
        self.assertEqual(len(ids), 4)
        self.assertEqual({r['pair_id'] for r in batch['reviews']}, ids)
        self.assertEqual(len({self.families[pid] for pid in ids}), 3)
        self.assertEqual(self.families['CVEfixes:178113201707295:223374160760278'],
                         self.families['CVEfixes:217287020088616:257925922616364'])
        self.assertEqual({self.latest[pid]['review_status'] for pid in ids}, {'assistant_supported'})
        self.assertEqual(sum(self.latest[pid]['category_id'] is None for pid in ids), 0)
        for pid in sorted(ids):
            with self.subTest(pair_id=pid):
                altered = deepcopy(batch)
                altered['reviews'] = [r for r in altered['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=altered, batch_name=name)

    def test_qutebrowser_three_introduced_after_failures_require_paired_deferral(self):
        name = consolidation.REVIEW_BATCHES[46]
        original = consolidation.audit.load(name)
        assessed = [r for r in original['reviews'] if r.get('paired_negative_assessment')]
        self.assertEqual({r['pair_id'] for r in assessed}, {
            'CVEfixes:174601873543324:246961049692720',
            'CVEfixes:178113201707295:223374160760278',
            'CVEfixes:273146909520550:207570596490192',
        })
        for item in assessed:
            self.assertEqual(item['paired_negative_assessment'], 'unresolved_contract_regression')
            for mutation in ('proposal', 'scope'):
                with self.subTest(pair_id=item['pair_id'], mutation=mutation):
                    batch = deepcopy(original)
                    record = next(r for r in batch['reviews'] if r['pair_id'] == item['pair_id'])
                    if mutation == 'proposal':
                        record['experimental_subset_proposal'] = 'defer_missing_context'
                    else:
                        record['paired_negative_scope'] = 'mechanism_local_only'
                    with self.assertRaises(AssertionError):
                        self.reviews(batch=batch, batch_name=name)

    def test_qutebrowser_context_and_regression_deferrals_cannot_be_promoted(self):
        name = consolidation.REVIEW_BATCHES[46]
        original = consolidation.audit.load(name)
        for item in original['reviews']:
            with self.subTest(pair_id=item['pair_id']):
                batch = deepcopy(original)
                record = next(r for r in batch['reviews'] if r['pair_id'] == item['pair_id'])
                record['experimental_subset_proposal'] = 'conditional_retain'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_qutebrowser_shared_peers_match_resolved_before_after_archives(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_047_PEERS.json')['sources']
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_047_CONTEXT.json')
        self.assertEqual(len(peers), 8)
        self.assertEqual(len(context['parents']), 3)
        self.assertEqual(len(context['archives']), 6)
        for peer in peers:
            with self.subTest(ref=peer['ref'], path=peer['path']):
                row = self.train[peer['training_case']]
                side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
                expected_ref = row['fixing_commit'] if side == 'after' else context['parents'][row['fixing_commit']]
                self.assertEqual(peer['ref'], expected_ref)
                lines, proof = consolidation.audit.source(row, side)
                self.assertEqual(peer['archive_proof'], proof)
                self.assertEqual(peer['text'], ''.join(lines))
                self.assertEqual(peer['sha256'], proof['sha256'])
                matches = [s for s in context['sources'] if (s['path'], s['ref']) == (peer['path'], peer['ref'])]
                self.assertEqual(len(matches), 1)
                self.assertEqual(matches[0]['text'], peer['text'])

    def test_cloudinit_complete_selection_preserves_ambiguous_classifier_and_shared_family(self):
        name = consolidation.REVIEW_BATCHES[47]
        batch = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items()
               if row['repository'] == 'github.com/canonical/cloud-init'}
        self.assertEqual(len(ids), 4)
        self.assertEqual({r['pair_id'] for r in batch['reviews']}, ids)
        self.assertEqual(len({self.families[pid] for pid in ids}), 3)
        self.assertEqual(self.families['CVEfixes:135933521508434:50738315137669'],
                         self.families['CVEfixes:24576305371879:42840899937464'])
        self.assertEqual({self.latest[pid]['review_status'] for pid in ids},
                         {'assistant_supported', 'assistant_ambiguous'})
        self.assertEqual(self.latest['CVEfixes:135933521508434:50738315137669']['review_status'],
                         'assistant_ambiguous')
        self.assertEqual(sum(self.latest[pid]['category_id'] is None for pid in ids), 0)
        for pid in sorted(ids):
            with self.subTest(pair_id=pid):
                altered = deepcopy(batch)
                altered['reviews'] = [r for r in altered['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=altered, batch_name=name)

    def test_cloudinit_classifier_attribution_and_log_context_remain_separate(self):
        batch = consolidation.audit.load(consolidation.REVIEW_BATCHES[47])
        records = {r['pair_id']: r for r in batch['reviews']}
        classifier = records.pop('CVEfixes:135933521508434:50738315137669')
        self.assertEqual(classifier['experimental_subset_proposal'], 'defer_selected_attribution')
        self.assertEqual(classifier['selected_relevance'], 'coordinated_component_not_isolated')
        self.assertEqual(classifier['security_screen'], 'unresolved_boundary')
        self.assertEqual(classifier['paired_negative_scope'], 'not_established_for_selected_component')
        for record in records.values():
            with self.subTest(pair_id=record['pair_id']):
                self.assertEqual(record['experimental_subset_proposal'], 'defer_missing_context')
                self.assertEqual(record['selected_relevance'], 'local_repair_supported')
                self.assertEqual(record['security_screen'], 'demonstrated_security_boundary')
                self.assertEqual(record['paired_negative_scope'], 'mechanism_local_only')
                self.assertEqual(record['function_only_context'], 'requires_missing_project_contract')

    def test_cloudinit_context_and_selected_attribution_deferrals_cannot_be_promoted(self):
        name = consolidation.REVIEW_BATCHES[47]
        original = consolidation.audit.load(name)
        for item in original['reviews']:
            with self.subTest(pair_id=item['pair_id']):
                batch = deepcopy(original)
                record = next(r for r in batch['reviews'] if r['pair_id'] == item['pair_id'])
                record['experimental_subset_proposal'] = 'conditional_retain'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_cloudinit_peers_match_all_selected_archives_and_resolved_parents(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_048_PEERS.json')['sources']
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_048_CONTEXT.json')
        self.assertEqual(len(peers), 8)
        self.assertEqual(len(context['parents']), 3)
        self.assertEqual(len(context['archives']), 6)
        self.assertEqual(len({(p['training_case'], p['ref']) for p in peers}), 8)
        for peer in peers:
            with self.subTest(ref=peer['ref'], path=peer['path']):
                row = self.train[peer['training_case']]
                side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
                expected_ref = row['fixing_commit'] if side == 'after' else context['parents'][row['fixing_commit']]
                self.assertEqual(peer['ref'], expected_ref)
                lines, proof = consolidation.audit.source(row, side)
                self.assertEqual(peer['archive_proof'], proof)
                self.assertEqual(peer['text'], ''.join(lines))
                self.assertEqual(peer['sha256'], proof['sha256'])
                matches = [s for s in context['sources'] if (s['path'], s['ref']) == (peer['path'], peer['ref'])]
                self.assertEqual(len(matches), 1)
                self.assertEqual(matches[0]['text'], peer['text'])

    def test_rdiffweb_complete_selection_preserves_four_supported_families(self):
        name = consolidation.REVIEW_BATCHES[48]
        batch = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items()
               if row['repository'] == 'github.com/ikus060/rdiffweb'}
        self.assertEqual(len(ids), 4)
        self.assertEqual({r['pair_id'] for r in batch['reviews']}, ids)
        self.assertEqual(len({self.families[pid] for pid in ids}), 4)
        self.assertEqual({self.latest[pid]['review_status'] for pid in ids}, {'assistant_supported'})
        self.assertEqual(sum(self.latest[pid]['category_id'] is None for pid in ids), 0)
        for pid in sorted(ids):
            with self.subTest(pair_id=pid):
                altered = deepcopy(batch)
                altered['reviews'] = [r for r in altered['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=altered, batch_name=name)

    def test_rdiffweb_loaded_session_residual_requires_paired_deferral(self):
        name = consolidation.REVIEW_BATCHES[48]
        original = consolidation.audit.load(name)
        assessed = [r for r in original['reviews'] if r.get('paired_negative_assessment')]
        self.assertEqual(len(assessed), 1)
        self.assertEqual(assessed[0]['pair_id'], 'CVEfixes:176115016783544:159434677704988')
        self.assertEqual(assessed[0]['paired_negative_assessment'], 'unresolved_contract_failure')
        for mutation in ('proposal', 'scope'):
            with self.subTest(mutation=mutation):
                batch = deepcopy(original)
                record = next(r for r in batch['reviews'] if r.get('paired_negative_assessment'))
                if mutation == 'proposal':
                    record['experimental_subset_proposal'] = 'defer_missing_context'
                else:
                    record['paired_negative_scope'] = 'mechanism_local_only'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_rdiffweb_context_and_session_residual_deferrals_cannot_be_promoted(self):
        name = consolidation.REVIEW_BATCHES[48]
        original = consolidation.audit.load(name)
        for item in original['reviews']:
            with self.subTest(pair_id=item['pair_id']):
                batch = deepcopy(original)
                record = next(r for r in batch['reviews'] if r['pair_id'] == item['pair_id'])
                record['experimental_subset_proposal'] = 'conditional_retain'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_rdiffweb_peers_match_all_selected_archives_and_resolved_parents(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_049_PEERS.json')['sources']
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_049_CONTEXT.json')
        self.assertEqual(len(peers), 8)
        self.assertEqual(len(context['parents']), 4)
        self.assertEqual(len(context['archives']), 8)
        self.assertEqual(len({(p['training_case'], p['ref']) for p in peers}), 8)
        for peer in peers:
            with self.subTest(ref=peer['ref'], path=peer['path']):
                row = self.train[peer['training_case']]
                side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
                expected_ref = row['fixing_commit'] if side == 'after' else context['parents'][row['fixing_commit']]
                self.assertEqual(peer['ref'], expected_ref)
                lines, proof = consolidation.audit.source(row, side)
                self.assertEqual(peer['archive_proof'], proof)
                self.assertEqual(peer['text'], ''.join(lines))
                self.assertEqual(peer['sha256'], proof['sha256'])
                matches = [s for s in context['sources'] if (s['path'], s['ref']) == (peer['path'], peer['ref'])]
                self.assertEqual(len(matches), 1)
                self.assertEqual(matches[0]['text'], peer['text'])

    def test_mlflow_complete_selection_preserves_ambiguous_and_supported_families(self):
        name = consolidation.REVIEW_BATCHES[49]
        batch = consolidation.audit.load(name)
        ids = {pid for pid, row in self.train.items()
               if row['repository'] == 'github.com/mlflow/mlflow'}
        self.assertEqual(len(ids), 4)
        self.assertEqual({r['pair_id'] for r in batch['reviews']}, ids)
        self.assertEqual(len({self.families[pid] for pid in ids}), 4)
        self.assertEqual({self.latest[pid]['review_status'] for pid in ids},
                         {'assistant_supported', 'assistant_ambiguous'})
        self.assertEqual(sum(self.latest[pid]['category_id'] is None for pid in ids), 0)
        for pid in sorted(ids):
            with self.subTest(pair_id=pid):
                altered = deepcopy(batch)
                altered['reviews'] = [r for r in altered['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=altered, batch_name=name)

    def test_mlflow_boundary_and_context_deferrals_cannot_be_promoted(self):
        name = consolidation.REVIEW_BATCHES[49]
        original = consolidation.audit.load(name)
        self.assertEqual(sum(r['experimental_subset_proposal'] == 'defer_security_boundary'
                             for r in original['reviews']), 3)
        self.assertEqual(sum(r['experimental_subset_proposal'] == 'defer_missing_context'
                             for r in original['reviews']), 1)
        for item in original['reviews']:
            with self.subTest(pair_id=item['pair_id']):
                batch = deepcopy(original)
                record = next(r for r in batch['reviews'] if r['pair_id'] == item['pair_id'])
                record['experimental_subset_proposal'] = 'conditional_retain'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_mlflow_uri_guards_keep_distinct_historical_contracts(self):
        batch = consolidation.audit.load(consolidation.REVIEW_BATCHES[49])
        records = {r['pair_id']: r for r in batch['reviews']}
        earlier = records['CVEfixes:26682418100577:13728681899479']
        later = records['CVEfixes:211071458352479:226250294290403']
        old_guard = next(a for a in earlier['anchors']
                         if 'if not MLFLOW_ALLOW_FILE_URI_AS_MODEL_VERSION_SOURCE.get()' in a['needle'])
        self.assertEqual(old_guard['ref'], '1af5a88a972986525d6573c0a4455070a16b4f27')
        sibling = next(a for a in later['anchors']
                       if a['needle'] == 'if is_local_uri(run.info.artifact_uri):')
        self.assertEqual(sibling['kind'], 'supplement')
        self.assertEqual(sibling['ref'], 'f8d51e21523238280ebcfdb378612afd7844eca8')
        self.assertEqual(later['experimental_subset_proposal'], 'defer_missing_context')
        self.assertEqual(earlier['security_screen'], 'unresolved_boundary')
        self.assertEqual(earlier['paired_negative_scope'], 'mechanism_local_only')

    def test_mlflow_peers_match_all_selected_archives_and_resolved_parents(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_050_PEERS.json')['sources']
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_050_CONTEXT.json')
        self.assertEqual(len(peers), 8)
        self.assertEqual(len(context['parents']), 4)
        self.assertEqual(len(context['archives']), 8)
        self.assertEqual(len({(p['training_case'], p['ref']) for p in peers}), 8)
        for peer in peers:
            with self.subTest(ref=peer['ref'], path=peer['path']):
                row = self.train[peer['training_case']]
                side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
                expected_ref = row['fixing_commit'] if side == 'after' else context['parents'][row['fixing_commit']]
                self.assertEqual(peer['ref'], expected_ref)
                lines, proof = consolidation.audit.source(row, side)
                self.assertEqual(peer['archive_proof'], proof)
                self.assertEqual(peer['text'], ''.join(lines))
                self.assertEqual(peer['sha256'], proof['sha256'])
                matches = [s for s in context['sources'] if (s['path'], s['ref']) == (peer['path'], peer['ref'])]
                self.assertEqual(len(matches), 1)
                self.assertEqual(matches[0]['text'], peer['text'])

    def test_ten_candidate_selection_keeps_all_three_repositories_and_four_families(self):
        name = consolidation.REVIEW_BATCHES[50]
        original = consolidation.audit.load(name)
        selection = original['selection_rule']
        self.assertEqual(selection['candidate_count'], 10)
        self.assertEqual(len(selection['repositories']), 3)
        expected = {pid for pid, row in self.train.items()
                    if row['repository'] in selection['repositories']}
        self.assertEqual({r['pair_id'] for r in original['reviews']}, expected)
        self.assertEqual(len(expected), 10)
        self.assertEqual(len({self.families[pid] for pid in expected}), 4)
        for pid in expected:
            with self.subTest(pair_id=pid):
                batch = deepcopy(original)
                batch['reviews'] = [r for r in batch['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_multi_repository_selection_rejects_conflicting_duplicate_and_wrong_count(self):
        name = consolidation.REVIEW_BATCHES[50]
        original = consolidation.audit.load(name)
        for mutation in ('conflict', 'duplicate', 'count', 'empty'):
            with self.subTest(mutation=mutation):
                batch = deepcopy(original)
                selection = batch['selection_rule']
                if mutation == 'conflict':
                    selection['repository'] = selection['repositories'][0]
                elif mutation == 'duplicate':
                    selection['repositories'].append(selection['repositories'][0])
                elif mutation == 'count':
                    selection['candidate_count'] = 9
                else:
                    selection['repositories'] = []
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_ten_candidate_batch_preserves_nested_and_coordinated_attribution(self):
        original = consolidation.audit.load(consolidation.REVIEW_BATCHES[50])
        records = {r['pair_id']: r for r in original['reviews']}
        outer = records['CVEfixes:177610503639025:69341272094741']
        inner = records['CVEfixes:177610503639025:25048083255114']
        self.assertEqual(self.families[outer['pair_id']], self.families[inner['pair_id']])
        self.assertEqual(outer['experimental_subset_proposal'], 'defer_selected_attribution')
        self.assertEqual(inner['experimental_subset_proposal'], 'defer_missing_context')
        for side in ('before', 'after'):
            inner_lines, inner_proof = consolidation.audit.source(self.train[inner['pair_id']], side)
            outer_lines, outer_proof = consolidation.audit.source(self.train[outer['pair_id']], side)
            self.assertEqual(inner_lines, outer_lines)
            self.assertLessEqual(outer_proof['start'], inner_proof['start'])
            self.assertGreaterEqual(outer_proof['end'], inner_proof['end'])
        self.assertEqual(sum(r['experimental_subset_proposal'] == 'defer_selected_attribution'
                             for r in original['reviews']), 4)

    def test_ten_candidate_upload_after_failure_requires_paired_negative_deferral(self):
        name = consolidation.REVIEW_BATCHES[50]
        original = consolidation.audit.load(name)
        assessed = [r for r in original['reviews'] if r.get('paired_negative_assessment')]
        self.assertEqual(len(assessed), 1)
        self.assertEqual(assessed[0]['pair_id'], 'CVEfixes:234315831912053:127782130225341')
        self.assertEqual(assessed[0]['paired_negative_assessment'], 'unresolved_contract_regression')
        for mutation in ('proposal', 'scope'):
            with self.subTest(mutation=mutation):
                batch = deepcopy(original)
                record = next(r for r in batch['reviews'] if r.get('paired_negative_assessment'))
                if mutation == 'proposal':
                    record['experimental_subset_proposal'] = 'defer_missing_context'
                else:
                    record['paired_negative_scope'] = 'mechanism_local_only'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_ten_candidate_deferrals_cannot_be_silently_promoted(self):
        name = consolidation.REVIEW_BATCHES[50]
        original = consolidation.audit.load(name)
        for item in original['reviews']:
            with self.subTest(pair_id=item['pair_id']):
                batch = deepcopy(original)
                record = next(r for r in batch['reviews'] if r['pair_id'] == item['pair_id'])
                record['experimental_subset_proposal'] = 'conditional_retain'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_ten_candidate_peers_match_all_training_sources_and_parents(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_051_PEERS.json')['sources']
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_051_CONTEXT.json')
        self.assertEqual(len(peers), 20)
        self.assertEqual(len(context['parents']), 4)
        self.assertEqual(len(context['archives']), 8)
        self.assertEqual(len({(p['training_case'], p['ref']) for p in peers}), 20)
        for peer in peers:
            with self.subTest(ref=peer['ref'], pair_id=peer['training_case']):
                row = self.train[peer['training_case']]
                side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
                expected_ref = row['fixing_commit'] if side == 'after' else context['parents'][row['fixing_commit']]
                self.assertEqual(peer['ref'], expected_ref)
                lines, proof = consolidation.audit.source(row, side)
                self.assertEqual(peer['archive_proof'], proof)
                self.assertEqual(peer['text'], ''.join(lines))
                if row['source'] == 'HaPy-Bug':
                    # HaPy archive URLs use fix%5E; exact parent is separately
                    # resolved and full-file checked against the context below.
                    self.assertEqual(row['full_file_sha256'][side], peer['sha256'])
                else:
                    origin = consolidation.supplemental_origin(peer, self.train, {})
                    self.assertEqual(origin['archive_proof'], proof)
                matches = [s for s in context['sources'] if (s['repository'], s['path'], s['ref'])
                           == (peer['repository'], peer['path'], peer['ref'])]
                self.assertEqual(len(matches), 1)
                self.assertEqual(matches[0]['text'], peer['text'])

    def test_batch052_selection_preserves_every_repository_status_and_family(self):
        name = consolidation.REVIEW_BATCHES[51]
        original = consolidation.audit.load(name)
        selection = original['selection_rule']
        ids = {pid for pid, row in self.train.items()
               if row['repository'] in selection['repositories']}
        self.assertEqual(selection['candidate_count'], 10)
        self.assertEqual(len(ids), 10)
        self.assertEqual(len({self.families[pid] for pid in ids}), 4)
        self.assertEqual({r['pair_id'] for r in original['reviews']}, ids)
        self.assertEqual({self.latest[pid]['review_status'] for pid in ids},
                         {'assistant_supported', 'assistant_ambiguous'})
        for pid in ids:
            with self.subTest(pair_id=pid):
                batch = deepcopy(original)
                batch['reviews'] = [r for r in batch['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_batch052_sql_after_regression_requires_explicit_negative_deferral(self):
        name = consolidation.REVIEW_BATCHES[51]
        original = consolidation.audit.load(name)
        record = next(r for r in original['reviews'] if r.get('paired_negative_assessment'))
        self.assertEqual(record['pair_id'], 'CVEfixes:260854861546769:90609108934075')
        self.assertEqual(record['paired_negative_assessment'], 'unresolved_contract_regression')
        self.assertEqual(record['security_screen'], 'unresolved_boundary')
        for mutation in ('proposal', 'scope'):
            with self.subTest(mutation=mutation):
                batch = deepcopy(original)
                changed = next(r for r in batch['reviews'] if r.get('paired_negative_assessment'))
                if mutation == 'proposal':
                    changed['experimental_subset_proposal'] = 'defer_missing_context'
                else:
                    changed['paired_negative_scope'] = 'mechanism_local_only'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_batch052_cors_containment_and_deferrals_cannot_be_promoted(self):
        name = consolidation.REVIEW_BATCHES[51]
        original = consolidation.audit.load(name)
        records = {r['pair_id']: r for r in original['reviews']}
        inner = records['CVEfixes:26695807228249:162601659861075']
        outer = records['CVEfixes:26695807228249:56254439499420']
        self.assertEqual(inner['experimental_subset_proposal'], 'defer_missing_context')
        self.assertEqual(outer['experimental_subset_proposal'], 'defer_selected_attribution')
        for side in ('before', 'after'):
            inner_lines, ip = consolidation.audit.source(self.train[inner['pair_id']], side)
            outer_lines, op = consolidation.audit.source(self.train[outer['pair_id']], side)
            self.assertEqual(inner_lines, outer_lines)
            self.assertLessEqual(op['start'], ip['start'])
            self.assertGreaterEqual(op['end'], ip['end'])
        for item in original['reviews']:
            with self.subTest(pair_id=item['pair_id']):
                batch = deepcopy(original)
                next(r for r in batch['reviews'] if r['pair_id'] == item['pair_id'])[
                    'experimental_subset_proposal'] = 'conditional_retain'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_batch052_peers_match_exact_archives_and_corrected_connector_contracts(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_052_PEERS.json')['sources']
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_052_CONTEXT.json')
        self.assertEqual(len(peers), 20)
        self.assertEqual(len(context['parents']), 4)
        self.assertEqual(len(context['archives']), 8)
        self.assertEqual(len({(p['training_case'], p['ref']) for p in peers}), 20)
        for peer in peers:
            with self.subTest(ref=peer['ref'], pair_id=peer['training_case']):
                row = self.train[peer['training_case']]
                side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
                expected_ref = row['fixing_commit'] if side == 'after' else context['parents'][row['fixing_commit']]
                self.assertEqual(peer['ref'], expected_ref)
                lines, proof = consolidation.audit.source(row, side)
                self.assertEqual(peer['archive_proof'], proof)
                self.assertEqual(peer['text'], ''.join(lines))
                origin = consolidation.supplemental_origin(peer, self.train, {})
                self.assertEqual(origin['archive_proof'], proof)
                matches = [s for s in context['sources'] if (s['repository'], s['path'], s['ref'])
                           == (peer['repository'], peer['path'], peer['ref'])]
                self.assertEqual(len(matches), 1)
                self.assertEqual(matches[0]['text'], peer['text'])
        contracts = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_052_CONTRACTS.json')
        delivery = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_052_DELIVERY.json')
        self.assertEqual(len(contracts['requested_missing']), 7)
        self.assertTrue(all(m['http_status'] == 404 for m in contracts['requested_missing']))
        corrected = [s for s in delivery['sources'] if s['repository'] == 'mysql/mysql-connector-python']
        self.assertEqual(len(corrected), 7)
        self.assertTrue(all(s['ref'] == '8.2.0' and s['path'].startswith('lib/mysql/connector/')
                            for s in corrected))

    def test_batch053_exhaustive_selection_keeps_five_repositories_and_six_families(self):
        name = consolidation.REVIEW_BATCHES[52]
        original = consolidation.audit.load(name)
        repos = original['selection_rule']['repositories']
        ids = {pid for pid, row in self.train.items() if row['repository'] in repos}
        self.assertEqual(len(repos), 5)
        self.assertEqual(len(ids), 10)
        self.assertEqual({r['pair_id'] for r in original['reviews']}, ids)
        self.assertEqual(len({self.families[pid] for pid in ids}), 6)
        self.assertEqual({self.latest[pid]['review_status'] for pid in ids},
                         {'assistant_supported', 'assistant_ambiguous'})
        for pid in ids:
            with self.subTest(pair_id=pid):
                batch = deepcopy(original)
                batch['reviews'] = [r for r in batch['reviews'] if r['pair_id'] != pid]
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_batch053_introduced_json_transport_and_capability_output_need_deferral(self):
        name = consolidation.REVIEW_BATCHES[52]
        original = consolidation.audit.load(name)
        assessed = [r for r in original['reviews'] if r.get('paired_negative_assessment')]
        self.assertEqual({r['pair_id'] for r in assessed}, {
            'CVEfixes:158385455163425:203264623519386',
            'CVEfixes:56455623515815:4280509275020'})
        for item in assessed:
            self.assertEqual(item['paired_negative_assessment'], 'unresolved_contract_regression')
            for mutation in ('proposal', 'scope'):
                with self.subTest(pair_id=item['pair_id'], mutation=mutation):
                    batch = deepcopy(original)
                    changed = next(r for r in batch['reviews'] if r['pair_id'] == item['pair_id'])
                    if mutation == 'proposal':
                        changed['experimental_subset_proposal'] = 'defer_missing_context'
                    else:
                        changed['paired_negative_scope'] = 'mechanism_local_only'
                    with self.assertRaises(AssertionError):
                        self.reviews(batch=batch, batch_name=name)

    def test_batch053_nested_mjml_and_coordinated_template_deferrals_cannot_be_promoted(self):
        name = consolidation.REVIEW_BATCHES[52]
        original = consolidation.audit.load(name)
        records = {r['pair_id']: r for r in original['reviews']}
        outer = records['CVEfixes:81679705043896:14857560379839']
        inner = records['CVEfixes:81679705043896:158678979153150']
        self.assertEqual(outer['experimental_subset_proposal'], 'defer_selected_attribution')
        self.assertEqual(inner['experimental_subset_proposal'], 'defer_missing_context')
        for side in ('before', 'after'):
            il, ip = consolidation.audit.source(self.train[inner['pair_id']], side)
            ol, op = consolidation.audit.source(self.train[outer['pair_id']], side)
            self.assertEqual(il, ol)
            self.assertLessEqual(op['start'], ip['start'])
            self.assertGreaterEqual(op['end'], ip['end'])
        for item in original['reviews']:
            with self.subTest(pair_id=item['pair_id']):
                batch = deepcopy(original)
                next(r for r in batch['reviews'] if r['pair_id'] == item['pair_id'])[
                    'experimental_subset_proposal'] = 'conditional_retain'
                with self.assertRaises(AssertionError):
                    self.reviews(batch=batch, batch_name=name)

    def test_batch053_peers_match_exact_training_archives_and_first_parents(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_053_PEERS.json')['sources']
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_053_CONTEXT.json')
        self.assertEqual(len(peers), 20)
        self.assertEqual(len(context['parents']), 6)
        self.assertEqual(len(context['archives']), 12)
        self.assertEqual(len({(p['training_case'], p['ref']) for p in peers}), 20)
        for peer in peers:
            with self.subTest(ref=peer['ref'], pair_id=peer['training_case']):
                row = self.train[peer['training_case']]
                side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
                expected = row['fixing_commit'] if side == 'after' else context['parents'][row['fixing_commit']]
                self.assertEqual(peer['ref'], expected)
                lines, proof = consolidation.audit.source(row, side)
                self.assertEqual(peer['archive_proof'], proof)
                self.assertEqual(peer['text'], ''.join(lines))
                self.assertEqual(consolidation.supplemental_origin(peer, self.train, {})['archive_proof'], proof)
                matches = [s for s in context['sources'] if (s['repository'], s['path'], s['ref'])
                           == (peer['repository'], peer['path'], peer['ref'])]
                self.assertEqual(len(matches), 1)
                self.assertEqual(matches[0]['text'], peer['text'])

    def test_batch053_parser_archive_hash_matches_retained_package_metadata(self):
        sources = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_053_CONTRACTS.json')['sources']
        package = next(s for s in sources if s['path'] == 'pypi/beautifulsoup4/4.12.3.json')
        metadata = json.loads(package['text'])
        sdist = next(item for item in metadata['urls'] if item['packagetype'] == 'sdist')
        members = [s for s in sources if s['path'].startswith('bs4/')]
        self.assertEqual(len(members), 4)
        for member in members:
            self.assertEqual(member['ref'], '4.12.3')
            self.assertEqual(member['archive_sha256'], sdist['digests']['sha256'])
            self.assertEqual(member['archive_url'], sdist['url'])

    def test_batch054_context_view_preserves_original_and_resolves_duplicate_ref_paths(self):
        original = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_054_CONTEXT.json')
        view = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_054_CONTEXT_UNIQUE.json')
        keys = [(s['path'], s['ref']) for s in view['sources']]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(len(original['sources']), 448)
        self.assertEqual(len(view['sources']), 445)
        self.assertEqual(view['source_view_of']['sha256'], consolidation.audit.file_sha(
            consolidation.audit.ROOT/'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_054_CONTEXT.json'))
        indexed = {(s['path'], s['ref']): s['text'] for s in view['sources']}
        for source in original['sources']:
            self.assertEqual(indexed[source['path'], source['ref']], source['text'])

    def test_batch054_exhaustive_selection_includes_unused_helper_exclusion(self):
        name = consolidation.REVIEW_BATCHES[53]
        original = consolidation.audit.load(name)
        repositories = set(original['selection_rule']['repositories'])
        expected = {pid for pid, row in self.train.items() if row['repository'] in repositories}
        self.assertEqual(len(expected), 10)
        self.assertEqual(len({self.families[pid] for pid in expected}), 7)
        self.assertEqual({r['pair_id'] for r in original['reviews']}, expected)
        excluded = next(pid for pid in expected if self.latest[pid]['review_status'] == 'assistant_proposed_exclusion')
        changed = deepcopy(original)
        changed['reviews'] = [r for r in changed['reviews'] if r['pair_id'] != excluded]
        with self.assertRaises(AssertionError):
            self.reviews(batch=changed, batch_name=name)

    def test_batch054_introduced_and_residual_failures_cannot_lose_negative_deferral(self):
        name = consolidation.REVIEW_BATCHES[53]
        original = consolidation.audit.load(name)
        assessed = [r for r in original['reviews'] if r.get('paired_negative_assessment')]
        self.assertEqual(len(assessed), 4)
        self.assertEqual(sum(r['paired_negative_assessment'] == 'unresolved_contract_regression'
                             for r in assessed), 3)
        for item in assessed:
            for mutation in ('proposal', 'scope'):
                with self.subTest(pair_id=item['pair_id'], mutation=mutation):
                    changed = deepcopy(original)
                    record = next(r for r in changed['reviews'] if r['pair_id'] == item['pair_id'])
                    if mutation == 'proposal':
                        record['experimental_subset_proposal'] = 'defer_missing_context'
                    else:
                        record['paired_negative_scope'] = 'mechanism_local_only'
                    with self.assertRaises(AssertionError):
                        self.reviews(batch=changed, batch_name=name)

    def test_batch054_peers_match_first_parents_and_both_version_chains(self):
        peers = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_054_PEERS.json')['sources']
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_054_CONTEXT.json')
        self.assertEqual(len(peers), 20)
        self.assertEqual(len(context['parents']), 7)
        self.assertEqual(len(context['archives']), 14)
        for peer in peers:
            row = self.train[peer['training_case']]
            side = 'after' if peer['ref'] == row['fixing_commit'] else 'before'
            expected_ref = row['fixing_commit'] if side == 'after' else context['parents'][row['fixing_commit']]
            self.assertEqual(peer['ref'], expected_ref)
            lines, proof = consolidation.audit.source(row, side)
            self.assertEqual(peer['archive_proof'], proof)
            self.assertEqual(peer['text'], ''.join(lines))
        records = consolidation.audit.load(consolidation.REVIEW_BATCHES[53])['reviews']
        zenml = [self.train[r['pair_id']] for r in records
                 if self.train[r['pair_id']]['repository'] == 'github.com/zenml-io/zenml']
        self.assertEqual(zenml[0]['after'], zenml[1]['before'])
        log = next(r for r in records if 'CVE-2017-15111' in r['pair_id'])
        password = next(r for r in records if 'CVE-2017-15112' in r['pair_id'])
        self.assertEqual(''.join(consolidation.audit.source(self.train[password['pair_id']], 'after')[0]),
                         ''.join(consolidation.audit.source(self.train[log['pair_id']], 'before')[0]))

    def test_batch055_exhaustive_plan_and_negative_deferrals(self):
        name = consolidation.REVIEW_BATCHES[54]
        original = consolidation.audit.load(name)
        plan = next(b for b in consolidation.audit.load(
            'CATEGORY_AUDIT_CONSOLIDATION_BATCH_PLAN_051_059.json')['batches']
                    if b['batch_id'] == 'consolidation-055')
        self.assertEqual({r['pair_id'] for r in original['reviews']}, set(plan['pair_ids']))
        self.assertEqual(len({self.families[p] for p in plan['pair_ids']}), 8)
        assessed = [r for r in original['reviews'] if r.get('paired_negative_assessment')]
        self.assertEqual(len(assessed), 3)
        self.assertEqual(sum(r['paired_negative_assessment'] == 'unresolved_contract_regression'
                             for r in assessed), 2)
        for item in assessed:
            for field, value in [('experimental_subset_proposal', 'defer_missing_context'),
                                 ('paired_negative_scope', 'mechanism_local_only')]:
                with self.subTest(pair_id=item['pair_id'], field=field):
                    batch = deepcopy(original)
                    next(r for r in batch['reviews'] if r['pair_id'] == item['pair_id'])[field] = value
                    with self.assertRaises(AssertionError):
                        self.reviews(batch=batch, batch_name=name)
        omitted = deepcopy(original)
        omitted['reviews'] = omitted['reviews'][:-1]
        with self.assertRaises(AssertionError):
            self.reviews(batch=omitted, batch_name=name)

    def test_tail_batches_remain_exhaustive_under_the_immutable_schedule(self):
        plan_name = 'CATEGORY_AUDIT_CONSOLIDATION_BATCH_PLAN_051_059.json'
        self.assertEqual(consolidation.audit.file_sha(consolidation.audit.ROOT/plan_name),
                         '4e3ac55537b81febeb642123f9d9b3daa63acc59ee2779d66a704bd58c79a98a')
        planned = {b['batch_id']: b for b in consolidation.audit.load(plan_name)['batches']}
        for name in consolidation.REVIEW_BATCHES[54:]:
            original = consolidation.audit.load(name)
            batch_plan = planned[original['batch_id']]
            expected = {pid for pid, row in self.train.items()
                        if row['repository'] in batch_plan['repositories']}
            self.assertEqual(expected, set(batch_plan['pair_ids']))
            self.assertEqual({r['pair_id'] for r in original['reviews']}, expected)
            changed = deepcopy(original)
            changed['reviews'] = changed['reviews'][:-1]
            with self.assertRaises(AssertionError):
                self.reviews(batch=changed, batch_name=name)

    def test_batch056_moved_path_validation_and_post_match_strip_need_attribution_deferral(self):
        name = consolidation.REVIEW_BATCHES[55]
        original = consolidation.audit.load(name)
        coordinated = [r for r in original['reviews']
                       if r['experimental_subset_proposal'] == 'defer_selected_attribution']
        self.assertEqual(len(coordinated), 2)
        for item in coordinated:
            changed = deepcopy(original)
            next(r for r in changed['reviews'] if r['pair_id'] == item['pair_id'])[
                'experimental_subset_proposal'] = 'conditional_retain'
            with self.assertRaises(AssertionError):
                self.reviews(batch=changed, batch_name=name)

    def test_batch057_default_symlink_and_explicit_file_failures_need_negative_deferral(self):
        name = consolidation.REVIEW_BATCHES[56]
        original = consolidation.audit.load(name)
        assessed = [r for r in original['reviews'] if r.get('paired_negative_assessment')]
        self.assertEqual(len(assessed), 2)
        for item in assessed:
            self.assertEqual(item['paired_negative_assessment'], 'unresolved_contract_regression')
            for field, value in [('experimental_subset_proposal', 'defer_missing_context'),
                                 ('paired_negative_scope', 'mechanism_local_only')]:
                with self.subTest(pair_id=item['pair_id'], field=field):
                    changed = deepcopy(original)
                    next(r for r in changed['reviews'] if r['pair_id'] == item['pair_id'])[field] = value
                    with self.assertRaises(AssertionError):
                        self.reviews(batch=changed, batch_name=name)

    def test_batch058_locked_tarsafe_root_failure_cannot_be_promoted_to_negative(self):
        name = consolidation.REVIEW_BATCHES[57]
        original = consolidation.audit.load(name)
        record = next(r for r in original['reviews']
                      if self.train[r['pair_id']]['repository'] == 'github.com/rasahq/rasa')
        self.assertEqual(record['paired_negative_assessment'], 'unresolved_contract_failure')
        for field, value in [('experimental_subset_proposal', 'defer_missing_context'),
                             ('paired_negative_scope', 'mechanism_local_only')]:
            changed = deepcopy(original)
            next(r for r in changed['reviews'] if r['pair_id'] == record['pair_id'])[field] = value
            with self.assertRaises(AssertionError):
                self.reviews(batch=changed, batch_name=name)
        retained = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_058_TARSAFE.json')
        metadata = json.loads(consolidation.audit.load(
            'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_058_TARSAFE_METADATA.json')['sources'][0]['text'])
        release = next(item for item in metadata['urls']
                       if item['filename'] == 'tarsafe-0.0.3-py3-none-any.whl')
        expected = 'f8181c5559aea70af2579a0dc0811d2e9e3eabd706dd594555b4dfa52c0be51a'
        self.assertEqual(retained['archive_sha256'], expected)
        self.assertEqual(release['digests']['sha256'], expected)
        self.assertEqual(retained['archive_url'], release['url'])
        context = consolidation.audit.load('CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_058_CONTEXT.json')
        lock = context['sources'][95]
        self.assertEqual(lock['path'], 'poetry.lock')
        self.assertIn('hash = "sha256:'+expected+'"', lock['text'])
        for source in retained['sources']:
            self.assertEqual(source['archive_sha256'], expected)
            self.assertEqual(source['url'], release['url']+'#'+source['path'])
            self.assertEqual(source['sha256'], consolidation.audit.sha(source['text']))

    def test_tail_released_peer_views_preserve_bytes_and_exact_released_urls(self):
        for name in consolidation.REVIEW_BATCHES[54:]:
            number = consolidation.audit.load(name)['batch_id'].rsplit('-', 1)[1]
            stem = f'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_{number}_PEERS'
            view = consolidation.audit.load(stem+'_RELEASED.json')
            original = consolidation.audit.load(stem+'.json')
            self.assertEqual(view['original_sha256'], consolidation.audit.file_sha(
                consolidation.audit.ROOT/(stem+'.json')))
            context = consolidation.audit.load(
                f'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_{number}_CONTEXT.json')
            self.assertEqual(len(view['sources']), len(original['sources']))
            for peer in view['sources']:
                with self.subTest(number=number, pair_id=peer['training_case'], side=peer['side']):
                    row = self.train[peer['training_case']]
                    raw = original['sources'][peer['original_source_index']]
                    self.assertEqual(peer['text'], raw['text'])
                    self.assertEqual(peer['original_url'], raw['url'])
                    lines, proof = consolidation.audit.source(row, peer['side'])
                    self.assertEqual(peer['archive_proof'], proof)
                    self.assertEqual(peer['text'], ''.join(lines))
                    self.assertEqual(peer['sha256'], consolidation.audit.sha(peer['text']))
                    snapshot = row.get('upstream_snapshots', {}).get(peer['side'])
                    if snapshot:
                        self.assertEqual(peer['url'], snapshot['url'])
                        self.assertEqual(peer['sha256'], snapshot['sha256'])
                    else:
                        self.assertEqual(peer['url'], row['source_urls'][peer['side']])
                        self.assertEqual(peer['sha256'], row['full_file_sha256'][peer['side']])
                    if peer['parent_resolved']:
                        expected_ref = (row['fixing_commit'] if peer['side'] == 'after'
                                        else context['parents'][row['fixing_commit']])
                        self.assertEqual(peer['ref'], expected_ref)
                        matches = [s for s in context['sources']
                                   if (s['repository'], s['path'], s['ref']) ==
                                   (peer['repository'], peer['path'], peer['ref'])]
                        self.assertEqual(len(matches), 1)
                        self.assertEqual(matches[0]['text'], peer['text'])
                    else:
                        self.assertNotIn(row['fixing_commit'], context['parents'])
                        self.assertTrue(context['requested_missing'])

    def test_coordinated_component_cannot_be_promoted_to_retain(self):
        name = consolidation.REVIEW_BATCHES[1]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(item for item in batch['reviews']
                      if item['selected_relevance'] == 'coordinated_component_not_isolated')
        record['experimental_subset_proposal'] = 'conditional_retain'
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch, batch_name=name)

    def test_missing_paired_negative_cannot_be_promoted_to_retain(self):
        batch = deepcopy(self.batch)
        record = next(item for item in batch['reviews']
                      if item['experimental_subset_proposal'] == 'conditional_retain')
        record['paired_negative_scope'] = 'not_established_for_selected_component'
        with self.assertRaises(AssertionError):
            self.reviews(batch=batch)

    def test_multiple_source_revisions_require_explicit_evidence_ref(self):
        name = consolidation.REVIEW_BATCHES[1]
        batch = deepcopy(consolidation.audit.load(name))
        record = next(item for item in batch['reviews'] if item['pair_id'].endswith(':Bash.get_aliases'))
        anchor = next(a for a in record['anchors'] if a.get('path') == 'thefuck/types.py')
        anchor.pop('ref')
        with self.assertRaisesRegex(AssertionError, 'unambiguous path/ref'):
            self.reviews(batch=batch, batch_name=name)

    def test_evidence_anchors_need_a_unique_exact_match(self):
        self.assertEqual(consolidation.retained_anchor('first\nsecond\nthird\n', 'second\nthird'),
                         {'start_line': 2, 'end_line': 3, 'excerpt': 'second\nthird'})
        for text, needle in [('duplicate duplicate', 'duplicate'), ('source text', 'absent'), ('text', '')]:
            with self.subTest(needle=needle), self.assertRaises(AssertionError):
                consolidation.retained_anchor(text, needle)


if __name__ == '__main__':
    unittest.main()
