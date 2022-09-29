#! /usr/bin/env python3

from pathlib import Path
from datetime import datetime
import os
import json
import yaml


SIG_SOURCES = {
    'izzy.json': Path('izzy'),
    'suss.json': Path('suss'),
}


def parseyml(filepath):
    with open(filepath, 'r', encoding='utf8') as f:
        return yaml.safe_load(f)


if __name__ == '__main__':
    outdir = Path('public')
    outdir.mkdir(exist_ok=True)

    for cachefilename, sigdir in SIG_SOURCES.items():
        print('assembling', cachefilename, '...', end=' ')
        cache = {
            'timestamp': datetime.now().astimezone().isoformat(),
            'version': 1,
            'signatures': {}
        }
        sigdir.mkdir(exist_ok=True)
        for name, data in [(x, parseyml(sigdir / x)) for x in os.listdir(sigdir) if x.endswith('.yml')]:
            cache['signatures'][name[:-4]] = data
        with open(outdir / cachefilename, 'w', encoding='utf8') as f:
            json.dump(cache, f, sort_keys=True, indent=2)
        print(len(cache['signatures']), 'entries ... OK')

    with open(outdir / 'index.html', 'w', encoding='utf8') as f:
        f.write('<html><body><ul>{}</ul></body></html>'.format(''.join(['<li><a href="{}">{}</a></li>'.format(x, x) for x in SIG_SOURCES.keys()])))
