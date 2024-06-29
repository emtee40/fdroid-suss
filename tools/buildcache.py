#! /usr/bin/env python3

import json
import os
from datetime import datetime
from pathlib import Path

import ruamel.yaml

SIG_SOURCES = {
    'izzy.json': Path('izzy'),
    'suss.json': Path('suss'),
}


CONFIG_DEFAULTS = {'cache_duration': 86400}


def parseyml(filepath):
    with open(filepath, 'r', encoding='utf8') as f:
        yaml = ruamel.yaml.YAML(typ='safe')
        return yaml.load(f)


if __name__ == '__main__':
    outdir = Path('public')
    outdir.mkdir(exist_ok=True)

    config = dict(CONFIG_DEFAULTS)
    config.update(parseyml('config.yml'))

    for cachefilename, sigdir in SIG_SOURCES.items():
        print('assembling', cachefilename, '...', end=' ')
        cache = {
            'timestamp': datetime.utcnow().timestamp(),
            'version': 1,
            'signatures': {},
            'cache_duration': config['cache_duration'],
        }
        sigdir.mkdir(exist_ok=True)
        for name, data in [
            (x, parseyml(sigdir / x)) for x in os.listdir(sigdir) if x.endswith('.yml')
        ]:
            cache['signatures'][name[:-4]] = data
        with open(outdir / cachefilename, 'w', encoding='utf8') as f:
            json.dump(cache, f, sort_keys=True, indent=2)
        print(len(cache['signatures']), 'entries ... OK')

    with open(outdir / 'index.html', 'w', encoding='utf8') as f:
        f.write(
            '<html><body><ul>{}</ul></body></html>'.format(
                ''.join(
                    [
                        '<li><a href="{}">{}</a></li>'.format(x, x)
                        for x in SIG_SOURCES.keys()
                    ]
                )
            )
        )
