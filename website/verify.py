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
if errors: raise SystemExit('\n'.join(errors))
print('PASS: local page links, portable paths, and publication privacy boundaries')
