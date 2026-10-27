# Source and provenance

- **Artifact:** `data/leads/query_manifest.json`
- **SHA-256:** `be4e46cb37523e4ab30bab876951f9101438988d1c3894bc9cc765931c791b45`
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
