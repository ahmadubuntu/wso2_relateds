# AGENTS

WSO2 / APIM analytics notes and Kibana saved-object work around `https://wso2kib.charisma.tech`.

## Purpose

Operational workspace for WSO2 API Manager analytics (Kibana/Elastic) and related cluster logs. Feature work for dashboards is done via the Kibana Saved Objects API, not application source.

## Layout

- `plans/` — append-only plan history. Read the **latest** file before changing behavior.
- `scripts/` — operational CLIs against remote WSO2 APIM (no credentials in repo).
- `kibana/dashboards/` — JSON snapshots of dashboards created from this repo (no credentials).
- `lastWorkingDate/` — captured WSO2 MI pod logs (not the source of truth for dashboards).

## Configure / run

Kibana is remote. Create or update dashboards with session login to `/internal/security/login` (basic provider), then `POST /api/saved_objects/dashboard/{id}?overwrite=true`.

APIM Publisher (`https://apig-am.charisma.tech`, AM 4.2): use `scripts/apim_grant_scope.py` with env `WSO2_PRD_USER` / `WSO2_PRD_PASS`. Default dry-run; persist with `--apply`; gateway pickup needs `--deploy`.

Credentials live outside git (shell env / password manager). Never put passwords in `plans/` or `kibana/` or `scripts/`.

## Secrets

- Kibana user for agent work: `ahmad_agent` (role `kibana_admin`).
- APIM Publisher agent work: `WSO2_PRD_USER` / `WSO2_PRD_PASS` (env only).
- Passwords: **not in this repo**.
- Kibana role can manage Kibana objects but currently **cannot read** `apim_event*` in Elasticsearch. Charts stay empty / forbidden until a role with `read` on those indices is granted.

## Landmines

- Data view time field is `requestTimestamp`, not `@timestamp`. Time-series Lens charts must use `requestTimestamp` or they will not follow the dashboard time picker.
- User field used by existing APIM dashboards: `userName.keyword`.
- CharismaHelios ops currently use shared scope `admin`; adding another scope requires API-level shared-scope attach + per-operation scopes + revision deploy.
- Spec Kit (`.specify/`) present but constitution still template; ops scripts use `plans/` as source of truth for now.

## Plans

Convention: `plans/YYYY-MM-DD_HHMMSS_<slug>.md`. Never delete old plan files.

## Current focus

[APIM grant-scope script](plans/2026-09-29_015200_apim-grant-scope-script.md)
