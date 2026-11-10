#!/usr/bin/env python3
"""Build a deterministic native plugin archive without development/media assets."""
import argparse
import hashlib
from pathlib import Path
import tomllib
import zipfile

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
version = tomllib.loads((root/'pyproject.toml').read_text())['project']['version']
args.output.mkdir(parents=True, exist_ok=True)
paths = [root/name for name in ('__init__.py', 'plugin.yaml', 'README.md', 'LICENSE', 'SECURITY.md', 'CHANGELOG.md', 'pyproject.toml', 'build_support.py', 'MANIFEST.in', 'scripts/install-sources.py')]
for directory, pattern in [('kujo_hermes', '*.py'), ('catalog', '*.json'), ('skills', '*.md'), ('docs', '*.md'), ('docs', '*.json')]:
    paths.extend((root/directory).rglob(pattern))
paths.extend((root/'kujo_hermes').rglob('LICENSE*'))
archive = args.output/f'kujo-hermes-{version}-plugin.zip'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as bundle:
    for path in sorted(set(paths)):
        if '_resources' in path.parts:
            continue
        info = zipfile.ZipInfo('kujo-hermes/'+path.relative_to(root).as_posix(), (2026, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        bundle.writestr(info, path.read_bytes())
with (args.output/'SHA256SUMS').open('w') as checksums:
    for path in sorted(args.output.iterdir()):
        if path.suffix in ('.zip', '.whl', '.gz'):
            checksums.write(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n')
print(archive)
