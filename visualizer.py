"""
可视化模块
负责生成交互式图表，包括雷达图、柱状图等
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Optional
import streamlit as st


class Visualizer:
    """可视化生成器"""
    
    def __init__(self):
        self.theme_color = '#1f77b4'
        self.accent_color = '#ff7f0e'
    
    def generate_radar_chart(self, ratings: Dict[str, float], title: str = '学业状态多维度评分') -> go.Figure:
        """
        生成学业状态多维度雷达图
        
        Args:
            ratings: 评分字典 {维度名: 分数(0-1)}
            title: 图表标题
        
        Returns:
            Plotly Figure 对象
        """
        categories = list(ratings.keys())
        values = list(ratings.values())
        
        # 添加首尾相连（闭合图形）
        categories.append(categories[0])
        values.append(values[0])
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='学业评分',
            line=dict(color=self.theme_color, width=2),
            fillcolor='rgba(31, 119, 180, 0.3)',
            hovertemplate='<b>%{theta}</b><br>评分: %{r:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    tickvals=[0.2, 0.4, 0.6, 0.8, 1.0],
                    ticktext=['0.2', '0.4', '0.6', '0.8', '1.0'],
                    gridcolor='#d3d3d3'
                ),
                angularaxis=dict(
                    gridcolor='#d3d3d3'
                )
            ),
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            height=600,
            font=dict(size=12),
            showlegend=False,
            hovermode='closest',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(240,240,240,0.5)'
        )
        
        return fig
    
    def generate_score_distribution_chart(self, scores: List[float], title: str = '成绩分布') -> go.Figure:
        """
        生成成绩分布直方图
        
        Args:
            scores: 成绩列表
            title: 图表标题
        
        Returns:
            Plotly Figure 对象
        """
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=scores,
            nbinsx=10,
            name='成绩',
            marker_color=self.theme_color,
            marker_line_color='white',
            marker_line_width=1.5,
            hovertemplate='成绩范围: %{x}<br>课程数: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis_title='分数',
            yaxis_title='课程数量',
            height=400,
            font=dict(size=12),
            hovermode='x unified',
            bargap=0.1
        )
        
        return fig
    
    def generate_subject_comparison_chart(self, subject_stats: Dict[str, Dict]) -> go.Figure:
        """
        生成学科对比柱状图
        
        Args:
            subject_stats: 学科统计字典 {学科: {平均成绩, 课程数, ...}}
        
        Returns:
            Plotly Figure 对象
        """
        subjects = list(subject_stats.keys())
        avg_scores = [subject_stats[s].get('平均成绩', 0) for s in subjects]
        course_counts = [subject_stats[s].get('课程数', 0) for s in subjects]
        
        fig = make_subplots(
            specs=[[{'secondary_y': True}]],
            subplot_titles=['学科平均成绩对比']
        )
        
        # 添加柱状图（平均成绩）
        fig.add_trace(
            go.Bar(
                x=subjects,
                y=avg_scores,
                name='平均成绩',
                marker_color=self.theme_color,
                marker_line_color='white',
                marker_line_width=1,
                hovertemplate='<b>%{x}</b><br>平均成绩: %{y:.1f}<extra></extra>',
                yaxis='y'
            ),
            secondary_y=False
        )
        
        # 添加折线图（课程数）
        fig.add_trace(
            go.Scatter(
                x=subjects,
                y=course_counts,
                name='课程数',
                line=dict(color=self.accent_color, width=3),
                marker=dict(size=8),
                hovertemplate='<b>%{x}</b><br>课程数: %{y}<extra></extra>',
                yaxis='y2'
            ),
            secondary_y=True
        )
        
        fig.update_xaxes(title_text='学科')
        fig.update_yaxes(title_text='平均成绩', secondary_y=False, range=[0, 100])
        fig.update_yaxes(title_text='课程数', secondary_y=True)
        
        fig.update_layout(
            height=400,
            font=dict(size=12),
            hovermode='x unified',
            legend=dict(x=0.01, y=0.99)
        )
        
        return fig
    
    def generate_gpa_progress_chart(self, df: pd.DataFrame) -> go.Figure:
        """
        生成绩点进度图
        
        Args:
            df: 成绩 DataFrame
        
        Returns:
            Plotly Figure 对象
        """
        if df is None or len(df) == 0:
            return go.Figure()
        
        # 按绩点分级统计
        grade_dist = df['等级'].value_counts().sort_index()
        
        fig = go.Figure(data=[
            go.Pie(
                labels=grade_dist.index,
                values=grade_dist.values,
                marker=dict(colors=['#2ecc71', '#3498db', '#f39c12', '#e74c3c', '#95a5a6']),
                hovertemplate='<b>%{label} 等级</b><br>课程数: %{value}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title={
                'text': '成绩等级分布',
                'x': 0.5,
                'xanchor': 'center'
            },
            height=400,
            font=dict(size=12)
        )
        
        return fig
    
    def generate_performance_gauge(self, avg_gpa: float, title: str = '整体学业表现') -> go.Figure:
        """
        生成性能指示表（仪表盘）
        
        Args:
            avg_gpa: 平均绩点（0-4）
            title: 图表标题
        
        Returns:
            Plotly Figure 对象
        """
        # 将绩点转换到 0-100 的百分比
        percentage = (avg_gpa / 4.0) * 100
        
        fig = go.Figure(go.Indicator(
            mode='gauge+number+delta',
            value=percentage,
            title={'text': title},
            delta={'reference': 80},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': self.theme_color},
                'steps': [
                    {'range': [0, 50], 'color': 'rgba(255, 0, 0, 0.3)'},
                    {'range': [50, 75], 'color': 'rgba(255, 165, 0, 0.3)'},
                    {'range': [75, 100], 'color': 'rgba(0, 128, 0, 0.3)'}
                ],
                'threshold': {
                    'line': {'color': 'red', 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            },
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        
        fig.update_layout(
            height=400,
            font=dict(size=12),
            paper_bgcolor='white'
        )
        
        return fig
    
    @staticmethod
    def create_metrics_table(stats: Dict) -> str:
        """
        创建统计指标的 HTML 表格
        
        Args:
            stats: 统计字典
        
        Returns:
            HTML 表格字符串
        """
        table_html = """
        <table style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #f0f0f0;">
                <th style="border: 1px solid #ddd; padding: 8px;">指标</th>
                <th style="border: 1px solid #ddd; padding: 8px;">数值</th>
            </tr>
        """
        
        for key, value in stats.items():
            if isinstance(value, float):
                value_str = f"{value:.2f}"
            else:
                value_str = str(value)
            
            table_html += f"""
            <tr>
                <td style="border: 1px solid #ddd; padding: 8px;">{key}</td>
                <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">{value_str}</td>
            </tr>
            """
        
        table_html += "</table>"
        return table_html


if __name__ == '__main__':
    # 测试可视化
    viz = Visualizer()
    
    # 测试雷达图
    ratings = {
        '数学基础': 0.85,
        '英语能力': 0.72,
        '专业课程': 0.88,
        '整体表现': 0.80
    }
    
    fig = viz.generate_radar_chart(ratings)
    print("雷达图已生成")
    
    # 测试成绩分布图
    scores = [87, 92, 78, 88, 91, 85, 89, 82, 86, 79, 90, 84, 80]
    fig = viz.generate_score_distribution_chart(scores)
    print("成绩分布图已生成")
