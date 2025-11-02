# AURORA 运行指南

## 快速启动

### 方法 1: 使用 Python 脚本（推荐）

```bash
python3 run.py
```

或

```bash
./run.py
```

### 方法 2: 使用 Shell 脚本

```bash
./run.sh
```

## 脚本功能

运行脚本会自动：

1. ✅ 检查项目依赖是否已安装
2. ✅ 启动 FastAPI 后端服务器（端口 8000）
3. ✅ 启动 React 前端开发服务器（端口 3000）
4. ✅ 等待服务器就绪后自动打开浏览器

## 系统要求

- **无需 API Key**：系统使用 mock 数据，完全不需要任何外部 API 密钥
- **无需数据库**：所有数据都在内存中生成和处理
- Python 3.10+
- Node.js 18+ 和 npm

## 首次运行前的准备

如果这是第一次运行项目，请确保：

1. **后端虚拟环境已创建**：
   ```bash
   cd aurora-backend
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # 或 venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **前端依赖已安装**：
   ```bash
   cd aurora-frontend
   npm install
   ```

运行脚本会自动检查这些依赖是否已安装。

## 停止服务

按 `Ctrl+C` 停止所有运行中的服务。

## 访问地址

- **前端**: http://localhost:3000
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs (Swagger UI)

## 注意事项

- 系统完全使用 mock 数据，无需配置任何 API key
- 所有数据在内存中生成，无需数据库
- 脚本会并行启动前后端服务，并自动处理进程管理

