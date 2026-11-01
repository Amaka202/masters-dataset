"""Own packager rejection tests; no retained source code is executed."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from package_training_audit import MANIFEST, audit_files, checked_source


class AuditPackagingTests(unittest.TestCase):
    def test_source_name_cannot_leave_flat_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            for name in ('../outside.json', '/outside.json', '.', '..', ''):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    checked_source(Path(directory), name)

    def test_changed_source_is_rejected_without_overwriting_it(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            path = source/'record.json'
            path.write_bytes(b'changed evidence')
            with self.assertRaisesRegex(ValueError, 'digest mismatch'):
                checked_source(source, path.name, hashlib.sha256(b'original evidence').hexdigest())
            self.assertEqual(path.read_bytes(), b'changed evidence')

    def test_manifest_with_stale_generated_output_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source/'reviews.json').write_bytes(b'changed generated output')
            manifest = dict(scope='training_only', training_candidates=742,
                            consolidation_reviewed_candidates=742, researcher_approval_ready=False,
                            source_sha256={}, output_sha256={
                                'reviews.json': hashlib.sha256(b'original output').hexdigest()})
            (source/MANIFEST).write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, 'digest mismatch: reviews.json'):
                audit_files(source)


if __name__ == '__main__':
    unittest.main()
