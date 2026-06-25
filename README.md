# 智能学业状态诊断助手

*一个基于大模型的教务数据分析与选课建议系统*

---

## 📋 项目简介

**智能学业状态诊断助手**是一款利用生成式AI和数据可视化技术，为高校学生提供个性化学业评估和选课指导的智能应用。通过解析教务系统成绩数据，系统能够：

- 📊 **智能评分**：基于大模型分析，生成学生学业状态的多维度雷达图评分
- 💡 **选课建议**：结合成绩、偏好和课程特性，生成个性化选课推荐方案
- 🎯 **学业诊断**：识别学生的强弱学科，提供针对性的改进建议
- 🚀 **零代码体验**：Streamlit 驱动，无需编程即可交互使用

## 🎬 项目演示

[![演示视频](https://img.shields.io/badge/视频演示-YouTube-red?style=flat-square)](https://www.youtube.com/watch?v=your_video_id)
*演示视频链接（待更新）*

## 📁 目录结构

```
hw08/
├── README.md                 # 项目说明文档
├── report.md                 # 课程作业技术报告
├── requirements.txt          # Python 依赖列表
├── .env.example              # 环境变量配置示例
├── score.html                # 示例教务成绩数据（HTML格式）
├── app.py                     # Streamlit 应用主入口
├── data_processor.py          # 数据提取与处理模块
├── llm_analyzer.py            # 大模型分析接口模块
├── visualizer.py              # 可视化生成模块
└── utils/
    ├── __init__.py
    ├── config.py              # 配置管理
    └── helpers.py              # 工具函数
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- pip 或 conda 包管理器

### 安装步骤

#### 1. 克隆项目
```bash
git clone https://github.com/yourusername/hw08.git
cd hw08
```

#### 2. 创建虚拟环境（推荐）
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

#### 3. 安装依赖
```bash
pip install -r requirements.txt
```

#### 4. 配置环境变量
```bash
# 复制示例配置文件
cp .env.example .env

# 编辑 .env 文件，添加你的 API Key（敏感信息已从仓库中排除）
# 支持的大模型：
#   - 通义千问：QWEN_API_KEY
#   - 智谱 GLM：ZHIPU_API_KEY
#   - OpenAI：OPENAI_API_KEY
#   - 豆包（火山引擎）：VOLCANOENGINE_API_KEY
```

#### 5. 一键运行
```bash
streamlit run app.py
```

应用将自动在浏览器中打开，地址：`http://localhost:8501`

### 使用流程

1. **上传成绩文件**：在侧边栏选择本地 `score.html` 教务成绩文件
2. **智能分析**：点击"生成诊断"，系统将调用大模型进行分析
3. **查看结果**：
   - 📈 学业状态雷达图评分
   - 💬 个性化学业诊断报告
   - 📚 个性化选课建议方案

## 📊 效果摘要

### 核心功能演示

| 功能模块 | 功能描述 | 输出形式 |
|---------|--------|--------|
| 数据提取 | 自动解析 HTML 教务成绩单 | 结构化成绩数据表 |
| 智能分析 | 调用大模型进行多维度评估 | 诊断报告 (Markdown) |
| 雷达评分 | 生成学业状态多维评分 | 交互式雷达图 |
| 选课建议 | 基于成绩的个性化推荐 | 选课方案列表 |

### 关键特性

✅ **自动化数据处理**：一次上传，智能提取所有课程信息  
✅ **多模型支持**：兼容主流国内外大模型 API  
✅ **敏感信息保护**：API Key 通过环境变量管理，未提交仓库  
✅ **可视化展示**：Plotly 交互式图表，美观易用  
✅ **零配置启动**：一条命令运行完整系统  

## 🔐 安全说明

- **API Key 管理**：所有敏感密钥存储在 `.env` 文件中，已添加到 `.gitignore`
- **数据隐私**：本地处理，不存储用户成绩数据
- **开源依赖**：所有依赖均在 `requirements.txt` 中明确列出

## 🛠️ 技术栈

| 技术 | 说明 |
|------|------|
| Python 3.8+ | 核心编程语言 |
| Streamlit | Web 应用框架 |
| BeautifulSoup4 | HTML 数据提取 |
| Plotly | 交互式数据可视化 |
| Requests | HTTP 请求库 |
| Python-dotenv | 环境变量管理 |
| 大模型 API | 通义千问 / 智谱 GLM / OpenAI / 豆包 |

## 📝 依赖清单

完整的项目依赖请参考 [requirements.txt](requirements.txt)。主要依赖包括：

```
streamlit>=1.28.0
beautifulsoup4>=4.12.0
requests>=2.31.0
plotly>=5.17.0
python-dotenv>=1.0.0
pandas>=2.0.0
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📞 联系方式

如有问题或建议，欢迎通过以下方式联系：
- 提交 GitHub Issues
- 发送邮件至 [1849284893@qq.com]

---

**最后更新**：2026 年 6 月 25 日  