# 数据生成平台（Data Mock Platform）

面向测试、演示和原型验证的可视化数据建模与批量生成平台。

- 设计稿（Figma）：https://www.figma.com/make/mfqYLeS0rLAbvK2TNRwerU/%E6%95%B0%E6%8D%AE%E7%94%9F%E6%88%90%E5%B9%B3%E5%8F%B0?node-id=0-4
- 平台愿景：降低高质量模拟数据的生产门槛，帮助产品/测试/数仓在无真实数据或受隐私限制时快速迭代。
- 当前状态：本仓库为文档与规划，代码实现待后续仓库对齐。

---

## 适用场景

- 接口联调与端到端测试：为前后端联调提供稳定可控的 Mock 数据。
- 演示与沙箱：用于演示环境或培训，避免暴露真实数据。
- 原型和数据可视化：为报表、BI、图表快速生成符合分布的样本数据。
- 性能压测：批量生成海量数据，验证系统吞吐与稳定性。

---

## 核心特性（依据通用需求与设计预期）

- 可视化数据建模
  - 数据集（Dataset）/ 模板（Template）管理
  - 字段编辑器，支持基础与语义类型（如邮箱、手机号、身份证、地址、姓名、公司、IP、UUID 等）
  - 字段约束：取值范围、长度、正则匹配、空值比例、唯一性
  - 分布控制：均匀、正态、泊松、权重、自定义分布
  - 字段依赖与引用：计算字段、跨数据集引用、外键关系

- 数据源与引用
  - 文件数据源：CSV/JSON 导入作为引用/字典
  - 数据库数据源（计划）：PostgreSQL/MySQL/SQLite
  - HTTP API 数据源（计划）：从远端接口获取字典或样本

- 生成任务与调度
  - 一次性生成 / 批量生成
  - 定时任务（Cron）
  - 并发与分片、失败重试策略
  - 任务进度、日志与告警

- 导出与集成
  - 导出格式：CSV、JSON、NDJSON、SQL INSERT
  - 压缩打包 ZIP
  - Webhook 通知（计划）与 REST API

- 质量与可视化
  - 采样预览、字段分布可视化
  - 数据质量校验（约束、唯一性、空值比例）

- 权限与审计
  - 角色：管理员（Admin）/ 项目成员（Member）/ 访客（Viewer）
  - 操作审计、任务执行记录

- 模板库（行业预置）
  - 电商：用户、商品、订单、支付、物流
  - 金融：账户、交易、对账
  - IoT：设备、事件、传感器采样
  - 通用：地址簿、组织与人员

---

## 页面与交互映射（参考 Figma）

- 登录 / 注册
  - 支持邮箱或企业 SSO（视实现而定）

- 概览（Dashboard）
  - 项目与数据集概况、最近任务、失败/成功统计
  - 快捷入口：创建数据集、发起任务、查看导出

- 项目（Projects）
  - 项目列表与搜索、成员管理
  - 项目内资源：数据集、数据源、任务、导出、审计

- 数据集（Datasets / Templates）
  - 列表、创建、复制、版本管理
  - 详情：字段结构、约束与分布、依赖图

- 字段编辑器（Field Editor）
  - 类型选择：基础/语义/复合（对象/数组）
  - 约束与分布配置、引用与计算字段
  - 预览采样与校验提示

- 数据源（Data Sources）
  - 添加 CSV/JSON、数据库连接、HTTP API
  - 字段映射与字典预览

- 生成任务（Jobs）
  - 新建任务：目标数据集、数量、分片/并发、定时配置
  - 任务详情：进度、日志、重试、取消

- 导出与下载（Exports）
  - 格式选择、压缩、分包
  - 可分享下载链接（权限受控）

- 历史与审计（Activity / Logs）
  - 操作记录与任务历史，筛选与导出

- 系统设置（Settings）
  - 全局配置、国际化、存储与缓存、Webhooks（计划）

- 用户与权限（Access Control）
  - 成员邀请、角色分配、项目级权限

---

## 数据模型与规则

- 字段类型
  - 基础：整数、小数、布尔、字符串、日期/时间
  - 语义：姓名、手机号、邮箱、地址、公司、职位、身份证、银行卡、IP、MAC、域名、URL、UUID
  - 复合：数组、对象、枚举
  - 生成器：正则、随机文本（句子/段落）、计算表达式

- 字段约束
  - 取值范围（数值/日期）、长度（字符串）
  - 正则匹配、唯一性（含跨字段唯一组合）
  - 空值比例（Null/Undefined）、默认值

- 分布与权重
  - 均匀、正态（μ/σ）、泊松（λ）
  - 权重枚举、离散分布、用户自定义分布

- 依赖与引用
  - 引用另一个字段或数据源（例如地址省市区联动）
  - 跨数据集引用（外键）
  - 计算字段（表达式：加减乘除、拼接、日期运算）

---

## 任务与调度

- 任务类型：一次性、批量、定时（Cron）
- 并发与分片：提升生成吞吐，适配海量场景
- 重试策略：指数退避、最大重试次数、失败告警
- 任务可观测性：进度百分比、速率（rows/s）、剩余时间估算
- 资源配额（计划）：项目级任务配额与并发上限

---

## 导出与集成

- 导出格式：CSV、JSON、NDJSON、SQL INSERT
- 压缩类型：ZIP
- 下载与分享：基于权限的临时链接
- 集成方式（计划）：Webhook、对象存储（S3/OSS）、数据库直写

---

## API 草案（待实现）

基础路径：`/api`

- 项目
  - `GET /api/projects` 列出项目
  - `POST /api/projects` 创建项目

- 数据集
  - `GET /api/datasets` 列出数据集
  - `POST /api/datasets` 创建数据集（含字段结构）
  - `GET /api/datasets/{id}` 查看数据集详情
  - `PUT /api/datasets/{id}` 更新数据集
  - `POST /api/datasets/{id}/clone` 克隆数据集

- 生成任务
  - `POST /api/jobs` 发起生成任务
  - `GET /api/jobs/{id}` 查询任务状态
  - `POST /api/jobs/{id}/cancel` 取消任务
  - `POST /api/jobs/{id}/retry` 重试任务

- 导出
  - `POST /api/exports` 发起导出
  - `GET /api/exports/{id}` 查询导出状态
  - `GET /api/exports/{id}/download` 下载导出文件

示例：创建一个包含基础字段的数据集（JSON 负载示例）
```json
{
  "name": "orders",
  "description": "电商订单数据集",
  "fields": [
    { "name": "order_id", "type": "uuid", "unique": true },
    { "name": "user_id", "type": "uuid" },
    { "name": "created_at", "type": "datetime", "distribution": { "type": "uniform", "start": "2024-01-01", "end": "2024-12-31" } },
    { "name": "amount", "type": "float", "min": 1, "max": 9999.99 },
    { "name": "status", "type": "enum", "values": ["pending", "paid", "shipped", "delivered", "refunded"], "weights": [0.1, 0.4, 0.2, 0.25, 0.05] },
    { "name": "province", "type": "string", "source": { "kind": "csv", "path": "dicts/provinces.csv" } }
  ]
}
```

---

## 快速开始（后端原型）

- 环境要求
  - Python ≥ 3.9（macOS，Apple Silicon/M 芯片）
  - 可选：`curl` 或 Postman 用于接口测试

- 创建虚拟环境与安装依赖
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# 若公司内网源不可达，可改用官方索引
pip install -r requirements.txt --index-url https://pypi.org/simple
```

- 启动服务
```bash
python app.py
```
访问 `http://127.0.0.1:5000/`，预期响应：`{"status":"ok"}`（健康检查，见 app.py:26-30）。

- 主要 API 端点
  - `POST /api/generate` 生成数据（校验后执行）
  - `POST /api/export` 导出数据（json 返回字符串；csv/sql 作为附件流）
  - `GET /api/field-types` 字段类型列表（来自 SQLite 缓存）
  - `POST /api/validate-config` 只校验不生成

- 示例命令
  - 生成 5 行数据
```bash
curl -X POST http://127.0.0.1:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "fields": [
      {"name": "id", "type": "int", "params": {"min_value": 1, "max_value": 10}},
      {"name": "email", "type": "email", "params": {}}
    ],
    "count": 5,
    "include_null": false,
    "random_seed": 42
  }'
```
  - 导出为 JSON（字符串返回）
```bash
curl -X POST http://127.0.0.1:5000/api/export \
  -H "Content-Type: application/json" \
  -d '{
    "data": [{"id": 1, "email": "a@b.com"}],
    "format": "json",
    "options": {"pretty": true}
  }'
```
  - 导出为 CSV（附件流）
```bash
curl -X POST http://127.0.0.1:5000/api/export \
  -H "Content-Type: application/json" \
  -d '{
    "data": [{"id": 1, "email": "a@b.com"}, {"id": 2, "email": null}],
    "format": "csv",
    "options": {"include_header": true, "delimiter": ","}
  }' -D -
```
  - 导出为 SQL INSERT（批量）
```bash
curl -X POST http://127.0.0.1:5000/api/export \
  -H "Content-Type: application/json" \
  -d '{
    "data": [{"id": 1, "email": "a@b.com", "name": "O\'Hara"}],
    "format": "sql",
    "options": {"table_name": "users", "include_header": true, "batch_size": 100}
  }' -D -
```
  - 字段类型
```bash
curl http://127.0.0.1:5000/api/field-types
```

- 运行测试
```bash
pytest -q
```
包含生成/校验/导出与 API 行为的单测（见 tests/ 目录）。

- 配置项（`config.py`）
  - `DB_PATH`：SQLite 文件路径，默认 `data_generator.db`
  - `DEFAULT_LOCALE`：Faker 默认语言，`zh_CN`
  - `NULL_PROBABILITY`：当 `include_null=true` 时返回 `null` 的概率（默认 0.3）
如需调整，直接编辑 `config.py` 并重启服务。

- 数据库说明
  - 首次启动自动建表并插入 15 种字段类型（`backend/models/db.py:17-64`）
  - 数据库文件已被 `.gitignore` 忽略，避免入库

- 常见问题
  - 405 报错：`/api/export` 仅支持 `POST`，使用浏览器 `GET` 会返回 405
  - 依赖安装网络问题：使用 `--index-url https://pypi.org/simple` 或配置可用的公司内网源

- 项目结构（后端）
```
backend/
  models/db.py        # SQLite 初始化与种子
  routes/api.py       # Flask 路由与统一回复
  services/           # 生成/校验/导出/类型缓存
app.py                # 应用入口与健康检查
config.py             # 配置项
tests/                # 单元测试
```

## 权限与角色

- 管理员（Admin）：系统/项目设置、成员与权限、模板库管理
- 项目成员（Member）：创建与编辑数据集、发起任务、导出数据
- 访客（Viewer）：查看项目、下载已授权的导出

---

## 常见问题（FAQ）

- 如何保证生成数据“看起来真实”？
  - 使用语义类型（姓名、地址等）与权重分布组合
  - 使用真实字典（CSV/数据库）作为引用，提升真实性

- 如何生成海量数据？
  - 通过并发与分片生成任务，按批导出，使用 NDJSON/CSV 提升吞吐
  - 合理的重试与失败告警确保稳定性

- 隐私与合规怎么处理？
  - 仅生成模拟数据，不使用真实个人数据
  - 如需从真实库抽样，必须在数据源层做脱敏/聚合处理（企业级需求）

---

## 术语表

- 数据集（Dataset）：一组字段结构与规则的定义，可用于生成数据
- 模板（Template）：可复用的数据集预设
- 字典（Dictionary）：来源于 CSV/DB/API 的值集合，可被字段引用
- 任务（Job）：一次数据生成的执行实例
- 导出（Export）：任务结果文件与下载

---

## 路线图（Roadmap，规划）

- 数据库与消息队列接入（PostgreSQL/Redis）
- Webhook、对象存储导出（S3/OSS）
- 更丰富的语义类型库与国际化
- 模板市场与分享机制
- 生成质量度量与报告

---

## 贡献与反馈

- Issue 与建议：请在仓库中提出问题与功能建议
- 设计对齐：如需严格对齐 Figma 的模块命名与流程，请提供截图或具体节点 ID，我将进一步细化文档与文案

---