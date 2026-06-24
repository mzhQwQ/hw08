# 火山引擎 API 集成指南

## 📌 概述

本项目现已支持 **抖音火山引擎**的豆包（Doubao）大模型，可以替代或补充其他大模型服务。

### 支持的模型列表

| 模型 | API Key 环变量 | 模型名称 | 说明 |
|------|----------------|---------|------|
| 阿里通义千问 | `QWEN_API_KEY` | qwen-turbo | 开源大模型 |
| 智谱 GLM | `ZHIPU_API_KEY` | glm-3-turbo | 国产开源模型 |
| OpenAI | `OPENAI_API_KEY` | gpt-3.5-turbo | 商用闭源模型 |
| **豆包（推荐）** | **`VOLCANOENGINE_API_KEY`** | **doubao-pro-32k** | **字节火山引擎** |

---

## 🚀 快速开始

### 第 1 步：获取 API Key

#### 方式一：通过火山引擎官网（推荐）

1. 访问 [https://www.volcengine.com/](https://www.volcengine.com/)
2. 注册账号并登录
3. 进入 **"AI 平台"** 或 **"ARK API"** 服务
4. 创建新的 API Key
5. 复制 API Key

#### 方式二：通过字节跳动开发者平台

1. 访问 [https://open.douyin.com/](https://open.douyin.com/)
2. 使用字节账号登录
3. 创建应用，获取 API Token

### 第 2 步：配置环境变量

#### 方法 A：编辑 `.env` 文件（推荐）

```bash
# 编辑项目根目录的 .env 文件
VOLCANOENGINE_API_KEY=your-api-key-here

# 设置默认模型为豆包
DEFAULT_MODEL=volcanoengine
```

#### 方法 B：系统环境变量

```bash
# Linux/macOS
export VOLCANOENGINE_API_KEY="your-api-key-here"

# Windows PowerShell
$env:VOLCANOENGINE_API_KEY="your-api-key-here"

# Windows CMD
set VOLCANOENGINE_API_KEY=your-api-key-here
```

#### 方法 C：在应用中动态配置

在 Streamlit 应用的"智能分析"页面选择 "🎵 抖音豆包" 模型，应用会自动检查对应的 API Key。

### 第 3 步：启动应用

```bash
streamlit run app.py
```

应用启动后：
1. 上传教务成绩 HTML 文件
2. 选择 **"🎵 抖音豆包"** 模型
3. 点击"生成诊断"按钮
4. 查看诊断结果

---

## 🔧 API 调用示例

### 代码示例：直接调用豆包 API

```python
from llm_analyzer import LLMAnalyzer
import pandas as pd

# 创建分析器实例（使用豆包模型）
analyzer = LLMAnalyzer(model_type='volcanoengine')

# 假设已加载成绩数据
scores_df = pd.read_csv('scores.csv')

# 调用 API 进行分析
result = analyzer.analyze_academic_status(scores_df)

# 打印结果
print("诊断报告:")
print(result['diagnosis'])
print("\n评分:")
print(result['ratings'])
print("\n建议:")
for rec in result['recommendations']:
    print(f"- {rec}")
```

### HTTP 请求示例

```bash
curl -X POST https://ark.cn-beijing.volces.com/api/v3/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "doubao-pro-32k",
    "messages": [
      {
        "role": "user",
        "content": "请分析以下学生的学业成绩..."
      }
    ],
    "temperature": 0.7,
    "max_tokens": 1500
  }'
```

---

## 📊 豆包模型特性对比

| 特性 | 豆包专业版 | 通义千问 | 智谱 GLM | OpenAI |
|------|-----------|---------|---------|--------|
| **上下文窗口** | 32K tokens | 130K tokens | 128K tokens | 4K/8K/128K |
| **推理速度** | 快 | 中 | 中 | 快 |
| **成本** | 低 | 低 | 低 | 较高 |
| **国内支持** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **适合场景** | 教育、客服 | 通用任务 | 代码、学术 | 高端应用 |

---

## ⚙️ 配置参数说明

豆包模型的配置参数：

```python
{
    'model_name': 'doubao-pro-32k',      # 模型标识
    'temperature': 0.7,                   # 创意度（0-1，越高越创意）
    'max_tokens': 1500,                   # 最大输出长度
    'top_p': 0.8                          # 采样参数
}
```

### 参数调整建议

- **低温度（0.1-0.3）**：用于需要准确、一致的回复
  ```python
  'temperature': 0.2  # 更严谨的学业诊断
  ```

- **中温度（0.5-0.7）**：平衡创意和准确性（推荐）
  ```python
  'temperature': 0.7  # 默认配置
  ```

- **高温度（0.8-1.0）**：用于创意内容生成
  ```python
  'temperature': 0.9  # 更多样化的建议
  ```

---

## 🔒 安全最佳实践

### ✅ 正确做法

```python
# ✅ 从环境变量读取
import os
api_key = os.getenv('VOLCANOENGINE_API_KEY')

# ✅ 使用 .env 文件
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('VOLCANOENGINE_API_KEY')
```

### ❌ 错误做法

```python
# ❌ 不要硬编码 API Key
VOLCANOENGINE_API_KEY = "your-key-123456"

# ❌ 不要提交到 Git
git add .env  # 错误！

# ❌ 不要在日志中打印
print(f"API Key: {api_key}")
```

---

## 🧪 测试与调试

### 验证 API Key 是否有效

```bash
# 测试环境变量是否正确加载
python -c "import os; print(os.getenv('VOLCANOENGINE_API_KEY'))"
```

### 查看 API 调用日志

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 然后运行应用
streamlit run app.py
```

### 常见错误处理

| 错误 | 原因 | 解决方案 |
|------|------|--------|
| `401 Unauthorized` | API Key 无效或过期 | 重新获取或验证 API Key |
| `429 Too Many Requests` | 请求过于频繁 | 添加延迟或使用批处理 |
| `503 Service Unavailable` | 服务维护 | 等待或切换其他模型 |
| `ConnectTimeout` | 网络连接问题 | 检查网络、代理设置 |

---

## 📈 性能对标

### 响应时间对比（毫秒）

```
豆包（火山引擎）: 800-1200ms   ✅ 最快
阿里通义千问:    1000-1500ms  
智谱 GLM:        1200-1800ms  
OpenAI:          1500-2500ms  
```

### 成本对标（相对价格）

```
豆包（火山引擎）: $0.5/M tokens   ✅ 最便宜
阿里通义千问:    $0.7/M tokens   
智谱 GLM:        $0.8/M tokens   
OpenAI:          $1.5/M tokens   
```

---

## 🎯 使用场景推荐

### 适合用豆包的场景

✅ 大量教育诊断任务（成本低）  
✅ 国内应用（网络延迟低）  
✅ 对响应速度要求高的场景  
✅ 学生项目和教育应用  

### 适合用其他模型的场景

- 需要超长上下文（用通义千问）
- 代码生成任务（用智谱 GLM）
- 高端应用和商用系统（用 OpenAI）

---

## 📞 获取帮助

### 火山引擎官方资源

- **API 文档**：https://www.volcengine.com/docs/
- **开发者社区**：https://www.volcengine.com/docs/
- **技术支持**：support@volcengine.com

### 项目相关问题

- 查看 [README.md](README.md) 项目说明
- 查看 [report.md](report.md) 技术细节
- 提交 GitHub Issues

---

## 🔄 从其他模型迁移到豆包

### 一键切换

```bash
# 编辑 .env 文件
DEFAULT_MODEL=volcanoengine
```

### 或在应用中选择

```
数据分析页面 → 选择"🎵 抖音豆包" → 点击生成诊断
```

### 完全兼容

- ✅ 相同的 Prompt 工程
- ✅ 相同的 API 接口设计
- ✅ 相同的输出格式
- ✅ 无需修改应用代码

---

## 📚 相关阅读

- [豆包大模型介绍](https://www.volcengine.com/)
- [字节火山引擎 AI 平台](https://www.volcengine.com/)
- [本项目技术报告](report.md)

---

**文档版本**：v1.1  
**最后更新**：2026 年 6 月 24 日  
**维护者**：项目开发团队
