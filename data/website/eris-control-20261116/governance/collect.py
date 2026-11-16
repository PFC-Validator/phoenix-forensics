"""Read-only governance-capability evidence; never submit a chain transaction."""
from pathlib import Path
import subprocess,json,hashlib,datetime,base64,time
ROOT=Path(__file__).resolve().parent
COMMIT='e68dd029990a4cf347157f2426cabba4d9eb5c30'
BASE='https://raw.githubusercontent.com/phoenix-directive/core/'+COMMIT+'/'
URLS={
'node-publicnode.json':'https://terra-rest.publicnode.com/cosmos/base/tendermint/v1beta1/node_info',
'node-polkachu.json':'https://terra-api.polkachu.com/cosmos/base/tendermint/v1beta1/node_info',
'core-keepers.go':BASE+'app/keepers/keepers.go','core-wasm-keeper.go':BASE+'x/wasm/keeper/keeper.go','core-wasm-msg-server.go':BASE+'x/wasm/keeper/msg_server.go','core-wasm-module.go':BASE+'x/wasm/module.go','core-go.mod':BASE+'go.mod',
'wasmd-authz-policy.go':'https://raw.githubusercontent.com/CosmWasm/wasmd/v0.54.10/x/wasm/keeper/authz_policy.go',
'wasmd-msg-server.go':'https://raw.githubusercontent.com/CosmWasm/wasmd/v0.54.10/x/wasm/keeper/msg_server.go',
'sdk-gov-proposal.go':'https://raw.githubusercontent.com/phoenix-directive/cosmos-sdk/v0.50.15-terra.0/x/gov/keeper/proposal.go'}
rows=[]
def capture(url):
 p=subprocess.run(['curl','-f','-sSL','--max-time','30',url],capture_output=True,check=True);return p.stdout
for name,url in URLS.items():
 b=capture(url);(ROOT/name).write_bytes(b);rows.append({'file':name,'url':url,'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':hashlib.sha256(b).hexdigest()})
versions=[]
for name in ['node-publicnode.json','node-polkachu.json']:
 a=json.loads((ROOT/name).read_text())['application_version'];versions.append({'source':name,'version':a['version'],'git_commit':a['git_commit'],'cosmos_sdk_version':a['cosmos_sdk_version'],'wasmd_dependency':next(d for d in a['build_deps'] if d['path']=='github.com/CosmWasm/wasmd')})
def exports(b):
 pos=8;out=[]
 assert b[:8]==b'\x00asm\x01\x00\x00\x00'
 def u(pos):
  n=0;s=0
  while True:
   x=b[pos];pos+=1;n|=(x&127)<<s
   if not x&128:return n,pos
   s+=7
 while pos<len(b):
  sec=b[pos];pos+=1;size,pos=u(pos);end=pos+size
  if sec==7:
   count,pos=u(pos)
   for _ in range(count):
    length,pos=u(pos);name=b[pos:pos+length].decode();pos+=length;kind=b[pos];pos+=1;idx,pos=u(pos);out.append({'name':name,'kind':kind,'index':idx})
  pos=end
 return out
binaries=[]
for code in [3347,2726]:
 url='https://terra-phoenix-api.highstakes.ch/cosmwasm/wasm/v1/code/'+str(code);raw=capture(url);d=json.loads(raw);b=base64.b64decode(d['data']);digest=hashlib.sha256(b).hexdigest();assert digest.upper()==d['code_info']['data_hash'].upper()
 name='code'+str(code)+'.wasm';(ROOT/name).write_bytes(b)
 binaries.append({'code_id':code,'url':url,'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'response_sha256':hashlib.sha256(raw).hexdigest(),'code_info':d['code_info'],'wasm_sha256':digest,'wasm_file':name,'exports':exports(b),'has_sudo_export':any(x['name']=='sudo' for x in exports(b))})
 time.sleep(.5)
(ROOT/'capture-manifest.json').write_text(json.dumps({'records':rows},indent=2)+'\n')
(ROOT/'verification.json').write_text(json.dumps({'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'versions':versions,'binaries':binaries,'scope':'Node-reported release corroborated by two endpoints; pinned Terra wiring and Wasmd policy inspected. Binary exports parsed without executing contracts. No proposal submitted and no full chain simulation. Source checks establish capability; exact recovery payloads remain to be designed and tested.','sources':rows},indent=2)+'\n')
print('Verified live release dependencies and byte hashes; sudo exports:',[(x['code_id'],x['has_sudo_export']) for x in binaries])
