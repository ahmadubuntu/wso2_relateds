# Kibana dashboard: APIM top users over time

Date: 2026-09-09
Goal: On https://wso2kib.charisma.tech, using data view `apim_event*`, show which API users sent the most requests over time (vertical bar + breakdown filters).

## Decisions

- Kibana 8.12.1, space `default`.
- Data view: `apim_event*` (`0d83f380-6eda-11ec-9dad-f7e4782fdbce`). Time field: `requestTimestamp`.
- User dimension: `userName.keyword` (same as existing “API Users” dashboard). Extra filters: `apiName.keyword`, `applicationName.keyword`.
- Chart: Lens XY **stacked vertical bar** (`bar_stacked`) — time on X, request count on Y, split by top 10 users. Stacked bars stay readable with a user breakdown; grouped bars with 10 series overlap.
- Dashboard-level **Options list** controls (Kibana Control Group) for Username / API / Application.
- Supporting panels: total requests, unique users, horizontal ranking bar, datatable.
- Login username is `ahmad_agent` (the typed `agmad_agent` is a typo). Do **not** store the password in this repo.
- Role `kibana_admin` can create saved objects but **cannot search** `apim_event*` (`indices:data/read/search` unauthorized). Dashboard still publishes; data appears only for users with index `read`.
- Spec Kit is **not** initialized in this workspace. This is an ops/Kibana saved-object change, not app source.

## Steps

1. Authenticate to Kibana form login (`/internal/security/login`, provider `basic`).
2. Create one dashboard saved object with inline Lens panels + `controlGroupInput`.
3. Return the dashboard URL.
4. Record definition under `kibana/dashboards/` (no secrets) for handoff.

## Constraints

- Never commit credentials.
- Do not overwrite the existing “API Users” dashboard (`499bbdd0-fd05-11ec-aaa3-29ae7b5675fa`).
- Default time range: last 7 days (`now-7d` → `now`), `timeRestore: true`.
