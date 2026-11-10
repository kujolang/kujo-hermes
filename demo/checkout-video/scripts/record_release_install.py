"""Record real, pinned installation commands; operator answers native prompts.
Requires an installed Hermes >=0.22.7, official Kujo on PATH, Git and disk space.
No runtime flags, dependency policies or approval checks are bypassed.
"""
import argparse
import os
from pathlib import Path
import subprocess
import time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--home', type=Path, required=True, help='Dedicated Hermes test home')
parser.add_argument('--workspace', type=Path, required=True, help='Dedicated repository to trust')
parser.add_argument('--ref', default='4f7b27ef0216cf6284af42fb23f5211a22befd0b')
args = parser.parse_args()
home = args.home.resolve()
workspace = args.workspace.resolve()
workspace.mkdir(parents=True, exist_ok=True)
os.environ['HERMES_HOME'] = str(home)
os.chdir(workspace)
for command in (
    ['hermes', 'plugins', 'install', 'kujolang/kujo-hermes', '--ref', args.ref],
    ['hermes', 'kujo', 'setup', '--trust-workspace', '.'],
):
    print('\n$ '+' '.join(command), flush=True)
    time.sleep(1)
    subprocess.run(command, check=True)
    time.sleep(3)
sha = subprocess.check_output(['git', '-C', str(home/'plugins/kujo-hermes'), 'rev-parse', 'HEAD'], text=True).strip()
assert sha == args.ref, sha
print('\nInstalled candidate '+sha, flush=True)
time.sleep(5)
