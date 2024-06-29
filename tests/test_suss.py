#!/usr/bin/env python3

import os
import re
import unittest
from pathlib import Path

import ruamel.yaml
import validators


class TestValidate(unittest.TestCase):
    def setUp(self):
        self.all_yml = (Path(__file__).parent.parent / 'suss').glob('*.yml')

    def test_validate_all_regexs(self):
        """Compile all regexs and try a search"""
        for f in self.all_yml:
            with open(f) as fp:
                yaml = ruamel.yaml.YAML(typ='safe')
                profile = yaml.load(fp)
            for k in (
                'api_key_ids',
                'artifact_id',
                'code_signatures',
                'gradle_signatures',
                'group_id',
                'network_signatures',
            ):
                if k in profile:
                    v = profile.get(k)
                    if not v:
                        continue
                    assert isinstance(v, list), k + ' should be a list'
                    f_rel = f.relative_to(os.getcwd())
                    for pat in v:
                        out = '%s: %s: %s' % (f_rel, k, pat)
                        with self.subTest(out):
                            self.assertIsNotNone(re.compile(pat))

                    if k == 'gradle_signatures':
                        gradle_signatures = []
                        for pat in v:
                            gradle_signatures.append(re.compile(pat))
                        for p in profile.get('gradle_signatures_positive_examples', []):
                            matches = 0
                            for s in gradle_signatures:
                                if re.search(s, p):
                                    matches += 1
                            out = '%s: %s should match' % (f_rel, p)
                            with self.subTest(out):
                                self.assertTrue(matches > 0)
                        for n in profile.get('gradle_signatures_negative_examples', []):
                            matches = 0
                            for s in gradle_signatures:
                                if re.search(s, n):
                                    matches += 1
                            out = '%s: %s should not match' % (f_rel, n)
                            with self.subTest(out):
                                self.assertTrue(matches == 0)

    def test_validate_all_urls(self):
        """Validate all fields that should contain URLs"""

        def _raise_if_bad(f, s):
            with self.subTest('%s' % f.relative_to(os.getcwd())):
                self.assertTrue(validators.url(s, public=True))

        for f in self.all_yml:
            with open(f) as fp:
                yaml = ruamel.yaml.YAML(typ='safe')
                profile = yaml.load(fp)
            for k in ('documentation', 'maven_repository', 'website'):
                v = profile.get(k)
                if v is None:
                    continue
                elif isinstance(v, str):
                    _raise_if_bad(f, v)
                elif isinstance(v, list):
                    for i in v:
                        _raise_if_bad(f, i)
                else:
                    _raise_if_bad(f, v)


if __name__ == "__main__":
    os.chdir(Path(__file__).parent.parent)
    newSuite = unittest.TestSuite()
    newSuite.addTest(unittest.makeSuite(TestValidate))
    unittest.main(failfast=False)
