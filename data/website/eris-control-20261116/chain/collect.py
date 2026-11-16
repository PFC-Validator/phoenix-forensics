from pathlib import Path
import json,base64,subprocess,datetime,time,hashlib
ROOT=Path('data/website/eris-control-20261116/chain');ROOT.mkdir(parents=True,exist_ok=True)
BASE='https://terra-phoenix-api.highstakes.ch'
records=[]
def capture(name,path):
 url=BASE+path
 for attempt in range(4):
  r=subprocess.run(['curl','-sS','--max-time','30','-w','\n%{http_code}',url],capture_output=True)
  body,_,status=r.stdout.rpartition(b'\n')
  if status==b'200': break
  time.sleep(3*(attempt+1))
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 fn=name+'.json';(ROOT/fn).write_bytes(body)
 record={'file':fn,'url':url,'captured_at':now,'http_status':status.decode(),'sha256':hashlib.sha256(body).hexdigest()};records.append(record)
 (ROOT/'manifest.json').write_text(json.dumps({'scope':'Sequential latest-state LCD reads; not a single-height snapshot or exhaustive chain inventory. No live transactions submitted.','records':records},indent=2)+'\n')
 time.sleep(.45)
 try: return json.loads(body)
 except: return {}
def smart(name,addr,q):return capture(name,'/cosmwasm/wasm/v1/contract/'+addr+'/smart/'+base64.b64encode(json.dumps(q,separators=(',',':')).encode()).decode())
contracts={'treasury':'terra16st8yfprkdl06kccktshd3p2vccq93xcn9mkhjl8s4jumyjtd4kqye0me5','tla-registry':'terra1hwxg6s732eparz3ys7sa4t5f64ngpd2w8syrca6z7ckv3fs9uqnsvrpcqa','creda-registry':'terra1skhnhcj653zfkqzd4txcashg0qu4v0vnpckeztgmsm46cqn33lhsxyej6c','hub':'terra10788fkzah89xrdm27zkj5yvhj9x3494lxawzm5qq3vvxcqz2yzaqyd3enk','ics20':'terra1e0mrzy8077druuu42vs0hu7ugguade0cj65dgtauyaw4gsl4kv0qtdf2au','ampluna-token':'terra1ecgazyd0waaj3g7l9cmy5gulhxkps2gmxu9ghducvuypjq68mq2s5lvsct','arbluna':'terra1se7rvuerys4kd2snt6vqswh9wugu49vhyzls8ymc02wl37g2p2ms5yz490','proposal-gauge':'terra1z0cxlq62a9dsjhz7g7hhgpuplcl32c0qeckhm9jyggln0rxq6z8syesq8j','operations':'terra1l0ny38guhwrzczesgvk2zwj7xcen63jzmpusjv9hemvua9vptcyqwqy7pl'}
capture('block-before','/cosmos/base/tendermint/v1beta1/blocks/latest')
for name in ['tla-registry','creda-registry']:
 addr=contracts[name]
 smart(name+'-ownership',addr,{'ownership':{}})
 roles=smart(name+'-roles',addr,{'all_addresses':{}})
 for role,address in roles.get('data',[]):
  if len(address)>50 and address not in contracts.values():contracts[name+'-'+role.lower()]=address
for name,addr in contracts.items():
 data=capture(name+'-contract','/cosmwasm/wasm/v1/contract/'+addr)
 print(name,data.get('contract_info',{}).get('label'),data.get('contract_info',{}).get('admin'),flush=True)
for name in ['treasury','hub','ics20','arbluna','proposal-gauge']:
 smart(name+'-config',contracts[name],{'config':{}})
smart('treasury-state',contracts['treasury'],{'state':{}})
smart('tla-dca-executors',contracts['tla-registry'],{'address_list':'PDT_DCA_EXECUTOR'})
for name,addr in [('upgrade-admin','terra1q0vny4wx2pfteh9zq323wh48c654xacpfq5tew'),('registry-owner','terra1kefa2zgjn45ctj32d3tje5jdwus7px6n2klgzl'),('governance','terra10d07y265gmmuvt4z0w9aw880jnsr700juxf95n')]:capture(name+'-account','/cosmos/auth/v1beta1/accounts/'+addr)
smart('board-threshold','terra1660g9mle5kfsq8c0p4k4hgr9ujdyr3m48c22cawy0akr98rmwksqehqnup',{'config':{}})
smart('board-members','terra1pq9f4a8cn4cdvvm9j7v0mu8n5elf44tgtre8mzrfz3j4x6yyl2yq4hnkuk',{'list_members':{'limit':100}})
capture('treasury-bank-balances','/cosmos/bank/v1beta1/balances/'+contracts['treasury']+'?pagination.limit=1000')
capture('block-after','/cosmos/base/tendermint/v1beta1/blocks/latest')
(ROOT/'inventory.json').write_text(json.dumps([{'name':n,'address':a,**json.loads((ROOT/(n+'-contract.json')).read_text()).get('contract_info',{})} for n,a in contracts.items()],indent=2)+'\n')
print('Captured',len(records),'responses',flush=True)
