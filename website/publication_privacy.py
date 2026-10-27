"""Apply the requested first-name-only policy to every publicly served artifact."""
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import hashlib
import json
import re
import unicodedata

SURNAME = re.compile(r'\bmager\b', re.I)
IDENTITY_REFERENCE = re.compile(r'public[-_]identity|public name and account records|author/account record', re.I)
TEXT_EXTENSIONS = {'.html', '.json', '.csv', '.txt', '.js', '.css', '.svg', '.rs'}
DROP = object()

def first_name_only(text):
    text = re.sub(r'\bPhilipp\s+Mager\b', 'Philipp', text, flags=re.I)
    return SURNAME.sub('Philipp', text)

def display_handle(text):
    """Change presentation labels, preserving source URLs and raw transaction data."""
    def label(value):
        return re.sub(r'(?<![\w/])@?(?:0x)?Philipp\b', '0xphilipp', value, flags=re.I)
    parts = re.split(r'(<[^>]*>)', text)
    for i, part in enumerate(parts):
        if part.startswith('<'):
            parts[i] = re.sub(r'((?:aria-label|content|title|alt)=["\'])(.*?)(["\'])',
                              lambda m: m[1]+label(m[2])+m[3], part)
        else:
            parts[i] = label(part)
    return ''.join(parts)

def clean_html(text):
    text = re.sub(r'<section\b[^>]*\bid=["\']public-identity["\'][^>]*>[\s\S]*?</section>', '', text, flags=re.I)
    text = re.sub(r'<h2>Public-record attribution</h2>[\s\S]*?(?=<h2>Giving feedback</h2>)', '', text, flags=re.I)
    def paragraph(match):
        body = match.group()
        if IDENTITY_REFERENCE.search(body):
            if 'All data here has been sourced' in body:
                return '<p class="verification-note">The figures are drawn from public transaction records, proposals and supporting datasets. Sources are linked throughout for verification.</p>'
            return ''
        return body
    text = re.sub(r'<p\b[^>]*>[\s\S]*?</p>', paragraph, text, flags=re.I)
    text = re.sub(r'<a\b[^>]*href=["\'][^"\']*public[-_]identity[^"\']*["\'][^>]*>[\s\S]*?</a>', '', text, flags=re.I)
    text = re.sub(r'<a\b[^>]*>\s*Author/account record\s*</a>', '', text, flags=re.I)
    text = re.sub(r'<li\b[^>]*>\s*</li>', '', text, flags=re.I)
    text = text.replace('Preserved source presentation ·', 'Source presentation · Some labels edited for privacy ·')
    return display_handle(first_name_only(text))

def clean_json(value):
    if isinstance(value, dict):
        if any(isinstance(v, str) and IDENTITY_REFERENCE.search(v) for k, v in value.items() if k in {'url', 'file', 'title', 'name', 'path'}):
            return DROP
        result = {}
        for key, item in value.items():
            cleaned = clean_json(item)
            if cleaned is not DROP:
                result[first_name_only(key)] = cleaned
        return result
    if isinstance(value, list):
        return [cleaned for item in value if (cleaned := clean_json(item)) is not DROP]
    if isinstance(value, str):
        if IDENTITY_REFERENCE.search(value) and value.startswith(('https://', 'http://', 'public-identity')):
            return DROP
        return clean_html(value) if '<' in value else first_name_only(value)
    return value

class Readable(HTMLParser):
    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base, self.skip, self.parts, self.href = base, 0, [], None
    def handle_starttag(self, tag, attrs):
        if tag in {'head', 'script', 'style', 'svg'}: self.skip += 1
        if self.skip: return
        if tag in {'p', 'h1', 'h2', 'h3', 'section', 'tr', 'li', 'summary'}: self.parts.append('\n\n')
        if tag == 'a': self.href = dict(attrs).get('href')
    def handle_endtag(self, tag):
        if tag in {'head', 'script', 'style', 'svg'}: self.skip = max(0, self.skip - 1)
        if self.skip: return
        if tag == 'a' and self.href:
            self.parts.append(' [' + urljoin(self.base, self.href) + ']')
            self.href = None
        if tag in {'td', 'th'}: self.parts.append(' | ')
    def handle_data(self, text):
        if not self.skip: self.parts.append(text)
    def text(self):
        text = ''.join(self.parts)
        text = re.sub(r'[ \t]+', ' ', text)
        return re.sub(r'\n\s*\n(?:\s*\n)+', '\n\n', text).strip() + '\n'

def apply_privacy(dist):
    dist = Path(dist)
    removed, modified = [], set()
    for path in list(dist.rglob('*')):
        if not path.is_file(): continue
        if re.search(r'public[-_]identity', path.name, re.I):
            path.unlink()
            removed.append(str(path.relative_to(dist)))
            continue
        if path.suffix not in TEXT_EXTENSIONS: continue
        original = path.read_text()
        if path.suffix in {'.html', '.svg'}:
            cleaned = clean_html(original)
        elif path.suffix == '.json':
            value = json.loads(original)
            cleaned_value = clean_json(value)
            if cleaned_value is DROP:
                path.unlink(); removed.append(str(path.relative_to(dist))); continue
            cleaned = json.dumps(cleaned_value, ensure_ascii=False, indent=2) if cleaned_value != value else original
        else:
            cleaned = '\n'.join(line for line in original.split('\n') if not IDENTITY_REFERENCE.search(line))
            cleaned = first_name_only(cleaned)
        if cleaned != original:
            path.write_text(cleaned)
            modified.add(path)

    # Publish readable versions of the privacy-edited pages, not the original identity appendix.
    for name, route in {'overview':'', 'payments':'payments/', 'evidence':'evidence/', 'history':'history/', 'handover':'handover/', 'sources':'sources/'}.items():
        source = dist/'record'/route/'index.html'
        target = dist/'record/readable'/f'{name}.txt'
        if source.exists() and target.exists():
            parser = Readable('https://phoenix-foundation-irregularities.pfc.zone/record/'+route)
            parser.feed(source.read_text())
            target.write_text(parser.text())
            modified.add(target)

    # Source indexes must identify the actual edited download, while retaining original hashes separately.
    for path in (dist/'record/evidence/source_index.json', dist/'record/history/sources/source-index.json'):
        if not path.exists(): continue
        data = json.loads(path.read_text())
        for entry in data.get('sources', []):
            rel = entry.get('file')
            if not rel: continue
            target = next((p for p in (path.parent/rel, path.parent.parent/rel, dist/'record'/rel) if p.is_file()), None)
            if target in modified:
                entry['sha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
                if 'bytes' in entry: entry['bytes'] = target.stat().st_size
                entry['handling'] = 'Published copy with privacy edits; original source hash retained separately where recorded.'
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    manifest = dist/'record/verification.json'
    if manifest.exists():
        data = json.loads(manifest.read_text())
        data['publication_note'] = 'This publication omits personal-identification material and personal-allegation galleries. Curated source guides replace the original commentary; the older editorial chronology is omitted. Amounts and transaction references in retained financial datasets are unchanged.'
        for entry in data.get('pages', []):
            target = dist/'record'/urlparse(entry.get('text', '')).path.lstrip('/')
            if target.is_file(): entry['text_sha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
        for entry in data.get('datasets', []):
            target = dist/'record'/urlparse(entry.get('url', '')).path.lstrip('/')
            if target.is_file() and 'sha256' in entry:
                actual = hashlib.sha256(target.read_bytes()).hexdigest()
                if actual != entry['sha256']:
                    entry.setdefault('original_source_sha256', entry['sha256'])
                    entry['sha256'] = actual
                    entry['handling'] = 'Published copy with privacy edits.'
        manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    for manifest in dist.rglob('manifest.json'):
        data = json.loads(manifest.read_text())
        for entry in data.get('files', []):
            if not isinstance(entry, dict): continue
            target = manifest.parent / entry.get('file', '')
            if target.is_file():
                entry['sha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
                entry['bytes'] = target.stat().st_size
        manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    for sums in dist.rglob('SHA256SUMS.txt'):
        entries = []
        for path in sorted(sums.parent.rglob('*')):
            # Sidecars are generated after checksums. Including a checksum's
            # own sidecar creates a circular hash and makes rebuilds drift.
            # Payloads remain covered; provenance binds sidecars separately.
            if path.is_file() and path != sums and not path.name.endswith('.source.md'):
                entries.append(hashlib.sha256(path.read_bytes()).hexdigest()+'  '+str(path.relative_to(sums.parent)))
        sums.write_text('\n'.join(entries)+'\n')

    failures = []
    for path in dist.rglob('*'):
        if path.is_file() and path.suffix in TEXT_EXTENSIONS:
            text = unicodedata.normalize('NFKC', unescape(path.read_text()))
            if SURNAME.search(text) or IDENTITY_REFERENCE.search(text): failures.append(str(path.relative_to(dist)))
    if failures: raise RuntimeError('Publication privacy check failed in: '+', '.join(failures))
    return {'removed_artifacts':removed, 'edited_files':len(modified), 'remaining_surname_or_disclosure_references':0}
