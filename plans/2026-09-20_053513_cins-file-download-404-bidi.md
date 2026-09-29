# CharismaInsurance File/download → 404 (bidirectional Unicode in resource)

Date: 2026-09-20  
Goal: Explain gateway `404 No matching resource found` for `/cins/v1.0/chr/fl/File/download`.

Previous plan: `plans/2026-09-09_080908_kibana-top-users-dashboard.md` (unrelated Kibana work).

## Verdict

Root cause is **not auth**. Same Internal-Key works on other resources of the same API.  
Resource path and query param in Publisher were saved with **invisible Unicode bidirectional marks** (typical RTL paste). Synapse then cannot match the request → runtime 404.

## Evidence (logged in with `WSO2_PRD_USER` / `WSO2_PRD_PASS`)

- Publisher Basic auth OK; API `CharismaInsurance` id `80d8305d-e568-4ffa-9350-f91038633a20`, context `/cins`, version `v1.0`.
- Generated fresh Internal-Key via `POST /api/am/publisher/v4/apis/{id}/generate-key`.
- Gateway control: `GET /cins/v1.0/chr/cs/report/GetReportFinancial` → **200**.
- Gateway download (clean ASCII) → **404** same message.
- Gateway download (percent-encoded bidi, as browser curl) → **404** same message.

### Corrupted definition in Publisher / swagger

| Field | Stored value (repr) | Bad codepoints |
|-------|---------------------|----------------|
| operation target / swagger path | `'/chr/fl/File/download\u202c\u202c'` | U+202C ×2 POP DIRECTIONAL FORMATTING |
| query param name | `'\u202b\u202aFileId\u202c\u202c'` | U+202B, U+202A, U+202C ×2 |

Other three operations on this API are clean ASCII and work.

Browser curl URL decoded to the **same** corrupted path/param names — client copied what swagger/Publisher shows.

## Fix (Publisher — do not leave bidi in path)

1. Open API **CharismaInsurance** in Publisher.
2. Change resource to clean path: `/chr/fl/File/download`.
3. Change query param to clean name: `FileId`.
4. Save and **Deploy** / republish to gateway.
5. Call:  
   `https://apig-gw.charisma.tech/cins/v1.0/chr/fl/File/download?FileId=<uuid>`  
   with valid `Internal-Key` or app token.

Optional: re-import cleaned OpenAPI so swagger params are ASCII-only.

## Constraints

- Do not commit credentials; use env `WSO2_PRD_USER` / `WSO2_PRD_PASS` only.
- Production API change needs explicit operator approval before Publisher update via API.

## Open

- Whether to auto-PATCH Publisher swagger via agent (await user OK).
