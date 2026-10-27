"""Capture a new, bounded 4853 snapshot without replacing earlier evidence."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import base64, csv, hashlib, json, urllib.request
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'data/governance_4853/refresh_20261027'
BASE='https://terra2.tdrsys.com'
HUB='terra10788fkzah89xrdm27zkj5yvhj9x3494lxawzm5qq3vvxcqz2yzaqyd3enk'
GAUGE='terra1z0cxlq62a9dsjhz7g7hhgpuplcl32c0qeckhm9jyggln0rxq6z8syesq8j'
OUT.mkdir(exist_ok=True)
captures=[]
def get(name,path):
    url=BASE+path
    with urllib.request.urlopen(url,timeout=45) as r:
        raw=r.read(); height=r.headers.get('x-cosmos-block-height')
    obj=json.loads(raw)
    (OUT/(name+'.json')).write_bytes(raw)
    captures.append(dict(file=name+'.json',url=url,captured_at=datetime.now(timezone.utc).isoformat(),sha256=hashlib.sha256(raw).hexdigest(),response_height=height))
    return obj
def account(operator):
    alphabet='qpzry9x8gf2tvdw0s3jn54khce6mua7l'
    values=[alphabet.index(c) for c in operator.rsplit('1',1)[1][:-6]]
    hrp='terra'; chk=1
    expanded=[ord(c)>>5 for c in hrp]+[0]+[ord(c)&31 for c in hrp]
    for v in expanded+values+[0]*6:
        top=chk>>25; chk=((chk&0x1ffffff)<<5)^v
        for i,g in enumerate([0x3b6a57b2,0x26508e6d,0x1ea119fa,0x3d4233dd,0x2a1462b3]):
            if top>>i&1: chk^=g
    chk^=1
    return hrp+'1'+''.join(alphabet[v] for v in values+[(chk>>(5*(5-i)))&31 for i in range(6)])
def complete(obj,key):
    assert not obj.get('pagination',{}).get('next_key'), 'Pagination incomplete'
    return obj[key]
if __name__=='__main__':
    get('block_before','/cosmos/base/tendermint/v1beta1/blocks/latest')
    proposal=get('proposal','/cosmos/gov/v1/proposals/4853')['proposal']
    tally=get('tally','/cosmos/gov/v1/proposals/4853/tally')['tally']
    votes=complete(get('votes','/cosmos/gov/v1/proposals/4853/votes?pagination.limit=1000'),'votes')
    delegations=complete(get('hub_delegations','/cosmos/staking/v1beta1/delegations/'+HUB+'?pagination.limit=1000'),'delegation_responses')
    validators=complete(get('validators','/cosmos/staking/v1beta1/validators?pagination.limit=1000'),'validators')
    get('parameters','/cosmos/gov/v1/params/tallying')
    get('pool','/cosmos/staking/v1beta1/pool')
    gauge=get('active_gauge','/cosmwasm/wasm/v1/contract/'+GAUGE+'/smart/'+base64.b64encode(b'{"active_props":{}}').decode())
    get('block_after','/cosmos/base/tendermint/v1beta1/blocks/latest')
    assert HUB not in {v['voter'] for v in votes}, 'Hub already voted; baseline replacement needs a different model'
    keys=['yes_count','abstain_count','no_count','no_with_veto_count']
    options={'VOTE_OPTION_YES':'yes_count','VOTE_OPTION_ABSTAIN':'abstain_count','VOTE_OPTION_NO':'no_count','VOTE_OPTION_NO_WITH_VETO':'no_with_veto_count'}
    base={k:Decimal(v) for k,v in tally.items()}; scenario=base.copy(); rows=[]
    byvote={v['voter']:v for v in votes}; byval={v['operator_address']:v for v in validators}
    for d in delegations:
        op=d['delegation']['validator_address']; val=byval[op]; addr=account(op)
        assert d['balance']['denom']=='uluna'
        amount=Decimal(d['balance']['amount']); vote=byvote.get(addr); effects={k:Decimal(0) for k in keys}
        bonded=val['status']=='BOND_STATUS_BONDED'
        if bonded:
            if vote:
                assert sum(Decimal(o['weight']) for o in vote['options'])==1
                for o in vote['options']: effects[options[o['option']]]-=amount*Decimal(o['weight'])
            effects['yes_count']+=amount
            for k in keys: scenario[k]+=effects[k]
        rows.append(dict(validator=val['description']['moniker'],operator=op,account=addr,bonded=bonded,delegation_uluna=str(amount),ballot=vote['options'] if vote else [],effect_uluna={k:str(v) for k,v in effects.items()}))
    def metrics(t):
        total=sum(t.values()); active=total-t['abstain_count']
        return dict(yes_share_non_abstain_percent=str(100*t['yes_count']/active),veto_share_all_percent=str(100*t['no_with_veto_count']/total),total_uluna=str(total))
    result=dict(captured_at=captures[-1]['captured_at'],ballot_count=len(votes),proposal_status=proposal['status'],voting_end_time=proposal['voting_end_time'],base={k:str(v) for k,v in base.items()},full_hub_yes_scenario={k:str(v) for k,v in scenario.items()},base_metrics=metrics(base),scenario_metrics=metrics(scenario),hub_total_uluna=str(sum(Decimal(d['balance']['amount']) for d in delegations)),validators=rows,gauge=gauge,limits='Sequential current-state queries, not a confirmed common-height snapshot. Counterfactual applies bonded hub delegation amounts to validator ballot weights, adds non-voting validator delegations as YES, and excludes synthetic Alliance weight. Not an observed hub vote or an inclusion proof.')
    (OUT/'scenario.json').write_text(json.dumps(result,indent=2)+'\n')
    with (OUT/'votes.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=['proposal_id','voter','options','metadata']); w.writeheader()
        for v in votes: w.writerow({**v,'options':json.dumps(v['options'])})
    (OUT/'capture_manifest.json').write_text(json.dumps(captures,indent=2)+'\n')
    print(json.dumps(result,indent=2))
