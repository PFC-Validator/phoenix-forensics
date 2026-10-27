# Source and provenance

- **Artifact:** `data/leads/rpc_manifest.json`
- **SHA-256:** `50365c330a9c9c1cff6f668326baac029be1d34d6b17cd02836e1b835f7990c3`
- **Timestamp basis:** No original acquisition timestamp established; file mtime is not used as acquisition evidence.
- **Classification:** Derived dataset
- **Acquisition / transformation:** Local transformation using `analysis/collect_lead_transactions.py; analysis/collect_lead_queries.py; analysis/crosscheck_lead_transactions.py`.
- **Transformation:** `analysis/collect_lead_transactions.py; analysis/collect_lead_queries.py; analysis/crosscheck_lead_transactions.py`

## Immediate source(s)

- data/leads/requests.json
- data/leads/query_requests.json
- data/leads/transactions/
- data/leads/queries/
- data/leads/rpc/

## Upstream original source(s)

- data/leads/requests.json
- data/leads/query_requests.json
- data/leads/transactions/
- data/leads/queries/
- data/leads/rpc/

## Scope, limits, and notes

Capture inventory includes unsuccessful attempts; unavailable records do not establish absence of a transaction. Individual capture logs identify exact sources and hashes.

This sidecar records provenance only. It does not independently validate every assertion in the artifact.
