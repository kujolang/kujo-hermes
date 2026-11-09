#!/usr/bin/env python3
"""Independently check recorded receipt and artifact hashes without importing the plugin.
This checks integrity, not authorship or the truth of arbitrary verification claims.
"""
import argparse
import hashlib
import json
from pathlib import Path


def verify(directory):
    root = Path(directory).resolve()
    for stage, expected in [('before', (2, 1)), ('after', (3, 0))]:
        value = json.loads((root/(stage+'-receipt.json')).read_text())
        claimed = value.pop('receipt_digest')
        actual = hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
        if claimed != actual: raise ValueError(stage+': receipt digest mismatch')
        result = value['result']['structured']['data']
        if (result['passed'], result['failed']) != expected: raise ValueError(stage+': unexpected verdict')
        snapshot = (root/(stage+'-snapshot')).resolve()
        for item in value['artifacts']['files']:
            file = snapshot/item['path']
            if file.is_symlink() or not file.resolve().is_relative_to(snapshot):
                raise ValueError('Artifact escapes snapshot')
            if hashlib.sha256(file.read_bytes()).hexdigest() != item['sha256']:
                raise ValueError(stage+': artifact mismatch: '+item['path'])
        print(stage+': receipt and '+str(len(value['artifacts']['files']))+' artifact hashes match')
    if (root/'before-snapshot/test_checkout.py').read_bytes() != (root/'after-snapshot/test_checkout.py').read_bytes():
        raise ValueError('Tests changed between runs')
    print('PASS: the same tests failed before and passed after; stored artifacts match both receipts.')

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory')
    verify(p.parse_args().directory)
