"""Record real independent checks; prints the exact command before execution."""
import pathlib,subprocess,time
root=pathlib.Path(__file__).resolve().parents[3]
command=['python3','demo/checkout/verify.py','demo/checkout-video/evidence/run']
print('$ '+' '.join(command),flush=True);time.sleep(1)
subprocess.run(command,cwd=root,check=True);time.sleep(4)
