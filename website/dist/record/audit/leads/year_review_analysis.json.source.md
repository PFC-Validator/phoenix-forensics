# Source and provenance

- **Artifact:** `data/leads/year_review_analysis.json`
- **SHA-256:** `53b9fa10fa1d83e1555b0b50f5a109771687e458ade0dd4aafd4aaa81dffa9c3`
- **Timestamp basis:** No original acquisition timestamp established; file mtime is not used as acquisition evidence.
- **Classification:** Derived dataset
- **Acquisition / transformation:** Local transformation using `analysis/integrate_lead_evidence.py`.
- **Transformation:** `analysis/integrate_lead_evidence.py`

## Immediate source(s)

- data/leads/queries/review_creda_metrics.json
- data/leads/queries/review_creda_portfolio_operations.json
- data/leads/queries/review_creda_portfolio_board.json
- data/leads/queries/review_creda_portfolio_tla_single.json
- data/leads/queries/review_treasury_action_28.json
- data/leads/queries/review_treasury_action_72.json
- data/leads/queries/review_treasury_action_109.json
- data/leads/queries/review_treasury_action_110.json
- https://forum.cosmos.network/t/aadao-wind-down-oversight-updates-and-reports/15913/22

## Upstream original source(s)

- data/leads/queries/review_creda_metrics.json
- data/leads/queries/review_creda_portfolio_operations.json
- data/leads/queries/review_creda_portfolio_board.json
- data/leads/queries/review_creda_portfolio_tla_single.json
- data/leads/queries/review_treasury_action_28.json
- data/leads/queries/review_treasury_action_72.json
- data/leads/queries/review_treasury_action_109.json
- data/leads/queries/review_treasury_action_110.json
- https://forum.cosmos.network/t/aadao-wind-down-oversight-updates-and-reports/15913/22

## Scope, limits, and notes

Current query arithmetic; no common confirmed historical height. External Votion payment/completion are explicitly funder-reported from the public AADAO report, not independently replayed settlement transactions. Funding does not establish causal attribution, total costs or personal profit.

This sidecar records provenance only. It does not independently validate every assertion in the artifact.
