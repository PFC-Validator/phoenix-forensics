# Phoenix governance audit pack

Start with `REPORT.md`, then `PAYMENTS.md` for the ownership, validator-transfer, Treasury, OTC, and compensation review.

## Contents

- `data/`: raw chain/forum records and CSV voting histories.
- `repos/`: exact source code and governance documents reviewed.
- `downloads/packaged_ledger.json`: preserved authority-use ledger and transaction locators.
- `analysis/`: export and verification scripts.
- `SHA256SUMS`: local integrity hashes.

## Evidence cautions

- `data/mb_voting_record.json` is a preserved compiled A1–A289 dataset with per-record original ballot query URLs, transaction hashes, timestamps, and source hashes. Fresh chain queries were also made for key proposals and current rules.
- Native 4853, ERIS multisig, current admin/owner, and hub-delegation JSON files were queried directly from public chain APIs during this review.
- No surname or identity-attribution research is included. Public wallet addresses appear only as governance/contract evidence.
- Snapshot data changes. Proposal 4853 remains open until 31 October 2026 at 03:40:11 UTC.

## Reproduce exports

```sh
python3 analysis/export_data.py
python3 analysis/verify.py
python3 analysis/verify_payments.py
```

`analysis/make_download_manifest.py` creates a URL manifest for deeper per-proposal downloads. Public API availability and historical indexing vary by provider.
