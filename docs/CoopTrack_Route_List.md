# CoopTrack REST API — Route List (v1)

给 Erica 参考：Streamlit 页面里所有对数据的读写，都通过下面这些 route 调用
Flask API（不要让 Streamlit 直接连 MySQL）。

- Base URL 举例：`http://api:4000`（容器内）或 `http://localhost:4000`（本地）
- 5 个 Blueprint，29 条 route
- 满足要求：≥4 Blueprint、每个 ≥5 条、5 POST / 5 PUT / 4 DELETE、每个 Blueprint 每种写动词 ≤1

---

## Blueprint 1 — students（学生）

| 方法 | 路径 | Story | 作用 |
|---|---|---|---|
| GET | `/students` | — | 返回所有学生 |
| GET | `/students/<student_id>` | — | 某学生的资料 |
| GET | `/students/<student_id>/applications` | 1.x | 某学生的所有申请 |
| POST | `/students/<student_id>/saved` | 1.2 | 收藏一个职位到 shortlist |
| DELETE | `/students/<student_id>/saved/<position_id>` | 1.5 | 从 shortlist 移除职位 |
| PUT | `/students/<student_id>` | 3.1 | 封禁 / 恢复学生账号（admin 用）|

## Blueprint 2 — positions（职位）

| 方法 | 路径 | Story | 作用 |
|---|---|---|---|
| GET | `/positions` | 1.1 / 1.6 | 搜索 / 列出开放职位（可按 role、location、skill、deadline 筛选）|
| GET | `/positions/<position_id>` | — | 某职位详情 |
| GET | `/positions/<position_id>/applicants` | 2.2 | 该职位的申请者（按技能匹配度排序）|
| GET | `/positions/<position_id>/count` | 2.6 | 该职位收到的申请数量 |
| POST | `/positions` | 2.1 | 发布新职位 |
| PUT | `/positions/<position_id>` | 2.4 / 2.5 | 编辑职位 / 关闭职位 |
| DELETE | `/positions/<position_id>` | 3.2 | 下架职位（admin 审核）|

## Blueprint 3 — applications（申请）

| 方法 | 路径 | Story | 作用 |
|---|---|---|---|
| GET | `/applications` | — | 返回所有申请 |
| GET | `/applications/<application_id>` | — | 某条申请详情 |
| POST | `/applications` | 1.3 | 提交新申请 |
| PUT | `/applications/<application_id>` | 1.4 / 2.3 | 更新申请 / 流程状态 |
| DELETE | `/applications/<application_id>` | — | 撤回申请 |

## Blueprint 4 — skills（技能）

| 方法 | 路径 | Story | 作用 |
|---|---|---|---|
| GET | `/skills` | 3.6 | 列出所有技能 |
| GET | `/skills/<skill_id>` | — | 某技能详情 |
| GET | `/skills/demand` | 5.4 | 最抢手的技能（analytics）|
| POST | `/skills` | 3.6 | 新增技能到总表 |
| PUT | `/skills/<skill_id>` | — | 更新技能（改名 / 状态）|
| DELETE | `/skills/<skill_id>` | 3.4 | 删除未使用的重复技能 |

## Blueprint 5 — admin（审核 / 雇主）

| 方法 | 路径 | Story | 作用 |
|---|---|---|---|
| GET | `/admin/reports` | 3.3 | 待处理的被举报职位 |
| GET | `/admin/employers` | — | 列出所有雇主（含 pending）|
| GET | `/admin/placements` | 5.1 | placement 统计（dashboard 用）|
| POST | `/admin/employers` | 3.5 | 注册并验证新雇主 |
| PUT | `/admin/reports/<report_id>` | 3.3 | 处理 / 关闭一条举报 |

---

## Streamlit 页面 → route 对应参考（谁调哪些）

**Sofia / Student 页面**
- Position Search：`GET /positions`
- Save / Remove Position：`POST /students/<id>/saved`、`DELETE /students/<id>/saved/<pid>`
- Application Tracker：`GET /students/<id>/applications`、`POST /applications`、`PUT /applications/<id>`
- Upcoming Deadlines：`GET /positions`（按 deadline 筛）

**Marcus / Employer 页面**
- Create Position：`POST /positions`
- Edit / Close Position：`PUT /positions/<id>`
- Applicant Review：`GET /positions/<id>/applicants`
- Candidate Pipeline：`PUT /applications/<id>`
- Dashboard：`GET /positions/<id>/count`

**Nikki / Admin 页面**
- Pending Reports：`GET /admin/reports`、`PUT /admin/reports/<id>`
- Employer Verification：`GET /admin/employers`、`POST /admin/employers`
- Student Management：`PUT /students/<id>`（封禁）
- Skill Management：`GET /skills`、`POST /skills`、`DELETE /skills/<id>`

> 注：`DELETE /positions/<id>`、`GET /skills/demand`、`GET /admin/placements`
> 也要在某个页面被用到（checklist 要求所有 route 都被 UI 调用）。
> 可放进 Admin 的 moderation 页 / dashboard。
