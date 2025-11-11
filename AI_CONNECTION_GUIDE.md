# AI 连接指南

## 当前状态

目前系统支持两种模式：

### 1. Mock 模式（默认）
- 当没有设置 OpenAI API Key 时，系统使用模拟的 AI 回答
- 回答是基于预定义的模板和逻辑生成的
- 适合开发和测试，不需要 API 费用

### 2. OpenAI API 模式（真实 AI）
- 当设置了 OpenAI API Key 时，系统会调用真实的 OpenAI API
- 使用 GPT-4o 或 GPT-4 Turbo 模型
- 提供真实的 AI 生成回答

## 如何启用真实 AI

### 步骤 1: 获取 OpenAI API Key

1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 注册或登录账户
3. 进入 API Keys 页面：https://platform.openai.com/api-keys
4. 创建新的 API Key
5. 复制 API Key（格式类似：`sk-...`）

### 步骤 2: 设置环境变量

在 `aurora-backend` 目录下创建或编辑 `.env` 文件：

```bash
# 在 aurora-backend 目录下
cd aurora-backend

# 创建或编辑 .env 文件
echo "OPENAI_API_KEY=sk-your-api-key-here" > .env
```

或者手动创建 `.env` 文件：

```env
OPENAI_API_KEY=sk-your-api-key-here
```

### 步骤 3: 重启后端服务

设置 API Key 后，需要重启后端服务：

```bash
# 停止当前运行的后端（Ctrl+C）
# 然后重新启动
cd aurora-backend
source venv/bin/activate
python main.py
```

### 步骤 4: 验证连接

启动后端后，查看终端输出：

- **如果看到**：`[NarrativeAgent] Using OpenAI API with model: GPT-4o (OpenAI)`
  - ✅ 成功连接到 OpenAI API

- **如果看到**：`[NarrativeAgent] Initialized in Mock mode`
  - ❌ 仍在 Mock 模式，请检查 API Key 是否正确设置

## 后端 API 支持

### 当前后端提供的 API 端点

#### 1. `GET /api/hrv`
获取 HRV（心率变异性）生理数据

**查询参数：**
- `days` (int, 可选): 返回数据的天数，默认 7，范围 1-30

**响应示例：**
```json
{
  "data": [...],
  "count": 84,
  "metrics": {
    "avg_rmssd": 45.23,
    "avg_sdnn": 62.15,
    "avg_pnn50": 15.67
  }
}
```

#### 2. `GET /api/stress`
获取压力生理数据

**查询参数：**
- `days` (int, 可选): 返回数据的天数，默认 7，范围 1-30

**响应示例：**
```json
{
  "data": [...],
  "count": 168,
  "metrics": {
    "avg_stress_level": 35.23,
    "avg_heart_rate": 72.15,
    "avg_respiratory_rate": 16.67
  }
}
```

#### 3. `POST /api/insight`
获取 AI 生成的洞察、数据分析和可视化

**请求体：**
```json
{
  "query": "分析我的 HRV 数据",
  "mode": "energy"  // 可选: "energy", "longevity"
}
```

**响应结构（Energy Insight 模式示例）：**
```json
{
  "hero": {
    "greeting": "早安，今天的心率节奏较平稳。想听听你的身体在说什么吗？",
    "quick_prompts": ["我今天有点累。", "我还不错。", "查看今日镜。"],
    "top_dialog": "早安，旅人。你的系统正以温柔的节奏醒来，让我们一起倾听身体和心的低语。",
    "mirror_summary": "你的 Purpose 指标与恢复周期高度相关，说明意义感驱动了你的神经平衡。"
  },
  "data": {
    "coordination_score": 78,
    "insight_summary": "你正在保持专注，但恢复速度略低于平均。",
    "mirror_layers": { "physiology": { "title": "Physiology", "metrics": [...] }, "mind": { "...": "..." }, "meaning": { "...": "..." } },
    "mirror_trend": [
      {"date": "11-01", "hrv": 52.1, "stress": 38.5, "focus": 64.2},
      {"date": "11-02", "hrv": 51.4, "stress": 39.9, "focus": 66.0}
    ],
    "energy_pattern": "过去 3 天你的心率变异性下降，但专注指数上升。你的身体在努力跟上你的意志力。"
  },
  "chart": {
    "chart_type": "mirror_trend",
    "plotly_json": { "data": [...], "layout": {...}, "config": {...} }
  },
  "insight": "你正在保持专注，但恢复速度略低于平均。"
}
```

**模式说明：**
- `energy`: Energy Insight 模式 - 提供层级化的生理/心理/意义视图和意识拓扑叙事
- `longevity`: Longevity Exploration 模式 - 生成专业、科学的回答，聚焦恢复与长效表现

#### 4. `GET /health`
健康检查端点

**响应：**
```json
{
  "status": "healthy"
}
```

#### 5. `GET /docs`
Swagger API 文档（自动生成）

访问：http://localhost:8000/docs

## 前端如何使用后端 API

### 当前实现

前端通过以下方式使用后端 API：

1. **数据获取**：
   - 前端可以调用 `/api/hrv` 和 `/api/stress` 获取生理数据
   - 目前前端主要使用 `/api/insight` 端点

2. **AI 查询**：
   - 用户在输入框中输入查询
   - 前端发送 POST 请求到 `/api/insight`
   - 请求包含 `query`（用户查询）和 `mode`（当前模式）
   - 后端根据模式调用相应的 Agent
   - Agent 根据是否设置了 API Key 决定使用真实 AI 还是 Mock 模式

3. **结果展示**：
   - 后端返回包含 `data`、`chart`、`insight` 的 JSON
   - 前端根据当前模式在 Content 区域展示结果

## 费用说明

使用 OpenAI API 会产生费用：

- **GPT-4o**: 约 $2.50 - $10.00 / 1M tokens（输入）
- **GPT-4 Turbo**: 约 $10.00 - $30.00 / 1M tokens（输入）

建议：
- 开发阶段使用 Mock 模式
- 生产环境或需要真实 AI 回答时再启用 API
- 设置使用限额以避免意外费用

## 故障排除

### 问题：仍然显示 Mock 模式

**解决方案：**
1. 检查 `.env` 文件是否在 `aurora-backend` 目录下
2. 确认 API Key 格式正确（以 `sk-` 开头）
3. 确认没有多余的空格或引号
4. 重启后端服务

### 问题：API 调用失败

**可能原因：**
1. API Key 无效或过期
2. 账户余额不足
3. 网络连接问题

**解决方案：**
1. 检查 OpenAI 账户状态
2. 查看后端终端错误信息
3. 检查网络连接

### 问题：前端无法连接后端

**解决方案：**
1. 确认后端服务正在运行（http://localhost:8000）
2. 检查 CORS 配置（已在 `main.py` 中配置）
3. 检查前端访问的端口是否正确

