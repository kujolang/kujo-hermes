"""Record an actual checkout charge, with the command visible."""
import pathlib,subprocess,time
folder=pathlib.Path(__file__).resolve().parent
print('$ python3 show_charge.py',flush=True);time.sleep(1)
subprocess.run(['python3','show_charge.py'],cwd=folder,check=True);time.sleep(5)
