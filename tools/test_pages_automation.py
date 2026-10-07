#!/usr/bin/env python3
"""Offline regression tests: no credentials, database, or production writes."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from pages_automation import resolve, fingerprint


class AutomationTests(unittest.TestCase):
    def setUp(self):
        self.alias = {'projectId': 'prj_peace', 'deploymentId': 'dpl_peace'}
        self.deployment = {'id': 'dpl_peace', 'projectId': 'prj_peace', 'target': 'production',
                           'readyState': 'READY', 'gitSource': {'sha': 'a' * 40},
                           'meta': {'githubCommitOrg': 'AcoHon53114', 'githubCommitRepo': 'peace'}}

    def get(self, path, token, team, params):
        return copy.deepcopy(self.alias if '/aliases/' in path else self.deployment)

    def resolve(self):
        return resolve('https://peace-beta-sandy.vercel.app', 'prj_peace', 'test-token', fetch=self.get)

    def test_current_production_commit(self):
        self.assertEqual(self.resolve()['sha'], 'a' * 40)

    def test_preview_is_rejected(self):
        self.deployment['target'] = None
        with self.assertRaises(ValueError): self.resolve()

    def test_other_project_is_rejected(self):
        self.alias['projectId'] = 'prj_other'
        with self.assertRaises(ValueError): self.resolve()

    def test_unready_is_rejected(self):
        self.deployment['readyState'] = 'BUILDING'
        with self.assertRaises(ValueError): self.resolve()

    def test_missing_sha_is_rejected(self):
        self.deployment['gitSource'] = {}
        with self.assertRaises(ValueError): self.resolve()

    def test_legacy_commit_metadata(self):
        self.deployment['gitSource'] = {}
        self.deployment['meta']['githubCommitSha'] = 'b' * 40
        self.assertEqual(self.resolve()['sha'], 'b' * 40)

    def test_rollback_changes_identity(self):
        before = self.resolve()
        self.deployment['gitSource']['sha'] = 'c' * 40
        self.assertNotEqual(before, self.resolve())

    def test_wrong_repository_is_rejected(self):
        self.deployment['meta']['githubCommitRepo'] = 'other'
        with self.assertRaises(ValueError): self.resolve()

    def test_source_with_path_is_rejected(self):
        with self.assertRaises(ValueError):
            resolve('https://example.com/admin/', 'prj_peace', 'test', fetch=self.get)

    def test_fingerprint_content_images_and_relative_age(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / 'en/news/index.html'
            page.parent.mkdir(parents=True)
            html = '<div class="custom-block-body"><h5>Title</h5><i class="bi-calendar4"></i>DATE<br><i class="bi-calendar4"></i><span>1 hour</span><h7>Body</h7></div>'
            page.write_text(html)
            image = root / 'image.webp'
            image.write_bytes(b'first')
            original = fingerprint(root)
            page.write_text(html.replace('1 hour', '2 hours'))
            self.assertEqual(original, fingerprint(root))
            (root / 'export-report.json').write_text(json.dumps({'source': 'changed'}))
            self.assertEqual(original, fingerprint(root))
            for old, new in [('Title', 'New title'), ('Body', 'Changed body'), ('DATE', 'NEWDATE')]:
                page.write_text(html.replace(old, new))
                self.assertNotEqual(original, fingerprint(root))
            page.write_text(html)
            image.write_bytes(b'second')
            self.assertNotEqual(original, fingerprint(root))


if __name__ == '__main__':
    unittest.main()
