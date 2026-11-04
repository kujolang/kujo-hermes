import json
import tempfile
from pathlib import Path
import unittest
from kujo_hermes.approval import ApprovalGate
from kujo_hermes.config import Config
from kujo_hermes.service import Service

class ApprovalTests(unittest.TestCase):
 def test_exact_human_one_time_grant(self):
  with tempfile.TemporaryDirectory() as temp:
   service=Service(Config(trusted_workspaces=(temp,),profile='full'),Path(temp)/'state')
   # Catalog description labels Scout as mutating; use extension to avoid external dependency.
   item=service.catalog.get('kujo.ability.catalog.list'); item['extension']=True; item['binding']={'argv':['/bin/echo','ok']}
   service.catalog.entries[item['definition']['id']]=item
   gate=ApprovalGate(service); args={'ability':item['definition']['id'],'input':{},'workspace':temp}
   directive=gate.pre_tool('kujo_execute',args); reason=directive['message']
   self.assertFalse(gate.consume('',reason)['approved'])
   gate.response(pattern_key='plugin_rule:'+directive['rule_key'],choice='once')
   changed=json.loads(reason); changed['request_digest']='wrong'
   self.assertFalse(gate.consume('',json.dumps(changed))['approved'])
   self.assertTrue(gate.consume('',reason)['approved'])
   self.assertFalse(gate.consume('',reason)['approved'])
 def test_untrusted_preflight(self):
  with tempfile.TemporaryDirectory() as temp:
   gate=ApprovalGate(Service(Config(profile='full'),Path(temp)/'state'))
   self.assertEqual(gate.pre_tool('kujo_execute',{'ability':'kujo.ability.catalog.list','input':{},'workspace':temp})['action'],'block')
