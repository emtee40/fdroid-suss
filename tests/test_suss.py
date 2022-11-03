#!/usr/bin/env python3

import os
import re
import validators
import unittest
import yaml
from pathlib import Path


def test_suspects_found():
    signatures = []
    for f in (Path(__file__).parent.parent / 'suss').glob('*.yml'):
        with open(f) as fp:
            signatures.append(yaml.safe_load(fp))
    for line in [
        "	compile 'com.google.firebase:firebase-crash:11.0.8'",
        "	compile 'com.google.firebase:firebase-core:11.0.8'",
        'com.firebase:firebase-client-android:2.5.2',
        'com.google.firebase.crashlytics',
        'com.google.firebase.firebase-perf',
        'com.google.firebase:firebase-ads',
        'com.google.firebase:firebase-analytics',
        'com.google.firebase:firebase-appindexing',
        'com.google.firebase:firebase-auth',
        'com.google.firebase:firebase-config',
        'com.google.firebase:firebase-core',
        'com.google.firebase:firebase-crash',
        'com.google.firebase:firebase-crashlytics',
        'com.google.firebase:firebase-database',
        'com.google.firebase:firebase-dynamic-links',
        'com.google.firebase:firebase-firestore',
        'com.google.firebase:firebase-inappmessaging',
        'com.google.firebase:firebase-inappmessaging-display',
        'com.google.firebase:firebase-messaging',
        'com.google.firebase:firebase-ml-natural-language',
        'com.google.firebase:firebase-ml-natural-language-smart-reply-model',
        'com.google.firebase:firebase-ml-vision',
        'com.google.firebase:firebase-perf',
        'com.google.firebase:firebase-plugins',
        'com.google.firebase:firebase-storage',
        'com.mapbox.mapboxsdk:mapbox-android-plugin-annotation-v7:0.6.0',
        'com.mapbox.mapboxsdk:mapbox-android-plugin-annotation-v8:0.7.0',
        'com.mapbox.mapboxsdk:mapbox-android-plugin-localization-v7:0.7.0',
        'com.mapbox.mapboxsdk:mapbox-android-plugin-locationlayer:0.4.0',
        'com.mapbox.mapboxsdk:mapbox-android-plugin-markerview-v8:0.3.0',
        'com.mapbox.mapboxsdk:mapbox-android-plugin-places-v8:0.9.0',
        'com.mapbox.mapboxsdk:mapbox-android-plugin-scalebar-v8:0.2.0',
        'com.mapbox.mapboxsdk:mapbox-android-sdk:7.3.0',
    ]:
        matches = []
        for d in signatures:
            gradle_signatures = d.get('gradle_signatures', [])
            for s in gradle_signatures:
                m = re.search(s, line)
                if m:
                    matches.append(s)
        assert matches != [], line + ' should have matches'

    # These are free exceptions to the above rules
    # 'firebase-jobdispatcher', https://github.com/firebase/firebase-jobdispatcher-android/blob/master/LICENSE
    # 'com.firebaseui', https://github.com/firebase/FirebaseUI-Android/blob/master/LICENSE
    # 'geofire-android', https://github.com/firebase/geofire-java/blob/master/LICENSE
    # 'com.yandex.android:authsdk', https://github.com/yandexmobile/yandex-login-sdk-android/blob/master/LICENSE.txt
    # 'com.hypertrack:hyperlog', https://github.com/hypertrack/hyperlog-android#license
    # 'com.mapbox.mapboxsdk:mapbox-sdk-services',  # https://github.com/mapbox/mapbox-java/blob/main/LICENSE
    # 'com.github.johan12345' https://github.com/johan12345/EVMap/blob/19c0f311ad/app/build.gradle#L199-L213
    for line in [
        "    compile 'com.firebase:firebase-jobdispatcher:0.8.4'",
        "    compile 'com.firebaseui:firebase-ui-auth:3.1.3'",
        "implementation 'com.firebase:geofire-java:3.0.0'",
        'com.firebaseui:firebase-ui-database',
        'com.firebaseui:firebase-ui-storage',
        'com.github.axet:android-firebase-fake',
        'com.github.b3er.rxfirebase:firebase-database',
        'com.github.b3er.rxfirebase:firebase-database-kotlin',
        'com.hypertrack:hyperlog',
        'com.mapbox.mapboxsdk:mapbox-sdk-services:5.0.0',
        'com.segment.analytics.android.integrations:firebase',
        'com.yandex.android:authsdk',
        'implementation("com.github.johan12345.AnyMaps:anymaps-mapbox:$anyMapsVersion")',
        'com.github.johan12345:mapbox-events-android:a21c324501',
    ]:
        matches = []
        for d in signatures:
            gradle_signatures = d.get('gradle_signatures', [])
            for s in gradle_signatures:
                m = re.search(s, line)
                if m:
                    matches.append(s)
        assert matches == [], line + ' should not have matches'


class TestValidate(unittest.TestCase):
    def setUp(self):
        self.all_yml = (Path(__file__).parent.parent / 'suss').glob('*.yml')

    def test_validate_all_regexs(self):
        """Compile all regexs and try a search"""
        for f in self.all_yml:
            with open(f) as fp:
                profile = yaml.safe_load(fp)
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
                    f_rel = f.relative_to(os.getcwd())
                    if isinstance(v, str):
                        out = '%s: %s: %s' % (f_rel, k, v)
                        with self.subTest(out):
                            self.assertIsNotNone(re.compile(v))
                    elif isinstance(v, str):
                        for pat in v:
                            out = '%s: %s: %s' % (f_rel, k, pat)
                            with self.subTest(out):
                                self.assertIsNotNone(re.compile(pat))

    def test_validate_all_urls(self):
        """Validate all fields that should contain URLs"""

        def _raise_if_bad(f, s):
            with self.subTest('%s' % f.relative_to(os.getcwd())):
                self.assertTrue(validators.url(s, public=True))

        for f in self.all_yml:
            with open(f) as fp:
                profile = yaml.safe_load(fp)
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
    test_suspects_found()
    os.chdir(Path(__file__).parent.parent)
    newSuite = unittest.TestSuite()
    newSuite.addTest(unittest.makeSuite(TestValidate))
    unittest.main(failfast=False)
