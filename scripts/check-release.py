#!/usr/bin/env python3
"""Validate release archive layout, isolation and repeatable packaging."""
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

archive = Path(sys.argv[1]).resolve()
with tempfile.TemporaryDirectory() as temp:
    folder = Path(temp)
    with zipfile.ZipFile(archive) as bundle:
        assert archive.stat().st_size < 1024 * 1024, 'Review intentional archive growth before raising the 1 MiB budget'
        for name in bundle.namelist():
            path = Path(name)
            assert path.parts[0] == 'kujo-hermes' and '..' not in path.parts
            assert not set(path.parts) & {'.git', '.local', 'demo', '__pycache__'}
        bundle.extractall(folder)
    plugin = folder/'kujo-hermes'
    assert (plugin/'plugin.yaml').is_file()
    subprocess.run([sys.executable, '-I', '-c', '''
import sys
sys.path.insert(0, sys.argv[1])
from kujo_hermes.catalog import Catalog
from kujo_hermes.config import Config
assert len(Catalog(Config(profile="full")).all()) == 51
''', str(plugin)], cwd=folder, check=True)
    subprocess.run([sys.executable, str(Path(__file__).with_name('package-release.py')), '--output', str(folder/'repeat')], check=True)
    assert hashlib.sha256(archive.read_bytes()).digest() == hashlib.sha256((folder/'repeat'/archive.name).read_bytes()).digest()
print('Native archive: complete catalog, safe layout, size budget and reproducibility verified')
