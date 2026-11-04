"""Cut a real recording without replacing terminal output; preserve state across cuts."""
import argparse,json,pathlib
p=argparse.ArgumentParser();p.add_argument('cast');p.add_argument('--windows',required=True);p.add_argument('--output',required=True);a=p.parse_args()
lines=[json.loads(l) for l in pathlib.Path(a.cast).read_text().splitlines()];events=[e for e in lines[1:] if e[1]=='o'];windows=json.loads(a.windows);out=[lines[0]];idx=0;offset=0
for start,end,duration in windows:
 assert end>=start and duration>0
 prefix=[]
 while idx<len(events) and events[idx][0]<=start:prefix.append(events[idx][2]);idx+=1
 if prefix:out.append([offset,'o',''.join(prefix)])
 while idx<len(events) and events[idx][0]<=end:
  t,kind,value=events[idx];out.append([offset+(t-start)/(end-start)*duration,kind,value]);idx+=1
 offset+=duration
out.append([offset,'o',''])
pathlib.Path(a.output).write_text('\n'.join(json.dumps(x) for x in out)+'\n')
pathlib.Path(a.output+'.edits.json').write_text(json.dumps({'source':a.cast,'windows':windows,'duration':offset,'note':'Original terminal bytes. Waiting time cut; terminal state preserved.'},indent=2)+'\n')
