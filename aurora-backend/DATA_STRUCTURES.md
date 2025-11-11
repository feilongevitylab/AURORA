# AURORA Backend - 数据结构规范文档

本文档定义了 AURORA 后端系统中所有API端点和Agent的数据结构要求。

---

## 目录

1. [API 端点数据结构](#api-端点数据结构)
2. [Agent 返回数据结构](#agent-返回数据结构)
   - [DataAgent](#dataagent)
   - [VizAgent](#vizagent)
   - [NarrativeAgent](#narrativeagent)
   - [AuroraCoreAgent](#auroracoreagent)

---

## API 端点数据结构

### GET `/api/hrv`

获取HRV（心率变异性）生理数据。

**查询参数：**
- `days` (int, 可选): 返回数据的天数，默认值 7，范围 1-30

**响应结构：**
```json
{
  "data": [
    {
      "timestamp": "2024-11-01T12:00:00",
      "rmssd": 45.2,
      "sdnn": 62.5,
      "pnn50": 15.3,
      "frequency_domain_lf": 450.2,
      "frequency_domain_hf": 320.8
    }
  ],
  "count": 84,
  "metrics": {
    "avg_rmssd": 45.23,
    "avg_sdnn": 62.15,
    "avg_pnn50": 15.67
  }
}
```

**字段说明：**
- `data`: HRV数据点数组
  - `timestamp`: ISO 8601格式的时间戳
  - `rmssd`: 连续RR间期的均方根差（Root Mean Square of Successive Differences）
  - `sdnn`: NN间期的标准差（Standard Deviation of NN intervals）
  - `pnn50`: NN50间隔的百分比
  - `frequency_domain_lf`: 低频域功率
  - `frequency_domain_hf`: 高频域功率
- `count`: 数据点总数
- `metrics`: 聚合指标

---

### GET `/api/stress`

获取压力生理数据。

**查询参数：**
- `days` (int, 可选): 返回数据的天数，默认值 7，范围 1-30

**响应结构：**
```json
{
  "data": [
    {
      "timestamp": "2024-11-01T12:00:00",
      "stress_level": 35.5,
      "heart_rate": 72.3,
      "respiratory_rate": 16.2,
      "skin_conductance": 5.8
    }
  ],
  "count": 168,
  "metrics": {
    "avg_stress_level": 35.23,
    "avg_heart_rate": 72.15,
    "avg_respiratory_rate": 16.67
  }
}
```

**字段说明：**
- `data`: 压力数据点数组
  - `timestamp`: ISO 8601格式的时间戳
  - `stress_level`: 压力水平 (0-100 量表)
  - `heart_rate`: 心率 (次/分钟)
  - `respiratory_rate`: 呼吸率 (次/分钟)
  - `skin_conductance`: 皮肤电导度
- `count`: 数据点总数
- `metrics`: 聚合指标

---

### POST `/api/insight`

获取AI生成的洞察分析。

**请求体结构：**
```json
{
  "query": "分析我的HRV数据",
  "context": {
    "days": 7,
    "metrics": ["hrv", "stress"]
  }
}
```

**响应结构：**
```json
{
  "insight": "Based on your query: \"分析我的HRV数据\", here is an AI-generated insight placeholder...",
  "timestamp": "2024-11-01T12:00:00",
  "query": "分析我的HRV数据",
  "context": {
    "days": 7,
    "metrics": ["hrv", "stress"]
  }
}
```

**字段说明：**
- `insight`: AI生成的洞察文本
- `timestamp`: 生成时间戳
- `query`: 原始查询
- `context`: 上下文数据（可选）

---

## Agent 返回数据结构

### DataAgent

数据处理和分析代理，使用pandas进行数据分析。

**调用方式：**
```python
from agents.data_agent import DataAgent

agent = DataAgent()
result = agent.run("analyze HRV by stress level")
```

**返回结构：**
```json
{
  "agent": "DataAgent",
  "result": {
    "query": "analyze HRV by stress level",
    "timestamp": "2024-11-01T12:00:00",
    "data_summary": {
      "total_records": 15,
      "columns": ["id", "hrv", "stress_score", "age"],
      "shape": [15, 4]
    },
    "statistics": {
      "hrv": {
        "count": 15,
        "mean": 50.28,
        "std": 7.21,
        "min": 38.5,
        "max": 61.3,
        "median": 49.7
      },
      "stress_score": {
        "count": 15,
        "mean": 27.33,
        "std": 14.23,
        "min": 8.0,
        "max": 55.0,
        "median": 25.0
      },
      "age": {
        "count": 15,
        "mean": 30.07,
        "std": 5.23,
        "min": 22,
        "max": 40,
        "median": 29.0
      }
    },
    "hrv_by_stress_level": {
      "Low": {
        "count": 5,
        "average_hrv": 57.24,
        "std": 3.78,
        "min": 52.8,
        "max": 61.3
      },
      "Medium": {
        "count": 6,
        "average_hrv": 50.32,
        "std": 4.48,
        "min": 45.2,
        "max": 56.4
      },
      "High": {
        "count": 4,
        "average_hrv": 41.52,
        "std": 2.74,
        "min": 38.5,
        "max": 44.6
      }
    },
    "hrv_by_age_group": {
      "Young": {
        "count": 7,
        "average_hrv": 48.15,
        "std": 6.23
      },
      "Middle": {
        "count": 5,
        "average_hrv": 52.34,
        "std": 5.67
      },
      "Senior": {
        "count": 3,
        "average_hrv": 51.67,
        "std": 4.12
      }
    },
    "correlations": {
      "hrv_vs_stress": -0.723,
      "hrv_vs_age": 0.156,
      "stress_vs_age": -0.089
    },
    "insights": [
      "Average HRV across all records: 50.28",
      "Average HRV for Low stress (57.24) is higher than High stress (41.52)",
      "Strong negative correlation (-0.723) between HRV and stress score",
      "Analysis completed on 15 records"
    ],
    "status": "processed"
  },
  "success": true
}
```

**字段说明：**

- `agent`: Agent名称
- `result`: 分析结果
  - `query`: 原始查询
  - `timestamp`: 处理时间戳
  - `data_summary`: 数据摘要
    - `total_records`: 总记录数
    - `columns`: 列名列表
    - `shape`: DataFrame形状 (行数, 列数)
  - `statistics`: 基本统计信息
    - `hrv/stress_score/age`: 各字段的统计（count, mean, std, min, max, median）
  - `hrv_by_stress_level`: **按压力水平分组的平均HRV**
    - `Low`/`Medium`/`High`: 压力分类
      - `count`: 该分类的记录数
      - `average_hrv`: 平均HRV值
      - `std`: 标准差
      - `min`/`max`: 最小/最大值
  - `hrv_by_age_group`: 按年龄组分组的HRV统计
    - `Young`/`Middle`/`Senior`: 年龄分组
  - `correlations`: 相关性系数
    - `hrv_vs_stress`: HRV与压力的相关性
    - `hrv_vs_age`: HRV与年龄的相关性
    - `stress_vs_age`: 压力与年龄的相关性
  - `insights`: 自动生成的洞察列表
  - `status`: 处理状态
- `success`: 操作是否成功

#### Energy Insight 模式附加字段

当 `context.mode === "energy"` 时，`result` 中还会包含：

```json
{
  "coordination_score": 78,
  "insight_summary": "你正在保持专注，但恢复速度略低于平均。",
  "mirror_layers": {
    "physiology": {
      "title": "Physiology",
      "description": "HRV · Sleep Quality · Heart Coherence",
      "metrics": [
        {"label": "HRV", "value": "52.4"},
        {"label": "Sleep Quality", "value": "78.3"},
        {"label": "Heart Coherence", "value": "71.5"}
      ]
    },
    "mind": { "...": "..." },
    "meaning": { "...": "..." }
  },
  "mirror_trend": [
    {"date": "11-01", "hrv": 52.1, "stress": 38.5, "focus": 64.2},
    {"date": "11-02", "hrv": 51.4, "stress": 39.9, "focus": 66.0}
  ],
  "energy_pattern": "过去 3 天你的心率变异性下降，但专注指数上升。你的身体在努力跟上你的意志力。",
  "hero": {
    "greeting": "早安，今天的心率节奏较平稳。想听听你的身体在说什么吗？",
    "quick_prompts": ["我今天有点累。", "我还不错。", "查看今日镜。"],
    "top_dialog": "早安，旅人。你的系统正以温柔的节奏醒来，让我们一起倾听身体和心的低语。",
    "mirror_summary": "你的 Purpose 指标与恢复周期高度相关，说明意义感驱动了你的神经平衡。"
  }
}
```

字段说明：

- `coordination_score`：身体-心理-意义的综合协同指数（0-100）。
- `insight_summary`：Energy Insight 模式的一句话洞察。
- `mirror_layers`：三层视图（Physiology / Mind / Meaning），每层包含主要指标与说明。
- `mirror_trend`：近 7 日 HRV / Stress / Focus 趋势数据，供 VizAgent 生成折线图。
- `energy_pattern`：AI 生成的 narrative 描述，用于 Energy Pattern 区域。
- `hero`：Hero 区动态问候与 quick prompt 配置。

**压力水平分类标准：**
- `Low`: stress_score < 20
- `Medium`: 20 ≤ stress_score ≤ 35
- `High`: stress_score > 35

**年龄分组标准：**
- `Young`: age < 30
- `Middle`: 30 ≤ age ≤ 35
- `Senior`: age > 35

---

### VizAgent

可视化生成代理，生成Plotly.js图表配置。

**调用方式：**
```python
from agents.viz_agent import VizAgent

agent = VizAgent()
result = agent.run("visualize stress levels over time", data=data_dict)
```

**返回结构：**
```json
{
  "agent": "VizAgent",
  "result": {
    "chart_type": "line",
    "plotly_config": {
      "data": [
        {
          "x": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
          "y": [35.2, 38.5, 32.1, 40.3, 35.7, 42.2, 39.8, 36.5, 41.2, 38.9],
          "type": "line",
          "name": "Dataset 1",
          "marker": {
            "color": "rgb(59, 130, 246)"
          }
        }
      ],
      "layout": {
        "title": {
          "text": "visualize stress levels over time",
          "font": {
            "size": 18
          }
        },
        "xaxis": {
          "title": "Time",
          "showgrid": true
        },
        "yaxis": {
          "title": "Value",
          "showgrid": true
        },
        "hovermode": "closest",
        "template": "plotly_white"
      },
      "config": {
        "responsive": true,
        "displayModeBar": true
      }
    },
    "recommendations": [
      "Recommended chart type: line",
      "Interactive zoom and pan enabled",
      "Hover tooltips configured"
    ],
    "timestamp": "2024-11-01T12:00:00"
  },
  "success": true
}
```

**字段说明：**
- `agent`: Agent名称
- `result`: 可视化结果
  - `chart_type`: 图表类型（Energy Insight 模式下为 `mirror_trend`，默认 `scatter`）
  - `plotly_json`: Plotly `Figure.to_json()` 解析后的对象，包含 `data`、`layout`、`config`
  - `recommendations`: 推荐配置列表
  - `timestamp`: 生成时间戳
- `success`: 操作是否成功

Energy Insight 模式下，当 `data` 中带有 `mirror_trend` 时，VizAgent 会生成包含 HRV / Stress / Focus 三条折线的趋势图；否则回退到默认的 HRV vs Stress 散点图。

---

### NarrativeAgent

叙事生成代理，生成自然语言解释和总结。

**调用方式：**
```python
from agents.narrative_agent import NarrativeAgent

agent = NarrativeAgent()
result = agent.run("explain the HRV analysis", data=data_dict, insights=insights_list)
```

**返回结构：**
```json
{
  "agent": "NarrativeAgent",
  "result": {
    "narrative": "Based on your query: \"explain the HRV analysis\", here's what the data tells us:\n\nThe analysis of your physiological measurements reveals several interesting patterns...",
    "summary": "Analysis identified 3 key insights: Average HRV increased by 15% over the past week; Stress levels peaked during afternoon hours; Sleep quality correlates with morning recovery metrics",
    "key_takeaways": [
      "Takeaway 1: Average HRV increased by 15% over the past week",
      "Takeaway 2: Stress levels peaked during afternoon hours",
      "Takeaway 3: Sleep quality correlates with morning recovery metrics"
    ],
    "insights_used": [
      "Average HRV increased by 15% over the past week",
      "Stress levels peaked during afternoon hours",
      "Sleep quality correlates with morning recovery metrics"
    ],
    "tone": "professional",
    "length": "medium",
    "timestamp": "2024-11-01T12:00:00"
  },
  "success": true
}
```

**字段说明：**
- `agent`: Agent名称
- `result`: 叙事结果
  - `narrative`: 完整的叙事文本
  - `summary`: 简洁摘要
  - `key_takeaways`: 关键要点列表（最多3个）
  - `insights_used`: 使用的洞察列表
  - `tone`: 语调 ("professional", "casual", "technical")
  - `length`: 长度 ("short", "medium", "long")
  - `timestamp`: 生成时间戳
- `success`: 操作是否成功

返回结果中的关键字段：
- `explanation`: 主叙述文本
- `narrative`: 详细 narrative（在使用 OpenAI 时与 explanation 相同）
- `model`: 使用的模型（OpenAI or 模拟）
- `data_analyzed`: 参与分析的记录数与指标列表
- `key_insights`: 关键洞察列表（最多5条）
- `mirror_story`: Energy Insight 模式专属输出，包含 `summary`、`energy_pattern`、`top_dialog` 等字段
 - `timestamp`: 生成时间戳

---

### AuroraCoreAgent

核心协调代理，根据查询类型协调所有子代理。

**调用方式：**
```python
from agents.core_agent import AuroraCoreAgent

agent = AuroraCoreAgent()
result = agent.run("analyze and visualize my HRV data", query_type="combined")
```

**返回结构（combined类型示例）：**
```json
{
  "agent": "AuroraCoreAgent",
  "result": {
    "query": "analyze and visualize my HRV data",
    "query_type": "combined",
    "timestamp": "2024-11-01T12:00:00",
    "agents_executed": [
      "DataAgent",
      "VizAgent",
      "NarrativeAgent"
    ],
    "analysis": {
      "agent": "DataAgent",
      "result": { /* DataAgent 返回结构 */ },
      "success": true
    },
    "visualization": {
      "agent": "VizAgent",
      "result": { /* VizAgent 返回结构 */ },
      "success": true
    },
    "narrative": {
      "agent": "NarrativeAgent",
      "result": { /* NarrativeAgent 返回结构 */ },
      "success": true
    },
    "summary": "Query processed successfully using 3 agent(s).\nQuery type: combined\nAgents executed: DataAgent, VizAgent, NarrativeAgent",
    "success": true
  },
  "success": true
}
```

**返回结构（Energy Insight 模式示例）：**
```json
{
  "insight": "你正在保持专注，但恢复速度略低于平均。",
  "hero": {
    "greeting": "早安，今天的心率节奏较平稳。想听听你的身体在说什么吗？",
    "quick_prompts": ["我今天有点累。", "我还不错。", "查看今日镜。"],
    "top_dialog": "早安，旅人。你的系统正以温柔的节奏醒来，让我们一起倾听身体和心的低语。",
    "mirror_summary": "你的 Purpose 指标与恢复周期高度相关，说明意义感驱动了你的神经平衡。"
  },
  "data": {
    "coordination_score": 78,
    "insight_summary": "你正在保持专注，但恢复速度略低于平均。",
    "mirror_layers": { "physiology": { "title": "Physiology", "metrics": [...] }, "mind": {"...": "..."}, "meaning": {"...": "..."} },
    "mirror_trend": [
      {"date": "11-01", "hrv": 52.1, "stress": 38.5, "focus": 64.2},
      {"date": "11-02", "hrv": 51.4, "stress": 39.9, "focus": 66.0}
    ],
    "energy_pattern": "过去 3 天你的心率变异性下降，但专注指数上升。你的身体在努力跟上你的意志力。"
  },
  "chart": {
    "chart_type": "mirror_trend",
    "plotly_json": { "data": [...], "layout": {...}, "config": {...} }
  }
}
```

**Energy Insight 模式字段说明补充：**
- `hero`: Hero 输入区的动态文案配置。
- `data.mirror_layers`: 三层视图结构，供前端展示 Physiology/Mind/Meaning 指标。
- `data.mirror_trend`: HRV / Stress / Focus 趋势数据，供 VizAgent 渲染折线图。
- `data.energy_pattern`: NarrativeAgent 生成的情绪化长文案。
- `chart.chart_type`: Energy Insight 模式下为 `mirror_trend`。

**字段说明：**
- `agent`: Agent名称
- `result`: 协调结果
  - `query`: 原始查询
  - `query_type`: 查询类型 ("analysis", "visualization", "explanation", "combined")
  - `timestamp`: 处理时间戳
  - `agents_executed`: 执行的Agent列表
  - `analysis`: DataAgent返回结果（如果执行）
  - `visualization`: VizAgent返回结果（如果执行）
  - `narrative`: NarrativeAgent返回结果（如果执行）
  - `summary`: 执行摘要
  - `success`: 是否成功
- `success`: 整体操作是否成功

**查询类型说明：**
- `analysis`: 仅执行DataAgent
- `visualization`: 执行DataAgent + VizAgent
- `explanation`: 执行DataAgent + NarrativeAgent
- `combined`: 执行所有Agent（DataAgent + VizAgent + NarrativeAgent）

**自动检测关键词：**
- **Analysis**: "analyze", "analysis", "statistics", "stats", "calculate", "compute", "process", "data"
- **Visualization**: "visualize", "visualization", "chart", "graph", "plot", "show", "display", "diagram", "visual"
- **Explanation**: "explain", "explanation", "describe", "story", "narrative", "tell", "summary", "interpret"

---

## 数据文件格式

### mock_hrv_data.csv

DataAgent使用的CSV数据文件格式。

**文件结构：**
```csv
id,hrv,stress_score,age
1,45.2,25,28
2,52.8,15,32
3,38.5,45,25
4,61.3,10,35
5,49.7,30,30
...
```

**列说明：**
- `id`: 记录唯一标识符（整数）
- `hrv`: 心率变异性值（浮点数）
- `stress_score`: 压力评分（整数，范围通常 0-100）
- `age`: 年龄（整数）

---

## 更新日志

- **2024-11-01**: 初始版本，包含所有Agent和API端点的数据结构定义
- **2024-11-01**: 添加DataAgent的详细结构，包括按压力水平分组的HRV统计

---

## 注意事项

1. 所有时间戳使用ISO 8601格式：`YYYY-MM-DDTHH:MM:SS`
2. 所有数值保留2位小数（除非特别说明）
3. 相关性系数范围：-1.0 到 1.0
4. Agent返回结构统一包含 `agent`, `result`, `success` 字段
5. 数据结构可能在开发过程中调整，请定期查看此文档

---

## 贡献指南

当添加新的API端点或Agent时，请：
1. 在此文档中添加相应的数据结构定义
2. 包含完整的请求/响应示例
3. 说明字段含义和数据类型
4. 更新更新日志

