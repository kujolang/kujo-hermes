"""Operator-only onboarding through Hermes' native CLI and configuration writer."""
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from .config import Config
from .resources import ROOT


def parser_setup(parser):
    commands = parser.add_subparsers(dest='kujo_action', required=True)
    setup = commands.add_parser('setup', help='Install pinned sources and configure this Hermes profile')
    setup.add_argument('--trust-workspace', help='Explicitly trust this exact repository root for execution')
    setup.add_argument('--sources', help='Destination for pinned canonical source checkouts')
    setup.add_argument('--kujo-bin', help='Existing official Kujo executable (never downloaded)')
    setup.add_argument('--profile', choices=['essentials', 'review', 'ship', 'full'])
    setup.add_argument('--dry-run', action='store_true', help='Check prerequisites and show the plan without fetching or saving')
    commands.add_parser('doctor', help='Inspect configuration and dependencies without repository work')


def existing_settings(config):
    value = config
    for key in ('plugins', 'entries', 'kujo-hermes', 'settings'):
        if not isinstance(value, dict):
            raise ValueError('Expected a mapping at plugins.entries.kujo-hermes.settings')
        value = value.get(key, {})
    if not isinstance(value, dict):
        raise ValueError('Kujo Hermes settings must be a mapping')
    return copy.deepcopy(value)


def settings_plan(config, args):
    settings = existing_settings(config)
    Config.parse(settings)  # Never erase malformed policy to get setup working.
    source = args.sources or settings.get('ecosystem_root') or str(Path.home()/'.local/share/kujo/hermes-sources')
    binary = args.kujo_bin or settings.get('kujo_bin') or 'kujo'
    found = shutil.which(os.path.expanduser(binary))
    if not found:
        raise FileNotFoundError('Install official Kujo >=1.6,<2 first: https://github.com/kujolang/kujo ; or pass --kujo-bin /absolute/path/to/kujo')
    settings.update(ecosystem_root=str(Path(source).expanduser().resolve()), kujo_bin=str(Path(found).resolve()),
                    profile=args.profile or settings.get('profile') or 'full')
    if args.trust_workspace:
        workspace = Path(args.trust_workspace).expanduser().resolve(strict=True)
        if not workspace.is_dir() or not (workspace/'.git').exists():
            raise ValueError('--trust-workspace must name a Git repository root, not a broad parent directory')
        if workspace == Path(workspace.anchor) or workspace == Path.home().resolve():
            raise ValueError('Refusing to trust the filesystem root or home directory')
        trusted = list(settings.get('trusted_workspaces', []))
        if str(workspace) not in trusted:
            trusted.append(str(workspace))
        settings['trusted_workspaces'] = trusted
    Config.parse(settings)
    return settings


def run_setup(args):
    from hermes_cli import config as host_config
    from plugins.plugin_storage import plugin_data_dir
    from .service import Service
    if host_config.is_managed():
        raise PermissionError('This Hermes profile is managed; configure Kujo through its operator-owned configuration')
    original = host_config.require_readable_config_before_write()
    settings = settings_plan(original, args)
    if not shutil.which('git'):
        raise FileNotFoundError('Install Git before running Kujo setup')
    service = Service(Config.parse(settings), plugin_data_dir('kujo-hermes'))
    try:
        version = service.check_runtime()
    finally:
        service.close()
    lock = ROOT/'catalog/sources.lock.json'
    count = len(json.loads(lock.read_text())['sources'])
    print('Kujo Hermes setup')
    print('Runtime:', version)
    print('Sources:', settings['ecosystem_root'], f'({count} pinned official repositories)')
    print('Profile:', settings['profile'])
    print('Trust:', str(Path(args.trust_workspace).expanduser().resolve()) if args.trust_workspace else 'No new workspace grant')
    print('Execution approvals and existing restrictions remain required.')
    if args.dry_run:
        print('Dry run: no sources fetched and no configuration saved.')
        return
    installer = ROOT/'scripts/install-sources.py'
    subprocess.run([sys.executable, str(installer), '--destination', settings['ecosystem_root']], check=True)
    # Re-read after network I/O; refuse a concurrent policy change. Hermes owns atomic writes.
    with host_config._CONFIG_LOCK:
        latest = host_config.require_readable_config_before_write()
        if existing_settings(latest) != existing_settings(original):
            raise RuntimeError('Kujo settings changed during setup; configuration was not saved. Review and rerun.')
        host_config.save_config({'plugins': {'entries': {'kujo-hermes': {'settings': settings}}}}, merge_existing=True)
        if existing_settings(host_config.require_readable_config_before_write()) != settings:
            raise RuntimeError('Hermes did not persist the requested settings; inspect managed policy and rerun')
    print('Setup complete. Start a new Hermes conversation; restart a running gateway.')
    print('Try: Run ShipCheck and show me the release-review findings.')
    print('Use hermes kujo doctor to inspect optional service and tool dependencies.')


def handler(args):
    try:
        if args.kujo_action == 'setup':
            run_setup(args)
        else:
            from hermes_cli.config import load_config_readonly
            from plugins.plugin_storage import plugin_data_dir
            from .service import Service
            service = Service(Config.parse(existing_settings(load_config_readonly())), plugin_data_dir('kujo-hermes'))
            try:
                print(json.dumps(service.doctor(), indent=2))
            finally:
                service.close()
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        print('Kujo setup:', str(error), file=sys.stderr)
        raise SystemExit(1) from None
