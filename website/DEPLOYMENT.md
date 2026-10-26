# Update the public website

The existing site is hosted with the Sites plugin at:
https://phoenix-foundation-irregularities.pfc.zone/

Its existing Site project ID is `appgprj_6adf4698221c81918dd746d55f98bd5c`. This identifies the deployment, not an authentication credential. Reuse this Site; do not create a second one or change the DNS records for ordinary content updates.

## Build changes locally

From `website/`:

```sh
python3 build.py
python3 verify.py
python3 -m http.server 5173 --bind 127.0.0.1 --directory dist
```

Check the affected pages at http://127.0.0.1:5173/. The build and preview commands do not update the live website. Copying files into this audit directory or pushing an unrelated Git repository also does not publish it.

## Publish through Codex and Sites

Use Codex with the Sites plugin connected to an account that can edit the existing Site. Give it this instruction:

> Publish the website in this audit pack's `website/` directory to the existing public Site at https://phoenix-foundation-irregularities.pfc.zone/. Follow AGENTS.md and website/DEPLOYMENT.md. Reuse the existing Site project ID, preserve public access and the custom domain, build and verify, publish only dist/, and confirm the custom-domain URL loads. Keep owner information and credentials out of the copied files and public output.

The publishing agent should:

1. Read the installed Sites skill and call `sites_get_site` with the project ID above. Confirm that the Site and public audience match. Do not replace its identity or access settings.
2. Obtain a fresh `sites_create_source_repository_write_credential` for that same project. Keep credentials in session memory; never print them, commit them, put them in shell arguments, or save them in this directory.
3. Open the existing remote source with the Sites `site-workflow.mjs` helper, using the installed plugin's actual path. Open into a separate private working checkout if this portable copy has no Site Git checkout. Pass the credential as newline-terminated JSON through the helper's hidden stdin. Retain the complete opening result.
4. Compare the remote source with this copy before applying edits. Preserve newer remote work and resolve differences explicitly. Copy the intended site source and build inputs into the managed checkout, without importing unrelated audit files or owner information. Preserve its existing `.openai/hosting.json`; its static output directory is `dist`. Keep that hosting configuration in the private working checkout, outside the distributable audit copy and public output.
5. Run `python3 build.py` and `python3 verify.py` in the publishing checkout. Inspect affected pages when layout or behavior changed. Preserve the privacy/editorial guards and original-source input boundaries. Do not publish the entire source directory.
6. Package with the same Sites helper, passing the credential, the complete opening result as `source`, remaining check commands (or `[]` when already completed), and a temporary absolute `archivePath`. The helper prepares the exact commit, pushes to the Site's source repository, and packages its configured static assets. Retain its returned project ID, full commit SHA and archive path. Do not manually substitute a different commit or archive.
7. Call `sites_save_site_version` with those exact returned values, then `sites_deploy_site_version` with the saved version ID. Preserve public access. For a nonterminal deployment, inspect status until success or a concrete failure; do not report a pending deployment as live.
8. Verify the changed content at the custom-domain URL over HTTPS. Check that metadata and copy-link controls still use the custom domain. Report the published URL and any remaining verification limits.

The local Python build needs no extra packages. The Sites publishing helper additionally needs Node.js, the installed Sites plugin and authenticated network access. If the connector is unavailable or the account lacks access, retain the verified local output and report that publishing is blocked; do not create a replacement Site as a workaround.

## Deployment privacy and recovery

Publish only `dist/`. Keep original HTML inputs, audit reports, account configuration, Git history, credentials and local paths out of served files. Do not disable the privacy or editorial transformations to make a deployment pass. Review changes involving amounts or source records separately from styling changes.

Before replacing a live version, retain its saved version ID in the private operator record so it can be redeployed if needed. Saved Site versions provide the publishing history; this portable audit directory intentionally contains no account credentials or private operator history.
