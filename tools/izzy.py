#!/usr/bin/env python3

import json
import os
import sys
import yaml
import urllib.request
from pathlib import Path


def selective_representer(dumper, data):
    out = data.strip()
    return dumper.represent_scalar(
        u"tag:yaml.org,2002:str",
        out,
        style="|" if len(out) > 60 or '\n' in out else None,
    )


if __name__ == "__main__":
    yaml.add_representer(str, selective_representer)

    outdir = Path('izzy')
    os.makedirs(outdir, exist_ok=True)

    for libfileurl in [
        'https://gitlab.com/IzzyOnDroid/repo/-/raw/master/lib/libinfo.jsonl',
        'https://gitlab.com/IzzyOnDroid/repo/-/raw/master/lib/libsmali.jsonl',
    ]:
        cnt = 0
        print('processing \'', libfileurl, '\' ...', end=' ')
        with urllib.request.urlopen(libfileurl) as f:
            for line in f:
                data = json.loads(line)
                if not data.get('anti') and data.get('license'):
                    continue
                name = data['id'].strip('/').replace('/', '.')
                out = dict()
                for k, v in data.items():
                    if not v:
                        continue
                    if k == 'anti':
                        out['anti_features'] = v
                    elif k == 'details':
                        out['description'] = v
                    elif k == 'id':
                        out['code_signatures'] = [v.strip('/').replace('/', '\\.')]
                    else:
                        out[k] = v
                with open(outdir / (name + '.yml'), 'w', encoding='utf8') as fout:
                    yaml.dump(out, fout, default_flow_style=False)
                cnt += 1
        print('updated', cnt, 'files ... OK')
