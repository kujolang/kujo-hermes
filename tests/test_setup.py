"""Onboarding cannot erase policy, infer trust, or overwrite unrelated settings."""
import argparse
import copy
import pathlib
import sys
import tempfile
import unittest
from kujo_hermes.setup import existing_settings, settings_plan, parser_setup

class SetupTests(unittest.TestCase):
    def arguments(self, *extra):
        parser=argparse.ArgumentParser();parser_setup(parser)
        return parser.parse_args(['setup','--kujo-bin',sys.executable,*extra])
    def test_preserves_policy_and_does_not_infer_trust(self):
        old={'denied_abilities':['kujo.eval.suite.run'],'extension_catalogs':['/reviewed/catalog.json'],
             'secrets':['API_TOKEN'],'trusted_workspaces':['/trusted/repo'],'profile':'review','timeout_seconds':17}
        cfg={'model':'keep','plugins':{'entries':{'kujo-hermes':{'settings':old},'other':{'enabled':True}}}}
        before=copy.deepcopy(cfg);result=settings_plan(cfg,self.arguments())
        for key,value in old.items():self.assertEqual(result[key],value)
        self.assertEqual(cfg,before)
    def test_explicit_exact_repository_trust_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            root=pathlib.Path(temp);(root/'.git').mkdir()
            args=self.arguments('--trust-workspace',str(root))
            settings=settings_plan({},args)
            self.assertEqual(settings['trusted_workspaces'],[str(root.resolve())])
            again=settings_plan({'plugins':{'entries':{'kujo-hermes':{'settings':settings}}}},args)
            self.assertEqual(again,settings)
    def test_rejects_parent_directory_and_malformed_policy(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):settings_plan({},self.arguments('--trust-workspace',temp))
        for cfg in [{'plugins':[]},{'plugins':{'entries':{'kujo-hermes':{'settings':[]}}}},
                    {'plugins':{'entries':{'kujo-hermes':{'settings':{'trusted_workspaces':'*'}}}}}]:
            with self.assertRaises(ValueError):settings_plan(cfg,self.arguments())
    def test_missing_runtime_has_install_guidance(self):
        with self.assertRaisesRegex(FileNotFoundError,'Install official Kujo'):
            settings_plan({},self.arguments('--kujo-bin','/missing/kujo-binary'))
    def test_default_full_exposes_tools_without_trust(self):
        result=settings_plan({},self.arguments())
        self.assertEqual(result['profile'],'full');self.assertFalse(result.get('trusted_workspaces'))
    def test_explicit_profile_overrides_only_exposure(self):
        cfg={'plugins':{'entries':{'kujo-hermes':{'settings':{'profile':'essentials','denied_abilities':['a']}}}}}
        result=settings_plan(cfg,self.arguments('--profile','ship'))
        self.assertEqual(result['profile'],'ship');self.assertEqual(result['denied_abilities'],['a'])

if __name__=='__main__':unittest.main()
