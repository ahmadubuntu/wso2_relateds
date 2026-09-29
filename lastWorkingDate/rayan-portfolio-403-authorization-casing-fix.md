# راهنمای رفع 403 سرویس `lastWorkingDate` (Rayan Portfolio / WSO2 MI)

## خلاصه مشکل

سرویس `GET /rp/lastWorkingDate` (API: `rportfolio`) روی Gateway:

- **دفعه اول** (معمولاً وقتی توکن Rayan در Redis نیست و authenticate می‌شود) پاسخ درست برمی‌گرداند (مثلاً `"1405/03/29"`).
- **دفعه دوم** (وقتی توکن از Redis خوانده می‌شود) از سمت آپ‌استریم Rayan خطای **HTTP 403** می‌دهد.

پیام Rayan:

```json
{
  "message": "جهت استفاده از خدمات باید توکن امنیتی ارسال شود",
  "errorId": 10000002,
  "description": "در درخواست ارسالی توکن امنیتی یافت نشد"
}
```

**مهم:** این 403 از WSO2 API Manager / OAuth کلاینت نیست. درخواست از گتوی رد شده و به `https://ag.rayanbroker.ir/...` رسیده؛ خود Rayan می‌گوید توکن امنیتی را در درخواست ندیده است.

رفتار مشابه روی **Production** و **Staging** مشاهده شد.

---

## علت ریشه‌ای (Root Cause)

Rayan هدر Authorization را **case-sensitive** پردازش می‌کند:

| هدر ارسالی به Rayan | نتیجه |
|---------------------|--------|
| `Authorization: Bearer <token>` | **200 OK** |
| `authorization: Bearer <token>` (حروف کوچک) | **403** با `errorId: 10000002` |

### چرا دفعه اول OK و دفعه دوم 403؟

در mediation دو مسیر وجود دارد:

1. **Cache miss (توکن در Redis نیست)**  
   MI اول به `auth-ag.rayanbroker.ir` authenticate می‌کند. بعد از چند call داخلی، هدرهای کلاینت معمولاً از روی پیام پاک/جایگزین شده‌اند. سپس هدر تازه با نام درست `Authorization` ست می‌شود → **200**.

2. **Cache hit (توکن در Redis هست)**  
   MI همان پیام ورودی کلاینت را نگه می‌دارد. اگر کلاینت (مثلاً DevPortal / مرورگر از طریق Ingress) هدر را به صورت `authorization` (lowercase) فرستاده باشد، Synapse با این خط:

   ```xml
   <header expression="fn:concat('Bearer ', get-property('TokenValue_redis'))"
           name="Authorization" scope="transport"/>
   ```

   معمولاً **مقدار همان هدر موجود را عوض می‌کند** و **نام lowercase را نگه می‌دارد**. روی wire به Rayan می‌رود: `authorization: Bearer <rayan-token>` → Rayan توکن را «پیدا نمی‌کند» → **403**.

توکن Redis در تست‌ها سالم بود؛ همان مقدار با `Authorization` درست کار می‌کرد و با `authorization` کوچک شکست می‌خورد.

---

## اثبات با curl (مستقیم به Rayan)

از ماشینی که به `ag.rayanbroker.ir` دسترسی دارد (مثلاً داخل Pod MI استیج)، با یک توکن معتبر Rayan:

```bash
export TOKEN='...'   # توکن Rayan (نه توکن WSO2)
URL='https://ag.rayanbroker.ir/api/v1/portfolio/lastWorkingDate?dsCode=10856'
```

### موفق

```bash
curl -sS -w '\nHTTP %{http_code}\n' "$URL" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
```

انتظار: **HTTP 200** و بدنه شبیه `"1405/03/29"`.

### ناموفق (بازتولید باگ)

```bash
curl -sS -w '\nHTTP %{http_code}\n' "$URL" \
  -H "authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
```

انتظار: **HTTP 403** و `errorId: 10000002`.

سایر هدرهای مرورگر (`Origin`, `Referer`, `sec-fetch-*`, `X-Forwarded-*`, `X-JWT-Assertion`, …) به‌تنهایی در تست ایزوله باعث این 403 نشدند؛ **مقصر قطعی، case نام هدر Authorization است.**

نمونه اجرای تست از داخل کلاستر Staging:

```bash
kubectl exec -n wso2 deploy/wso2am-pattern-1-mi-rayan-deployment \
  -c wso2micro-integrator -- \
  curl -sS -w '\nHTTP %{http_code}\n' "$URL" \
  -H "authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
```

---

## ریپو و برنچ

| مورد | مقدار |
|------|--------|
| Azure DevOps | `DataPlatform` / `DataPlatform` |
| ریپو | `wso2-integration-rayan_portfolio` |
| برنچ بررسی‌شده | `dev` |
| URL | https://azure.charisma.tech/DataPlatform/DataPlatform/_git/wso2-integration-rayan_portfolio?version=GBdev |

---

## محل دقیق فیکس

### فایل اصلی (باید تغییر کند)

`src/main/wso2mi/artifacts/templates/rportfolioResourceCallSEQT.xml`

این template جایی است که قبل از call به Rayan، Bearer ست می‌شود. تقریباً همه resourceهای API (از جمله `/lastWorkingDate`) از مسیر زیر به آن می‌رسند:

```text
rportfolio.xml  (resource)
  → rportfolioSetTokenAndCallSEQT
    → rportfolioResourceCallSEQT   ← فیکس اینجاست
```

قطعه فعلی (مشکل‌دار):

```xml
<header expression="fn:concat('Bearer ', get-property('TokenValue_redis'))"
        name="Authorization" scope="transport"/>
```

### تغییر پیشنهادی

**بلافاصله قبل از set کردن Bearer**، هدرهای قبلی Authorization را remove کنید، بعد دوباره با نام درست set کنید:

```xml
<!-- Ensure Rayan sees canonical Authorization (case-sensitive upstream) -->
<header action="remove" name="Authorization" scope="transport"/>
<header action="remove" name="authorization" scope="transport"/>
<header expression="fn:concat('Bearer ', get-property('TokenValue_redis'))"
        name="Authorization" scope="transport"/>
```

اگر در نسخه Synapse/MI شما `header action="remove"` برای نام case-insensitive عمل می‌کند، یک remove کافی است؛ برای اطمینان، هر دو نام در بالا آمده است.

### اختیاری (سخت‌گیرانه / دفاعی)

قبل از call به Rayan می‌توان هدرهای کلاینت که نباید به آپ‌استریم بروند را هم پاک کرد، مثلاً:

- `Origin`, `Referer`
- `sec-fetch-mode`, `sec-fetch-site`, `sec-fetch-dest`
- `X-JWT-Assertion`
- سایر `X-Forwarded-*` / `X-Real-IP` در صورت عدم نیاز Rayan

این برای باگ فعلی **الزامی نیست**؛ فیکس الزامی همان remove + set مجدد `Authorization` است.

---

## فایلهایی که برای این باگ لازم نیست عوض شوند

| فایل | نقش | توضیح |
|------|-----|--------|
| `rportfolio.xml` | تعریف API / resourceها | `/lastWorkingDate` فقط template را صدا می‌زند |
| `rportfolioSetTokenAndCallSEQT.xml` | wrapper + retry روی 401/بعضی 403ها | محل set هدر نیست |
| `rportfolioTokenSEQT.xml` | توکن از DB / authenticate | مربوط به تهیه توکن است |
| `rportfolioRequestClientTokenSEQ.xml` | POST authenticate | بعد از auth معمولاً مسیر clean است |
| `rportfolioSetRedisSEQT.xml` | Redis get/set/lock | مربوط به کش توکن است |

---

## نکته جانبی درباره retry روی 403

در `rportfolioSetTokenAndCallSEQT.xml` برای HTTP 403 فقط این `errorId`ها باعث invalidate و retry می‌شوند:

- `50000005`
- `50000011`

`errorId: 10000002` (توکن یافت نشد به‌خاطر case هدر) پوشش داده **نمی‌شود**. با فیکس casing معمولاً نیازی به تغییر این بخش نیست؛ فقط بدانید که retry فعلی این سناریو را درست نمی‌کند.

---

## چک‌لیست تست بعد از فیکس

1. توکن Redis را پاک کنید (یا TTL را صبر کنید) تا یک بار مسیر authenticate طی شود → باید **200** بماند.
2. بلافاصله همان `GET /rp/lastWorkingDate` را دوباره از DevPortal (Staging: `am-stg.charisma.digital` / Prod: `apig-am.charisma.tech`) بزنید → باید **200** بماند (قبلاً 403 می‌شد).
3. در لاگ MI (wire/headers) برای call دوم به `ag.rayanbroker.ir` تأیید کنید هدر خروجی دقیقاً `Authorization:` است نه `authorization:`.
4. چند resource دیگر `rportfolio` را هم smoke کنید چون همه از `rportfolioResourceCallSEQT` استفاده می‌کنند.

### لاگ مفید Staging

- Namespace: `wso2`
- Deployment مربوط: `wso2am-pattern-1-mi-rayan-deployment`
- کلید Redis توکن: `wso2_data_token_rayan_portfolio`

جستجو در لاگ:

```text
lastWorkingDate
TokenFlow = Step 2: Token Exists in Redis
TokenFlow = Step 2: Token Not Found in Redis
errorId
10000002
```

---

## خلاصه یک‌خطی برای همکار

> قبل از call به Rayan در `rportfolioResourceCallSEQT.xml`، هدر `authorization`/`Authorization` قدیمی را remove کنید و دوباره با نام دقیق `Authorization` و مقدار توکن Redis set کنید؛ وگرنه وقتی کلاینت هدر lowercase بفرستد، Rayan با 403 و `errorId: 10000002` جواب می‌دهد.

---

## منبع تشخیص

- لاگ‌های Production MI (`lastWorkingDate` روی گتوی پرود)
- لاگ زنده Staging در namespace `wso2` / pod `mi-rayan`
- تست ایزوله curl از داخل pod MI به `ag.rayanbroker.ir`
- بررسی سورس برنچ `dev` ریپوی `wso2-integration-rayan_portfolio` (فقط خواندنی؛ بدون commit/PR در زمان تهیه این سند)
