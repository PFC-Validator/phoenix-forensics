"""Shared, fail-closed parsing and capture-completeness helpers."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECENT_CUTOFF = '2026-09-26'
USDC = 'ibc/2C962DAB9F57FE0921435426AE75196009FAA1981BF86991203C8411F8980FDB'
WBTC = 'ibc/CF57A83CED6CEC7D706631B5DC53ABC21B7EDA7DF7490732B4361E6D5DD19C73'
DENOM_DECIMALS = {'uluna': 6, USDC: 6, WBTC: 8}
COIN = re.compile(r'(?P<amount>[0-9]+)(?P<denom>[a-zA-Z][a-zA-Z0-9/:._-]*)')


def parse_coins(value: str) -> list[dict]:
    """Parse a Cosmos coin list; never discard an invalid or multi-coin amount."""
    if not isinstance(value, str) or not value:
        raise ValueError(f'Missing or invalid coin amount: {value!r}')
    coins = []
    for part in value.split(','):
        match = COIN.fullmatch(part.strip())
        if not match:
            raise ValueError(f'Unparseable coin amount: {value!r}')
        coins.append({'amount': int(match['amount']), 'denom': match['denom']})
    if not coins:
        raise ValueError(f'Empty coin amount: {value!r}')
    return coins


def display_amount(amount: int, denom: str) -> dict:
    """Return an explicit display value only when the denom's decimals are known."""
    if denom not in DENOM_DECIMALS:
        return {'base_amount': str(amount), 'base_denom': denom, 'display_amount': None, 'display_denom': None}
    decimals = DENOM_DECIMALS[denom]
    return {
        'base_amount': str(amount), 'base_denom': denom,
        'display_amount': amount / 10 ** decimals,
        'display_denom': {'uluna': 'LUNA', USDC: 'USDC', WBTC: 'WBTC'}[denom],
    }


def load_json(rel: str):
    return json.loads((ROOT / rel).read_text())


def capture_status(rel: str) -> dict:
    """Describe legacy total/page captures without calling them complete."""
    path = ROOT / rel
    data = load_json(rel)
    saved = len(data.get('tx_responses', []))
    total = int(data.get('total') or saved)
    complete = saved == total
    zero_countercheck = rel.endswith('MB_prior_treasury_transactions.json') and (ROOT / 'data/phoenix/MB_prior_counter_queries.json').exists()
    caution = None
    classification = 'complete capture' if complete else 'truncated window'
    if saved == 0 and total == 0:
        classification = 'zero indexed results with counter-queries' if zero_countercheck else 'zero indexed results; counter-query required'
        caution = 'Zero indexed results are not proof that the address never acted.'
    return {
        'file': rel,
        'saved': saved,
        'reported_total': total,
        'missing': total - saved,
        'complete': complete,
        'classification': classification,
        'caution': caution or (None if complete else 'Do not use this file alone for lifetime totals, cross-wallet comparisons, or absence claims.'),
    }


WALLET_CAPTURES = [
    'data/phoenix/MB_prior_treasury_transactions.json',
    'data/phoenix/MB_current_treasury_transactions.json',
    'data/phoenix/Vini_treasury_transactions.json',
    'data/phoenix/Rose_treasury_transactions.json',
    'data/transfers/rebel_project_sender.json',
    'data/transfers/rebel_project_recipient.json',
    'data/transfers/rebel_orbital_sender.json',
    'data/transfers/rebel_orbital_recipient.json',
]


def write_capture_report():
    rows = [capture_status(rel) for rel in WALLET_CAPTURES]
    result = {
        'wallet_history_census_complete': all(row['complete'] for row in rows),
        'captures': rows,
        'absence_claim_policy': 'Negative transfer findings cover only the preserved union. Complete both sender and recipient histories before making an unbounded absence claim.',
    }
    (ROOT / 'data' / 'capture_completeness.json').write_text(json.dumps(result, indent=2) + '\n')
    return result
