#! /usr/bin/env python3

from pathlib import Path
from datetime import datetime
import os
import json
import yaml


def parseyml(filepath):
    with open(filepath, 'r', encoding='utf8') as f:
        return yaml.safe_load(f)


if __name__ == '__main__':
    for cachefilename, sigdir in [('izzy.json', Path('izzy')), ('sigs.json', Path('sigs'))]:
        print('assembling', cachefilename, '...', end=' ')
        cache = {
            'timestamp': datetime.now().astimezone().isoformat(),
            'version': 1,
            'signatures': {}
        }
        for name, data in [(x, parseyml(sigdir / x)) for x in os.listdir(sigdir) if x.endswith('.yml')]:
            cache['signatures'][name[:-4]] = data
        with open(cachefilename, 'w', encoding='utf8') as f:
            json.dump(cache, f, sort_keys=True, indent=2)
        print(len(cache['signatures']), 'entries ... OK')
