#!/usr/bin/env python3
"""Re-fetch the small two-provider anchor set; read-only, network required."""
import json
import urllib.request
from pipeline_utils import load_json

record = load_json('data/cross_checks/anchor_endpoints.json')
results = []
for check in record['checks']:
    values = {}
    for provider in record['providers']:
        with urllib.request.urlopen(provider + check['path'], timeout=30) as response:
            values[provider] = json.load(response)
    exact = len(set(json.dumps(value, sort_keys=True) for value in values.values())) == 1
    results.append({'artifact': check['artifact'], 'exact_match': exact, 'responses': values})
    if check['artifact'] != 'native 4853 live tally' and not exact:
        raise SystemExit(f'Static anchor mismatch: {check["artifact"]}')
print(json.dumps({'checks': results}, indent=2))
