#!/usr/bin/env python3

import os
import re
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
    ]:
        matches = []
        for d in signatures:
            gradle_signatures = d.get('gradle_signatures', [])
            for s in  gradle_signatures:
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
        'com.segment.analytics.android.integrations:firebase',
        'com.yandex.android:authsdk',
    ]:
        matches = []
        for d in signatures:
            gradle_signatures = d.get('gradle_signatures', [])
            for s in  gradle_signatures:
                m = re.search(s, line)
                if m:
                    matches.append(s)
        assert matches == [], line + ' should not have matches'
