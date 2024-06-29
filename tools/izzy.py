#!/usr/bin/env python3

import json
import os
import re
import urllib.request
from pathlib import Path

import ruamel.yaml

if __name__ == "__main__":
    outdir = Path('izzy')
    os.makedirs(outdir, exist_ok=True)

    known_regex = []

    for file in Path('suss').glob('*.yml'):
        yaml = ruamel.yaml.YAML(typ='safe')
        signatures = map(re.compile, yaml.load(file).get('code_signatures', []))
        known_regex.extend(signatures)

    libinfourl = 'https://gitlab.com/IzzyOnDroid/repo/-/raw/master/lib/libinfo.jsonl'
    libsmaliurl = 'https://gitlab.com/IzzyOnDroid/repo/-/raw/master/lib/libsmali.jsonl'
    libs = {}
    cnt = 0
    new = 0

    with urllib.request.urlopen(libinfourl) as f:
        for line in f:
            data = json.loads(line)
            if data.get('license') == "Proprietary":
                libs[data["id"]] = data

    with urllib.request.urlopen(libsmaliurl) as f:
        for line in f:
            smali = json.loads(line)
            info = libs.get(smali['id'])
            if not info:
                continue
            id = smali['id'].strip('/').replace('/', '.')

            out = {
                'license': 'NonFree',
                'anti_features': info.get('anti'),
                'description': info.get('details'),
                'code_signatures': [smali.get('path').strip('/')],
                'name': info.get('name'),
                'documentation': info.get('url'),
            }

            out = {k: v for k, v in out.items() if v and v != [None]}

            with open(outdir / (id + '.yml'), 'w', encoding='utf8') as fout:
                yaml = ruamel.yaml.YAML()
                yaml.indent(mapping=2, sequence=4, offset=2)
                yaml.dump(out, stream=fout)

            for regex in known_regex:
                if out.get('code_signatures') and re.match(
                    regex, out['code_signatures'][0]
                ):
                    break
            else:
                (outdir / 'new').mkdir(exist_ok=True)
                with open(outdir / 'new' / (id + '.yml'), 'w', encoding='utf8') as fout:
                    yaml = ruamel.yaml.YAML()
                    yaml.indent(mapping=2, sequence=4, offset=2)
                    yaml.dump(out, stream=fout)

                new += 1

            cnt += 1

    print('imported', cnt, 'files')
    print(new, 'new files')
