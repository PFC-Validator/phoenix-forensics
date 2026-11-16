"""Check portable publication files, privacy boundaries and local page links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import base64,re,json,hashlib

ROOT=Path(__file__).parent
DIST=ROOT/'dist'
errors=[]
class Links(HTMLParser):
    def __init__(self, page): super().__init__(); self.page=page
    def handle_starttag(self, tag, attrs):
        for key,value in attrs:
            if key not in {'href','src'} or not value: continue
            parsed=urlsplit(value)
            if parsed.scheme or parsed.netloc or not parsed.path: continue
            target=DIST/unquote(parsed.path).lstrip('/') if parsed.path.startswith('/') else self.page.parent/unquote(parsed.path)
            if not target.exists(): errors.append(f'{self.page.relative_to(ROOT)}: missing {value}')

for page in DIST.rglob('*.html'): Links(page).feed(page.read_text())
private=re.compile(r'/Users/[^/\s]+|/home/[^/\s]+|https?://[^/\s"<>]+\.[^./\s"<>]+\.chatgpt\.site|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')
for path in ROOT.rglob('*'):
    if not path.is_file() or path.suffix.lower() not in {'.py','.html','.js','.css','.json','.txt','.md','.svg','.csv','.rs'}: continue
    if path.name==Path(__file__).name: continue
    if private.search(path.read_text()): errors.append(f'{path.relative_to(ROOT)}: owner or machine-specific material requires review')
for name in ['.git','.openai','.env']:
    if (ROOT/name).exists(): errors.append(f'{name}: excluded local/account configuration present')

for manifest in DIST.rglob('SHA256SUMS.txt'):
    for line in manifest.read_text().splitlines():
        digest, relative = line.split('  ', 1)
        target = manifest.parent / relative
        if not target.resolve().is_relative_to(manifest.parent.resolve()):
            errors.append(f'{manifest.relative_to(ROOT)}: checksum path escapes its record directory')
        elif not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest()!=digest:
            errors.append(f'{manifest.relative_to(ROOT)}: checksum mismatch for {relative}')

# Editorial and numerical consistency checks for the rebuilt review.
required=['index.html','voting/index.html','stakeholders/index.html','treasury/index.html','governance/index.html','evidence/index.html','privacy/index.html']
for rel in required:
    if not (DIST/rel).is_file(): errors.append(f'dist/{rel}: required rebuilt page missing')
home=(DIST/'index.html').read_text()
voting=(DIST/'voting/index.html').read_text()
stakeholders=(DIST/'stakeholders/index.html').read_text()
governance=(DIST/'governance/index.html').read_text()
evidence=(DIST/'evidence/index.html').read_text()
treasury=(DIST/'treasury/index.html').read_text()
for needle in ['4855, in plain language','Disclose financial interests','Why we propose these changes','Questions for continuing oversight','200,000 USDC','210,000 USDC','A209','A215','265,000 USDC','A272','It failed','does not prove that no work occurred']:
    if needle not in home: errors.append(f'homepage: missing purpose, finding or qualification: {needle}')
for needle in ['138 ballots','29,449,635.974','59.192M','30.054M','The hub voted ABSTAIN','Below 50%','Unattributed account']:
    if needle not in voting: errors.append(f'voting: missing consistent evidence statement: {needle}')
# Keep the featured grant tied to the actual milestone amounts and approvals.
creda_action=json.loads((DIST/'record/audit/leads/queries/review_treasury_action_72.json').read_text())['data']
milestones=creda_action['setup']['milestone']['milestones']
assert sum(int(m['amount']) for m in milestones[:3])==200000000000
assert int(milestones[3]['amount'])==10000000000
assert all(m['claimed'] for m in creda_action['runtime']['milestone']['milestones'])
assert 'id="creda-approval"' in stakeholders
assert 'Vini proposed and voted for A249' not in home
for statement in ['What happens if 4853 passes?','2.4.5.4','2.6.2','1.10','two-of-three','3 of 3','60%','not automatically enacted by 4853','Vini was not the only recorded dissenting director','off-chain commitment','A272 failed.']:
    if statement not in voting: errors.append('4853 effects: missing power, limit or counterevidence: '+statement)
assert not json.loads((DIST/'record/audit/native_4853/proposal.json').read_text())['proposal']['messages']
for needle in ['0xPhilipp','MB','Vini','Rose','4719','7183','David','Rebel','RyanLion','ERIS fixed multisig']:
    if needle not in stakeholders: errors.append(f'stakeholders: missing {needle}')
for needle in ['wasm.update_admin','config.owner','gov_contract','Longer-term reforms','OECD','ISO 37000']:
    if needle not in governance: errors.append(f'governance: missing {needle}')
for needle in ['phoenix_board_votes_all.csv','eris_multisig_votes_all.csv','thinktank/votes.csv','native_4853_votes_all.csv','uncorroborated spreadsheet']:
    if needle not in evidence: errors.append(f'evidence: missing {needle}')
for needle in ['265,000 USDC','215,000 USDC','liquidity capital','funder reports payment and completion','23.8% of supply','18.2% of supply','does not establish that Creda never reached $1M']:
    if needle not in treasury: errors.append(f'treasury: missing funding or snapshot qualification: {needle}')
for needle in ['83,000 ampLUNA','21,600.000001 ampLUNA','Superbolt: three beneficiary YES votes','audit scope and independent acceptance','full grant-to-distribution and delivery reconciliation remains open']:
    if needle not in stakeholders: errors.append(f'stakeholders: missing supplemental record or limit: {needle}')
for needle in ['1,680,127.496132 LUNA','662,828.893153 LUNA','moved to private source for security','Timing alone does not establish retaliation']:
    if needle not in governance: errors.append(f'governance: missing authority record or response: {needle}')
for needle in ['48 successful primary transaction records','38 Terra transactions','Six cited transactions remain unavailable','Fourteen requested historical state queries','not independent consensus']:
    if needle not in evidence: errors.append(f'evidence: missing verification scope: {needle}')
supplement_root=DIST/'record/audit/leads'
captured=json.loads((supplement_root/'capture_manifest.json').read_text())['transactions']
if sum(r['status']=='successful_primary_record' for r in captured)!=48: errors.append('supplement: successful record count drift')
if sum(r['status']=='unavailable' for r in captured)!=6: errors.append('supplement: unresolved record count drift')
if len(json.loads((supplement_root/'rpc_manifest.json').read_text())['checks'])!=38: errors.append('supplement: Terra byte/hash count drift')
review=json.loads((supplement_root/'year_review_analysis.json').read_text())
if review['identified_named_project_grants_USDC']!='265000' or review['review_period_grants_excluding_earlier_votion_USDC']!='215000': errors.append('supplement: project grant calculation drift')
locks=json.loads((supplement_root/'voting_locks.json').read_text())
if sum(int(r['amount_base']) for r in locks if r['token_id'] in ['429','430','431','432'])!=83000000000: errors.append('supplement: A43 funded lock total drift')
for page in DIST.glob('*.html'):
    text=page.read_text()
    if 'Philipp’s project funding' in text or 'LUNA holder briefing' in text:
        errors.append(f'{page.relative_to(ROOT)}: superseded person-focused briefing text remains')
import csv
with (DIST/'record/audit/native_4853_votes_all.csv').open() as f:
    if sum(1 for _ in csv.DictReader(f)) != 83: errors.append('native 4853 CSV does not contain 83 ballots')

if errors: raise SystemExit('\n'.join(errors))
print('PASS: local page links, portable paths, and publication privacy boundaries')

# Verify refreshed scenario from primary captured ballots and validator records.
from decimal import Decimal
import importlib.util
spec=importlib.util.spec_from_file_location('refresh_4853', ROOT.parent/'analysis/refresh_4853.py')
if spec and spec.loader:
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    current=DIST/'record/audit/governance_4853/refresh_20261030'
    scenario=json.loads((current/'scenario.json').read_text())
    votes=json.loads((current/'votes.json').read_text())['votes']
    assert len(votes)==scenario['ballot_count']==138
    assert scenario['hub_ballot']==next(v['options'] for v in votes if v['voter']==module.HUB)
    assert scenario['hub_ballot']==[{'option':'VOTE_OPTION_ABSTAIN','weight':'1.000000000000000000'}]
    for capture in json.loads((current/'capture_manifest.json').read_text()):
        assert hashlib.sha256((current/capture['file']).read_bytes()).hexdigest()==capture['sha256']
    raw_tally=json.loads((current/'tally.json').read_text())['tally']
    assert scenario['base']==raw_tally
    for key in raw_tally:
        assert Decimal(scenario['full_hub_yes_scenario'][key])==Decimal(raw_tally[key])+sum(Decimal(r['effect_uluna'][key]) for r in scenario['validators'])
    assert Decimal(scenario['base_metrics']['yes_share_non_abstain_percent'])<50
    assert Decimal(scenario['scenario_metrics']['yes_share_non_abstain_percent'])<50
    print('PASS: fresh tally response hashes, complete ballots and scenario arithmetic')

    byvote={v['voter']:v for v in votes}
    byval={v['operator_address']:v for v in json.loads((current/'validators.json').read_text())['validators']}
    expected={k:Decimal(v) for k,v in raw_tally.items()}
    option={'VOTE_OPTION_YES':'yes_count','VOTE_OPTION_NO':'no_count','VOTE_OPTION_ABSTAIN':'abstain_count','VOTE_OPTION_NO_WITH_VETO':'no_with_veto_count'}
    for delegation in json.loads((current/'hub_delegations.json').read_text())['delegation_responses']:
        operator=delegation['delegation']['validator_address']
        if byval[operator]['status']!='BOND_STATUS_BONDED': continue
        amount=Decimal(delegation['balance']['amount'])
        vote=byvote.get(module.HUB) or byvote.get(module.account(operator))
        if vote:
            for weighted in vote['options']: expected[option[weighted['option']]]-=amount*Decimal(weighted['weight'])
        expected['yes_count']+=amount
    assert expected=={k:Decimal(v) for k,v in scenario['full_hub_yes_scenario'].items()}
    assert abs(Decimal(scenario['scenario_metrics']['yes_share_non_abstain_percent'])-100*expected['yes_count']/(sum(expected.values())-expected['abstain_count']))<Decimal('0.000000001')
    print('PASS: scenario independently reconstructed from primary ballots and delegations')

    assert sum(expected.values())==sum(Decimal(v) for v in raw_tally.values())
    assert all(v>=0 for v in expected.values())
    for name in ['votes.json','validators.json','hub_delegations.json']:
        assert not json.loads((current/name).read_text())['pagination'].get('next_key')

# Verify the 4855 explanation against its preserved primary records.
from datetime import datetime
amp_root = DIST / 'record/ampluna-4855'
def amp_read(name):
    return json.loads((amp_root / (name + '.json')).read_text())
for rec in amp_read('manifest')['records']:
    assert hashlib.sha256((amp_root / rec['file']).read_bytes()).hexdigest() == rec['sha256'], rec['file']
ap = amp_read('gauge-4855')['data']['prop']
av = amp_read('gauge-voters-4855')['data']['voters']
assert len(av) == 2 and all(v[2] == 'no_with_veto' for v in av)
assert sum(int(v[0]) for v in av) == int(ap['nwv_vp'])
assert all(int(ap[k]) == 0 for k in ['yes_vp', 'no_vp', 'abstain_vp'])
assert amp_read('gauge-config')['data']['quorum_bps'] == 1000
assert amp_read('gauge-config')['data']['use_weighted_vote'] is True
assert int(ap['nwv_vp']) * 10 >= int(ap['total_vp'])
assert amp_read('hub-vote-4855')['vote']['options'] == [{'option': 'VOTE_OPTION_NO_WITH_VETO', 'weight': '1.000000000000000000'}]
assert amp_read('proposal-4853')['proposal']['status'] == 'PROPOSAL_STATUS_REJECTED'
assert amp_read('proposal-4855')['proposal']['status'] == 'PROPOSAL_STATUS_VOTING_PERIOD'
assert amp_read('proposal-4855')['proposal']['messages'] == []
ft=amp_read('fee-vote-tx');vt=amp_read('validator-gauge-vote-tx')
assert ft['tx_response']['code'] == vt['tx_response']['code'] == 0
assert (datetime.fromisoformat(vt['tx_response']['timestamp'].replace('Z','+00:00')) - datetime.fromisoformat(ft['tx_response']['timestamp'].replace('Z','+00:00'))).total_seconds() == 146
assert ft['tx']['body']['memo'] == vt['tx']['body']['memo'] == 'www.erisprotocol.com'
assert ft['tx']['auth_info']['signer_infos'][0]['public_key'] != vt['tx']['auth_info']['signer_infos'][0]['public_key']
assert amp_read('fee-recipient-account')['account']['pub_key']['@type'] == '/cosmos.crypto.secp256k1.PubKey'
assert ft['tx']['body']['messages'][0]['sender'] == amp_read('hub-config')['data']['fee_config']['protocol_fee_contract']
for needle in ['11.38%', '100% NO WITH VETO', '2 minutes 26 seconds', 'does not identify a shared person or machine', 'not all ampLUNA holders', '§7.3', '4853 · rejected', 'no operational upper bound']:
    assert needle in home, needle
print('PASS: 4855 source hashes, voting arithmetic, wallet roles, transaction timing and editorial limits')

# Keep the final results separate from the preserved 5 November voting snapshot.
final_root = DIST / 'record/governance-20261114'
for rec in json.loads((final_root / 'manifest.json').read_text())['records']:
    assert hashlib.sha256((final_root / rec['file']).read_bytes()).hexdigest() == rec['sha256']
final4855 = json.loads((final_root / 'proposal-4855.json').read_text())['proposal']
assert final4855['status'] == 'PROPOSAL_STATUS_PASSED'
final_tally = final4855['final_tally_result']
final_yes = Decimal(final_tally['yes_count']) / sum(Decimal(final_tally[k]) for k in ['yes_count', 'no_count', 'no_with_veto_count']) * 100
assert f'{final_yes:.2f}%' in home
a296 = json.loads((final_root / 'a296-proposal.json').read_text())['data']['proposal']
a296_votes = json.loads((final_root / 'a296-votes.json').read_text())['data']['votes']
assert a296['status'] == 'rejected'
assert a296['threshold']['absolute_percentage']['percentage']['percent'] == '0.75'
assert a296['total_power'] == '100' and a296['votes'] == {'yes': '50', 'no': '0', 'abstain': '0'}
assert {v['voter'] for v in a296_votes} == {'terra14p3mc04s7jcaxvvetlzehvhx9gdx6w4nm3zzw3', 'terra18ruqkccl5tp493uhvra0u6jylrzq8t8dv5qs4c'}
assert all(v['vote'] == 'yes' for v in a296_votes) and sum(int(v['power']) for v in a296_votes) == 50
for needle in ['3-of-3', '3-of-4', '3-of-5', 'the record alone does not establish why either did not vote', 'Neither proposal can use the other’s unadopted powers to authorize itself', 'https://forum.phoenix.money/t/discussion-phoenix-foundation-remove-0xphilipp-and-establish-final-on-chain-governance-authority/72']:
    assert needle in home, needle
assert 'Voting closes 12 November.' not in home
print('PASS: final 4855 and A296 records, ballot attribution and proposal qualifications')

# Keep the current proposal summary separate from historical threshold proposals.
for content in [home, governance]:
    assert 'All directors must approve until a fourth director is appointed, after which three approvals are required.' in content
    for anchor in ['01-removal-and-transition', '02-governance-and-accountability']:
        assert 'f5c703162cb9b08a218dcec67aae6fe645d064dd#file-' + anchor + '-md' in content
    for stale in ['Why temporary 2-of-3?', 'allowing temporary <strong>2-of-3</strong>', 'temporary 2-of-3 operation until community elections', 'could remain with, or return to, ERIS']:
        assert stale not in content, stale
assert 'Proposal 2 can operate with the existing Board if Proposal 1 fails.' in home
assert 'At the 14 November evidence capture' in home
assert 'within <strong>21 calendar days of passage</strong>' in home
for needle in ['every four calendar months from adoption', 'within 90 calendar days of adoption', 'a status report is not an independent review', 'Preparing it grants no new spending power']:
    assert needle in governance, needle
print('PASS: independent proposals, revised approval rule, implementation clocks and safeguards')

# Reconcile the two locks and the before-extension comparison to the 4855 snapshot.
lock_file = amp_root / 'lock-evidence.json'
assert hashlib.sha256(lock_file.read_bytes()).hexdigest() in lock_file.with_suffix('.json.source.md').read_text()
lock_sources = amp_read('lock-evidence')['sources']
assert lock_sources['voters']['response']['data']['voters'] == av
assert lock_sources['gauge']['response']['data']['prop'] == ap
extension = lock_sources['extension']['response']
message, = extension['tx']['body']['messages']
assert extension['tx_response']['code'] == 0
assert message['sender'] == av[0][1] and message['funds'] == []
assert message['msg']['extend_lock_time']['time'] == 47 * 604800
assert extension['tx_response']['timestamp'] < amp_read('proposal-4855')['proposal']['voting_start_time']
before = json.loads(base64.b64decode(lock_sources['pre_extension_checkpoint']['response']['data']))
fee_lock = lock_sources['fee_lock']['response']['data']
assert fee_lock['amount'] == before['fixed']
assert fee_lock['end'] - before['end'] == 47
prior_power = int(before['fixed']) + int(before['power']) - int(before['slope']) * (ap['period'] - before['start'])
extra_power = int(av[0][0]) - prior_power
prior_share = Decimal(int(ap['nwv_vp']) - extra_power) * 100 / (int(ap['total_vp']) - extra_power)
assert f'{prior_share:.2f}' == '8.43'
for needle in ['33,750 LUNA', '32.85 million LUNA', '19,190.92 LUNA', '30 October 2028', '06 December 2027', '8.43%']:
    assert needle in home, needle
print('PASS: escrow locks, lock-extension transaction and quorum comparison')

# Reconcile historical totals to distinct recorded wallet ballots.
ah = json.loads((DIST/'record/ampluna-history/participation.json').read_text())
assert [r['id'] for r in ah['records']] == [4853,4823,4822,4803,4802]
for r in ah['records']:
    p = r['detail_response']['data']['prop']
    assert sum(int(v[0]) for v in r['voters']) == sum(int(p[k]) for k in ['yes_vp','no_vp','abstain_vp','nwv_vp'])
    assert len(r['voters']) == len({v[1] for v in r['voters']})
assert len({v[1] for r in ah['records'] for v in r['voters']}) == 5
print('PASS: historical gauge totals reconcile to unique wallet ballots')

# Reconcile the contract-control review to captured permissions and actual proposal messages.
control_root=DIST/'record/control-20261116'
def cr(name): return json.loads((control_root/name).read_text())
ci=cr('chain/inventory.json')
assert len(ci)==len({r['address'] for r in ci})==27
by_name={r['name']:r for r in ci}
eris_admin='terra1q0vny4wx2pfteh9zq323wh48c654xacpfq5tew'
eris_owner='terra1kefa2zgjn45ctj32d3tje5jdwus7px6n2klgzl'
board='terra1k8ug6dkzntczfzn76wsh24tdjmx944yj6mk063wum7n20cwd7lxq4lppjg'
assert sum(r['admin']==eris_admin for r in ci)==22
assert by_name['treasury']['admin']==eris_admin
assert by_name['hub']['admin']==by_name['ics20']['admin']==board
for registry in ['tla','creda']:
    ownership=cr('chain/'+registry+'-registry-ownership.json')['data']
    assert ownership['owner']==eris_owner and ownership['pending_owner'] is None
roles=dict(cr('chain/tla-registry-roles.json')['data'])
assert roles['PDT_CONTROLLER']==board and roles['PDT_CONFIG_OWNER']==eris_owner
assert cr('chain/board-threshold.json')['data']['threshold']['absolute_percentage']['percentage']['percent']=='0.75'
assert [m['weight'] for m in cr('chain/board-members.json')['data']['members']]==[25]*4
p9=next(p for p in cr('handover/eris-proposals.json')['data']['proposals'] if p['id']==9)
assert p9['status']=='executed' and len(p9['msgs'])==2
assert {m['wasm']['update_admin']['contract_addr'] for m in p9['msgs']}=={by_name[n]['address'] for n in ['hub','ics20']}
assert all(m['wasm']['update_admin']['admin']==board for m in p9['msgs'])
a292=cr('handover/A292.json')['data']['proposal']
assert a292['status']=='executed' and a292['votes']['yes']=='75'
assert int(by_name['hub']['code_id'])==a292['msgs'][0]['wasm']['migrate']['new_code_id']==2726
for pid in [3796,4813,4816,4817,4822,4823]:assert cr(f'approvals/native-{pid}.json')['proposal']['status']=='PROPOSAL_STATUS_PASSED'
for pid in [3460,4830,4836]:assert cr(f'approvals/native-{pid}.json')['proposal']['status']=='PROPOSAL_STATUS_REJECTED'
for pid,total in [(190,210000000000),(266,125000000000)]:
    prop=cr(f'approvals/board-A{pid}.json')['data']['proposal']
    assert prop['status']=='executed'
    setup=json.loads(base64.b64decode(prop['msgs'][0]['wasm']['execute']['msg']))['setup']
    assert sum(int(m['amount']) for m in setup['action']['milestone']['milestones'])==total
for manifest_name in ['chain/manifest.json','chain/supplement-manifest.json','approvals/capture-manifest.json','approvals/supplement-manifest.json','approvals/board-manifest.json']:
    manifest=control_root/manifest_name;data=json.loads(manifest.read_text());records=data if isinstance(data,list) else data['records']
    for row in records:
        target=manifest.parent/row.get('file','')
        if target.is_file() and row.get('sha256'):assert hashlib.sha256(target.read_bytes()).hexdigest()==row['sha256'],target
print('PASS: contract control, P9/A292 execution, award amounts and capture hashes')
