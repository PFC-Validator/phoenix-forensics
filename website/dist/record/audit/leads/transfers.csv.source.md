# Source and provenance

- **Artifact:** `data/leads/transfers.csv`
- **SHA-256:** `955b245af8c034bf6a9c2bd1145a98d8d66aa0cd7a0b78127f370a83715d6dd4`
- **Timestamp basis:** No original acquisition timestamp established; file mtime is not used as acquisition evidence.
- **Classification:** Derived dataset
- **Acquisition / transformation:** Local transformation using `analysis/integrate_lead_evidence.py`.
- **Transformation:** `analysis/integrate_lead_evidence.py`

## Immediate source(s)

- data/leads/capture_manifest.json
- data/leads/query_manifest.json
- data/leads/rpc_manifest.json
- data/leads/evm_metadata_manifest.json

## Upstream original source(s)

- data/leads/capture_manifest.json
- data/leads/query_manifest.json
- data/leads/rpc_manifest.json
- data/leads/evm_metadata_manifest.json

## Scope, limits, and notes

Supplemental records only; earlier aggregate datasets are not incremented. Transfers, fee-share annotations, unknown units and unquantified events remain distinct. Findings are bounded by their explicit limits. No identity attribution added.

This sidecar records provenance only. It does not independently validate every assertion in the artifact.
