"""Record actual CLI commands; the operator answers Hermes consent prompts."""
import subprocess,time
for command in [['hermes','plugins','install','kujolang/kujo-hermes'],['hermes','kujo','setup','--trust-workspace','.']]:
 print('\n$ '+' '.join(command),flush=True)
 time.sleep(1)
 subprocess.run(command,check=True)
 time.sleep(2)
