# 测试数据生成平台 - 需求文档

版本：v0.1  
设计稿（Figma）：https://www.figma.com/make/mfqYLeS0rLAbvK2TNRwerU/%E6%95%B0%E6%8D%AE%E7%94%9F%E6%88%90%E5%B9%B3%E5%8F%B0?node-id=0-4  
目标：为测试、联调、演示与数据可视化提供高质量、可控的模拟数据生产能力。

---

## 一、产品愿景与目标

- 降低模拟数据生产门槛：通过可视化模板与规则配置，非数据工程人员也可快速生成。
- 支持真实业务建模：围绕用户、订单、支付等场景定义字段、约束与表间关系。
- 覆盖多格式导出与集成：CSV、JSON、NDJSON、SQL INSERT，并计划支持 Webhook/对象存储。
- 面向规模化生成：支持批量并发、分片、重试与可观测性。
- 合规与安全：仅生成模拟数据，避免真实个人数据泄露。

---

## 二、角色与使用场景

- 角色
  - 管理员（Admin）：系统/项目设置、成员与权限、模板库管理。
  - 项目成员（Member）：创建模板、配置生成任务、导出数据。
  - 访客（Viewer）：查看项目、下载已授权导出、仅预览。

- 场景
  - 前后端联调：根据接口契约生成稳定字段集合。
  - 演示沙箱：产品演示或培训环境，避免真实数据。
  - BI/报表：为图表与报表生成符合分布的数据样本。
  - 压测：生成百万级数据以验证系统吞吐与稳定性。

---

## 三、功能需求（分模块）

1) 模板管理（Datasets/Templates）
- 新建/编辑/复制/版本管理模板。
- 字段类型：基础（int/float/string/bool/datetime），语义（邮箱、手机、身份证、地址、姓名、公司、IP、UUID），复合（数组、对象、枚举）。
- 字段约束：长度、范围、正则、唯一性、空值比例、默认值。
- 字段分布：均匀、正态、泊松、权重枚举、自定义离散分布。
- 字段依赖：计算字段（表达式）、字段引用（跨数据集外键）。
- 采样预览与校验提示（约束冲突、唯一性不足等）。

2) 数据源管理（Data Sources）
- 导入 CSV/JSON 作为字典引用。
- 数据库连接（计划）：PostgreSQL/MySQL/SQLite。
- 外部 API（计划）：字典或样本值拉取与缓存。

3) 生成任务（Jobs）
- 一次性、批量、定时（Cron）。
- 并发与分片、失败重试策略。
- 进度/速率/剩余时间估算，任务日志与告警。
- 任务取消/重试。

4) 关联关系
- 外键引用（如订单.user_id 引用用户表 id）。
- 多表生成顺序控制与级联生成。
- 关系一致性校验（孤儿记录检测）。

5) 导出与下载（Exports）
- 导出为 CSV、JSON、NDJSON、SQL INSERT。
- 支持压缩（ZIP）、分包。
- 基于权限的下载链接。

6) 权限与审计
- 项目级访问控制（Admin/Member/Viewer）。
- 操作审计与任务执行记录。

7) 系统设置
- 国际化、全局参数（并发上限、默认分布）、对象存储配置（计划）。

---

## 四、非功能性需求

- 性能：单节点支持≥10万/分钟生成速率，支持分片并发。
- 可靠性：任务失败可重试、断点续生成（分片级）。
- 可用性：前端页面响应≤200ms（不含生成执行），导出下载稳定。
- 安全：CORS 配置、输入校验、速率限制（后续）。
- 兼容：macOS（Apple Silicon/M 系列）开发环境。
- 可维护：模块化设计、清晰日志、错误码规范。

---

## 五、MVP 范围与验收标准

- 范围
  - 单表模板管理：基础与语义字段、基本约束（长度、范围、唯一性）。
  - 一次性生成任务：count 指定数量生成。
  - 导出为 CSV/JSON。
  - 采样预览（前端表格展示）。
  - 简单 API：`POST /api/generate`。

- 验收
  - 可创建模板并保存。
  - 可生成≥10万条单表数据（分批/分页返回或导出）。
  - 可导出为 CSV/JSON 文件并下载。
  - 字段约束生效，唯一性冲突给出校验提示。

---

## 六、阶段规划（递进式）

- 第一阶段（MVP，单表）
  - 后端：生成引擎、导出器、/api/generate。
  - 前端：模板编辑、生成配置、预览与导出。
- 第二阶段（扩展，多表 + 业务规则）
  - 外键关联、生成顺序、规则引擎（表达式/DSL）。
  - 定时任务、任务日志、失败重试。
- 第三阶段（完善，高级功能 + 性能优化）
  - 大数据导出（NDJSON/分片/流式）、Webhook/S3。
  - 并发优化、对象存储、权限/审计完善。

---

## 七、接口需求（草案）

- 模板
  - `GET /api/datasets`
  - `POST /api/datasets`
  - `GET /api/datasets/{id}`
  - `PUT /api/datasets/{id}`
  - `POST /api/datasets/{id}/clone`

- 生成任务
  - `POST /api/generate`（MVP）
  - `POST /api/jobs`（阶段二）
  - `GET /api/jobs/{id}`
  - `POST /api/jobs/{id}/cancel` / `retry`

- 导出
  - `POST /api/exports`
  - `GET /api/exports/{id}`
  - `GET /api/exports/{id}/download`

---

## 八、数据结构（概念模型）

- Dataset：`id`, `name`, `description`, `fields[]`, `version`, `created_at`.
- Field：`name`, `type`, `constraints{min,max,len,regex,unique,null_pct,default}`, `distribution`, `source_ref`, `calc_expr`.
- Source：`id`, `kind(csv/json/db/api)`, `config`, `status`.
- Job：`id`, `dataset_id`, `count`, `shards`, `status`, `progress`, `logs`.
- Export：`id`, `job_id`, `format`, `path`, `size`, `status`.
- Activity：`id`, `actor`, `action`, `target`, `timestamp`.

---

## 九、边界与假设

- 仅生成模拟数据，不接入真实用户隐私数据。
- 大规模生成优先使用流式/分片导出，避免一次性加载内存。
- Faker 为基础供给，百万级场景可替换为自研生成器。

---

## 十、风险与对策

- 跨域问题：后端开启 CORS。
- 生成性能：批量/分片、NDJSON 流式写出、异步并发。
- 关联复杂：先设计模型与顺序，提供一致性校验。
- 前后端联调：先用 Postman 验证 API，再接前端。

---

## 十一、成功度量（KPIs）

- 生成速率、任务成功率、导出失败率、模板复用率。
- 前端可用性：关键操作点击到响应时间。