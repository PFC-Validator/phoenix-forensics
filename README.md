# Phoenix governance audit pack

Start with `REPORT.md`, then `PAYMENTS.md` for the ownership, validator-transfer, Treasury, OTC, and compensation review. See `THINKTANK.md` for the veto DAO, its voting record, member payment relationships and bounded wallet-link analysis. `GOVERNANCE_4853.md` assesses the live native vote, ERIS/vAMP influence, Lion DAO and potential governance issues.

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

## Capture completeness and verification order

The monitored director/Rebel wallet-history files include truncated query windows. Run `python3 analysis/verify_captures.py` for the current report and `python3 analysis/refresh_captures.py` in a network-enabled environment to fetch every page. Do not use those windows alone for lifetime comparisons or absence claims. The Treasury-outbound and validator-payment conclusions use separately completed captures.

Use this order so the website never references provenance files that have not been generated yet:

```sh
python3 analysis/export_data.py
python3 analysis/treasury_patterns.py
python3 analysis/eris_incoming_patterns.py
python3 analysis/counterparty_flows.py
python3 analysis/payment_summary.py
python3 analysis/director_profiles.py
python3 website/build.py
python3 analysis/generate_provenance.py
python3 analysis/test_pipeline.py
python3 analysis/verify_captures.py
python3 analysis/verify_provenance.py
python3 analysis/verify.py
python3 analysis/verify_payments.py
python3 analysis/verify_thinktank.py
python3 analysis/verify_anchor_crosschecks.py
python3 website/verify.py
```

`analysis/generate_upstream_indexes.py` is a separate, explicit refresh step for upstream indexes; verification never regenerates its own inputs. Sidecars are deterministic apart from the top-level register timestamp. `downloads/index.html` is inside the provenance boundary.

## Reproduce exports

```sh
python3 analysis/export_data.py
python3 analysis/verify.py
python3 analysis/verify_payments.py
```

`analysis/make_download_manifest.py` creates a URL manifest for deeper per-proposal downloads. Public API availability and historical indexing vary by provider.
