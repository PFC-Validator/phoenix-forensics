# LUNA holder briefing website

Portable source and the current generated HTML for the public briefing:
https://phoenix-foundation-irregularities.pfc.zone/

## Build and preview

Requires Python 3.10 or newer. No package installation, Node.js, account credentials or network access is required to rebuild.

```sh
python3 build.py
cd ..
python3 analysis/generate_provenance.py
cd website
python3 verify.py
python3 -m http.server 5173 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:5173/. Deploy **only `dist/`** with any static website host.

## Update the live site

See [DEPLOYMENT.md](DEPLOYMENT.md) for the existing Site identifier, a ready-to-use Codex publishing instruction, the authenticated Sites workflow, and verification steps. Building or previewing locally does not publish changes.

## Where to edit

Published checksum manifests cover evidence payloads and exclude provenance sidecars to avoid circular hashes. Sidecars retain their artifact hashes in the provenance register. The verifier checks published manifests after provenance generation.

- `build.py`: page content, navigation and metadata.
- `visuals.py`: responsive role diagrams and controlled timeline.
- `dist/site.css`, `dist/visuals.css`, `dist/site.js`: maintained styles and browser interactions; these are build inputs as well as published assets.
- `motion-controller.js`: canonical Diagram Design playback controller.
- `publication_editorial.py`: replaces archived commentary with neutral source guides and omits personal-allegation galleries.
- `publication_privacy.py`: removes surname and identity-disclosure material from publication, uses the public handle `0xphilipp` in presentation labels, and regenerates readable copies and checksums.
- `dist/record/`: retained evidence and receipt datasets used by the build. Preserve this directory when rebuilding.
- `source-records/original-pages/`: preserved HTML inputs; never deploy this directory.
- `PRODUCT.md`, `DESIGN.md`, `diagram-style-guide.md`: editorial and design context.

`collect_sources.py` was used for initial collection. Do not run it as a build step; the retained inputs already support an offline build. It may overwrite publication safeguards if used without review.

## Editorial boundaries

This is a rewritten presentation of public records, not an independent audit of every transaction. Keep the four governance concerns clear and link them to evidence. Distinguish beneficiary participation from unilateral approval; A272's proposed configuration from its failed outcome; project receipts from personal profit; and dated page captures from proof that no work occurred. Include relevant explanations and uncertainties. No personal attacks, assertions about character or unsupported motives, harassment, identity research or calls for unwanted contact.

Use the public custom domain in metadata and copy-link controls. Do not add information identifying the site owner. Hosting-account configuration, Git history, credentials and machine-specific paths are intentionally excluded from this copy.

Fonts and Diagram Design license notices are retained with the assets. Before publishing a revision, rebuild, generate provenance, verify and inspect the affected pages at desktop and mobile widths.
