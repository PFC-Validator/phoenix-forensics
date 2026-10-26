# Analysis-pipeline review remediation

Response to the 26 October 2026 adversarial review of the aggregation, analysis and verification pipeline. The website was outside that review's scope.

## Remediated in code

- **F17 — silent amount loss.** Cosmos amounts now use a fail-closed parser. Multi-coin events produce multiple rows; malformed amounts raise. Display conversion occurs only for registered denominations, and unknown denominations remain in base units. Unit tests cover these cases.
- **F18 — bounded-negative wording.** Verification output now says “preserved captures (bounded)” and the Think Tank result labels its transfer union as incomplete rather than a census.
- **F16 — typed-in derived figures.** Director windows, combined ballots, Rose's OTC amounts, ERIS weights/records, native ballots, Rebel's invoice and Orbital delegation are computed from preserved source records. `RECENT_CUTOFF` is shared.
- **F8 — packet hashes.** Verification rejects unregistered packet-source mismatches. The one pre-existing `AUTH-S01` mismatch is checked against the packet's own retained-artifact hash and reported separately: one registered, zero unregistered.
- **F14/F9 — sidecar churn and timestamp basis.** Generation time was removed from individual sidecars; the top-level register retains it. Existing timestamps are preserved, and new files distinguish file mtime from acquisition time. Repeated generation is byte-stable.
- **F4 — verifier-generated inputs.** Upstream-index generation moved to `analysis/generate_upstream_indexes.py`; ordinary provenance generation and verification do not refresh those inputs.
- **F19 — lossy exports.** Native vote export retains every option in split ballots. Transaction-message extraction prefers embedded messages and rejects unsafe unequal `txs`/`tx_responses` pairing.
- **F15/F13 — provenance boundaries.** `downloads/index.html` is now covered. README files document build → provenance → verify ordering.
- **F12 — referenced versus sourced.** Generic website-record rules no longer promote arbitrary URLs in artifact content to upstream sources.

## Capture and trust improvements

- `analysis/verify_captures.py` reports saved/total/missing counts. `--require-complete` fails on incomplete wallet histories.
- `analysis/refresh_captures.py` implements bounded, duplicate-checked, atomic legacy-page refresh for network-enabled runs and writes ordered page-source manifests.
- `data/capture_completeness.json` makes the current incomplete windows machine-readable.
- MB prior-wallet `message.sender`, `transfer.sender` and `transfer.recipient` counter-queries all returned zero. This is preserved as a bounded indexer result, not “never acted.”
- Two-provider anchor checks found exact matches for ampLUNA-hub and ICS20 configuration. Sequential live-tally reads differed slightly and remain separately labelled.
- `analysis/refetch_anchors.py` repeats the small two-provider comparison without rewriting evidence.

## Still open

1. **F1 — five truncated wallet histories.** The paginator is implemented, but the current environment cannot complete the network refresh. Rose, MB-current and Vini remain oldest-first windows; Rebel project sender/recipient remain newest-first windows. Do not use them for lifetime comparisons or unbounded absence claims. The completed Treasury-outbound and validator-payment captures are unaffected.
2. **F10 — semantic 4853 merge.** The 83-ballot file is now explicitly classified as a derived merged dataset. A byte-for-byte refetch is still required to replace it with a raw primary response.
3. **F3/F7 — broader independent replay.** Small anchor endpoints now have a second-LCD check, but the complete A1–A300 manifest has not been replayed against two providers.
4. **F5 — vintage mixing.** Per-file vintage notes remain necessary; no claim is made that every artifact has one capture time.
5. **F11 — low-priority rule cleanup.** Provenance-rule deduplication can be simplified further; it does not change evidence values.

## Verification

Run the documented sequence in `README.md`, plus:

```sh
python3 analysis/test_pipeline.py
python3 analysis/verify_captures.py
python3 analysis/verify_captures.py --require-complete  # expected to fail until F1 is refreshed
python3 analysis/verify_anchor_crosschecks.py
```

The `--require-complete` failure is intentional and reports the incomplete wallet census rather than silently passing it. The review table lists five truncated files; its sixth row, `rebel_orbital_sender.json`, is complete.


## Round 2 follow-up

- **F21 closed with bounded evidence.** `data/phoenix/MB_prior_counter_queries.json` preserves zero results for `message.sender`, `transfer.sender` and `transfer.recipient`. This resolves the need for a counter-query; it does not prove the wallet never acted.
- **F20 closed.** `analysis/payment_summary.py` now reproduces every pre-existing summary field exactly from completed transfer/action captures. `analysis/counterparty_flows.py` adds the contract-counterparty classification.
- **REPORT drift closed.** The vote-change paragraph now distinguishes 79 ballots in the earlier raw capture from 83 in the refreshed documented merge.
- **`terra1tuuwm8…` classified.** Fresh metadata confirms `ve3-bribe-manager`. Its receipts are `claim_bribes` voting incentives, not an unidentified personal counterparty. The round-two combined totals mix assets: preserved flows are 8,809.069532 LUNA + 69,095.412349 FUEL + 19.075632 USDC, with October values 2,431.438843 LUNA + 48,995.522472 FUEL + 11.011553 USDC. They are intentionally reported separately.
- **F1 remains open.** The five truncated histories still require network pagination and a refreshed absence graph.
