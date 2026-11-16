from pathlib import Path
import json,subprocess,base64,time,hashlib,datetime
r=Path('data/website/eris-control-20261116/chain');base='https://terra-phoenix-api.highstakes.ch';rows=[]
def get(n,p):
 url=base+p;x=subprocess.run(['curl','-sS','--max-time','30','-w','\n%{http_code}',url],capture_output=True);b,_,s=x.stdout.rpartition(b'\n');(r/(n+'.json')).write_bytes(b);rows.append({'file':n+'.json','url':url,'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'http_status':s.decode(),'sha256':hashlib.sha256(b).hexdigest()});time.sleep(.7);return json.loads(b)
def smart(n,a,q):return get(n,'/cosmwasm/wasm/v1/contract/'+a+'/smart/'+base64.b64encode(json.dumps(q,separators=(',',':')).encode()).decode())
inv=json.loads((r/'inventory.json').read_text())
new={'vamp-escrow':json.loads((r/'proposal-gauge-config.json').read_text())['data']['escrow_addr'],'validator-gauge':json.loads((r/'hub-config.json').read_text())['data']['delegation_strategy']['gauges']['amp_gauges']}
for n in ['arbluna','ampluna-token']:
 a=next(x['address'] for x in inv if x['name']==n);d=smart(n+'-minter',a,{'minter':{}})
 if n=='arbluna':new['arb-vault']=d['data']['minter']
for n,a in new.items():
 d=get(n+'-contract','/cosmwasm/wasm/v1/contract/'+a);inv.append({'name':n,'address':a,**d.get('contract_info',{})});smart(n+'-config',a,{'config':{}})
get('supplement-block','/cosmos/base/tendermint/v1beta1/blocks/latest')
(r/'supplement-manifest.json').write_text(json.dumps({'records':rows},indent=2)+'\n');(r/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
print(json.dumps([{k:v for k,v in x.items() if k in ['name','address','admin','code_id']} for x in inv[-3:]],indent=2))
