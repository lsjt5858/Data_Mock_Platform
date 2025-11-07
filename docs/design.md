# 测试数据生成平台 - 设计文档

版本：v0.1  
参考 Figma 原型与目标需求，采用前后端分离的轻量架构。

---

## 一、总体架构与技术选型

- 架构
  ```
  ┌─────────────────────────────────────────────────────┐
  │     React 前端（Ant Design UI）                     │
  │  ├─ 模板管理 / 生成配置 / 预览&导出                 │
  └────────────────┬──────────────────────────────────┘
                   │ HTTP REST API
  ┌────────────────▼──────────────────────────────────┐
  │   Python 后端（Flask）                             │
  │  ├─ 路由层：API端点                                │
  │  ├─ 业务层：生成引擎 / 规则引擎 / 关联处理          │
  │  ├─ 数据层：模板存储 / 导出管理                    │
  │  └─ 工具层：Faker / 校验 / 日志                    │
  └────────────────┬──────────────────────────────────┘
                   │
          ┌────────┴────────┐
          │                 │
      ┌───▼────┐       ┌───▼────┐
      │ SQLite │       │ 文件系 │
      │（元数据）      │ 统（导出）│
      └────────┘       └────────┘
  ```

- 技术选型
  - 前端：React + Ant Design + Axios（必要时 Zustand 管理局部状态）
  - 后端：Flask + Faker + flask-cors（后续可切 FastAPI）
  - 存储：SQLite（模板与任务元数据）+ 文件系统（导出）
  - 运行环境：macOS（Apple Silicon/M 系列）

---

## 二、模块设计

- 路由层（API）
  - `datasets`: 模板 CRUD
  - `generate/jobs`: 生成任务
  - `exports`: 导出管理与下载
  - `sources`: 数据源管理（阶段二）

- 业务层
  - `DataGenerator`: 解析模板→生成行→批量生成→应用约束与分布
  - `RuleEngine`: 解析规则 DSL/表达式→校验/变换
  - `RelationResolver`: 处理外键与跨数据集引用，生成顺序控制
  - `Exporter`: CSV/JSON/NDJSON/SQL INSERT，支持分片与压缩
  - `Previewer`: 采样预览，分页返回

- 数据层
  - `TemplateRepo`: 读写模板（SQLite），版本管理
  - `JobRepo`: 任务状态、日志、进度
  - `ExportRepo`: 导出记录、路径与元数据
  - `SourceRepo`: 数据源配置与缓存（计划）

- 工具层
  - `FakerAdapter`: 字段类型与 Faker 方法映射，支持自定义 Provider
  - `Validator`: 约束校验（范围、正则、唯一性等）
  - `Logger`: 统一日志（结构化），错误码与异常封装

---

## 三、数据模型（简化表结构）

- `datasets`（模板）
  - `id` TEXT PK, `name` TEXT, `desc` TEXT, `version` INT, `schema` JSON, `created_at` DATETIME

- `jobs`（生成任务）
  - `id` TEXT PK, `dataset_id` TEXT FK, `count` INT, `status` TEXT, `progress` FLOAT, `logs` TEXT, `created_at` DATETIME

- `exports`（导出）
  - `id` TEXT PK, `job_id` TEXT FK, `format` TEXT, `path` TEXT, `size` INT, `status` TEXT, `created_at` DATETIME

- `sources`（数据源）
  - `id` TEXT PK, `kind` TEXT, `config` JSON, `status` TEXT, `created_at` DATETIME

`schema` 示例（字段定义）：
```json
{
  "fields": [
    { "name": "user_id", "type": "uuid", "unique": true },
    { "name": "email", "type": "email", "constraints": { "regex": ".+@.+\\..+" } },
    { "name": "age", "type": "int", "constraints": { "min": 18, "max": 80 } },
    { "name": "created_at", "type": "datetime",
      "distribution": { "type": "uniform", "start": "2024-01-01", "end": "2024-12-31" } },
    { "name": "province", "type": "string", "source_ref": { "kind": "csv", "path": "dicts/provinces.csv" } }
  ],
  "rules": [
    { "expr": "amount > 0 && amount < 10000" }
  ]
}
```

---

## 四、生成引擎设计（核心）

- 字段生成流程
  1. 解析字段类型与约束、分布、来源。
  2. 若 `source_ref`：从字典/数据源取值（可缓存）。
  3. 若 `calc_expr`：计算表达式求值（可引用其他字段）。
  4. 应用约束与分布；若 `unique`：维护哈希集合避免重复。
  5. 返回字段值。

- 批量生成策略
  - 分批 `batch_size`（如 10k/批）生成→写入导出文件或分页缓存。
  - 大数据采用 NDJSON 流式写出，降低内存占用。
  - 并发：按分片拆分（随机种子隔离），最终合并或分包导出。

- 伪代码（单行）
```python
def generate_row(schema, ctx):
    row = {}
    for f in schema['fields']:
        if 'calc_expr' in f:
            row[f['name']] = eval_expr(f['calc_expr'], row, ctx)
        elif 'source_ref' in f:
            row[f['name']] = pick_from_source(f['source_ref'])
        else:
            row[f['name']] = faker_value(f)  # type+constraints+distribution
        row[f['name']] = enforce_constraints(row[f['name']], f['constraints'])
    validate_rules(schema.get('rules', []), row)
    return row
```

---

## 五、规则引擎与关联处理

- 规则引擎
  - 表达式/DSL：布尔表达（比较、逻辑与或非）、算术、字符串/日期操作。
  - 执行阶段：生成后校验与修正；失败记录日志。
  - 示例：`amount > 0 && amount < 10000`

- 关联处理
  - 生成顺序：先主表（用户），再子表（订单、支付）。
  - 外键引用：缓存主键集合，在子表随机选择或按分布选择。
  - 一致性校验：检测孤儿记录与引用缺失。

---

## 六、导出与预览

- 导出
  - CSV、JSON、NDJSON、SQL INSERT。
  - 支持压缩（ZIP），分包（N 条/包）。
  - NDJSON：流式写出，适合大数量。

- 预览
  - 采样（如 100 条），前端表格展示。
  - 校验提示：约束、唯一性冲突、高空值比例等。

---

## 七、API 设计（示例）

- `POST /api/generate`
  - 请求：
    ```json
    { "fields": [{ "name": "id", "type": "int" }, { "name": "email", "type": "email" }], "count": 100 }
    ```
  - 响应：
    ```json
    { "data": [ { "id": 1, "email": "a@b.com" } ], "total": 100 }
    ```

- `POST /api/exports`
  - 请求：
    ```json
    { "job_id": "job-1", "format": "csv", "compress": true, "chunk_size": 10000 }
    ```
  - 响应：
    ```json
    { "id": "exp-1", "status": "processing" }
    ```

- `GET /api/exports/{id}/download` → 返回文件流

---

## 八、前端设计

- 页面
  - 模板编辑页：字段列表（拖拽）、字段配置面板、规则配置区、采样预览。
  - 数据生成配置：选择模板、输入数量、高级选项（NULL 比例、唯一性）。
  - 数据预览&导出：表格预览、导出格式选择、下载。

- 组件与状态
  - `TemplateEditor`、`FieldConfigForm`、`RuleEditor`、`PreviewTable`、`ExportPanel`。
  - 状态管理：局部组件状态 + Axios 请求；必要时 Zustand。

---

## 九、部署与配置

- 本地开发（macOS, Apple Silicon）
  - Python 3.10+、Flask、Faker、flask-cors。
  - Node.js 18+、React、AntD。
  - SQLite 文件存储、导出文件目录可配置。
- 环境变量
  - `EXPORT_DIR`、`BATCH_SIZE`、`DEFAULT_LOCALE`、`MAX_CONCURRENCY`。

---

## 十、日志、监控与错误处理

- 日志：结构化日志（JSON），包含 `job_id`、耗时、速率、错误码。
- 错误处理：输入校验、边界检查（唯一性冲突、源数据缺失）、可恢复重试。
- 监控（后续）：任务成功率、生成速率、导出失败率。

---

## 十一、性能优化建议

- 生成阶段使用批量与分片；NDJSON 流式输出。
- Faker 仅用于语义类型；基础类型可用自研生成器提升性能。
- 唯一性用布隆过滤器/哈希集合（按分片局部唯一，下游再合并）。

---

## 十二、测试策略

- 单测：字段映射、约束、规则校验、导出器。
- 集成：`/api/generate`、`/api/exports` 端到端。
- 基准：不同 `count` 与格式的吞吐测试。

---