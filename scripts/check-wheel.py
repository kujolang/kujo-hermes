#!/usr/bin/env python3
"""Check a non-editable wheel outside the source checkout."""
import pathlib
import subprocess
import sys
import tempfile

wheel = pathlib.Path(sys.argv[1]).resolve()
with tempfile.TemporaryDirectory() as folder:
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--no-deps', '--target', folder, str(wheel)], check=True)
    subprocess.run([sys.executable, '-I', '-c', '''
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from kujo_hermes.catalog import Catalog
from kujo_hermes.config import Config
from kujo_hermes.resources import ROOT
assert ROOT.is_relative_to(Path(sys.argv[1]).resolve())
assert len(Catalog(Config(profile="full")).all()) == 51
for name in ("catalog/profiles.json", "catalog/sources.lock.json", "skills/kujo-engineering/SKILL.md", "scripts/install-sources.py"):
    assert (ROOT/name).is_file(), name
print("Installed wheel: 51 Abilities and all runtime resources verified")
''', folder], cwd=folder, check=True)
