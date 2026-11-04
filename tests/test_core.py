import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest
from kujo_hermes.config import Config, contained
from kujo_hermes.catalog import Catalog, check_schema
from kujo_hermes.process import run
from kujo_hermes.service import Service, digest, redact

class CoreTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name); self.workspace=self.root/'repo'; self.workspace.mkdir()
  self.cfg=Config(trusted_workspaces=(str(self.workspace),),profile='full')
  self.service=Service(self.cfg,self.root/'state')
 def tearDown(self): self.service.close(); self.tmp.cleanup()
 def extension(self,code,effects='read',output=None):
  item=copy.deepcopy(Catalog(self.cfg).all()['kujo.runtime.version.inspect'])
  item.pop('digest'); item.update({'binding':{'argv':[sys.executable,'-c',code]},'operation':'custom'})
  item['definition']['id']='kujo.test.command.execute'
  item['definition']['effects']=[{'kind':effects,'resource':'kujo.test.command'}]
  item['definition']['output_schema']=output or {}
  path=self.root/'catalog.json'; path.write_text(json.dumps([item])); self.cfg=Config(trusted_workspaces=(str(self.workspace),),profile='full',extension_catalogs=(str(path),))
  self.service=Service(self.cfg,self.root/'state',lambda *a,**k:{'approved':True})
  return item['definition']['id']
 def test_profile_counts(self):
  self.assertEqual([len(Catalog(Config(profile=x)).exposed()) for x in ['essentials','review','ship','full']],[5,18,29,46])
 def test_config_rejects_unknown(self):
  for value in [{'yolo':True},{'timeout_seconds':True},{'profile':'other'},{'trusted_workspaces':['.']}]:
   with self.assertRaises(ValueError): Config.parse(value)
 def test_schema_validation(self):
  item=self.service.catalog.get('kujo.spec.contract.validate')
  for v in [{},{'file':7},{'file':'x','approved':True}]:
   with self.assertRaises(Exception): self.service.catalog.inputs(item,v)
 def test_remote_schema_rejected(self):
  with self.assertRaises(ValueError): check_schema({'$ref':'https://example.com/schema'})
 def test_trust_exact(self):
  child=self.workspace/'child'; child.mkdir()
  with self.assertRaises(PermissionError): self.cfg.workspace(child)
 def test_symlink_escape(self):
  (self.workspace/'escape').symlink_to(self.root)
  with self.assertRaises(PermissionError): contained(self.workspace,'escape/secret')
 def test_lazy_catalog(self): self.assertIsNone(Service(self.cfg,self.root/'other').catalog.entries)
 def test_dynamic_discovery(self):
  id=self.extension('print(1)'); self.assertIn(id,self.service.catalog.exposed()); self.assertTrue(self.service.inspect(id)['approval_required'])
 def test_duplicate_catalog(self):
  id=self.extension('print(1)'); p=self.root/'catalog.json'; a=json.loads(p.read_text()); p.write_text(json.dumps(a+a))
  with self.assertRaises(ValueError): self.service.catalog.refresh()
 def test_denied_no_execution(self):
  marker=self.workspace/'changed'; id=self.extension('open('+repr(str(marker))+',"w").write("yes")')
  self.service.approve=lambda *a,**k:{'approved':False}
  result=self.service.execute(id,{},str(self.workspace)); self.assertEqual(result['status'],'denied'); self.assertFalse(marker.exists())
 def test_missing_approval_api(self):
  id=self.extension('print(1)'); self.service.approve=None
  self.assertEqual(self.service.execute(id,{},str(self.workspace))['status'],'denied')
 def test_execute_and_receipt(self):
  id=self.extension('print("{\\"value\\":42}")'); result=self.service.execute(id,{},str(self.workspace))
  self.assertTrue(result['ok'],result); self.assertEqual(result['result']['structured']['value'],42)
  read=self.service.receipts(result['receipt_id'],12000); self.assertTrue(read['verified'])
 def test_receipt_tamper(self):
  id=self.extension('print(1)'); r=self.service.execute(id,{},str(self.workspace)); p=self.root/'state/receipts'/(r['receipt_id']+'.json')
  d=json.loads(p.read_text()); d['status']='forged'; p.write_text(json.dumps(d))
  with self.assertRaises(ValueError): self.service.receipts(r['receipt_id'])
 def test_missing_receipt(self):
  with self.assertRaises(FileNotFoundError): self.service.receipts('00000000-0000-0000-0000-000000000000')
 def test_crash(self):
  id=self.extension('import sys; sys.exit(17)'); r=self.service.execute(id,{},str(self.workspace))
  self.assertFalse(r['ok']); self.assertEqual(r['result']['exit_code'],17)
 def test_output_schema_failure(self):
  id=self.extension('print(1)',output={'type':'object','required':['missing']})
  self.assertFalse(self.service.execute(id,{},str(self.workspace))['ok'])
 def test_redaction(self):
  self.assertEqual(redact({'api_key':'s','x':'Bearer abc','y':'token=xyz'}),{'api_key':'[REDACTED]','x':'Bearer [REDACTED]','y':'token=[REDACTED]'})
 def test_no_environment_leak(self):
  os.environ['KUJO_TEST_SECRET']='sensitive'
  self.assertNotIn('KUJO_TEST_SECRET',self.service.environment({}))
 def test_timeout(self):
  r=run([sys.executable,'-c','import time; time.sleep(4)'],self.workspace,{},0.1,1024,threading.Event())
  self.assertEqual(r['status'],'timeout')
 def test_large_output(self):
  r=run([sys.executable,'-c','print("x"*100000)'],self.workspace,{},3,1024,threading.Event())
  self.assertEqual(r['status'],'output_limit'); self.assertLessEqual(len(r['stdout']),1024)
 def test_cancel_background(self):
  id=self.extension('import time; time.sleep(30)'); r=self.service.execute(id,{},str(self.workspace),True)
  self.service.status(r['invocation_id'],True); self.service.close()
  read=self.service.receipts(r['invocation_id'],12000); self.assertEqual(json.loads(read['text'])['status'],'cancelled')
 def test_shutdown_prevents_new_work(self):
  self.service.close(); self.assertFalse(self.service.execute('kujo.ability.catalog.list',{},str(self.workspace))['ok'])
 def test_approval_grain_unique(self):
  id=self.extension('print(1)'); keys=[]
  def approve(*a,**kw): keys.append(kw['rule_key']); return {'approved':True}
  self.service.approve=approve
  for i in range(2): self.service.execute(id,{},str(self.workspace))
  self.assertNotEqual(keys[0],keys[1])
 def test_missing_binary(self):
  id=self.extension('print(1)'); p=self.root/'catalog.json'; a=json.loads(p.read_text()); a[0]['binding']['argv'][0]='/nonexistent/kujo'; p.write_text(json.dumps(a)); self.service.catalog.refresh()
  self.assertFalse(self.service.execute(id,{},str(self.workspace))['ok'])

if __name__=='__main__': unittest.main()
