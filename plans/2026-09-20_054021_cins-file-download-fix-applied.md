# CharismaInsurance File/download — fix applied

Date: 2026-09-20  
Previous plan: `plans/2026-09-20_053513_cins-file-download-404-bidi.md`

## Done

1. Logged in Publisher with `WSO2_PRD_USER` / `WSO2_PRD_PASS` (Basic).
2. Cleaned OpenAPI: path `/chr/fl/File/download`, query `FileId` (stripped U+202A/B/C).
3. `PUT .../swagger` multipart `apiDefinition` → 200.
4. Deleted unused Revision 2 & 3 (slot limit).
5. Created **Revision 7** (`446357d1-eed7-4a5f-a575-f8d103d48e40`) and deployed to **Default** / `apig-gw.charisma.tech`.

## Verify

| URL | Status |
|-----|--------|
| `GET /cins/v1.0/chr/fl/File/download?FileId=58cc3ef9-...` | **200** (`%PDF-1.5`) |
| Same path with bidi percent-encoding | 404 (expected) |
| `GetReportFinancial` | 200 |

## Client note

Frontend / Try-out must call **clean** ASCII URL only. Old bookmarks with `%E2%80%AC` etc. stay broken.
