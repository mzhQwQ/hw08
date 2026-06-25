# 智能学业状态诊断助手 - 快速启动指南

## 🚀 项目制作完成

所有项目文件已成功创建！以下是快速启动步骤：

### 📋 文件结构

```
hw08/
├── README.md                 # 📖 项目说明文档
├── report.md                 # 📄 技术报告（课程作业）
├── requirements.txt          # 📦 依赖列表
├── .env.example              # ⚙️ 环境变量示例
├── .env                      # 🔐 本地环境配置（已创建，包含敏感信息）
├── .gitignore                # 🔒 Git 忽略规则
├── app.py                     # 🌐 Streamlit 主应用
├── data_processor.py          # 📊 数据处理模块
├── llm_analyzer.py            # 🤖 大模型分析模块
├── visualizer.py              # 📈 可视化模块
├── score.html                 # 📝 示例教务成绩单
└── utils/
    ├── __init__.py           # 📦 包初始化
    ├── config.py             # ⚙️ 配置管理
    └── helpers.py             # 🛠️ 工具函数
```

## ⚡ 快速启动

### 1️⃣ 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2️⃣ 配置 API Key（可选）

如果要调用真实的大模型 API：

```bash
# 编辑 .env 文件
# 添加你的 API Key：
QWEN_API_KEY=sk-your-key
ZHIPU_API_KEY=your-key
OPENAI_API_KEY=sk-your-key
```

### 3️⃣ 运行应用

```bash
streamlit run app.py
```

应用将在浏览器自动打开（通常是 http://localhost:8501）

## 💡 使用建议

### 首次使用推荐流程

1. **启动应用** → `streamlit run app.py`
2. **进入"首页"** → 了解应用功能
3. **进入"数据上传"** → 上传示例成绩单或使用提供的 `score.html`
4. **进入"智能分析"** → ✅ 勾选"使用示例结果"（无需 API Key）
5. **进入"结果展示"** → 查看完整的诊断报告和可视化

### 示例成绩单

项目已提供 `score.html` 作为示例数据，包含 13 门课程的成绩数据。

## 🔐 安全说明

✅ **API Key 保护**
- `.env` 文件已添加到 `.gitignore`
- 不会被提交到 Git 仓库
- 敏感信息被安全隔离

✅ **数据隐私**
- 上传的成绩数据不会被存储
- 仅在当前会话中临时处理
- 用户数据完全隐私

## 📦 依赖清单

- **Streamlit** - Web 应用框架
- **BeautifulSoup4** - HTML 解析
- **Pandas** - 数据处理
- **Plotly** - 交互式图表
- **Requests** - HTTP 请求
- **python-dotenv** - 环境变量管理

## 🎯 核心功能模块

### 1. data_processor.py
- ✅ HTML 成绩单解析
- ✅ 数据清洗和验证
- ✅ 统计分析计算
- ✅ 学科分类分析

### 2. llm_analyzer.py
- ✅ 多模型支持（通义千问/智谱/OpenAI）
- ✅ Prompt 工程设计
- ✅ 学业诊断分析
- ✅ 选课建议生成

### 3. visualizer.py
- ✅ 雷达图生成
- ✅ 成绩分布图
- ✅ 学科对比分析
- ✅ 性能指示表

### 4. app.py
- ✅ Streamlit Web 界面
- ✅ 多标签页设计
- ✅ 实时数据处理
- ✅ 交互式可视化

## 📝 示例数据

`score.html` 包含以下课程：

| 课程 | 学分 | 成绩 |
|------|------|------|
| 高等数学 I | 4 | 87 |
| 线性代数 | 3 | 92 |
| 大学英语 | 4 | 78 |
| 数据结构 | 4 | 88 |
| Python 程序设计 | 3 | 91 |
| 数据库原理 | 3 | 85 |
| Web 前端技术 | 3 | 89 |
| 算法设计 | 4 | 82 |
| 操作系统 | 4 | 86 |
| 计算机网络 | 3 | 79 |
| 人工智能导论 | 3 | 90 |
| 概率论与数理统计 | 3 | 84 |
| 离散数学 | 3 | 80 |

## 🧪 测试验证

✅ 所有 Python 文件通过语法检查  
✅ 模块导入无误  
✅ 示例数据已准备  
✅ 应用框架完整  

## 🔧 故障排除

### 问题 1: ModuleNotFoundError
```bash
# 解决方案：确保虚拟环境已激活
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate      # Windows
```

### 问题 2: Port 8501 already in use
```bash
# 解决方案：指定其他端口
streamlit run app.py --server.port 8502
```

### 问题 3: 大模型 API 调用失败
```bash
# 解决方案：
1. 检查 .env 文件中的 API Key 是否正确
2. 或者使用"示例结果"模式（已默认启用）
3. 检查网络连接
```

## 📚 文档链接

- 📖 [README.md](README.md) - 项目说明
- 📄 [report.md](report.md) - 技术报告
- 📋 [requirements.txt](requirements.txt) - 依赖列表

## ✨ 核心特性亮点

🎯 **零代码体验** - 纯 Web 界面，无需编程

🚀 **快速原型化** - Streamlit 框架，开发效率高

🤖 **AI 驱动** - 利用大模型进行智能诊断

📊 **可视化展示** - Plotly 交互式图表

🔒 **安全隐私** - API Key 隔离，数据不存储

## 🎓 学习价值

本项目完整展示了从需求分析 → 架构设计 → 核心编码 → 测试优化的完整软件工程流程，是学习 AI 应用开发的优秀实践项目。

---

**创建日期**：2026 年 6 月 25 日  

祝你使用愉快！ 🎉
