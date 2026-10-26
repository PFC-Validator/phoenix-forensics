"""Check portable publication files, privacy boundaries and local page links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re

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

# Editorial and numerical consistency checks for the rebuilt review.
required=['index.html','voting/index.html','stakeholders/index.html','treasury/index.html','governance/index.html','evidence/index.html','privacy/index.html']
for rel in required:
    if not (DIST/rel).is_file(): errors.append(f'dist/{rel}: required rebuilt page missing')
home=(DIST/'index.html').read_text()
voting=(DIST/'voting/index.html').read_text()
stakeholders=(DIST/'stakeholders/index.html').read_text()
governance=(DIST/'governance/index.html').read_text()
evidence=(DIST/'evidence/index.html').read_text()
for needle in ['Make 4853 an impartial vote.','Disclose interests.','not YES, NO, or any person’s removal','What needs to happen now']:
    if needle not in home: errors.append(f'homepage: missing required process CTA: {needle}')
for needle in ['83 ballots','40,037,384.529','59.371M','29.700M','This has not happened at capture','Unattributed account']:
    if needle not in voting: errors.append(f'voting: missing consistent evidence statement: {needle}')
for needle in ['0xphilipp','MB','Vini','Rose','4719','7183','David','Rebel','RyanLion','ERIS fixed multisig']:
    if needle not in stakeholders: errors.append(f'stakeholders: missing {needle}')
for needle in ['wasm.update_admin','config.owner','gov_contract','Longer-term reforms','OECD','ISO 37000']:
    if needle not in governance: errors.append(f'governance: missing {needle}')
for needle in ['phoenix_board_votes_all.csv','eris_multisig_votes_all.csv','thinktank/votes.csv','native_4853_votes_all.csv','uncorroborated spreadsheet']:
    if needle not in evidence: errors.append(f'evidence: missing {needle}')
for page in DIST.glob('*.html'):
    text=page.read_text()
    if 'Philipp’s project funding' in text or 'LUNA holder briefing' in text:
        errors.append(f'{page.relative_to(ROOT)}: superseded person-focused briefing text remains')
import csv
with (DIST/'record/audit/native_4853_votes_all.csv').open() as f:
    if sum(1 for _ in csv.DictReader(f)) != 83: errors.append('native 4853 CSV does not contain 83 ballots')

if errors: raise SystemExit('\n'.join(errors))
print('PASS: local page links, portable paths, and publication privacy boundaries')
