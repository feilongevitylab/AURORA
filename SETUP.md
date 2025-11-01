# AURORA 项目设置指南

## 环境要求

### 后端 (Python)
- Python 3.10+
- pip

### 前端 (Node.js)
- Node.js 18+
- npm 或 yarn

## 设置步骤

### 1. 后端环境设置

后端虚拟环境已经创建并安装了依赖。

**激活虚拟环境：**
```bash
cd aurora-backend
source venv/bin/activate  # macOS/Linux
# 或在 Windows 上: venv\Scripts\activate
```

**运行后端服务器：**
```bash
python main.py
```

服务器将在 `http://localhost:8000` 运行。

### 2. 前端环境设置

**安装依赖：**
```bash
cd aurora-frontend
npm install
```

如果系统中没有 npm，请先安装 Node.js：
- macOS: `brew install node`
- 或从 https://nodejs.org/ 下载安装

**运行前端开发服务器：**
```bash
npm run dev
```

前端将在 `http://localhost:3000` 运行。

### 3. 环境变量配置

**后端环境变量：**
```bash
cd aurora-backend
cp .env.example .env  # 如果存在 .env.example
```

编辑 `.env` 文件，添加必要的 API 密钥：
```
OPENAI_API_KEY=your_openai_api_key_here
PANDASAI_API_KEY=your_pandasai_api_key_here
ENVIRONMENT=development
```

## 验证安装

### 后端
访问 `http://localhost:8000/health` 应该返回：
```json
{"status": "healthy"}
```

### 前端
访问 `http://localhost:3000` 应该显示 AURORA 界面。

## 项目结构

```
aurora/
├── aurora-backend/      # FastAPI 后端 (已设置 ✅)
│   ├── venv/           # Python 虚拟环境 (已创建 ✅)
│   ├── main.py         # API 入口
│   └── requirements.txt # Python 依赖 (已安装 ✅)
├── aurora-frontend/     # React 前端 (待安装 Node.js)
│   ├── package.json    # Node.js 依赖
│   └── src/            # React 源码
└── shared/             # 共享代码
```

## 常见问题

### 后端依赖冲突已解决
- 已调整 `pandas` 版本以兼容 `pandasai 2.0.12`
- 所有依赖已成功安装

### 前端需要 Node.js
如果 `npm` 命令不存在，请先安装 Node.js：
```bash
# macOS (使用 Homebrew)
brew install node

# 或下载安装包
# https://nodejs.org/
```

## 下一步

1. 安装 Node.js（如果尚未安装）
2. 运行 `cd aurora-frontend && npm install`
3. 配置后端 `.env` 文件（可选，用于 AI 功能）
4. 启动后端和前端服务器开始开发

