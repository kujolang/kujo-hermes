"""Continue the actual native setup in Hermes's selected supported interpreter."""
import subprocess,time
print('$ hermes kujo setup --trust-workspace .',flush=True)
time.sleep(1)
subprocess.run(['hermes','kujo','setup','--trust-workspace','.'],check=True)
time.sleep(3)
