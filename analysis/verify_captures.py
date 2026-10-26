#!/usr/bin/env python3
"""Report capture completeness; optionally fail when a census is required."""
import argparse
import json
from pipeline_utils import write_capture_report

parser = argparse.ArgumentParser()
parser.add_argument('--require-complete', action='store_true', help='Fail if any monitored wallet history is truncated.')
args = parser.parse_args()
report = write_capture_report()
print(json.dumps(report, indent=2))
if args.require_complete and not report['wallet_history_census_complete']:
    raise SystemExit('Incomplete wallet histories: refresh all pages before making census or absence claims.')
