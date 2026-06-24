"""
大模型分析模块
负责调用各种大模型 API 进行学业诊断和决策支持
"""
import requests
import json
from typing import Dict, Optional, List
import pandas as pd
from utils.config import Config
from utils.helpers import parse_json_response, format_diagnosis_report


class LLMAnalyzer:
    """大模型分析器"""
    
    def __init__(self, model_type: str = 'qwen'):
        """
        初始化分析器
        
        Args:
            model_type: 模型类型（qwen / zhipu / openai）
        """
        self.model_type = model_type
        self.model_config = Config.get_model_config(model_type)
        self.rating_dimensions = Config.RATING_DIMENSIONS
    
    def analyze_academic_status(self, scores_df: pd.DataFrame) -> Optional[Dict]:
        """
        调用大模型进行学业分析
        
        Args:
            scores_df: 成绩 DataFrame
        
        Returns:
            分析结果字典，包含 diagnosis / ratings / recommendations / strengths / weaknesses
        """
        try:
            # 构建分析 Prompt
            prompt = self._build_analysis_prompt(scores_df)
            
            # 调用对应的模型 API
            if self.model_type == 'qwen':
                response = self._call_qwen_api(prompt)
            elif self.model_type == 'zhipu':
                response = self._call_zhipu_api(prompt)
            elif self.model_type == 'volcanoengine':
                response = self._call_volcanoengine_api(prompt)
            else:
                response = self._call_openai_api(prompt)
            
            # 解析响应
            if response:
                return self._parse_analysis_response(response)
            
            return None
        
        except Exception as e:
            print(f"大模型分析失败: {str(e)}")
            return None
    
    def _build_analysis_prompt(self, scores_df: pd.DataFrame) -> str:
        """
        构建分析 Prompt
        
        Args:
            scores_df: 成绩 DataFrame
        
        Returns:
            Prompt 文本
        """
        # 构建成绩数据的文本表示
        scores_text = scores_df.to_string(index=False)
        
        # 计算一些基本统计
        avg_score = scores_df['成绩'].mean()
        max_score = scores_df['成绩'].max()
        min_score = scores_df['成绩'].min()
        
        prompt = f"""
请你作为一名资深教学顾问，对以下学生的课程成绩进行专业诊断和分析：

【学生成绩数据】
{scores_text}

【成绩概览】
- 平均成绩: {avg_score:.1f}
- 最高成绩: {max_score:.0f}
- 最低成绩: {min_score:.0f}
- 课程总数: {len(scores_df)}

【分析要求】
请从以下维度进行评估：
1. 数学基础能力（基于高等数学、线性代数等课程成绩）
2. 英语语言能力（基于英语课程成绩）
3. 专业课程掌握（基于计算机科学、编程、数据结构等专业课程成绩）
4. 整体学业表现（综合所有课程成绩）

每个维度的评分为 0-1 之间的数字，其中：
- 0.9-1.0 表示优秀
- 0.8-0.89 表示良好
- 0.7-0.79 表示中等
- 0.6-0.69 表示及格
- <0.6 表示需要改进

【输出格式】
请严格按照以下 JSON 格式返回分析结果（不要包含 markdown 代码块）：
{{
    "diagnosis": "对学生学业状态的完整诊断报告，应包括优势分析、劣势分析和改进建议（150-200 字）",
    "ratings": {{
        "数学基础": 0.85,
        "英语能力": 0.72,
        "专业课程": 0.88,
        "整体表现": 0.80
    }},
    "strengths": ["优势 1", "优势 2", "优势 3"],
    "weaknesses": ["劣势 1", "劣势 2"],
    "recommendations": [
        "建议 1（包括具体课程或学习方向）",
        "建议 2（包括具体课程或学习方向）",
        "建议 3（包括具体课程或学习方向）"
    ]
}}

确保 ratings 中的所有数值都在 0-1 之间，recommendations 列表中至少包含 3 条建议。
"""
        return prompt
    
    def _call_qwen_api(self, prompt: str) -> Optional[str]:
        """
        调用阿里通义千问 API
        
        Args:
            prompt: 提示词
        
        Returns:
            API 响应文本
        """
        try:
            api_key = Config.QWEN_API_KEY
            if not api_key:
                print("错误: 未配置 QWEN_API_KEY")
                return None
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': self.model_config['model_name'],
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': self.model_config['temperature'],
                'max_tokens': self.model_config['max_tokens'],
                'top_p': self.model_config['top_p']
            }
            
            response = requests.post(
                Config.QWEN_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                # 从嵌套的响应结构中提取文本
                if 'output' in result and 'text' in result['output']:
                    return result['output']['text']
                elif 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0].get('message', {}).get('content', '')
            
            return None
        
        except Exception as e:
            print(f"通义千问 API 调用失败: {str(e)}")
            return None
    
    def _call_zhipu_api(self, prompt: str) -> Optional[str]:
        """
        调用智谱 GLM API
        
        Args:
            prompt: 提示词
        
        Returns:
            API 响应文本
        """
        try:
            api_key = Config.ZHIPU_API_KEY
            if not api_key:
                print("错误: 未配置 ZHIPU_API_KEY")
                return None
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': self.model_config['model_name'],
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': self.model_config['temperature'],
                'max_tokens': self.model_config['max_tokens']
            }
            
            response = requests.post(
                Config.ZHIPU_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0].get('message', {}).get('content', '')
            
            return None
        
        except Exception as e:
            print(f"智谱 GLM API 调用失败: {str(e)}")
            return None
    
    def _call_volcanoengine_api(self, prompt: str) -> Optional[str]:
        """
        调用抖音火山引擎 API（豆包模型）
        
        Args:
            prompt: 提示词
        
        Returns:
            API 响应文本
        """
        try:
            api_key = Config.VOLCANOENGINE_API_KEY
            if not api_key:
                print("错误: 未配置 VOLCANOENGINE_API_KEY")
                return None
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': self.model_config['model_name'],
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': self.model_config['temperature'],
                'max_tokens': self.model_config['max_tokens'],
                'top_p': self.model_config['top_p']
            }
            
            response = requests.post(
                Config.VOLCANOENGINE_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0].get('message', {}).get('content', '')
            
            return None
        
        except Exception as e:
            print(f"火山引擎 API 调用失败: {str(e)}")
            return None
    
    def _call_openai_api(self, prompt: str) -> Optional[str]:
        """
        调用 OpenAI API
        
        Args:
            prompt: 提示词
        
        Returns:
            API 响应文本
        """
        try:
            api_key = Config.OPENAI_API_KEY
            if not api_key:
                print("错误: 未配置 OPENAI_API_KEY")
                return None
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': self.model_config['model_name'],
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': self.model_config['temperature'],
                'max_tokens': self.model_config['max_tokens']
            }
            
            response = requests.post(
                Config.OPENAI_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0].get('message', {}).get('content', '')
            
            return None
        
        except Exception as e:
            print(f"OpenAI API 调用失败: {str(e)}")
            return None
    
    def _parse_analysis_response(self, response: str) -> Optional[Dict]:
        """
        解析大模型的分析响应
        
        Args:
            response: 大模型的回复文本
        
        Returns:
            解析后的字典
        """
        # 尝试解析 JSON
        result = parse_json_response(response)
        
        if result is None:
            # 如果解析失败，构建默认结果
            result = self._create_fallback_response(response)
        
        # 验证必需字段
        if 'diagnosis' not in result:
            result['diagnosis'] = format_diagnosis_report(response[:500])
        
        if 'ratings' not in result:
            result['ratings'] = {dim: 0.75 for dim in self.rating_dimensions}
        
        if 'recommendations' not in result:
            result['recommendations'] = ['建议增强学科基础', '建议持续学习新技术', '建议参与实践项目']
        
        if 'strengths' not in result:
            result['strengths'] = ['学业基础扎实', '学习态度认真']
        
        if 'weaknesses' not in result:
            result['weaknesses'] = ['某些课程有改进空间']
        
        return result
    
    def _create_fallback_response(self, response_text: str) -> Dict:
        """
        创建备用响应（当解析失败时）
        
        Args:
            response_text: 原始响应文本
        
        Returns:
            构造的结果字典
        """
        return {
            'diagnosis': format_diagnosis_report(response_text),
            'ratings': {dim: 0.75 for dim in self.rating_dimensions},
            'strengths': ['学业表现稳定'],
            'weaknesses': ['某些课程可继续改进'],
            'recommendations': ['继续保持学习热情', '深化专业知识学习', '参与实践项目']
        }
    
    @staticmethod
    def build_recommendations_by_scores(scores_df: pd.DataFrame, analysis_result: Dict) -> List[str]:
        """
        基于成绩和分析结果构建更具体的选课建议
        
        Args:
            scores_df: 成绩 DataFrame
            analysis_result: 分析结果字典
        
        Returns:
            建议列表
        """
        recommendations = []
        
        avg_score = scores_df['成绩'].mean()
        
        # 基于平均成绩的建议
        if avg_score >= 85:
            recommendations.append("🎯 平均成绩优秀，建议选择具有挑战性的高级课程，如深度学习、分布式系统等")
        elif avg_score >= 75:
            recommendations.append("📚 成绩良好，建议选择专业进深课程，巩固基础同时拓展知识广度")
        else:
            recommendations.append("💪 建议加强基础课程学习，选择难度适中的课程，同时参加辅导课程")
        
        # 基于分析结果的弱势课程建议
        if 'ratings' in analysis_result:
            ratings = analysis_result['ratings']
            
            # 找到最弱的维度
            weakest = min(ratings.items(), key=lambda x: x[1])
            if weakest[1] < 0.7:
                recommendations.append(f"⚠️ {weakest[0]}相对较弱（评分 {weakest[1]:.2f}），建议选择相关基础课程进行强化")
        
        # 基于分析建议的补充
        if 'recommendations' in analysis_result and len(analysis_result['recommendations']) > 0:
            # 添加第一条建议作为补充
            recommendations.append(f"💡 {analysis_result['recommendations'][0]}")
        
        return recommendations[:3]  # 只返回前 3 条最重要的建议


if __name__ == '__main__':
    # 测试（需要配置 API Key）
    print("LLMAnalyzer 模块已加载")
    print(f"支持的模型: {list(Config.MODEL_CONFIG.keys())}")
