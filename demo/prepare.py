#!/usr/bin/env python3
"""Create a fresh, reproducible demo repository. No simulated command outputs."""
import json,pathlib,shutil,subprocess,sys
root=pathlib.Path(__file__).resolve().parents[1]
if len(sys.argv)!=2: raise SystemExit('Usage: python3 demo/prepare.py /absolute/new/demo-repository')
target=pathlib.Path(sys.argv[1]).resolve()
if target.exists(): raise SystemExit('Refusing to overwrite an existing demo directory')
target.mkdir(parents=True); (target/'tests').mkdir()
(target/'calculator.py').write_text('def add(a, b):\n    return a + b\n')
(target/'tests/test_calculator.py').write_text('import unittest\nfrom calculator import add\nclass TestAdd(unittest.TestCase):\n    def test_add(self): self.assertEqual(add(2, 3), 5)\n')
(target/'README.md').write_text('# Hermes demo\n\n## Install\nPython 3.11+.\n\n## Usage\n`python3 -m unittest discover -s tests`\n')
(target/'VERSION').write_text('0.1.0\n'); (target/'LICENSE').write_text('MIT\n'); (target/'CHANGELOG.md').write_text('# Changes\n\nInitial fixture.\n')
(target/'.gitignore').write_text('__pycache__/\n.kujo/\n.loop-engineering/\n')
(target/'task.spec.json').write_text(json.dumps({'name':'Verify the calculator','goal':'Prove addition works and preserve execution evidence.','version':'0.1.0','scope':'calculator.py and tests','acceptance_criteria':['2 + 3 returns 5','All unit tests pass']},indent=2)+'\n')
(target/'eval.json').write_text(json.dumps({'name':'hermes-demo','tests':[{'name':'unit suite','check':'command_succeeds','params':{'command':'python3 -m unittest discover -s tests'}},{'name':'implementation exists','check':'file_exists','params':{'path':'calculator.py'}}]},indent=2)+'\n')
shutil.copytree(root/'agent',target/'agent')
for argv in [['git','init','-q'],['git','add','.'],['git','-c','user.name=Kujo Demo','-c','user.email=demo@example.invalid','commit','-qm','Reproducible Hermes demo fixture']]: subprocess.run(argv,cwd=target,check=True)
print(target)
