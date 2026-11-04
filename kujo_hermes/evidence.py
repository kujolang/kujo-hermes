"""Bounded artifact references; canonical files are never rewritten."""
import hashlib
from pathlib import Path

DEFAULTS={'scout':'.kujo/scout','scent':'.kujo/scent','eval':'.kujo/eval','dispatch_run':'.kujo/dispatch',
 'runledger_start':'.runledger','runledger_finish':'.runledger','casefile':'.casefile/cases',
 'redact_scan':'.redact','redact_sanitize':'.redact','tribunal_review':'.tribunal/runs',
 'howl_render':'dist/howl','lens_check':'.lens/runs/hermes','workcell_run':'.workcell/runs',
 'packwrite_init':'agent','loop':'.loop-engineering'}

def artifact_inventory(workspace,data,operation,max_files=128,max_bytes=10_000_000):
    root=Path(workspace).resolve(); targets=[]
    for key in ('output_dir','output_file','audit_dir','storage_dir','ledger_dir'):
        if key in data: targets.append(root/data[key])
    if operation in DEFAULTS: targets.append(root/DEFAULTS[operation])
    stack=list(targets); seen=set(); records=[]; total=0; examined=0; truncated=False
    while stack:
        p=stack.pop(); examined+=1
        if examined>4096 or len(records)>=max_files: truncated=True; break
        if p.is_symlink(): continue
        resolved=p.resolve()
        if resolved in seen or not resolved.is_relative_to(root): continue
        seen.add(resolved)
        if p.is_dir():
            # Bound directory enumeration independently of file size.
            import os
            with os.scandir(p) as entries:
                for entry in entries:
                    if len(stack)+examined>4096: truncated=True; break
                    stack.append(Path(entry.path))
        elif p.is_file():
            size=p.stat().st_size
            if total+size>max_bytes: truncated=True; continue
            with p.open('rb') as f: raw=f.read(min(size+1,max_bytes-total+1))
            if len(raw)!=size: truncated=True; continue
            total+=size; records.append({'path':str(resolved.relative_to(root)),'bytes':size,'sha256':hashlib.sha256(raw).hexdigest()})
    return {'files':sorted(records,key=lambda x:x['path']),'truncated':truncated,'bytes_hashed':total}
