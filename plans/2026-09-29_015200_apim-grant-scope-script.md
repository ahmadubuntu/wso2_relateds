# APIM grant-scope script (CharismaHelios / tester)

Date: 2026-09-29
Goal: Connect to `https://apig-am.charisma.tech` with `WSO2_PRD_USER` / `WSO2_PRD_PASS` and provide a reusable script to add a shared OAuth scope (e.g. `tester`) to specific or all operations of an API (default `CharismaHelios`).

Previous plan: `plans/2026-09-20_054021_cins-file-download-fix-applied.md`

## Decisions

- Auth: DCR (`/client-registration/v0.17/register`) + password grant (`/oauth2/token`) → Publisher API v4.
- Product is WSO2 API Manager **4.2.0**.
- `CharismaHelios` is a GraphQL API (`/helios`, PUBLISHED), id `c7fd2dad-b630-4436-8ad2-dace6ba7954d`, **20** `QUERY` operations, all currently scoped to `admin` only.
- Shared scope `tester` already exists (`e38cad81-2cbf-4f34-8b7d-2bf191ab28e4`, bindings `["tester"]`).
- Script default is **dry-run**. Persist with `--apply`. Gateway pickup needs `--deploy` (revision + deploy).
- Credentials stay in env vars only; never written to `plans/` or script defaults.

## Steps

1. [x] Probe AM host, confirm Publisher v4 + login
2. [x] Locate CharismaHelios + operation/scope shape
3. [x] Confirm shared scope `tester` exists
4. [x] Ship `scripts/apim_grant_scope.py`
5. [ ] User runs `--apply --deploy` when ready (not auto-applied in this session)

## Key commands

```bash
export WSO2_PRD_USER=...
export WSO2_PRD_PASS=...

# inspect
python3 scripts/apim_grant_scope.py --api CharismaHelios --list

# dry-run add tester to all ops
python3 scripts/apim_grant_scope.py --api CharismaHelios --scope tester --ops all

# apply + deploy
python3 scripts/apim_grant_scope.py --api CharismaHelios --scope tester --ops all --apply --deploy
```

## Constraints

- Production APIM: do not apply without explicit user intent.
- After `--apply` without `--deploy`, runtime gateway still uses previous revision.
- Revision cap is typically 5; script deletes oldest undeployed revision when needed.

## Open questions

- None for script delivery. User chooses when to `--apply --deploy`.
