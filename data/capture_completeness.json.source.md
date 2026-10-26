# Source and provenance

- **Artifact:** `data/capture_completeness.json`
- **SHA-256:** `48576081a4cb94e5c9785be6ab41d8c7b8cd288407717acf32f1f6cb12ca9f48`
- **Timestamp basis:** No original acquisition timestamp established; file mtime is not used as acquisition evidence.
- **Classification:** Derived dataset
- **Acquisition / transformation:** Local transformation using `analysis/verify_captures.py`.
- **Transformation:** `analysis/verify_captures.py`

## Immediate source(s)

- analysis/pipeline_utils.py
- data/phoenix/MB_prior_treasury_transactions.json
- data/phoenix/MB_current_treasury_transactions.json
- data/phoenix/Vini_treasury_transactions.json
- data/phoenix/Rose_treasury_transactions.json
- data/transfers/rebel_project_sender.json
- data/transfers/rebel_project_recipient.json
- data/transfers/rebel_orbital_sender.json
- data/transfers/rebel_orbital_recipient.json

## Upstream original source(s)

- analysis/pipeline_utils.py
- data/phoenix/MB_prior_treasury_transactions.json
- data/phoenix/MB_current_treasury_transactions.json
- data/phoenix/Vini_treasury_transactions.json
- data/phoenix/Rose_treasury_transactions.json
- data/transfers/rebel_project_sender.json
- data/transfers/rebel_project_recipient.json
- data/transfers/rebel_orbital_sender.json
- data/transfers/rebel_orbital_recipient.json

## Scope, limits, and notes

Reports saved responses against provider-reported totals; incomplete windows cannot support unbounded absence claims.

This sidecar records provenance only. It does not independently validate every assertion in the artifact.
