# 🚀 运行和调试程序完整指南

## 📖 目录

1. [快速开始](#快速开始) - 3 分钟上手
2. [完整安装步骤](#完整安装步骤) - 详细步骤
3. [运行应用](#运行应用) - 启动和使用
4. [调试指南](#调试指南) - 问题排查
5. [常见错误](#常见错误) - 解决方案
6. [高级调试](#高级调试) - 深度调试

---

## 🎯 快速开始

### 第 1 步：安装依赖（1 分钟）

```bash
# 进入项目目录
cd b:\Projects\hw08\hw08

# 安装所有依赖
pip install -r requirements.txt
```

### 第 2 步：配置 API Key（1 分钟）

编辑 `.env` 文件，填入你的 API Key：

```bash
# 方法 1: 用记事本打开
notepad .env

# 方法 2: 用 VS Code 打开
code .env
```

**需要至少配置一个模型的 API Key：**

```env
# 推荐：抖音豆包（最便宜、最快）
VOLCANOENGINE_API_KEY=your-key-here

# 或其他模型之一
QWEN_API_KEY=sk-xxx
ZHIPU_API_KEY=xxx
OPENAI_API_KEY=sk-xxx
```

### 第 3 步：启动应用（1 分钟）

```bash
# Windows PowerShell
streamlit run app.py

# 自动打开浏览器，访问 http://localhost:8501
```

✅ **完成！** 应用现在运行中

---

## 📋 完整安装步骤

### 1. 创建虚拟环境（推荐）

```bash
# 进入项目目录
cd b:\Projects\hw08\hw08

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate
```

**激活成功的标志**：命令行前出现 `(venv)` 前缀

```
(venv) PS b:\Projects\hw08\hw08>
```

### 2. 升级 pip（可选但推荐）

```bash
python -m pip install --upgrade pip
```

### 3. 安装依赖包

```bash
# 从 requirements.txt 安装
pip install -r requirements.txt

# 或单独安装核心依赖
pip install streamlit streamlit-option-menu beautifulsoup4 requests plotly python-dotenv pandas lxml
```

**验证安装成功：**

```bash
# 查看已安装的包
pip list

# 应该显示：
# streamlit                 1.28.1+
# streamlit-option-menu     0.3.6+
# beautifulsoup4           4.12.2+
# requests                 2.31.0+
# plotly                   5.17.0+
# python-dotenv            1.0.0+
# pandas                   2.0.3+
# lxml                     4.9.3+
```

### 4. 配置环境变量

#### 方法 A：编辑 `.env` 文件（推荐）

```bash
# 用 VS Code 打开
code .env

# 或用记事本打开
notepad .env
```

**模板内容：**

```env
# ========== 必须配置至少一个 ==========

# 方案 1：抖音豆包（推荐）⭐⭐⭐⭐⭐
VOLCANOENGINE_API_KEY=ark-xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# 方案 2：阿里通义千问
QWEN_API_KEY=sk-xxxxxxxxxxxxxxx

# 方案 3：智谱 GLM
ZHIPU_API_KEY=xxxxxxxxxxxxxxx

# 方案 4：OpenAI GPT
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxx
```

#### 方法 B：直接设置环境变量（不推荐）

```bash
# Windows PowerShell
$env:VOLCANOENGINE_API_KEY = "your-api-key"
$env:QWEN_API_KEY = "your-api-key"

# 只对当前会话有效
```

---

## ▶️ 运行应用

### 基本运行

```bash
# 确保虚拟环境已激活
# (venv) 前缀应该在命令行前

# 启动应用
streamlit run app.py
```

**输出示例：**

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501

  For better performance, install Watchdog: pip install watchdog
```

### 在浏览器中使用

1. **首页 (Home)**
   - 查看项目信息
   - 了解功能特性

2. **上传成绩 (Upload)**
   - 上传 HTML 成绩单
   - 或使用示例数据
   - 预览已上传的数据

3. **生成诊断 (Analysis)**
   - 选择大模型（4 种可选）
   - 配置分析参数
   - 点击"生成诊断"

4. **查看结果 (Results)**
   - 📊 诊断报告
   - 📈 数据统计
   - 🎯 成绩分析
   - 💡 改进建议
   - 📥 导出数据

5. **帮助 (Help)**
   - 常见问题解答
   - 使用指南

### 停止应用

按 `Ctrl + C` 停止应用

---

## 🔍 调试指南

### 方式 1：Streamlit 日志调试

#### 启用详细日志

```bash
# 运行时显示详细信息
streamlit run app.py --logger.level=debug
```

#### 查看控制台输出

应用运行时，在 **Streamlit 启动的终端** 中查看实时日志：

```
2026-06-24 10:30:45.123 log - Session started
2026-06-24 10:30:46.456 log - File uploaded: score.html
2026-06-24 10:30:47.789 log - Analysis started with model: volcanoengine
```

### 方式 2：VS Code 调试

#### 配置调试器

1. **创建调试配置** - 在 VS Code 中：
   - 按 `F5` 或点击 Run & Debug
   - 选择 "Create a launch.json file"
   - 选择 "Python"

2. **添加 Streamlit 调试配置** - 编辑 `.vscode/launch.json`：

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Streamlit",
            "type": "python",
            "module": "streamlit.cli",
            "args": [
                "run",
                "app.py"
            ],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```

3. **启动调试**：
   - 按 `F5` 启动调试器
   - 设置断点
   - 单步执行代码

### 方式 3：Python 脚本调试

创建测试脚本 `test_app.py`：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '.')

from data_processor import ScoreDataProcessor
from llm_analyzer import LLMAnalyzer
from visualizer import Visualizer
import pandas as pd

def test_data_processor():
    """测试数据处理模块"""
    print("=" * 60)
    print("🔧 测试 1: 数据处理模块")
    print("=" * 60)
    
    processor = ScoreDataProcessor()
    html_content = processor.create_sample_html()
    
    # 解析 HTML
    df = processor.parse_score_html(html_content)
    print(f"✅ 成功解析 {len(df)} 门课程")
    print(f"\n课程列表：")
    print(df.to_string())
    
    # 计算统计信息
    stats = processor.get_statistics(df)
    print(f"\n📊 统计信息：")
    print(f"  - 平均分：{stats['average_score']:.2f}")
    print(f"  - 加权GPA：{stats['weighted_gpa']:.2f}")
    print(f"  - 成绩范围：{stats['min_score']} - {stats['max_score']}")
    
    return df

def test_llm_analyzer(df):
    """测试 LLM 分析模块"""
    print("\n" + "=" * 60)
    print("🔧 测试 2: LLM 分析模块")
    print("=" * 60)
    
    try:
        # 创建分析器
        analyzer = LLMAnalyzer(model_type='volcanoengine')
        print(f"✅ 已创建分析器：{analyzer.model_type}")
        
        # 生成分析
        print("\n⏳ 正在调用 LLM API...")
        result = analyzer.analyze_academic_status(df)
        
        if result:
            print("\n✅ API 调用成功！")
            print(f"\n📋 分析结果（前 500 字）：")
            print(result[:500] + "...")
        else:
            print("❌ API 调用失败或返回空结果")
            
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()

def test_visualizer(df):
    """测试可视化模块"""
    print("\n" + "=" * 60)
    print("🔧 测试 3: 可视化模块")
    print("=" * 60)
    
    try:
        visualizer = Visualizer()
        print("✅ 已创建可视化器")
        
        # 测试各种图表
        charts = {
            '雷达图': visualizer.generate_radar_chart(df),
            '成绩分布': visualizer.generate_score_distribution_chart(df),
            '科目比较': visualizer.generate_subject_comparison_chart(df),
            '成绩进展': visualizer.generate_gpa_progress_chart(df),
            '性能仪表': visualizer.generate_performance_gauge(df),
        }
        
        for name, chart in charts.items():
            if chart:
                print(f"  ✅ {name} 生成成功")
            else:
                print(f"  ❌ {name} 生成失败")
                
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("\n" + "🧪 智能学业诊断助手 - 模块测试")
    
    # 运行测试
    try:
        df = test_data_processor()
        test_llm_analyzer(df)
        test_visualizer(df)
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
```

**运行测试脚本：**

```bash
# 激活虚拟环境
venv\Scripts\activate

# 运行测试
python test_app.py
```

### 方式 4：验证集成脚本

使用已有的验证脚本：

```bash
python verify_volcanoengine.py
```

**输出示例：**

```
🧪 火山引擎集成验证工具 v1.0
========================================================
✅ Python 3.13.13 - 符合要求
✅ utils/config.py - 已集成火山引擎支持
✅ llm_analyzer.py - 已集成火山引擎支持
✅ app.py - 已集成火山引擎支持
```

---

## ❌ 常见错误

### 错误 1: "ModuleNotFoundError: No module named 'streamlit'"

**原因**：未安装依赖

**解决方案**：

```bash
# 确保虚拟环境已激活（看到 (venv) 前缀）
pip install -r requirements.txt
```

### 错误 2: "VOLCANOENGINE_API_KEY 未配置"

**原因**：`.env` 文件中没有设置有效的 API Key

**解决方案**：

```bash
# 编辑 .env 文件
code .env

# 添加有效的 API Key
VOLCANOENGINE_API_KEY=ark-your-actual-key-here
```

### 错误 3: "Port 8501 is already in use"

**原因**：已有应用占用 8501 端口

**解决方案**：

```bash
# 方法 1：使用不同的端口
streamlit run app.py --server.port 8502

# 方法 2：杀死占用进程
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### 错误 4: "FileNotFoundError: score.html"

**原因**：缺少示例文件

**解决方案**：

```bash
# 在应用首页选择"使用示例数据"而不是上传文件
# 或重新生成示例数据
python data_processor.py  # 生成示例 HTML
```

### 错误 5: "API 调用超时"

**原因**：网络问题或 API 服务不可用

**解决方案**：

```bash
# 1. 检查网络连接
ping www.volcengine.com

# 2. 验证 API Key
# 在火山引擎控制台检查 API Key 是否有效

# 3. 增加超时时间
# 编辑 llm_analyzer.py，修改 requests 的 timeout 参数
```

### 错误 6: "编码错误: 'gbk' codec can't decode"

**原因**：文件编码问题（Windows 默认 GBK）

**解决方案**：

```bash
# 确保所有 Python 文件保存为 UTF-8 编码
# 在 VS Code 中：
# 1. 右下角点击编码（可能显示 "GBK"）
# 2. 选择 "UTF-8"
# 3. 保存文件
```

---

## 🔬 高级调试

### 1. 添加调试日志

在 `app.py` 中添加日志：

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 在代码中使用
logger.debug(f"正在处理文件：{filename}")
logger.info(f"成功解析 {rows} 行数据")
logger.error(f"API 调用失败：{error}")
```

### 2. 性能分析

```python
import time

# 测试函数执行时间
start = time.time()
result = analyzer.analyze_academic_status(df)
elapsed = time.time() - start

print(f"⏱️ 执行时间：{elapsed:.2f} 秒")
```

### 3. 内存分析

```bash
# 安装内存分析工具
pip install memory-profiler

# 分析脚本
python -m memory_profiler app.py
```

### 4. API 调试

创建文件 `debug_api.py`：

```python
import requests
import json
from utils.config import Config

def test_volcanoengine_api():
    """测试火山引擎 API 连接"""
    
    api_key = Config.VOLCANOENGINE_API_KEY
    api_url = Config.VOLCANOENGINE_API_URL
    
    print(f"🔍 测试火山引擎 API")
    print(f"  API URL: {api_url}")
    print(f"  API Key: {api_key[:20]}...")
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': 'doubao-pro-32k',
        'messages': [
            {
                'role': 'user',
                'content': '你好，请简短回复。'
            }
        ],
        'temperature': 0.7,
        'max_tokens': 100
    }
    
    try:
        print(f"\n📤 发送请求...")
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        
        print(f"📥 收到响应")
        print(f"  状态码: {response.status_code}")
        print(f"  响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ API 调用成功！")
            print(f"  回复: {data['choices'][0]['message']['content']}")
        else:
            print(f"\n❌ API 返回错误：{response.status_code}")
            print(f"  错误信息: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时（检查网络）")
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败（检查网络或 URL）")
    except json.JSONDecodeError:
        print("❌ 响应格式错误")
    except Exception as e:
        print(f"❌ 错误：{e}")

if __name__ == '__main__':
    test_volcanoengine_api()
```

**运行 API 调试：**

```bash
python debug_api.py
```

---

## 📚 调试清单

- [ ] ✅ 虚拟环境已创建并激活（命令行显示 `(venv)`）
- [ ] ✅ 所有依赖已安装（运行 `pip list` 确认）
- [ ] ✅ `.env` 文件已配置有效的 API Key
- [ ] ✅ 可以运行 `streamlit run app.py`
- [ ] ✅ 浏览器能访问 http://localhost:8501
- [ ] ✅ 能上传或使用示例数据
- [ ] ✅ 能选择模型并生成诊断
- [ ] ✅ 能查看结果和导出数据

---

## 🆘 获取帮助

### 检查日志

1. **Streamlit 日志**：在应用运行的终端中查看
2. **Python 日志**：查看错误堆栈跟踪
3. **浏览器控制台**：按 F12 查看前端日志

### 常用命令

```bash
# 查看 Python 版本
python --version

# 查看已安装的包
pip list

# 查看特定包信息
pip show streamlit

# 清理缓存
streamlit cache clear

# 更新依赖
pip install --upgrade -r requirements.txt
```

### 文档参考

- [Streamlit 文档](https://docs.streamlit.io/)
- [火山引擎文档](https://www.volcengine.com/docs/)
- [项目 README](README.md)
- [项目报告](report.md)

---

**最后更新**：2026-06-25  
