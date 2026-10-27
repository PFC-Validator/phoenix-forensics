#!/usr/bin/env python3
"""Capture narrowly scoped governance queries supporting the transaction checks."""
import base64
import concurrent.futures
import hashlib
import json
from collect_lead_transactions import BASE, COSMOS, dump, get, now

MAIN = 'terra1660g9mle5kfsq8c0p4k4hgr9ujdyr3m48c22cawy0akr98rmwksqehqnup'
HUB = 'terra10788fkzah89xrdm27zkj5yvhj9x3494lxawzm5qq3vvxcqz2yzaqyd3enk'
REGISTRY = 'terra1hwxg6s732eparz3ys7sa4t5f64ngpd2w8syrca6z7ckv3fs9uqnsvrpcqa'
ESCROW = 'terra1uqhj8agyeaz8fu6mdggfuwr3lp32jlrx5hqag4jxexde92rzkamq3l62zg'
CREDA = 'terra1y6hfmr3lxxj6srduhlfz96x7sga2984pr757a0nrfuqxa9rqxapqcjv4zz'
CREDA_REGISTRY = 'terra1skhnhcj653zfkqzd4txcashg0qu4v0vnpckeztgmsm46cqn33lhsxyej6c'
AMP = 'terra1ecgazyd0waaj3g7l9cmy5gulhxkps2gmxu9ghducvuypjq68mq2s5lvsct'
ARB = 'terra1se7rvuerys4kd2snt6vqswh9wugu49vhyzls8ymc02wl37g2p2ms5yz490'
NEUTRON_PROPOSAL = 'neutron19v3vnv8u67ynumwpltwnhd6umatjys9atmctwh288ummmlds5gms9efm6h'


def contract_path(address, query=None):
    path = '/cosmwasm/wasm/v1/contract/' + address
    if query is not None:
        encoded = base64.b64encode(json.dumps(query, separators=(',', ':')).encode()).decode()
        path += '/smart/' + encoded
    return path


def requests():
    rows = []
    def add(name, chain, path, leads, height=None):
        rows.append(dict(name=name, chain=chain, path=path, lead_ids=leads, requested_height=height))
    for n in [33, 43]:
        add(f'phoenix_A{n}_proposal', 'terra2', contract_path(MAIN, {'proposal': {'proposal_id': n}}), [23 if n == 43 else 24])
        add(f'phoenix_A{n}_votes', 'terra2', contract_path(MAIN, {'list_votes': {'proposal_id': n, 'limit': 100}}), [23 if n == 43 else 24])
    for address, name in [(AMP, 'ampluna'), (ARB, 'arbluna')]:
        add(name + '_token_info', 'terra2', contract_path(address, {'token_info': {}}), [5, 23, 24, 27, 46])
    for n in [429, 432]:
        add(f'lock_{n}', 'terra2', contract_path(ESCROW, {'lock_info': {'token_id': str(n)}}), [25], 23464975)
    for name, address in [('treasury', 'terra16st8yfprkdl06kccktshd3p2vccq93xcn9mkhjl8s4jumyjtd4kqye0me5'),
                          ('escrow', ESCROW), ('hub', HUB), ('creda_portfolio', CREDA)]:
        add(name + '_contract', 'terra2', contract_path(address), [55, 56], 23476938)
    for name, address, query in [
        ('registry_ownership', REGISTRY, {'ownership': {}}),
        ('registry_roles', REGISTRY, {'all_addresses': {}}),
        ('hub_config', HUB, {'config': {}}),
        ('creda_ownership', CREDA_REGISTRY, {'ownership': {}}),
        ('creda_roles', CREDA_REGISTRY, {'all_addresses': {}}),
        ('creda_state', CREDA, {'state': {}}),
        ('gauge_config', 'terra1z0cxlq62a9dsjhz7g7hhgpuplcl32c0qeckhm9jyggln0rxq6z8syesq8j', {'config': {}}),
    ]:
        add(name, 'terra2', contract_path(address, query), [20, 55, 56], 23476938)
    add('hub_vote_operator', 'terra2', contract_path(HUB) + '/raw/dm90ZV9vcGVyYXRvcg==', [20], 23476938)
    add('superbolt_35_proposal', 'neutron', contract_path(NEUTRON_PROPOSAL, {'proposal': {'proposal_id': 35}}), [13])
    add('superbolt_35_votes', 'neutron', contract_path(NEUTRON_PROPOSAL, {'list_votes': {'proposal_id': 35, 'limit': 100}}), [13])
    add('superbolt_usdc_trace', 'neutron', '/ibc/apps/transfer/v1/denom_traces/B559A80D62249C8AA07A380E2A2BEA6E5CA9A6F079C912C3A9E9B494105E4F81', [13])
    add('superbolt_usdc_trace_v2', 'neutron', '/ibc/apps/transfer/v1/denoms/B559A80D62249C8AA07A380E2A2BEA6E5CA9A6F079C912C3A9E9B494105E4F81', [13])
    add('review_creda_metrics', 'terra2', contract_path(CREDA, {'metrics': {}}), [4, 35])
    for n in [28, 72, 109, 110]:
        add(f'review_treasury_action_{n}', 'terra2', contract_path('terra16st8yfprkdl06kccktshd3p2vccq93xcn9mkhjl8s4jumyjtd4kqye0me5', {'action': {'id': n}}), [36, 37])
    operations = 'terra1l0ny38guhwrzczesgvk2zwj7xcen63jzmpusjv9hemvua9vptcyqwqy7pl'
    add('review_operations_config', 'terra2', contract_path(operations, {'config': {}}), [35])
    for name, address in [('operations', operations), ('board', 'terra1k8ug6dkzntczfzn76wsh24tdjmx944yj6mk063wum7n20cwd7lxq4lppjg'),
                          ('tla_single', 'terra1qdz5qgafx88kp5mf6m2tah8742g4u5g2cek0m3jrgssexexk7g4qw6e23k')]:
        add('review_creda_portfolio_' + name, 'terra2', contract_path(CREDA, {'portfolio': {'address': address}}), [35])
    # Preserve failed historical checks separately; a current response never
    # silently substitutes for the requested historical snapshot.
    rows += [{**r, 'name': r['name'] + '_current', 'requested_height': None,
              'historical_snapshot_not_established': True}
             for r in rows if r['requested_height'] is not None]
    return rows


def capture(row):
    path = BASE / 'queries' / (row['name'] + '.json')
    meta = path.with_suffix('.capture.json')
    if path.exists() and meta.exists():
        return {**row, **json.loads(meta.read_text())}
    attempts = []
    for host in COSMOS[row['chain']]:
        url = host + row['path']
        headers = {'x-cosmos-block-height': str(row['requested_height'])} if row['requested_height'] else {}
        try:
            raw, value, response_headers = get(url, headers=headers)
            if isinstance(value, dict) and 'code' in value and 'message' in value:
                raise ValueError('API error: ' + str(value)[:150])
            returned = response_headers.get('x-cosmos-block-height')
            pinned = row['requested_height'] is not None
            if pinned and returned != str(row['requested_height']):
                raise ValueError('Historical response height not confirmed: ' + str(returned))
            path.write_bytes(raw)
            result = {'status': 'historical_height_confirmed' if pinned else 'current_query',
                      'file': path.relative_to(BASE.parents[1]).as_posix(), 'source_url': url,
                      'acquired_utc': now(), 'sha256': hashlib.sha256(raw).hexdigest(),
                      'response_headers': response_headers, 'attempts': attempts,
                      'limitation': 'A provider response, not a consensus proof; current queries are not historical snapshots.'}
            dump(meta, result)
            return {**row, **result}
        except Exception as error:
            attempts.append({'url': url, 'error': str(error)[:240]})
    return {**row, 'status': 'unavailable', 'attempts': attempts, 'checked_utc': now()}


if __name__ == '__main__':
    rows = requests()
    dump(BASE / 'query_requests.json', rows)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(capture, rows))
    dump(BASE / 'query_manifest.json', {'acquired_utc': now(), 'queries': results})
    counts = {}
    for row in results:
        counts[row['status']] = counts.get(row['status'], 0) + 1
    print(json.dumps(counts, indent=2))
