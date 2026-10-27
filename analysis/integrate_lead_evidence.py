#!/usr/bin/env python3
"""Reproduce the supplemental transaction ledger and bounded governance findings.

No network access. Historical captures and earlier aggregate totals are preserved.
"""
import base64
import csv
import hashlib
import io
import json
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path
from collect_lead_transactions import BASE, ROOT, EVM, dump
from collect_lead_queries import AMP, ARB, ESCROW, CREDA, HUB
from crosscheck_lead_transactions import TRANSFER
from pipeline_utils import parse_coins, USDC

FEE = 'terra1rgggsspquaxjp4lmegx7a3q4l9lg44hnu7rjxa'
BOARD = 'terra1k8ug6dkzntczfzn76wsh24tdjmx944yj6mk063wum7n20cwd7lxq4lppjg'
NEUTRON_USDC = 'ibc/B559A80D62249C8AA07A380E2A2BEA6E5CA9A6F079C912C3A9E9B494105E4F81'
CERES = 'terravaloper1q8w4u2wyhx574m70gwe8km5za2ptanny9mnqy3'


def load(path):
    return json.loads((ROOT / path).read_text())


def attributes(event):
    result = defaultdict(list)
    for a in event['attributes']:
        result[a['key']].append(a['value'])
    return dict(result)


def one(attrs, key, default=None):
    values = attrs.get(key, [])
    if not values:
        return default
    if len(values) != 1:
        raise ValueError(f'Ambiguous {key}: {values}')
    return values[0]


def units(amount, decimals):
    return format(Decimal(amount) / Decimal(10) ** decimals, 'f')


def build():
    manifest = load('data/leads/capture_manifest.json')
    metadata = load('data/leads/evm_metadata_manifest.json')
    token_meta = {('terra2', 'uluna'): (6, 'LUNA'), ('terra2', USDC): (6, 'USDC')}
    for name, address in [('ampluna', AMP), ('arbluna', ARB)]:
        d = load('data/leads/queries/' + name + '_token_info.json')['data']
        token_meta[('terra2', address)] = (int(d['decimals']), d['symbol'])
    # The IBC trace establishes the base denomination; the 6-decimal USDC unit
    # is an explicit denomination convention, not inferred from the amount.
    trace = load('data/leads/queries/superbolt_usdc_trace_v2.json')['denom']
    assert trace['base'] == 'uusdc'
    trace_string = '/'.join(x for hop in trace['trace'] for x in (hop['port_id'], hop['channel_id'])) + '/uusdc'
    assert hashlib.sha256(trace_string.encode()).hexdigest().upper() == NEUTRON_USDC[4:]
    token_meta[('neutron', NEUTRON_USDC)] = (6, 'USDC')
    for r in metadata['queries']:
        if r['status'] != 'unavailable' and r['name'].endswith('_decimals'):
            address = r['request']['params'][0]['to']
            token_meta[(r['chain'], address)] = (int(load(r['file'])['result'], 16), None)
    transfers, redelegations, locks, fee_annotations, records, unquantified = [], [], [], [], [], []
    by_prefix = {}
    def movement(common, sender, recipient, amount, asset, kind):
        amount = str(amount)
        if not amount.isdigit():
            raise ValueError('Invalid integer amount')
        decimals, symbol = token_meta.get((common['chain'], asset), (None, None))
        transfers.append({**common, 'sender': sender, 'recipient': recipient,
                          'amount_base': amount, 'asset': asset, 'asset_kind': kind,
                          'decimals': decimals, 'symbol': symbol,
                          'amount_display': units(amount, decimals) if decimals is not None else None,
                          'classification': 'movement; not automatically income'})
    for row in manifest['transactions']:
        if row['status'] != 'successful_primary_record':
            continue
        raw = (ROOT / row['file']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row['sha256']
        doc = json.loads(raw)
        common = {k: row.get(k) for k in ['chain', 'hash', 'height', 'timestamp', 'file', 'lead_ids']}
        rec = {**common, 'source_url': row['source_url'], 'execution_code': row['execution_code']}
        if row['chain'] in EVM:
            receipt = doc['result']
            assert receipt['transactionHash'].lower() == row['hash'] and int(receipt['status'], 16) == 1
            rec['caller'] = receipt['from']
            rec['called_contract'] = receipt['to']
            rec['messages'] = []
            for i, event in enumerate(receipt['logs']):
                if event.get('topics', [None])[0] == TRANSFER and len(event['topics']) == 3:
                    assert not event.get('removed', False)
                    assert len(event['data']) == 66
                    movement({**common, 'event_index': i, 'event_type': 'ERC20 Transfer'},
                             '0x' + event['topics'][1][-40:], '0x' + event['topics'][2][-40:],
                             str(int(event['data'], 16)), event['address'], 'erc20')
        else:
            response = doc['tx_response']
            assert response['txhash'].upper() == row['hash'] and int(response['code']) == 0
            assert response['height'] == row['height']
            rec['messages'] = doc.get('tx', {}).get('body', {}).get('messages', [])
            rec['admin_changes'] = [{'event_index': i, 'attributes': attributes(e)} for i, e in enumerate(response.get('events', [])) if e['type'] == 'update_contract_admin']
            rec['event_types'] = dict(Counter(e['type'] for e in response.get('events', [])))
            pending_funding = None
            for i, event in enumerate(response.get('events', [])):
                a = attributes(event)
                c = {**common, 'event_index': i, 'event_type': event['type']}
                if event['type'] == 'transfer':
                    for key in ['sender', 'recipient', 'amount']:
                        assert len(a.get(key, [])) == 1, (row['hash'], i, a)
                    if one(a, 'amount') == '':
                        unquantified.append({**c, 'attributes': a,
                            'reason': 'Provider emitted an empty coin amount. Preserved separately, not converted to zero or included in amount totals.'})
                        continue
                    for coin in parse_coins(one(a, 'amount')):
                        movement(c, one(a, 'sender'), one(a, 'recipient'), coin['amount'], coin['denom'], 'native')
                elif event['type'] == 'wasm':
                    actions = a.get('action', [])
                    contract = one(a, '_contract_address')
                    if any(x in actions for x in ['transfer', 'send']) and all(k in a for k in ['from', 'to', 'amount']):
                        movement(c, one(a, 'from'), one(a, 'to'), one(a, 'amount'), contract, 'cw20')
                    if contract == AMP and 'send' in actions and one(a, 'to') == ESCROW:
                        pending_funding = {'amount_base': one(a, 'amount'), 'funding_event_index': i, 'funding_sender': one(a, 'from')}
                    if contract == ESCROW and 've/create_lock' in actions:
                        assert pending_funding is not None
                        locks.append({**c, **pending_funding, 'token_id': one(a, 'token_id'),
                                      'owner': one(a, 'owner'), 'lock_end': one(a, 'lock_end'),
                                      'amount_ampLUNA': units(pending_funding['amount_base'], 6),
                                      'voting_power_base': one(a, 'voting_power'),
                                      'fixed_power_base': one(a, 'fixed_power')})
                        pending_funding = None
                elif event['type'] == 'redelegate':
                    coin, = parse_coins(one(a, 'amount'))
                    assert coin['denom'] == 'uluna'
                    redelegations.append({**c, 'source_validator': one(a, 'source_validator'),
                                          'destination_validator': one(a, 'destination_validator'),
                                          'amount_base': str(coin['amount']), 'amount_LUNA': units(coin['amount'], 6)})
                elif event['type'] == 'juno.feeshare.v1.FeePayoutEvent':
                    fee_annotations.append({**c, 'recipient': json.loads(one(a, 'withdraw_address')),
                                            'coins': json.loads(one(a, 'fees_paid')),
                                            'accounting': 'Annotation only; corresponding bank transfer is already in transfers.json.'})
        records.append(rec)
        by_prefix[row['hash'][:10]] = rec
    def tx(prefix):
        return next(r for r in records if r['hash'].startswith(prefix))
    def moves(prefix, recipient=None, sender=None, asset=None):
        h = tx(prefix)['hash']
        return [r for r in transfers if r['hash'] == h and
                (recipient is None or r['recipient'] == recipient) and
                (sender is None or r['sender'] == sender) and (asset is None or r['asset'] == asset)]
    findings = []
    def finding(key, leads, title, facts, sources, limits):
        findings.append(dict(id=key, lead_ids=leads, status='supported_with_stated_limits',
                             title=title, facts=facts, sources=sources, limits=limits))
    def files(*prefixes):
        return [tx(p)['file'] for p in prefixes]
    for n, prefix in [(43, 'D660FD'), (33, '83EF0856')]:
        award = [r for r in locks if r['hash'] == tx(prefix)['hash']]
        votes = load(f'data/leads/queries/phoenix_A{n}_votes.json')['data']['votes']
        yes = {r['voter']: int(r['power']) for r in votes if r['vote'] == 'yes'}
        total = sum(int(r['amount_base']) for r in award)
        finding(f'phoenix_A{n}_locks', [23 if n == 43 else 24], f'Phoenix A{n}: funded permanent voting locks',
                {'locks': award, 'total_ampLUNA': units(total, 6), 'yes_weight': sum(yes.values()),
                 'recipient_yes_weight': sum(p for address, p in yes.items() if address in {r['owner'] for r in award}),
                 'ballots': votes}, files(prefix) + [f'data/leads/queries/phoenix_A{n}_proposal.json', f'data/leads/queries/phoenix_A{n}_votes.json'],
                'Funding and beneficiary participation are established by matching addresses. These are TLA locks, not native LUNA ballots. No claim of breach, sole key custody or personal profit.')
    redeemed = moves('DB4333', asset=AMP)
    receipts = [m['funds'][0] for m in tx('DB4333')['messages']]
    finding('receipt_redemption', [5, 53], 'Receipt redemption after BURN_RECIPIENT assignment',
            {'assignment_messages': tx('D3D3B6')['messages'], 'receipt_denominations': receipts,
             'ampLUNA_transfers': redeemed, 'ampLUNA_total': units(sum(int(r['amount_base']) for r in redeemed), 6),
             'gas_fee_share_LUNA': units(sum(int(c['amount']) for r in fee_annotations if r['hash'] == tx('DB4333')['hash'] for c in r['coins'] if c['denom'] == 'uluna'), 6)},
            files('D3D3B6', 'DB4333'), 'Each receipt denomination remains separate. No assertion of exclusive custody or complete intervening receipts history. Gas fee sharing is an annotation, not a second bank receipt.')
    start, end = tx('5E62BA'), tx('EDC654')
    from datetime import datetime
    duration = int((datetime.fromisoformat(end['timestamp'].replace('Z', '+00:00')) - datetime.fromisoformat(start['timestamp'].replace('Z', '+00:00'))).total_seconds())
    finding('restriction_assignment', [6], 'Restriction-list assignment and clearing',
            {'start_utc': start['timestamp'], 'end_utc': end['timestamp'], 'seconds_between': duration,
             'assignment_messages': start['messages'], 'clearing_messages': end['messages'],
             'migration_messages': [tx(p)['messages'] for p in ['D5111F', 'BB874B']]},
            files('D5111F', 'BB874B', '5E62BA', 'EDC654'), 'The interval between these two events is confirmed. No full intervening-history replay, deployed-binary permission analysis or failed withdrawal demonstrated in this supplement.')
    for prefix, key, lead in [('DC3118', 'fee_collector_assignment', 7), ('B71CF3', 'treasury_config_assignment', 9), ('3C9C6A', 'arbluna_collateral_added', 10)]:
        finding(key, [lead], key.replace('_', ' ').capitalize(), {'messages': tx(prefix)['messages']}, files(prefix),
                'Confirms this successful action only. Earlier assignment, prior role value, full revenue history and motive are not inferred.')
    redelegs = [r for r in redelegations if r['hash'] == tx('42CF09')['hash']]
    finding('ceres_removal_rebalance', [57], 'Ceres removal followed by seven redelegations',
            {'removal_messages': tx('536298')['messages'], 'redelegations': redelegs,
             'total_LUNA': units(sum(int(r['amount_base']) for r in redelegs), 6),
             'from_removed_validator_LUNA': units(sum(int(r['amount_base']) for r in redelegs if r['source_validator'] == CERES), 6),
             'seconds_after_removal': int((datetime.fromisoformat(tx('42CF09')['timestamp'].replace('Z', '+00:00')) - datetime.fromisoformat(tx('536298')['timestamp'].replace('Z', '+00:00'))).total_seconds())},
            files('536298', '42CF09'), 'Establishes allocation changes, not their reason. Hub staking redelegations are separate from Phoenix Alliance allocations.')
    super_moves = moves('4D7BC6', asset=NEUTRON_USDC)
    votes = load('data/leads/queries/superbolt_35_votes.json')['data']['votes']
    recipients = {r['recipient'] for r in super_moves}
    finding('superbolt_distribution', [13], 'Superbolt proposal 35: distribution and three YES ballots',
            {'transfers': super_moves, 'total_USDC': units(sum(int(r['amount_base']) for r in super_moves), 6),
             'ballots': votes, 'yes_ballots': sum(r['vote'] == 'yes' for r in votes),
             'recipient_yes_ballots': sum(r['vote'] == 'yes' and r['voter'] in recipients for r in votes)},
            files('F1ADBC', '456F47', '4D7BC6') + ['data/leads/queries/superbolt_35_votes.json', 'data/leads/queries/superbolt_35_proposal.json', 'data/leads/queries/superbolt_usdc_trace_v2.json'],
            'USDC base denomination verified by IBC trace; six-decimal USDC convention explicit. No cross-chain personal identity attribution; upstream grants and onward distributions are not additive funding.')
    finding('creda_reserve_collections', [34, 56], 'Two realized Creda reserve collections',
            {'collections': [{'timestamp': tx(p)['timestamp'], 'transfers': moves(p, recipient=FEE, sender=CREDA),
                              'LUNA_component': units(sum(int(r['amount_base']) for r in moves(p, recipient=FEE, sender=CREDA, asset='uluna')), 6)} for p in ['069AE6', '6A80B9']]},
            files('069AE6', '6A80B9'), 'LUNA is only one asset collected. Other assets stay separate; no lifetime fee total, personal profit or additive accrued-reserve estimate.')
    finding('compounder_fee_samples', [27], 'Two Votion compounder fee receipts',
            {'fee_transfers': moves('F4C13E', recipient=FEE, asset=ARB) + moves('1F2C0F', recipient=FEE, asset=AMP)},
            files('F4C13E', '1F2C0F'), 'Actual fee transfers in arbLUNA and ampLUNA; not LUNA. Does not verify the proposed 292-receipt history or lifetime totals.')
    funding_wallet = 'terra1vm5azhvaxeanc7auxh02y8jmxrk8tj93f6aywp'
    finding('milestone_receipts', [36, 42], 'Creda analytics and Estima kickoff payment receipts',
            {'creda_analytics': moves('1D09DC', recipient=funding_wallet, asset=USDC),
             'estima_kickoff': moves('491B94', recipient=funding_wallet, asset=USDC)},
            files('1D09DC', '491B94'), 'Verifies payment receipts only. Does not establish missing delivery, adequate acceptance or the source of every later cross-chain transfer.')
    pol = 'terra1kzkrm2a8qquer9dgztg4a3fvhh8d7fudsd7ualae843wsv9plhksv8ea3g'
    finding('liquidity_withdrawal_custody', [46], 'Liquidity withdrawal paid the deployment DAO',
            {'caller_messages': tx('BA2B95')['messages'], 'recipient_transfers': moves('BA2B95', recipient=pol)},
            files('BA2B95'), 'The transaction executor and asset recipient differ. No personal-income attribution to the executor.')
    finding('large_account_examples', [11, 12], 'Large unattributed account: dated transfer examples',
            {'first_example': moves('C17043'), 'latest_example': moves('3FFA5B'),
             'latest_example_utc': tx('3FFA5B')['timestamp'], 'outgoing_example': moves('F402C1')},
            files('C17043', '3FFA5B', 'F402C1'), 'Confirms examples, including the 19 October UTC date, not the claimed 26-payment/303,490-LUNA total. Wallet controller and payment purpose remain unattributed.')
    for key, leads, prefixes, title, limits in [
        ('reward_samples', [26], ['9503DA', 'B32A85', 'E6AB07'], 'Voting-incentive payment examples', 'Does not join receipts to a publicly funded NFT without ownership history; no lifetime totals.'),
        ('protocol_fee_samples', [29, 30, 31, 32], ['000C5A', '015C67', '799A3A', 'CF6DD2', '128BE2', '878952', '457D99'], 'Protocol and validator-fee transaction samples', 'Only individual samples captured. Protocol fees, commission and routing legs are distinct. Unknown token units remain raw; no extrapolated revenue or USD valuation.'),
        ('validator_unjail_samples', [18, 52], ['176C41', '6C92D0'], 'Successful validator unjail transactions', 'Unjail dates do not establish jail dates or uninterrupted Alliance shares. Historical policy and block-event checks remain open.'),
        ('superbolt_other_distribution', [38], ['1DE81B'], 'Additional Superbolt distribution', 'No reconciliation to AADAO grant receipts in this supplement; upstream funding and onward distribution are not additive.'),
        ('validator_payment_samples', [17], ['C940EB', 'B77EAB'], 'Validator payment examples', 'These examples are already represented in earlier datasets; do not add their totals again.'),
        ('cross_chain_individual_legs', [42, 43], ['F0F79E', '869878', '0x291699', '0x4da367', '0xd94656', '0x9154c3'], 'Cross-chain transaction and token-transfer legs', 'Individual successful records only. Full IBC/CCTP nonce and message matching remains open; no exchange-customer, cash-out or personal-use inference.'),
        ('partial_handover_execution', [55], ['86E599'], 'Successful two-contract migration-admin handover', 'Confirms execution and the two update_contract_admin events; retained configuration ownership is a separate current-state check.'),
    ]:
        selected = [tx(p) for p in prefixes]
        hashes = {r['hash'] for r in selected}
        finding(key, leads, title, {'transactions': selected, 'transfers': [r for r in transfers if r['hash'] in hashes]},
                [r['file'] for r in selected], limits)
    permissions = {}
    for name in ['treasury_contract_current', 'escrow_contract_current', 'hub_contract_current', 'creda_portfolio_contract_current',
                 'registry_ownership_current', 'registry_roles_current', 'hub_config_current', 'creda_ownership_current',
                 'creda_roles_current', 'gauge_config_current', 'hub_vote_operator_current']:
        p = BASE / 'queries' / (name + '.json')
        if p.exists():
            d = json.loads(p.read_text())
            if name == 'hub_vote_operator_current':
                d = {'decoded_vote_operator': json.loads(base64.b64decode(d['data']))}
            permissions[name] = {'response': d, 'file': p.relative_to(ROOT).as_posix()}
    finding('current_permission_layers', [20, 55, 56], 'Current permission layers after partial handover',
            permissions, [r['file'] for r in permissions.values()],
            'Current responses have no confirmed historical block height. Requested historical snapshots were not established. Public role labels do not prove exclusive personal key custody; capability checks require deployed-code matching.')
    changes = {}
    for n in [429, 432]:
        p = f'data/leads/queries/lock_{n}_current.json'
        changes[str(n)] = load(p)['data']
    finding('lock_current_state', [25], 'Current states differ from original permanent locks', changes,
            files('D660FD') + ['data/leads/queries/lock_429_current.json', 'data/leads/queries/lock_432_current.json'],
            'Current query only; exact change transactions, historical block and compliance with award terms remain unverified. No breach inferred.')
    outputs = {'transactions.json': records, 'transfers.json': transfers, 'redelegations.json': redelegations,
               'unquantified_transfer_events.json': unquantified,
               'voting_locks.json': locks, 'fee_share_annotations.json': fee_annotations,
               'verified_findings.json': {'scope': 'Bounded checks of cited transactions; not all lead narratives or full histories verified.', 'findings': findings}}
    statuses = []
    for lead in range(1, 60):
        rows = [r for r in manifest['transactions'] if lead in r['lead_ids']]
        checks = [r['id'] for r in findings if lead in r['lead_ids']]
        statuses.append({'lead_id': lead, 'status': 'bounded_findings_added' if checks else 'transaction_records_only' if rows else 'not_transaction_verified',
                         'successful_records': sum(r['status'] == 'successful_primary_record' for r in rows),
                         'unavailable_records': sum(r['status'] == 'unavailable' for r in rows), 'finding_ids': checks,
                         'limitation': 'Status does not verify every statement or proposed historical total in the lead.'})
    outputs['lead_status.json'] = statuses
    outputs['token_units.json'] = [{'chain': c, 'asset': a, 'decimals': d, 'symbol': s} for (c, a), (d, s) in sorted(token_meta.items())]
    review_metrics = BASE / 'queries/review_creda_metrics.json'
    if review_metrics.exists():
        metrics = json.loads(review_metrics.read_text())['data']
        supplied = Decimal(metrics['total_supplied_usd'])
        portfolios = {name: load('data/leads/queries/review_creda_portfolio_' + name + '.json')['data']
                      for name in ['operations', 'board', 'tla_single']}
        phoenix = sum(Decimal(portfolios[n]['total_supplied_value']) for n in ['operations', 'board'])
        tla = Decimal(portfolios['tla_single']['total_supplied_value'])
        actions = {}
        for n in [28, 72, 109, 110]:
            action = load(f'data/leads/queries/review_treasury_action_{n}.json')['data']
            if 'milestone' in action['setup']:
                scheduled = sum(int(m['amount']) for m in action['setup']['milestone']['milestones'])
                claimed = sum(int(m['amount']) for m in action['runtime']['milestone']['milestones'] if m['claimed'])
            else:
                scheduled = sum(int(p['asset']['amount']) for p in action['setup']['payment']['payments'])
                claimed = None  # An empty open list alone is not a fresh transfer replay.
            actions[str(n)] = {'name': action['name'], 'active_from': action['active_from'],
                               'scheduled_USDC': units(scheduled, 6),
                               'milestone_state_claimed_USDC': units(claimed, 6) if claimed is not None else None,
                               'done': action['done'], 'runtime': action['runtime'],
                               'source_file': f'data/leads/queries/review_treasury_action_{n}.json'}
        luna = next(a for a in metrics['assets'] if a['info'].get('native') == 'uluna')
        outputs['year_review_analysis.json'] = {
            'article_url': 'https://medium.com/@eris_protocol/eris-protocol-a-year-in-review-2025-2026-2973e303bed0',
            'treasury_actions': actions,
            'identified_named_project_grants_USDC': str(Decimal(actions['28']['scheduled_USDC']) + Decimal(actions['72']['scheduled_USDC']) + Decimal(actions['109']['scheduled_USDC'])),
            'review_period_grants_excluding_earlier_votion_USDC': str(Decimal(actions['72']['scheduled_USDC']) + Decimal(actions['109']['scheduled_USDC'])),
            'liquidity_capital_USDC_separate_from_expense': actions['110']['scheduled_USDC'],
            'external_votion_Hydro_grant': {'funder_reported_paid_USD': '50000',
                'source_url': 'https://forum.cosmos.network/t/aadao-wind-down-oversight-updates-and-reports/15913/22',
                'status': 'Funder reports full payment and jointly verified completion; settlement transactions not replayed in this review.'},
            'current_creda_metrics': {k: v for k, v in metrics.items() if k.startswith('total_')},
            'current_public_contract_positions': {n: {'address': p['address'], 'supplied_usd': p['total_supplied_value']} for n, p in portfolios.items()},
            'approximate_share_supplied_percent': {'phoenix_operations_and_board': str(phoenix / supplied * 100),
                'tla_single_pool': str(tla / supplied * 100), 'combined_public_contract_positions': str((phoenix + tla) / supplied * 100)},
            'luna_market': {k: luna[k] for k in ['total_supplied', 'total_borrowed', 'total_supplied_usd', 'total_borrowed_usd', 'utilization', 'borrow_apy']},
            'limits': ['Grant support is not causal attribution or total project cost.',
                'The Votion Treasury award predates the article period; Hydro funding purchases a separate scope.',
                'Liquidity capital, grants, payroll and deposited user capital are different categories.',
                'The external grant is funder-reported, not a new transaction verification.',
                'Position and metric queries are sequential current responses with no common confirmed height; percentages are approximate.',
                'TLA single-pool positions are pooled deposits, not necessarily Treasury-funded.',
                'The remaining supply is not proven to be independent external demand.',
                'Current supply does not establish an earlier peak or historical bad-debt absence.']}
    for name, value in outputs.items():
        dump(BASE / name, value)
    out = io.StringIO()
    fields = ['chain', 'hash', 'height', 'timestamp', 'event_index', 'event_type', 'sender', 'recipient', 'asset', 'amount_base', 'decimals', 'symbol', 'amount_display', 'asset_kind', 'classification', 'file']
    writer = csv.DictWriter(out, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(transfers)
    (BASE / 'transfers.csv').write_text(out.getvalue())
    artifacts = sorted(p for p in BASE.rglob('*') if p.is_file() and not p.name.endswith('.source.md') and p.name != 'SHA256SUMS')
    (BASE / 'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.relative_to(BASE).as_posix() + '\n' for p in artifacts))
    return {'successful_transactions': len(records), 'transfer_rows': len(transfers), 'locks': len(locks),
            'redelegations': len(redelegations), 'bounded_findings': len(findings),
            'unavailable_transactions': sum(r['status'] == 'unavailable' for r in manifest['transactions'])}


if __name__ == '__main__':
    print(json.dumps(build(), indent=2))
