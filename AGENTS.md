# Agent instructions

## Scope and existing audit material

This directory contains an existing audit pack and a separate website in `website/`. Preserve `REPORT.md`, `data/`, `analysis/`, `downloads/`, `raw/`, `repos/` and existing integrity files unless the user explicitly requests changes. Do not silently treat newer audit material as independently verified website copy.

## Website build

Work from `website/`. Read its `PRODUCT.md`, `DESIGN.md` and `README.md` before editing. Python 3.10+ and the standard library are sufficient:

```sh
python3 build.py
python3 verify.py
python3 -m http.server 5173 --bind 127.0.0.1 --directory dist
```

Deploy only `website/dist/`. Preserve the evidence under `dist/record/`; it is also a build input. Edit page content in `build.py`, diagrams in `visuals.py`, and maintained styles/interactions in `dist/site.css`, `dist/visuals.css`, `dist/site.js`. Keep the canonical `motion-controller.js` intact. Do not run `collect_sources.py` merely to rebuild. Run the build and verifier after changes; inspect affected diagrams and copy at desktop/mobile widths when layout changes.

## Publishing

For requests to update the public website, follow `website/DEPLOYMENT.md`. Reuse the existing Sites project and custom domain, preserve public access, and publish only the verified `dist/` output. Local copies and unrelated Git pushes do not deploy the live Site. Keep credentials and hosting-account configuration in a separate private publishing checkout.

## Privacy and public identity

Never add the owner's name, account identifier, email, local filesystem paths, screenshots containing account details, credentials, tokens, Git authentication configuration, or chat/session metadata to the website or distributable build inputs. Use relative paths and the public custom domain in documentation and metadata. Do not copy `.git`, `.openai`, `.env*`, cache files or private deployment configuration into distributable assets. Keep original-source HTML out of the public directory.

Use `0xphilipp` in authored page copy and diagrams. Do not add surnames, identity-disclosure sections or links whose purpose is personal identification. Raw transaction data may retain relevant original public labels. Preserve the privacy/editorial transformations in the build; do not restore omitted material by copying the original site over the published output.

## Evidence and editorial standards

Maintain calm, evidence-focused scrutiny of documented decisions and procedures. No character judgments, personal attacks, unsupported claims of intent or dishonesty, harassment, private-identity research or invitations to unwanted contact. Separate facts, interpretations and unanswered questions, and retain relevant responses and uncertainty.

Keep four concerns clear: beneficiary participation in payment approvals; authority retained beyond stated handover dates; verifiable milestone acceptance; and A272's proposed concentration of approval power. State that other directors approved Estima's original grant, the Superbolt example had three YES votes, A272 failed, and timing or voting agreement alone does not establish motive. Do not equate gross project funding with personal profit or a later page capture with proof that no work occurred. Preserve amounts, dates, transaction references, overlap exclusions and paid/conditional distinctions. Do not assert the briefing independently audits every transaction.

## GitHub authentication

Do not infer a remote Git push from a local file-copy request. For every authenticated GitHub CLI operation, retrieve the token for the repository-authorized account directly into that command's environment:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user <authorized-account>)" gh <command>
```

Replace the placeholder with the authorized account. Never use `gh auth switch`, print tokens, write them to files, enable tracing around retrieval, or substitute another account. If token retrieval fails or is empty, stop before the GitHub operation and report it.
