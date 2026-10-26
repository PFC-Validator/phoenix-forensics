#!/usr/bin/env python3
"""Verify preserved two-provider anchor comparisons without rewriting them."""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
d = json.loads((R / 'data/cross_checks/anchor_endpoints.json').read_text())
assert len(d['providers']) == 2
checks = {x['artifact']: x for x in d['checks']}
assert checks['ampLUNA hub config']['exact_match'] is True
assert checks['CW20-ICS20 config']['exact_match'] is True
tally = checks['native 4853 live tally']
assert tally['exact_match'] is False and 'live tally changing' in tally['interpretation']
print('Checked preserved two-LCD anchors: hub and ICS20 config match exactly; sequential live tally values remain separately labelled.')
