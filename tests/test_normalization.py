"""Input normalization and approval resource boundary regressions."""
import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from jsonschema import ValidationError

from kujo_hermes.approval import ApprovalGate
from kujo_hermes.config import Config
from kujo_hermes.service import Service


class NormalizationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.service = Service(Config(profile='full', trusted_workspaces=(self.temp.name,)),
                               Path(self.temp.name)/'state')
        self.addCleanup(self.service.close)
        self.item = copy.deepcopy(self.service.catalog.get('kujo.ability.catalog.list'))
        self.item.update(extension=True, binding={'argv': ['/bin/echo', 'ok']})
        self.service.catalog.entries[self.item['definition']['id']] = self.item
        self.gate = ApprovalGate(self.service)
        self.args = {'ability': self.item['definition']['id'], 'input': {}, 'workspace': self.temp.name}

    def inputs(self, schema, supplied):
        self.item['definition']['input_schema'] = schema
        return self.service.catalog.inputs(self.item, supplied)

    def test_boolean_property_schemas_are_supported(self):
        self.assertEqual(self.inputs({'type':'object', 'properties':{'allowed':True,'forbidden':False}}, {}), {})

    def test_invalid_default_is_rejected(self):
        with self.assertRaises(ValidationError):
            self.inputs({'type':'object', 'properties':{'count':{'type':'integer','default':'invalid'}}}, {})

    def test_defaults_cannot_break_object_constraints(self):
        with self.assertRaises(ValidationError):
            self.inputs({'type':'object','maxProperties':1,'properties':{
                'first':{'type':'integer','default':1}, 'second':{'type':'integer','default':2}}}, {})

    def test_default_expansion_is_size_bounded(self):
        with self.assertRaisesRegex(ValueError, '64 KiB'):
            self.inputs({'type':'object','properties':{'text':{'type':'string','default':'x'*65536}}}, {})

    def test_preflight_rejects_oversize_input_without_prompt(self):
        self.item['definition']['input_schema'] = {'type':'object'}
        self.args['input'] = {'text':'x'*65536}
        result = self.gate.pre_tool('kujo_execute', self.args)
        self.assertEqual(result['action'], 'block')
        self.assertIn('64 KiB', result['message'])
        self.assertEqual(self.gate.pending, {})

    def test_preflight_error_is_bounded_and_redacted(self):
        with patch.object(self.service.catalog, 'get', side_effect=ValueError('token=sensitive '+ 'x'*20000)):
            result = self.gate.pre_tool('kujo_execute', self.args)
        self.assertEqual(result['action'], 'block')
        self.assertLessEqual(len(result['message']), 8192)
        self.assertNotIn('sensitive', result['message'])

    def test_grants_and_pending_share_capacity(self):
        for _ in range(100):
            directive = self.gate.pre_tool('kujo_execute', self.args)
            self.assertEqual(directive['action'], 'approve')
            self.gate.response(pattern_key='plugin_rule:'+directive['rule_key'], choice='once')
        blocked = self.gate.pre_tool('kujo_execute', self.args)
        self.assertEqual(blocked['action'], 'block')
        self.assertEqual(len(self.gate.grants), 100)
        self.assertTrue(self.gate.consume('', directive['message'])['approved'])
        self.assertEqual(self.gate.pre_tool('kujo_execute', self.args)['action'], 'approve')
