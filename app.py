"""
智能学业状态诊断助手 - Streamlit 主应用
"""
import streamlit as st
import pandas as pd
import io
from data_processor import ScoreDataProcessor, create_sample_html
from llm_analyzer import LLMAnalyzer
from visualizer import Visualizer
from utils.config import Config
from utils.helpers import highlight_key_metrics
# 临时重定向 stderr 以防止在裸机模式下导入时发出 ScriptRunContext 的干扰警告
import sys
import io
old_stderr = sys.stderr
sys.stderr = io.StringIO()
try:
    from streamlit_option_menu import option_menu
finally:
    sys.stderr = old_stderr


def initialize_session_state():
    """初始化会话状态"""
    if 'scores_df' not in st.session_state:
        st.session_state.scores_df = None
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    if 'statistics' not in st.session_state:
        st.session_state.statistics = None
    if 'subject_analysis' not in st.session_state:
        st.session_state.subject_analysis = None


def main():
    """主函数"""
    # 页面配置
    st.set_page_config(**Config.APP_PAGE_CONFIG)
    
    # 添加自定义 CSS
    st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .stMetric {
            background-color: rgba(31, 119, 180, 0.1);
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #1f77b4;
        }
        .success-box {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
        }
        .info-box {
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
        }
        .warning-box {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    initialize_session_state()
    
    # 页面标题
    st.title("🎓 智能学业状态诊断助手")
    st.markdown("""
    > 基于人工智能的教务数据分析与个性化选课建议系统
    
    本系统利用大模型分析你的教务成绩数据，为你生成学业诊断报告和选课建议。
    """)
    
    # 导航菜单
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: #1f77b4; margin-bottom: 0;'>🎓 智能学业诊断</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray; font-size: 0.9rem; margin-top: 5px;'>教务数据分析与选课系统</p>", unsafe_allow_html=True)
        st.divider()
        
        selected = st.radio(
            "功能导航",
            options=['📊 首页', '📤 数据上传', '🤖 智能分析', '📈 结果展示', '❓ 帮助'],
            index=0,
            label_visibility="collapsed"
        )
        
        st.divider()
        st.markdown("### ⚙️ 数据状态")
        if st.session_state.scores_df is not None:
            st.success(f"📊 已导入 {len(st.session_state.scores_df)} 门课程")
            if st.session_state.analysis_result is not None:
                st.success("🤖 诊断报告：已生成")
            else:
                st.warning("🤖 诊断报告：未生成")
        else:
            st.info("💡 提示：请先到「📤 数据上传」页面导入成绩数据。")
            
    if selected == '📊 首页':
        show_home()
    
    elif selected == '📤 数据上传':
        show_upload()
    
    elif selected == '🤖 智能分析':
        show_analysis()
    
    elif selected == '📈 结果展示':
        show_results()
    
    elif selected == '❓ 帮助':
        show_help()


def show_home():
    """首页"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✨ 主要功能")
        st.markdown("""
        - **📊 数据提取**：自动解析教务成绩单，提取课程、学分、成绩信息
        - **🤖 智能诊断**：利用大模型进行多维度学业评估
        - **📈 可视化展示**：生成直观的雷达图、柱状图等
        - **💡 选课建议**：个性化的课程推荐方案
        - **🔒 安全可靠**：API Key 通过环境变量保护，数据不存储
        """)
    
    with col2:
        st.markdown("### 🚀 快速开始")
        st.markdown("""
        1. **上传成绩单** → 点击"数据上传"
        2. **选择大模型** → 支持通义千问、智谱 GLM、OpenAI
        3. **生成诊断** → 点击"智能分析"
        4. **查看结果** → 进入"结果展示"查看完整报告
        """)
    
    st.divider()
    
    # 技术栈信息
    st.markdown("### 🛠️ 技术栈")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("后端框架", "Streamlit")
    with col2:
        st.metric("数据处理", "BeautifulSoup")
    with col3:
        st.metric("可视化", "Plotly")
    with col4:
        st.metric("AI 能力", "多模型支持")


def show_upload():
    """数据上传页面"""
    st.header("📤 获取并导入教务数据")
    
    col1, col2 = st.columns([7, 3])
    
    with col1:
        tab_file, tab_paste, tab_auto = st.tabs([
            "📁 上传 HTML 文件",
            "📋 直接粘贴 HTML 代码",
            "🚀 WebVPN 自动获取指南"
        ])
        
        def process_html_data(html_content: str):
            """处理和保存解析后的成绩数据"""
            processor = ScoreDataProcessor()
            df = processor.parse_score_html(html_content)
            
            if df is not None and len(df) > 0:
                st.session_state.scores_df = df
                st.session_state.statistics = processor.get_statistics()
                st.session_state.subject_analysis = processor.get_subject_analysis()
                
                st.success(f"✅ 成功提取 {len(df)} 门课程数据！")
                
                # 显示数据预览
                with st.expander("📋 数据预览", expanded=True):
                    st.dataframe(df, use_container_width=True)
                
                # 显示统计信息
                with st.expander("📊 统计信息"):
                    stats = st.session_state.statistics
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        st.metric("总课程数", int(stats['总课程数']))
                    with c2:
                        st.metric("平均成绩", f"{stats['平均成绩']:.1f}")
                    with c3:
                        st.metric("总学分", f"{stats['总学分']:.0f}")
                    with c4:
                        st.metric("加权绩点", f"{stats['加权绩点']:.2f}")
            else:
                st.error("❌ 无法解析 HTML 数据，请检查文件格式或内容是否为完整的教务成绩页面。")

        with tab_file:
            st.markdown("### 📁 上传 HTML/DO 成绩单")
            st.markdown("请上传从教务系统导出保存的成绩单文件（支持 `.html` / `.htm` / `.do` 格式）。")
            uploaded_file = st.file_uploader(
                "选择成绩文件",
                type=['html', 'htm', 'do'],
                help="请上传从教务系统导出的 HTML 或 DO 成绩单文件",
                key="file_uploader_key"
            )
            
            if uploaded_file is not None:
                try:
                    html_content = uploaded_file.read().decode('utf-8')
                    process_html_data(html_content)
                except Exception as e:
                    st.error(f"❌ 文件读取失败: {str(e)}")
                    
        with tab_paste:
            st.markdown("### 📋 直接粘贴 HTML 代码")
            st.markdown("您也可以全选教务系统成绩页面并复制其源文件内容，然后直接粘贴到下方输入框中。")
            pasted_html = st.text_area(
                "粘贴你的成绩页面 HTML 代码",
                height=300,
                placeholder="在此处粘贴 HTML 源码...",
                key="pasted_html_key"
            )
            if st.button("🚀 开始解析粘贴的代码", use_container_width=True, key="btn_parse_pasted"):
                if pasted_html.strip():
                    try:
                        process_html_data(pasted_html)
                    except Exception as e:
                        st.error(f"❌ 解析失败: {str(e)}")
                else:
                    st.warning("⚠️ 请先粘贴 HTML 代码后再点击解析")
                    
        with tab_auto:
            st.markdown("### 🚀 最新 WebVPN 自动化抓取流程")
            st.markdown("通过以下最新工作流，可以免去繁琐操作，直接自动同步全部成绩：")
            
            st.markdown("#### 1️⃣ 第一步：统一认证与会话同步")
            st.markdown("点击下方按钮访问 WebVPN 登录入口，完成登录的同时会自动同步教务系统的 Session。")
            login_url = "https://webvpn.bipt.edu.cn/https/77726476706e69737468656265737421fae05b84693261406a468ca88d1b203b/academic/login/bipt/loginIds6.jsp"
            st.markdown(f'<a href="{login_url}" target="_blank" style="display:inline-block;padding:8px 16px;background-color:#1f77b4;color:white;text-decoration:none;border-radius:4px;font-weight:bold;margin-bottom:10px;">🔗 打开 WebVPN 登录入口</a>', unsafe_allow_html=True)
            
            st.markdown("#### 2️⃣ 第二步：跳转成绩页面")
            st.markdown("认证完成后，直接点击下方按钮跳转至成绩查询接口页面。")
            score_url = "https://webvpn.bipt.edu.cn/https/77726476706e69737468656265737421fae05b84693261406a468ca88d1b203b/academic/manager/score/studentOwnScore.do"
            st.markdown(f'<a href="{score_url}" target="_blank" style="display:inline-block;padding:8px 16px;background-color:#2ca02c;color:white;text-decoration:none;border-radius:4px;font-weight:bold;margin-bottom:10px;">📊 跳转成绩查询页面</a>', unsafe_allow_html=True)
            
            st.markdown("#### 3️⃣ 第三步：JS 注入绕过默认限制")
            st.markdown("""
            默认页面只显示当学期成绩，请在成绩页面按 `F12`（或右键 -> 检查），切换到 **Console (控制台)**，复制并粘贴运行以下 JavaScript 脚本。
            这将自动拉取全部学年和学期的历年成绩：
            """)
            js_code = """document.querySelector('select[name="year"]').value = "";
document.querySelector('select[name="term"]').value = "";
document.forms["form1"].submit();"""
            st.code(js_code, language="javascript")
            
            st.markdown("#### 4️⃣ 第四步：全选复制并粘贴")
            st.markdown("""
            脚本执行并页面重新加载后：
            1. 页面上按 `Ctrl+A` (全选) 接着 `Ctrl+C` (复制)；
            2. 返回本应用，切换到 **"直接粘贴 HTML 代码"** 标签页；
            3. 将内容粘贴到输入框中，点击解析按钮即可完成同步。
            """)
            
    with col2:
        st.markdown("### 📥 示例与参考")
        
        # 生成示例 HTML
        sample_html = create_sample_html()
        
        st.download_button(
            label="⬇️ 下载示例成绩单 (HTML)",
            data=sample_html,
            file_name="sample_scores.html",
            mime="text/html",
            help="下载示例成绩单，了解要求的文件格式",
            use_container_width=True,
            key="btn_download_sample"
        )
        
        # 查看示例
        with st.expander("👀 查看示例格式"):
            st.code(sample_html, language='html')



def show_analysis():
    """智能分析页面"""
    st.header("🤖 智能学业分析")
    
    if st.session_state.scores_df is None:
        st.warning("⚠️ 请先在'数据上传'页面上传成绩数据")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        model_choice = st.selectbox(
            "选择大模型",
            options=['volcanoengine', 'qwen', 'zhipu', 'openai'],
            format_func=lambda x: {
                'qwen': '阿里通义千问',
                'zhipu': '智谱 GLM',
                'openai': 'OpenAI GPT',
                'volcanoengine': '抖音豆包'
            }.get(x, x),
            help="选择要使用的大模型服务"
        )
    
    with col2:
        use_sample = st.checkbox(
            "使用示例结果（不调用 API）",
            value=True,
            help="勾选此项将使用预置的示例结果，不需要 API Key"
        )
    
    st.divider()
    
    # 分析按钮
    if st.button("🚀 生成诊断分析", key="analyze_button", use_container_width=True):
        with st.spinner("🔄 正在分析学业状态..."):
            if use_sample:
                # 使用示例结果
                analysis_result = get_sample_analysis_result()
                st.success("✅ 使用示例结果（演示模式）")
            else:
                # 调用真实 API
                try:
                    analyzer = LLMAnalyzer(model_type=model_choice)
                    analysis_result = analyzer.analyze_academic_status(st.session_state.scores_df)
                    
                    if analysis_result is None:
                        st.error("❌ 分析失败，请检查 API Key 配置或网络连接")
                        return
                    
                    st.success("✅ 分析完成！")
                
                except Exception as e:
                    st.error(f"❌ 分析过程出错: {str(e)}")
                    return
            
            st.session_state.analysis_result = analysis_result
            st.info("💡 分析结果已保存，请前往'结果展示'查看完整报告")


def show_results():
    """结果展示页面"""
    st.header("📈 分析结果展示")
    
    if st.session_state.scores_df is None:
        st.warning("⚠️ 请先上传成绩数据")
        return
    
    if st.session_state.analysis_result is None:
        st.warning("⚠️ 请先进行智能分析")
        return
    
    df = st.session_state.scores_df
    analysis = st.session_state.analysis_result
    stats = st.session_state.statistics
    subject_analysis = st.session_state.subject_analysis
    
    viz = Visualizer()
    
    # 标签页
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        '📋 诊断报告',
        '📊 数据分析',
        '🎯 评分结果',
        '💡 建议方案',
        '📥 导出数据'
    ])
    
    with tab1:
        st.markdown("### 📋 学业诊断报告")
        
        if 'diagnosis' in analysis:
            st.markdown(analysis['diagnosis'])
        else:
            st.info("暂无诊断报告")
        
        # 显示优势和劣势
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✅ 学生优势")
            if 'strengths' in analysis:
                for strength in analysis['strengths']:
                    st.markdown(f"- {strength}")
        
        with col2:
            st.markdown("#### ⚠️ 改进空间")
            if 'weaknesses' in analysis:
                for weakness in analysis['weaknesses']:
                    st.markdown(f"- {weakness}")
    
    with tab2:
        st.markdown("### 📊 成绩数据分析")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 主要指标")
            st.metric("平均成绩", f"{stats['平均成绩']:.1f}")
            st.metric("平均绩点", f"{stats['平均绩点']:.2f}")
            st.metric("加权绩点", f"{stats['加权绩点']:.2f}")
        
        with col2:
            st.markdown("#### 📊 等级分布")
            st.metric("A 等级课程", int(stats['A 等级课程']))
            st.metric("B 等级课程", int(stats['B 等级课程']))
            st.metric("C 等级课程", int(stats['C 等级课程']))
        
        st.divider()
        
        # 成绩分布图
        st.markdown("#### 成绩分布直方图")
        fig1 = viz.generate_score_distribution_chart(df['成绩'].tolist())
        st.plotly_chart(fig1, use_container_width=True)
        
        # 等级分布饼图
        st.markdown("#### 成绩等级分布")
        fig2 = viz.generate_gpa_progress_chart(df)
        st.plotly_chart(fig2, use_container_width=True)
        
        # 学科对比图
        if subject_analysis:
            st.markdown("#### 学科对比分析")
            fig3 = viz.generate_subject_comparison_chart(subject_analysis)
            st.plotly_chart(fig3, use_container_width=True)
    
    with tab3:
        st.markdown("### 🎯 多维度评分结果")
        
        if 'ratings' in analysis:
            ratings = analysis['ratings']
            
            # 雷达图
            fig = viz.generate_radar_chart(ratings, title='学业状态多维度评分')
            st.plotly_chart(fig, use_container_width=True)
            
            # 评分详情
            st.markdown("#### 评分详情")
            col1, col2, col3, col4 = st.columns(4)
            
            dimensions = ['数学基础', '英语能力', '专业课程', '整体表现']
            cols = [col1, col2, col3, col4]
            
            for dim, col in zip(dimensions, cols):
                if dim in ratings:
                    score = ratings[dim]
                    color = "green" if score >= 0.8 else "orange" if score >= 0.7 else "red"
                    with col:
                        st.metric(dim, f"{score:.2f}", delta=f"{score*100:.0f}%")
    
    with tab4:
        st.markdown("### 💡 个性化选课建议")
        
        if 'recommendations' in analysis:
            recommendations = analysis['recommendations']
            
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"""
                #### 建议 {i}
                {rec}
                """)
        else:
            st.info("暂无选课建议")
    
    with tab5:
        st.markdown("### 📥 导出数据")
        
        # 导出成绩数据 CSV
        csv = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="⬇️ 导出成绩数据（CSV）",
            data=csv,
            file_name="scores_data.csv",
            mime="text/csv"
        )
        
        # 导出分析结果 JSON
        import json
        analysis_json = json.dumps(analysis, ensure_ascii=False, indent=2)
        st.download_button(
            label="⬇️ 导出分析结果（JSON）",
            data=analysis_json,
            file_name="analysis_result.json",
            mime="application/json"
        )


def show_help():
    """帮助页面"""
    st.header("❓ 帮助与文档")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📖 使用指南")
        st.markdown("""
        **1. 准备数据**
        - 从学校教务系统导出成绩单（通常为 HTML 格式）
        - 确保包含：课程名、学分、成绩三个字段
        
        **2. 上传文件**
        - 进入"数据上传"页面
        - 上传 HTML 文件或使用示例数据
        
        **3. 选择模型**
        - 进入"智能分析"页面
        - 选择要使用的大模型（推荐使用示例模式）
        
        **4. 查看结果**
        - 进入"结果展示"页面
        - 查看诊断报告、图表分析、选课建议
        """)
    
    with col2:
        st.markdown("### ⚙️ 配置说明")
        st.markdown("""
        **环境变量配置**
        ```bash
        # 复制 .env.example 为 .env
        cp .env.example .env
        
        # 编辑 .env，添加 API Key
        QWEN_API_KEY=your-key
        ZHIPU_API_KEY=your-key
        OPENAI_API_KEY=your-key
        VOLCANOENGINE_API_KEY=your-key
        VOLCANOENGINE_MODEL_NAME=doubao-pro-32k
        ```
        
        **运行应用**
        ```bash
        streamlit run app.py
        ```
        
        **API 支持**
        - 阿里通义千问
        - 智谱 GLM
        - OpenAI GPT
        """)
    
    st.divider()
    
    st.markdown("### ❔ 常见问题")
    
    with st.expander("Q: 如何获取 API Key？"):
        st.markdown("""
        - **阿里通义千问**: 访问 [dashscope.aliyun.com](https://dashscope.aliyun.com)
        - **智谱 GLM**: 访问 [open.bigmodel.cn](https://open.bigmodel.cn)
        - **OpenAI**: 访问 [platform.openai.com](https://platform.openai.com)
        """)
    
    with st.expander("Q: 数据安全性如何保证？"):
        st.markdown("""
        - API Key 存储在 `.env` 文件中，已添加到 `.gitignore`
        - 不会被上传到版本控制系统
        - 用户上传的成绩数据不会被存储
        """)
    
    with st.expander("Q: 支持哪些文件格式？"):
        st.markdown("""
        目前支持：
        - HTML 格式（教务系统导出）
        - 计划支持：Excel、CSV、JSON
        """)
    
    with st.expander("Q: 分析结果准确吗？"):
        st.markdown("""
        - 分析基于大模型的自然语言理解能力
        - 结果仅供参考，不代表官方评价
        - 选课建议应结合个人实际情况判断
        """)


def get_sample_analysis_result() -> dict:
    """获取示例分析结果（用于演示）"""
    return {
        'diagnosis': """
### 📋 学业诊断报告

该学生的学业表现整体较为均衡，平均成绩在 85 分左右，体现了较好的学习能力。

**优势分析**：
- 在数学和专业课程方向表现突出，特别是编程、数据结构等核心课程成绩优秀
- 学习态度认真，绩点稳定，显示出持续的学习投入

**劣势分析**：
- 英语语言能力相对薄弱，存在一定的提升空间
- 部分通识课程成绩有进步空间

**改进建议**：
建议学生加强英语学习，同时继续深化专业课程知识，为后续高阶课程和实习做好准备。
        """,
        'ratings': {
            '数学基础': 0.85,
            '英语能力': 0.72,
            '专业课程': 0.88,
            '整体表现': 0.82
        },
        'strengths': [
            '编程和算法能力强，核心专业课成绩优秀',
            '学习态度认真，学分绩点稳定增长',
            '数学基础扎实，逻辑思维能力强'
        ],
        'weaknesses': [
            '英语语言应用能力需要加强',
            '部分通识课程学习投入不足',
            '跨学科综合应用能力可继续提升'
        ],
        'recommendations': [
            '💻 建议选修《深度学习基础》等进阶 AI 课程，进一步拓展专业知识广度',
            '🌐 建议加强英语学习，选修《专业英语》或参加托福/雅思等外语考试',
            '🎯 建议参与《大数据分析实践》项目，将理论知识应用到实际工程问题中'
        ]
    }


if __name__ == '__main__':
    import streamlit.runtime
    # 只有在 Streamlit 运行时上下文已建立的情况下才执行 main
    if streamlit.runtime.exists():
        main()
    else:
        import os
        import sys
        import subprocess
        # 如果尚未启动子进程，则使用子进程启动 Streamlit 服务
        if not os.environ.get("STREAMLIT_SUBPROCESS_RUN"):
            os.environ["STREAMLIT_SUBPROCESS_RUN"] = "1"
            # 使用干净的子进程启动 streamlit，避免主进程内共享 sys.modules 缓存导致自定义组件静态资源 404
            cmd = [sys.executable, "-m", "streamlit", "run", __file__] + sys.argv[1:]
            try:
                sys.exit(subprocess.run(cmd).returncode)
            except KeyboardInterrupt:
                sys.exit(0)
