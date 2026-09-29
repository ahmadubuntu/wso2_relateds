# Graph Report - wso2_relateds  (2026-09-20)

## Corpus Check
- 4 files · ~2,541 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 33 nodes · 31 edges · 6 communities (5 shown, 1 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- راهنمای رفع 403 سرویس `lastWorkingDate` (Rayan Portfolio / WSO2 MI)
- AGENTS
- Kibana dashboard: APIM top users over time
- محل دقیق فیکس
- اثبات با curl (مستقیم به Rayan)
- علت ریشه‌ای (Root Cause)

## God Nodes (most connected - your core abstractions)
1. `راهنمای رفع 403 سرویس `lastWorkingDate` (Rayan Portfolio / WSO2 MI)` - 11 edges
2. `AGENTS` - 8 edges
3. `محل دقیق فیکس` - 4 edges
4. `Kibana dashboard: APIM top users over time` - 4 edges
5. `اثبات با curl (مستقیم به Rayan)` - 3 edges
6. `علت ریشه‌ای (Root Cause)` - 2 edges
7. `چک‌لیست تست بعد از فیکس` - 2 edges
8. `Purpose` - 1 edges
9. `Layout` - 1 edges
10. `Configure / run` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities (6 total, 1 thin omitted)

### Community 0 - "راهنمای رفع 403 سرویس `lastWorkingDate` (Rayan Portfolio / WSO2 MI)"
Cohesion: 0.20
Nodes (9): خلاصه مشکل, خلاصه یک‌خطی برای همکار, راهنمای رفع 403 سرویس `lastWorkingDate` (Rayan Portfolio / WSO2 MI), ریپو و برنچ, فایلهایی که برای این باگ لازم نیست عوض شوند, لاگ مفید Staging, منبع تشخیص, نکته جانبی درباره retry روی 403 (+1 more)

### Community 1 - "AGENTS"
Cohesion: 0.25
Nodes (8): AGENTS, Configure / run, Current focus, Landmines, Layout, Plans, Purpose, Secrets

### Community 2 - "Kibana dashboard: APIM top users over time"
Cohesion: 0.33
Nodes (4): Constraints, Decisions, Kibana dashboard: APIM top users over time, Steps

### Community 3 - "محل دقیق فیکس"
Cohesion: 0.50
Nodes (4): اختیاری (سخت‌گیرانه / دفاعی), تغییر پیشنهادی, فایل اصلی (باید تغییر کند), محل دقیق فیکس

### Community 4 - "اثبات با curl (مستقیم به Rayan)"
Cohesion: 0.67
Nodes (3): اثبات با curl (مستقیم به Rayan), موفق, ناموفق (بازتولید باگ)

## Knowledge Gaps
- **23 isolated node(s):** `Purpose`, `Layout`, `Configure / run`, `Secrets`, `Landmines` (+18 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 24 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `راهنمای رفع 403 سرویس `lastWorkingDate` (Rayan Portfolio / WSO2 MI)` connect `راهنمای رفع 403 سرویس `lastWorkingDate` (Rayan Portfolio / WSO2 MI)` to `محل دقیق فیکس`, `اثبات با curl (مستقیم به Rayan)`, `علت ریشه‌ای (Root Cause)`?**
  _High betweenness centrality (0.286) - this node is a cross-community bridge._
- **Why does `AGENTS` connect `AGENTS` to `Kibana dashboard: APIM top users over time`?**
  _High betweenness centrality (0.127) - this node is a cross-community bridge._
- **Why does `محل دقیق فیکس` connect `محل دقیق فیکس` to `راهنمای رفع 403 سرویس `lastWorkingDate` (Rayan Portfolio / WSO2 MI)`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **What connects `Purpose`, `Layout`, `Configure / run` to the rest of the system?**
  _23 weakly-connected nodes found - possible documentation gaps or missing edges._