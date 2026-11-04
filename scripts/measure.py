#!/usr/bin/env python3
import json,pathlib,sys,tempfile,time,statistics
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from kujo_hermes.config import Config
from kujo_hermes.service import Service
from kujo_hermes.plugin import TOOLS
measurements=[]
with tempfile.TemporaryDirectory() as tmp:
 for i in range(20):
  start=time.perf_counter(); service=Service(Config(profile='full'),pathlib.Path(tmp)/'state'); init=time.perf_counter()-start
  start=time.perf_counter(); result=service.discover(limit=100); discovery=time.perf_counter()-start
  start=time.perf_counter(); service.inspect('kujo.shipcheck.repository.scan'); inspection=time.perf_counter()-start
  measurements.append({'initialization_ms':init*1000,'discovery_ms':discovery*1000,'inspection_ms':inspection*1000})
report={'runs':20,'medians':{k:statistics.median(x[k] for x in measurements) for k in measurements[0]},'native_tool_definition_bytes':len(json.dumps([{'type':'function','function':{'name':n,'description':d,'parameters':{'type':'object','properties':p,'required':r,'additionalProperties':False}}} for n,(d,p,r) in TOOLS.items()]).encode()),'full_catalog_response_bytes':len(json.dumps(result).encode()),'token_count':'Not measured: model tokenizer dependent','measurements':measurements}
pathlib.Path('evidence/performance.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps({k:v for k,v in report.items() if k!='measurements'},indent=2))
