# 数据生成平台 - Frontend

基于 React + TypeScript + Vite + Ant Design 构建的前端应用。

## 启动项目

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

服务将在 `http://localhost:5173` 启动

## 功能页面

### 1. 模板编辑器 (/)
- 可视化配置数据字段
- 支持多种字段类型（基础类型 + 语义类型）
- 约束配置（范围、长度、唯一性）
- 实时预览生成数据

### 2. 数据生成 (/generate)
- 批量数据生成
- 支持 CSV、JSON、NDJSON 导出格式
- 最大支持 100万 条数据生成
- 自动下载导出文件

## 技术栈

- React 18
- TypeScript
- Vite (构建工具)
- Ant Design 5 (UI组件库)
- Axios (HTTP客户端)
- React Router (路由)

## 项目结构

```
src/
├── components/     # 可复用组件
│   └── FieldEditor.tsx
├── pages/         # 页面组件
│   ├── TemplateEditor.tsx
│   └── DataGenerate.tsx
├── services/      # API服务
│   └── api.ts
├── types/         # TypeScript类型定义
│   └── index.ts
├── App.tsx        # 主应用组件
└── main.tsx       # 应用入口
```

## API配置

默认后端地址: `http://localhost:5000`

可在 `src/services/api.ts` 中修改 `API_BASE_URL`
