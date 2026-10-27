#!/usr/bin/env python3
"""Check Terra transaction bytes against SHA-256 and LCD height/result code.

The archive RPC and LCD may share infrastructure. This is a byte/hash and
endpoint consistency check, not independent consensus verification.
"""
import base64
import concurrent.futures
import hashlib
import json
from collect_lead_transactions import BASE, ROOT, EVM, dump, get, now

TRANSFER = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'


def evm_metadata(rows):
    checks = []
    for chain in sorted({r['chain'] for r in rows if r['chain'] in EVM and r['status'] == 'successful_primary_record'}):
        host = EVM[chain][0]
        calls = [('chain_id', 'eth_chainId', [])]
        tokens = {}
        for row in rows:
            if row['chain'] != chain or row['status'] != 'successful_primary_record':
                continue
            receipt = json.loads((ROOT / row['file']).read_text())['result']
            for event in receipt['logs']:
                if event.get('topics', [None])[0] == TRANSFER:
                    tokens[event['address']] = receipt['blockNumber']
        for token, block in tokens.items():
            calls.append((token + '_decimals', 'eth_call', [{'to': token, 'data': '0x313ce567'}, block]))
        for name, method, params in calls:
            path = BASE / 'queries' / (chain + '_' + name + '.json')
            meta = path.with_suffix('.capture.json')
            if path.exists() and meta.exists():
                checks.append(json.loads(meta.read_text()))
                continue
            request = {'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}
            try:
                raw, value, headers = get(host, request)
                if not value.get('result') or value.get('error'):
                    raise ValueError('Missing JSON-RPC result')
                int(value['result'], 16)
                path.write_bytes(raw)
                result = {'name': chain + '_' + name, 'chain': chain, 'status': 'current_query' if method == 'eth_chainId' else 'historical_rpc_call',
                          'source_url': host, 'request': request, 'acquired_utc': now(),
                          'sha256': hashlib.sha256(raw).hexdigest(), 'file': path.relative_to(ROOT).as_posix(),
                          'response_headers': headers, 'limitation': 'JSON-RPC provider response; token decimals do not establish economic value or ownership.'}
                dump(meta, result)
                checks.append(result)
            except Exception as error:
                checks.append({'name': chain + '_' + name, 'status': 'unavailable', 'error': str(error)[:240]})
    dump(BASE / 'evm_metadata_manifest.json', {'queries': checks})


def capture(row):
    name = 'terra2_' + row['hash']
    path = BASE / 'rpc' / (name + '.json')
    meta = path.with_suffix('.capture.json')
    if path.exists() and meta.exists():
        return json.loads(meta.read_text())
    url = 'http://15.204.43.42:26657/tx?hash=0x' + row['hash'] + '&prove=false'
    try:
        raw, value, headers = get(url)
        result = value['result']
        digest = hashlib.sha256(base64.b64decode(result['tx'], validate=True)).hexdigest().upper()
        if digest != row['hash'] or result['hash'].upper() != row['hash']:
            raise ValueError('Transaction bytes/hash mismatch')
        if result['height'] != row['height'] or int(result['tx_result']['code']) != row['execution_code']:
            raise ValueError('RPC/LCD execution mismatch')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        record = {'hash': row['hash'], 'file': path.relative_to(ROOT).as_posix(),
                  'source_url': url, 'acquired_utc': now(), 'sha256': hashlib.sha256(raw).hexdigest(),
                  'status': 'tx_bytes_hash_and_execution_match', 'lcd_file': row['file'],
                  'height': result['height'], 'execution_code': int(result['tx_result']['code']),
                  'response_headers': headers,
                  'limitation': 'Archive RPC/LCD may share infrastructure. No consensus inclusion proof or independent provider asserted.'}
        dump(meta, record)
        return record
    except Exception as error:
        return {'hash': row['hash'], 'status': 'unavailable_or_mismatch', 'source_url': url,
                'checked_utc': now(), 'error': str(error)[:240]}


if __name__ == '__main__':
    manifest = json.loads((BASE / 'capture_manifest.json').read_text())
    rows = [r for r in manifest['transactions'] if r['chain'] == 'terra2' and r['status'] == 'successful_primary_record']
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        checks = list(pool.map(capture, rows))
    dump(BASE / 'rpc_manifest.json', {'checks': checks})
    evm_metadata(manifest['transactions'])
    print(json.dumps({'checked': len(checks), 'matched': sum(r['status'] == 'tx_bytes_hash_and_execution_match' for r in checks)}, indent=2))
