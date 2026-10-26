import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text())
monthly=load('data/payment_summary.json')['monthly_validator_to_eris']
assert len(monthly)==20
assert sum(x['amount'] for x in monthly if x['validator']=='Galactic Punks')/1e6==116735
assert sum(x['amount'] for x in monthly if x['validator']=='Lion DAO')/1e6==105227
assert len(list((R/'data/transfers/monthly_validator_to_eris').glob('*.json')))==20
assert load('data/transfers/validator_multisig_native_matches.json')==[]
assert load('data/transfers/validator_multisig_wasm_matches.json')==[]
out=load('data/treasury/outbound_transfers.json')
assert len(out)==170
alx=[x for x in out if x['recipient']=='terra1alxk3fmhcl0ga80gl9yj9zp3ezjm4sdh8a9l9c']
assert len(alx)==10 and abs(sum(x['amount'] for x in alx)/1e6-795991.566014)<1e-9
for x in alx:
 tx=load(f"data/treasury/signer_payments/{x['txhash']}.json")
 msg=tx['tx']['body']['messages'][0]
 assert 'execute_otc' in msg['msg']
 assert tx['tx']['body']['memo']=='www.erisprotocol.com'
a100=load('data/treasury/actions/100.json')['data']
assert len(a100['setup']['payment']['payments'])==12 and a100['done']
assert load('data/treasury/actions/72.json')['data']['done']
for i in [118,119]:assert load(f'data/treasury/actions/{i}.json')['data']['done']
after=load('data/treasury/actions/actions_after100.json')['data']
assert after[19]['id']==120 and after[19]['done']
assert not any('stewardship payments (2026-10-01' in x['name'] and x['setup'].get('payment',{}).get('payments',[{}])[0].get('recipient')=='terra18ruqkccl5tp493uhvra0u6jylrzq8t8dv5qs4c' for x in after if x['id'] in [118,119,120])
print('Verified: 20 monthly validator payments, zero direct signer matches, 170 Treasury transfers, OTC classification, and October action roster.')
