"""Operator-owned configuration. Never load policy from a target repository."""
from dataclasses import dataclass, field
from pathlib import Path
import os

@dataclass(frozen=True)
class Config:
    ecosystem_root: str = ''
    kujo_bin: str = 'kujo'
    trusted_workspaces: tuple = ()
    profile: str = 'essentials'
    timeout_seconds: int = 240
    max_output_bytes: int = 524288
    extension_catalogs: tuple = ()
    denied_abilities: tuple = ()
    secrets: tuple = ()

    @classmethod
    def parse(cls, values):
        unknown = set(values) - set(cls.__dataclass_fields__)
        if unknown: raise ValueError('Unknown configuration: ' + ', '.join(sorted(unknown)))
        data = dict(values)
        for key in ('trusted_workspaces', 'extension_catalogs', 'denied_abilities', 'secrets'):
            value = data.get(key, ())
            if not isinstance(value, (list, tuple)) or any(not isinstance(x, str) for x in value):
                raise ValueError(key + ' must be a list of strings')
            data[key] = tuple(value)
        result = cls(**data)
        if result.profile not in ('essentials','review','ship','full'): raise ValueError('Invalid profile')
        for key, low, high in [('timeout_seconds',1,900),('max_output_bytes',1024,4194304)]:
            v = getattr(result,key)
            if type(v) is not int or not low <= v <= high: raise ValueError('Invalid '+key)
        for key in ('ecosystem_root','kujo_bin'):
            if not isinstance(getattr(result,key),str): raise ValueError(key+' must be a string')
        for p in (*result.trusted_workspaces,*result.extension_catalogs):
            if not Path(p).is_absolute(): raise ValueError('Configuration paths must be absolute')
        if result.ecosystem_root and not Path(result.ecosystem_root).is_absolute(): raise ValueError('ecosystem_root must be absolute')
        if any(not x.isidentifier() or not x.isupper() for x in result.secrets): raise ValueError('Invalid secret variable name')
        forbidden={'PATH','HOME','TMPDIR','KUJO','KUJO_BIN','MUZZLE_ROOT','BASH_ENV','ENV','PYTHONPATH','PYTHONHOME','NODE_OPTIONS','LD_PRELOAD','LD_LIBRARY_PATH','DYLD_INSERT_LIBRARIES','DYLD_LIBRARY_PATH'}
        if forbidden.intersection(result.secrets): raise ValueError('Secrets cannot override execution controls')
        return result

    def workspace(self, value):
        p = Path(value).resolve(strict=True)
        if not p.is_dir(): raise ValueError('Workspace must be a directory')
        # Exact roots prevent a broad ancestor grant silently authorizing every repo.
        if p not in [Path(x).resolve(strict=True) for x in self.trusted_workspaces]:
            raise PermissionError('Untrusted workspace: add its exact absolute root in Hermes settings')
        return p


def contained(root, value, must_exist=False):
    p = (root / value).resolve(strict=must_exist)
    if not p.is_relative_to(root): raise PermissionError('Path escapes trusted workspace')
    return str(p)
