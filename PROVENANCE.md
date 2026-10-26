# Provenance register

Every artifact under `data/`, `downloads/`, `repos/`, `website/source-records/original-pages/`, and `website/dist/record/` has a sibling `*.source.md` file.

Each sidecar identifies the immediate source and, where established, the upstream original chain/forum/GitHub record. It also records acquisition or transformation, timestamps, SHA-256, and limitations. `UPSTREAM_NOT_ESTABLISHED` means no source is inferred.

For the supplied packet, `data/source_index.json` is used to map preserved files to original URLs. The voting record and authority ledger additionally have operation-level upstream indexes.

Total artifacts with sidecars: **547**.
