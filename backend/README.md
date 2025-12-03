# Backend API 说明

## 启动服务

```bash
# 安装依赖
pip install -r requirements.txt

# 运行服务器
python app.py
```

服务将在 `http://localhost:5000` 启动

## API 端点

### 1. 生成数据
**POST** `/api/generate`

请求体:
```json
{
  "fields": [
    {"name": "user_id", "type": "uuid", "unique": true},
    {"name": "email", "type": "email"},
    {"name": "age", "type": "int", "constraints": {"min": 18, "max": 80}}
  ],
  "count": 100,
  "preview": true
}
```

### 2. 创建导出
**POST** `/api/exports`

请求体:
```json
{
  "fields": [...],
  "count": 1000,
  "format": "csv"
}
```

### 3. 下载导出
**GET** `/api/exports/{id}/download`

### 4. 健康检查
**GET** `/api/health`

## 支持的字段类型

- 基础类型: `int`, `float`, `string`, `boolean`, `datetime`
- 语义类型: `uuid`, `email`, `phone`, `name`, `address`, `company`, `job`, `city`, `country`, `ipv4`, `ipv6`, `url`
- 复合类型: `enum`
