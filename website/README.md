# LUNA holder briefing website

Portable source and the current generated HTML for the public briefing:
https://phoenix-foundation-irregularities.pfc.zone/

## Build and preview

Requires Python 3.10 or newer. No package installation, Node.js, account credentials or network access is required to rebuild.

```sh
python3 build.py
python3 verify.py
python3 -m http.server 5173 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:5173/. Deploy **only `dist/`** with any static website host.

The current vote snapshot is `refresh_20261030`. The build updates published checksums and artifact hashes in existing provenance sidecars while preserving their upstream descriptions. Incomplete refresh directories without a scenario are retained locally and excluded from the build.

The homepage and governance page summarize the two discussion proposals as revised on 16 November 2026. They link to the exact published revision and the latest discussion texts. This editorial update preserves the dated chain evidence; it does not refresh ballot or contract state. The current transition summary requires three approvals throughout, including all three directors while only three remain.

## Update the live site

See [DEPLOYMENT.md](DEPLOYMENT.md) for the existing Site identifier, a ready-to-use Codex publishing instruction, the authenticated Sites workflow, and verification steps. Building or previewing locally does not publish changes.

## Where to edit

Published checksum manifests cover evidence payloads and exclude provenance sidecars to avoid circular hashes. Sidecars retain their artifact hashes in the provenance register. The verifier checks the published checksum manifests.

- `build.py`: page content, navigation and metadata.
- `visuals.py`: responsive role diagrams and controlled timeline.
- `dist/site.css`, `dist/visuals.css`, `dist/site.js`: maintained styles and browser interactions; these are build inputs as well as published assets.
- `motion-controller.js`: canonical Diagram Design playback controller.
- `publication_editorial.py`: replaces archived commentary with neutral source guides and omits personal-allegation galleries.
- `publication_privacy.py`: removes surname and identity-disclosure material from publication, uses the public handle `0xPhilipp` in presentation labels, and regenerates readable copies and checksums.
- `dist/record/`: retained evidence and receipt datasets used by the build. Preserve this directory when rebuilding.
- `source-records/original-pages/`: preserved HTML inputs; never deploy this directory.
- `PRODUCT.md`, `DESIGN.md`, `diagram-style-guide.md`: editorial and design context.

`collect_sources.py` was used for initial collection. Do not run it as a build step; the retained inputs already support an offline build. It may overwrite publication safeguards if used without review.

## Editorial boundaries

This is a rewritten presentation of public records, not an independent audit of every transaction. Keep the four governance concerns clear and link them to evidence. Distinguish beneficiary participation from unilateral approval; A272's proposed configuration from its failed outcome; project receipts from personal profit; and dated page captures from proof that no work occurred. Include relevant explanations and uncertainties. No personal attacks, assertions about character or unsupported motives, harassment, identity research or calls for unwanted contact.

Use the public custom domain in metadata and copy-link controls. Do not add information identifying the site owner. Hosting-account configuration, Git history, credentials and machine-specific paths are intentionally excluded from this copy.

Fonts and Diagram Design license notices are retained with the assets. Before publishing a revision, rebuild, verify and inspect the affected pages at desktop and mobile widths.

## Contract control review — 16 November 2026

`/control/` compares 27 named contracts with approved grants and handover terms. New research is retained under `data/website/eris-control-20261116/`; the curated public subset is `source-records/control-20261116/`. Full forum threads and identifying metadata are excluded. Latest-state queries are sequential and do not establish an exhaustive asset inventory, private key custody, legal title, or abusive intent.
