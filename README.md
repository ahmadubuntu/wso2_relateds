# wso2_relateds

یادداشت‌ها و اسکریپت‌های عملیاتی برای WSO2 API Manager / analytics در محیط Charisma.

- Publisher: `https://apig-am.charisma.tech`
- Gateway: `https://apig-gw.charisma.tech`
- نسخهٔ اسکریپت scope: ببین تگ‌های `v0.1.0` (فقط operation scope) و `v0.2.0` (به‌علاوه DevPortal visibility role)

## Dual git

| Remote | URL |
|--------|-----|
| GitHub `origin` | https://github.com/ahmadubuntu/wso2_relateds |
| Azure `azure` | https://azure.charisma.tech/DataPlatform/DataPlatform/_git/wso2_relateds |

هر push باید به **هر دو** remote برود. برای Azure از `AZDO_PAT_DATAPLATFORM` با الگوی `http.extraHeader` استفاده کن (جزئیات در `.cursor/rules/azure-devops.mdc`).

## اسکریپت: اعطای scope به operationهای یک API

فایل: [`scripts/apim_grant_scope.py`](scripts/apim_grant_scope.py)

روی Publisher REST API v4 (AM 4.2) لاگین می‌کند (DCR + password grant) و یک **shared scope** را به operationهای یک API اضافه می‌کند.

### پیش‌نیاز

```bash
export WSO2_PRD_USER=...
export WSO2_PRD_PASS=...
# اختیاری:
# export WSO2_PRD_BASE=https://apig-am.charisma.tech
```

Shared scope باید از قبل در Publisher وجود داشته باشد (مثلاً `tester`, `admin`).

### سه کار که اسکریپت انجام می‌دهد

1. **API-level scopes** — اگر scope هنوز به API وصل نباشد، shared scope را attach می‌کند.
2. **Per-operation scopes** — نام scope را به لیست `scopes` هر operation انتخاب‌شده اضافه می‌کند (بدون حذف scopeهای قبلی مثل `admin`).
3. **Developer Portal visibility Roles** (`visibleRoles`) — به‌صورت پیش‌فرض همان نام scope را به نقش‌های visibility پرتال اضافه می‌کند.

نکتهٔ مهم (UI معادل):

Publisher → API → **Portal Configurations** → **Basic Info** → **Developer portal visibility Roles**

وقتی visibility روی `RESTRICTED` است، اگر role مربوط به scope را اینجا نگذاری، کاربر آن role حتی اگر روی operationها scope داشته باشد، API/کالکشن را در لیست DevPortal خودش **نمی‌بیند**.

مثال UI برای CharismaHelios:

https://apig-am.charisma.tech/publisher/apis/c7fd2dad-b630-4436-8ad2-dace6ba7954d/configuration

برای رد کردن این sync: `--no-visible-role`.

### دستورها

```bash
# لیست operationها + scopes + visibility
python3 scripts/apim_grant_scope.py --api CharismaHelios --list

# dry-run (پیش‌فرض): افزودن tester به همه operationها + visibleRoles
python3 scripts/apim_grant_scope.py --api CharismaHelios --scope tester --ops all

# فقط چند operation (target یا VERB:target)
python3 scripts/apim_grant_scope.py --api CharismaHelios --scope tester \
  --ops fund,funds,QUERY:instrument

# اعمال روی Publisher
python3 scripts/apim_grant_scope.py --api CharismaHelios --scope tester --ops all --apply

# اعمال + revision + deploy روی gateway
python3 scripts/apim_grant_scope.py --api CharismaHelios --scope tester --ops all \
  --apply --deploy
```

`--apply` بدون `--deploy` فقط تعریف API در Publisher را عوض می‌کند؛ runtime gateway تا deploy روی revision قبلی می‌ماند.

### مثال واقعی: CharismaHelios

- نام API: `CharismaHelios` (GraphQL، context `/helios`)
- قبلاً همهٔ operationها فقط `admin` داشتند
- افزودن `tester` به همه + `visibleRoles` تا کاربران role/`tester` کالکشن را در DevPortal ببینند

## بقیهٔ محتوا

- `plans/` — تاریخچهٔ پلن‌ها (append-only؛ آخرین فایل را قبل از تغییر رفتار بخوان)
- `kibana/dashboards/` — اسنپ‌شات داشبوردها
- `lastWorkingDate/` — یادداشت‌های تشخیصی MI (لاگ‌های حجیم در git نیستند)
- `AGENTS.md` — راهنمای ایجنت / landmineها

## Secrets

رمزها و PAT داخل ریپو نیستند. فقط env:

- `WSO2_PRD_USER` / `WSO2_PRD_PASS` — Publisher
- `AZDO_PAT_DATAPLATFORM` — push به Azure DevOps DataPlatform
