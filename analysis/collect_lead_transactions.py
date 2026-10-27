#!/usr/bin/env python3
"""Capture allowlisted public transaction leads; never import identity research.

Run with --leads PATH once to create requests.json. Subsequent runs use that
sanitized request inventory. Captures are immutable unless --refresh is passed.
"""
import argparse
import concurrent.futures
import datetime
import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'data/leads'
COSMOS = {
    'terra2': ['https://terra2.tdrsys.com', 'https://terra-phoenix-api.highstakes.ch', 'http://15.204.43.42:1317'],
    'neutron': ['https://rest-archive.neutron.solva.solutions', 'https://rest-kralum.neutron-1.neutron.org'],
    'archway': ['https://api.mainnet.archway.io'],
    'injective': ['https://injective-api.highstakes.ch', 'https://sentry.lcd.injective.network'],
}
EVM = {'base': ['https://base-rpc.publicnode.com', 'https://mainnet.base.org'],
       'ethereum': ['https://ethereum-rpc.publicnode.com', 'https://eth.llamarpc.com'],
       'injective_evm': ['https://sentry.evm-rpc.injective.network']}


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def inventory(path):
    """Only transaction locators from governance/financial leads 1–59."""
    text = path.read_text()
    rows = {}
    for match in re.finditer(r'^(\d+)\. ([^\n]+)\n(.*?)(?=^\d+\. |\Z)', text, re.M | re.S):
        number = int(match[1])
        if number > 59:
            continue
        for url in re.findall(r'https?://[^\s]+', match[3]):
            tx = re.search(r'/(?:tx|txs)/((?:0x)?[A-Fa-f0-9]{64})(?:[?#/]|$)', url)
            if not tx:
                continue
            h = tx[1]
            if h.startswith('0x'):
                chain = ('base' if 'basescan.org' in url else
                         'ethereum' if 'etherscan.io' in url else
                         'injective_evm' if 'blockscout.injective' in url else None)
                h = h.lower()
            else:
                chain = ('neutron' if 'neutron.' in url else 'archway' if 'archway.io' in url else
                         'injective' if 'injective-api' in url else 'cosmoshub' if 'mintscan.io/cosmos' in url else
                         'axelar' if 'axelarscan.io' in url else 'terra2' if any(s in url for s in
                         ['chainsco.pe/terra2', 'terra2.tdrsys', 'terra-phoenix-api']) else None)
                h = h.upper()
            if chain is None:
                continue
            key = chain + ':' + h
            row = rows.setdefault(key, {'chain': chain, 'hash': h, 'lead_ids': [], 'lead_urls': []})
            if number not in row['lead_ids']:
                row['lead_ids'].append(number)
            if url not in row['lead_urls']:
                row['lead_urls'].append(url)
    return {'scope': 'Public governance and financial transaction locators from leads 1–59 only; identity-research section excluded.',
            'transactions': list(rows.values())}


def get(url, rpc=None, headers=None):
    body = None if rpc is None else json.dumps(rpc).encode()
    request = urllib.request.Request(url, data=body, headers={
        'User-Agent': 'Phoenix-evidence-verifier/1.0',
        **({'Content-Type': 'application/json'} if rpc else {}), **(headers or {})})
    with urllib.request.urlopen(request, timeout=18) as response:
        raw = response.read()
        value = json.loads(raw)
        return raw, value, {k.lower(): v for k, v in response.headers.items()
                           if k.lower() in ['x-cosmos-block-height', 'content-type', 'date']}


def capture(row, refresh=False):
    chain, h = row['chain'], row['hash']
    relative = f'transactions/{chain}_{h}.json'
    path = BASE / relative
    meta_path = path.with_suffix('.capture.json')
    if path.exists() and meta_path.exists() and not refresh:
        return {**row, **json.loads(meta_path.read_text())}
    attempts = []
    hosts = COSMOS.get(chain, EVM.get(chain, []))
    if chain == 'cosmoshub':
        hosts = ['https://cosmos-rest.publicnode.com']
    if chain == 'axelar':
        hosts = ['https://axelar-rest.publicnode.com', 'https://lcd-axelar.imperator.co']
    for host in hosts:
        url = host + '/cosmos/tx/v1beta1/txs/' + h if chain not in EVM else host
        try:
            if chain in EVM:
                rpc = {'jsonrpc': '2.0', 'id': 1, 'method': 'eth_getTransactionReceipt', 'params': [h]}
                raw, value, headers = get(url, rpc)
                response = value.get('result')
                if not response or response.get('transactionHash', '').lower() != h:
                    raise ValueError('Missing or mismatched EVM receipt')
                code = int(response['status'], 16)
                success = code == 1
                height = str(int(response['blockNumber'], 16))
            else:
                raw, value, headers = get(url)
                response = value.get('tx_response', {})
                if response.get('txhash', '').upper() != h or 'code' not in response:
                    raise ValueError('Missing or mismatched Cosmos transaction response')
                success = int(response['code']) == 0
                code = int(response['code'])
                height = response['height']
                if int(height) <= 0:
                    raise ValueError('Transaction not included at positive height')
            path.write_bytes(raw)
            result = {'status': 'successful_primary_record' if success else 'failed_on_chain',
                      'file': 'data/leads/' + relative, 'source_url': url,
                      'acquired_utc': now(), 'sha256': hashlib.sha256(raw).hexdigest(),
                      'height': height, 'execution_code': code, 'response_headers': headers,
                      'attempts': attempts,
                      'limitation': 'Primary provider execution record; lead-specific claims require separate checks. No consensus proof or independent-provider agreement implied.'}
            if chain in EVM:
                result['request'] = rpc
            else:
                result['timestamp'] = response.get('timestamp')
            dump(meta_path, result)
            return {**row, **result}
        except Exception as error:
            attempts.append({'url': url, 'error': str(error)[:240]})
    return {**row, 'status': 'unavailable', 'attempts': attempts, 'checked_utc': now()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--leads', type=Path)
    parser.add_argument('--refresh', action='store_true')
    args = parser.parse_args()
    BASE.mkdir(parents=True, exist_ok=True)
    if args.leads:
        dump(BASE / 'requests.json', inventory(args.leads))
    requests = json.loads((BASE / 'requests.json').read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda row: capture(row, args.refresh), requests['transactions']))
    dump(BASE / 'capture_manifest.json', {'schema_version': 1, 'acquired_utc': now(),
         'scope': requests['scope'], 'transactions': results})
    counts = {}
    for row in results:
        counts[row['status']] = counts.get(row['status'], 0) + 1
    print(json.dumps({'transactions': len(results), 'statuses': counts}, indent=2))


if __name__ == '__main__':
    main()
