# 火山引擎快速参考卡片

## 🎯 3 步集成火山引擎

### ① 获取 API Key
访问 https://www.volcengine.com → 注册 → 创建 API Key → 复制

### ② 配置密钥
编辑 `.env` 文件：
```
VOLCANOENGINE_API_KEY=your-key-here
DEFAULT_MODEL=volcanoengine
```

### ③ 启动应用
```bash
streamlit run app.py
```

---

## 🔄 模型切换

### 通过 UI 切换
应用 → 智能分析 → 下拉框选择 "🎵 抖音豆包"

### 通过代码切换
```python
from llm_analyzer import LLMAnalyzer

analyzer = LLMAnalyzer(model_type='volcanoengine')
result = analyzer.analyze_academic_status(df)
```

---

## 📊 豆包 vs 其他模型

| | 豆包 | 通义千问 | 智谱 GLM | OpenAI |
|---|------|--------|---------|--------|
| 速度 | 🚀 快 | 中 | 中 | 快 |
| 成本 | 💰 低 | 低 | 低 | 高 |
| 国内 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |

---

## 🔧 常用配置

### 参数调优

```python
# 严谨的诊断（低创意度）
'temperature': 0.3

# 均衡配置（推荐）
'temperature': 0.7

# 创意建议（高创意度）
'temperature': 0.9
```

### 环变量

```bash
# 必需
VOLCANOENGINE_API_KEY=your-key

# 可选
DEFAULT_MODEL=volcanoengine
STREAMLIT_SERVER_PORT=8501
```

---

## ❌ 常见错误处理

| 错误 | 解决方案 |
|------|--------|
| `401 Unauthorized` | 检查 API Key 是否正确 |
| `ConnectTimeout` | 检查网络连接 |
| `429 Too Many Requests` | 等待后重试或购买更高额度 |
| `模块未找到` | 运行 `pip install -r requirements.txt` |

---

## 📱 完整流程

```
1️⃣ 上传成绩 HTML
   ↓
2️⃣ 选择豆包模型
   ↓
3️⃣ 点击生成诊断
   ↓
4️⃣ 查看诊断报告
   ↓
5️⃣ 导出结果
```

---

## 🎓 使用场景

✅ 教育应用  
✅ 成本敏感项目  
✅ 国内用户优先  
✅ 实时响应场景  

---

## 📚 详细文档

- **完整指南**：`VOLCANOENGINE_GUIDE.md`
- **集成报告**：`VOLCANOENGINE_INTEGRATION.md`
- **项目说明**：`README.md`

---

## 💡 技巧

```bash
# 查看已配置的 API Key
python -c "import os; print(os.getenv('VOLCANOENGINE_API_KEY'))"

# 测试 API 连接
python -c "from llm_analyzer import LLMAnalyzer; \
    analyzer = LLMAnalyzer(model_type='volcanoengine'); \
    print('✅ 连接成功')"

# 快速切换模型
sed -i 's/DEFAULT_MODEL=.*/DEFAULT_MODEL=volcanoengine/' .env
```

---

**最后更新**：2026-06-24
