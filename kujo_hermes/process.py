"""Bounded argv-only execution with process-group cancellation (POSIX)."""
import os
import selectors
import signal
import subprocess
import time

def terminate(proc):
    # Kill the group even when the leader exited, to clean up descendants.
    try: os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError: pass
    proc.wait()

def run(argv, cwd, env, timeout, limit, cancel):
    if os.name != 'posix': raise RuntimeError('Supported execution hosts are macOS and Linux')
    started=time.monotonic()
    proc=subprocess.Popen(argv,cwd=cwd,env=env,stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    selector=selectors.DefaultSelector(); streams={'stdout':bytearray(),'stderr':bytearray()}
    for key,pipe in [('stdout',proc.stdout),('stderr',proc.stderr)]:
        os.set_blocking(pipe.fileno(),False); selector.register(pipe,selectors.EVENT_READ,key)
    status='completed'; total=0
    try:
        while selector.get_map():
            if cancel.is_set(): status='cancelled'; break
            if time.monotonic()-started>timeout: status='timeout'; break
            for key,_ in selector.select(0.05):
                data=os.read(key.fileobj.fileno(),65536)
                if not data: selector.unregister(key.fileobj); continue
                total+=len(data)
                remaining=max(0,limit-sum(map(len,streams.values())))
                streams[key.data].extend(data[:remaining])
                if total>limit: status='output_limit'; break
            if status!='completed': break
        if status=='completed':
            while proc.poll() is None:
                if cancel.is_set(): status='cancelled'; break
                if time.monotonic()-started>timeout: status='timeout'; break
                cancel.wait(0.02)
    finally:
        terminate(proc); selector.close(); proc.stdout.close(); proc.stderr.close()
    return {'status':status,'exit_code':proc.returncode,
        **{k:v.decode('utf-8','replace') for k,v in streams.items()},
        'duration_ms':int((time.monotonic()-started)*1000)}
