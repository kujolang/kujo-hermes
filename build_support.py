"""Bundle host-independent runtime resources in non-editable Python installs."""
from pathlib import Path
import shutil
from setuptools.command.build_py import build_py


class BuildPy(build_py):
    def run(self):
        super().run()
        source = Path(__file__).resolve().parent
        target = Path(self.build_lib) / 'kujo_hermes' / '_resources'
        for directory in ('catalog', 'skills'):
            shutil.copytree(source / directory, target / directory, dirs_exist_ok=True)
        (target / 'scripts').mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / 'scripts/install-sources.py', target / 'scripts/install-sources.py')
