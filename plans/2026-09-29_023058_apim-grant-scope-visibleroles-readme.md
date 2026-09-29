# APIM grant-scope v0.2 — visibleRoles + README

Date: 2026-09-29
Goal: Preserve working v0.1.0 on dual-git, then ship v0.2 that documents the script in README and auto-syncs Developer Portal visibility Roles (`visibleRoles`) when granting a scope.

Previous plan: `plans/2026-09-29_015200_apim-grant-scope-script.md`

## Decisions

- v0.1.0 tagged and pushed to GitHub + Azure (`main`) before further edits.
- v0.2 lives on branch `feature/apim-grant-scope-visible-roles`.
- Default: add scope name to `visibleRoles` (same string as OAuth scope). Opt out with `--no-visible-role`.
- Do **not** auto-flip `visibility` from PUBLIC/PRIVATE to RESTRICTED; warn instead.
- README is Persian (operator-facing).

## Steps

1. [x] Dual-git bootstrap + push `v0.1.0`
2. [x] Script: `ensure_visible_role` + `--no-visible-role`
3. [x] README guide (ops + visibility Roles UI path)
4. [x] PR merged: https://github.com/ahmadubuntu/wso2_relateds/pull/1
5. [x] Tag `v0.2.0` on `main` + dual-push (GitHub + Azure)

## Key UI

Portal Configurations → Basic Info → Developer portal visibility Roles  
https://apig-am.charisma.tech/publisher/apis/c7fd2dad-b630-4436-8ad2-dace6ba7954d/configuration

## Constraints

- Secrets only via env.
- Dual push every time (`AZDO_PAT_DATAPLATFORM`).
