#!/usr/bin/env python3
"""Refresh monitored legacy tx queries through every page (network required)."""
from __future__ import annotations
import argparse
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path
from pipeline_utils import ROOT, WALLET_CAPTURES


def source_url(path: Path) -> str:
    sidecar = path.with_name(path.name + '.source.md').read_text()
    section = sidecar.split('## Immediate source(s)', 1)[1].split('## Upstream original source(s)', 1)[0]
    urls = [line[2:].strip() for line in section.splitlines() if line.startswith('- http')]
    if not urls:
        raise ValueError(f'{path}: no immediate source URL')
    return urls[0]


def fetch_page(base: str, page: int) -> dict:
    parts = urllib.parse.urlsplit(base)
    query = urllib.parse.parse_qs(parts.query)
    query['page'] = [str(page)]
    query['limit'] = ['100']
    url = urllib.parse.urlunsplit(parts._replace(query=urllib.parse.urlencode(query, doseq=True)))
    request = urllib.request.Request(url, headers={'User-Agent': 'phoenix-forensics-capture-refresh/1.0'})
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.load(response)


def refresh(rel: str) -> dict:
    path = ROOT / rel
    base = source_url(path)
    first = fetch_page(base, 1)
    total = int(first.get('total') or len(first.get('tx_responses', [])))
    pages = [first]
    for page in range(2, (total + 99) // 100 + 1):
        pages.append(fetch_page(base, page))
        time.sleep(0.1)
    txs = [tx for response in pages for tx in response.get('txs', [])]
    responses = [tx for response in pages for tx in response.get('tx_responses', [])]
    if len(responses) != total or len({tx['txhash'] for tx in responses}) != total:
        raise ValueError(f'{rel}: incomplete or duplicate refreshed responses; original left unchanged')
    result = dict(first)
    result['txs'] = txs
    result['tx_responses'] = responses
    result['pagination'] = None
    result['total'] = str(total)
    path.write_text(json.dumps(result, indent=2) + '\n')
    return {'file': rel, 'pages': len(pages), 'responses': total}


parser = argparse.ArgumentParser()
parser.add_argument('--only', choices=WALLET_CAPTURES, action='append')
args = parser.parse_args()
results = [refresh(rel) for rel in args.only or WALLET_CAPTURES]
print(json.dumps({'refreshed': results}, indent=2))
