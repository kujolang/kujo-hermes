"""Record git's actual diff after the model changes checkout.py."""
import pathlib,subprocess,time
root=pathlib.Path(__file__).resolve().parents[3]
command=['git','--no-pager','diff','--color=always','--unified=2','--','checkout.py']
print('$ '+' '.join(command),flush=True);time.sleep(1)
subprocess.run(command,cwd=root/'.local/checkout-recording/workspace',check=True);time.sleep(5)
