"""Check portable publication files, privacy boundaries and local page links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re,json,hashlib

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
for needle in ['Before voting on 4853','Disclose financial interests','does not recommend YES, NO or anyone’s removal','Before the vote closes','200,000 USDC','210,000 USDC','A209','A215','265,000 USDC','A272','It failed','does not prove that no work occurred']:
    if needle not in home: errors.append(f'homepage: missing purpose, finding or qualification: {needle}')
for needle in ['96 ballots','40,063,598.732','59.221M','29.939M','The hub had not voted at capture','Unattributed account']:
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
for needle in ['0xphilipp','MB','Vini','Rose','4719','7183','David','Rebel','RyanLion','ERIS fixed multisig']:
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
    current=DIST/'record/audit/governance_4853/refresh_20261027'
    scenario=json.loads((current/'scenario.json').read_text())
    votes=json.loads((current/'votes.json').read_text())['votes']
    assert len(votes)==scenario['ballot_count']==96
    assert module.HUB not in {v['voter'] for v in votes}
    for capture in json.loads((current/'capture_manifest.json').read_text()):
        assert hashlib.sha256((current/capture['file']).read_bytes()).hexdigest()==capture['sha256']
    raw_tally=json.loads((current/'tally.json').read_text())['tally']
    assert scenario['base']==raw_tally
    for key in raw_tally:
        assert Decimal(scenario['full_hub_yes_scenario'][key])==Decimal(raw_tally[key])+sum(Decimal(r['effect_uluna'][key]) for r in scenario['validators'])
    assert Decimal(scenario['base_metrics']['yes_share_non_abstain_percent'])<50
    assert Decimal(scenario['scenario_metrics']['yes_share_non_abstain_percent'])>50
    print('PASS: fresh tally response hashes, complete ballots and scenario arithmetic')

    byvote={v['voter']:v for v in votes}
    byval={v['operator_address']:v for v in json.loads((current/'validators.json').read_text())['validators']}
    expected={k:Decimal(v) for k,v in raw_tally.items()}
    option={'VOTE_OPTION_YES':'yes_count','VOTE_OPTION_NO':'no_count','VOTE_OPTION_ABSTAIN':'abstain_count','VOTE_OPTION_NO_WITH_VETO':'no_with_veto_count'}
    for delegation in json.loads((current/'hub_delegations.json').read_text())['delegation_responses']:
        operator=delegation['delegation']['validator_address']
        if byval[operator]['status']!='BOND_STATUS_BONDED': continue
        amount=Decimal(delegation['balance']['amount'])
        vote=byvote.get(module.account(operator))
        if vote:
            for weighted in vote['options']: expected[option[weighted['option']]]-=amount*Decimal(weighted['weight'])
        expected['yes_count']+=amount
    assert expected=={k:Decimal(v) for k,v in scenario['full_hub_yes_scenario'].items()}
    assert abs(Decimal(scenario['scenario_metrics']['yes_share_non_abstain_percent'])-100*expected['yes_count']/(sum(expected.values())-expected['abstain_count']))<Decimal('0.000000001')
    print('PASS: scenario independently reconstructed from primary ballots and delegations')
