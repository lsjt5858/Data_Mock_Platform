# Data Mock Platform - 数据生成平台

一个可视化的数据建模与批量生成平台，用于测试、演示和原型验证。

## 功能特性

- 🎯 **可视化模板编辑** - 通过界面配置字段类型、约束和分布
- ⚡ **高性能生成** - 支持10万+条数据批量生成（约7秒）
- 📊 **多格式导出** - 支持 CSV、JSON、NDJSON 格式
- 🔍 **实时预览** - 生成前可预览采样数据
- 🌐 **中文支持** - 默认使用中文 Faker 数据

## 支持的字段类型

| 基础类型 | 语义类型 |
|---------|---------|
| int (整数) | uuid |
| float (浮点数) | email |
| string (字符串) | phone |
| boolean (布尔值) | name |
| datetime (日期时间) | address |
| enum (枚举) | company, city, url, ipv4 |

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+

### 启动后端

```bash
cd backend
pip install -r requirements.txt
python3 app.py
```

后端运行在 http://localhost:5001

### 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端运行在 http://localhost:5173

## API 接口

| 方法 | 路径 | 说明 |
|-----|------|-----|
| GET | /api/health | 健康检查 |
| POST | /api/generate | 生成数据 |
| POST | /api/exports | 创建导出 |
| GET | /api/exports/{id}/download | 下载文件 |

### 生成数据示例

```bash
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "fields": [
      {"name": "user_id", "type": "uuid", "unique": true},
      {"name": "email", "type": "email"},
      {"name": "age", "type": "int", "constraints": {"min": 18, "max": 80}}
    ],
    "count": 100,
    "preview": true
  }'
```

## 技术栈

**后端:** Flask, Faker, SQLite, flask-cors

**前端:** React 18, TypeScript, Ant Design, Vite, Axios

## 项目结构

```
├── backend/
│   ├── app.py              # Flask 入口
│   ├── routes/             # API 路由
│   ├── services/           # 核心服务
│   │   ├── data_generator.py
│   │   ├── faker_adapter.py
│   │   ├── validator.py
│   │   └── exporter.py
│   ├── repos/              # 数据仓库
│   └── models/             # 数据模型
├── frontend/
│   └── src/
│       ├── pages/          # 页面组件
│       ├── components/     # 通用组件
│       ├── services/       # API 封装
│       └── types/          # 类型定义
└── docs/                   # 文档
```

## License

MIT
