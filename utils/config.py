"""
配置管理模块
负责从环境变量加载敏感信息（API Key等）和系统配置
"""
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()


class Config:
    """系统配置类"""
    
    # API 密钥配置
    QWEN_API_KEY = os.getenv('QWEN_API_KEY', '')
    ZHIPU_API_KEY = os.getenv('ZHIPU_API_KEY', '')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    VOLCANOENGINE_API_KEY = os.getenv('VOLCANOENGINE_API_KEY', '')
    
    # 默认模型
    DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'qwen')
    
    # API 端点
    QWEN_API_URL = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation'
    ZHIPU_API_URL = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
    OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions'
    VOLCANOENGINE_API_URL = 'https://ark.cn-beijing.volces.com/api/v3/chat/completions'
    
    # LLM 模型参数
    MODEL_CONFIG = {
        'qwen': {
            'model_name': 'qwen-turbo',
            'temperature': 0.7,
            'max_tokens': 1500,
            'top_p': 0.8
        },
        'zhipu': {
            'model_name': 'glm-3-turbo',
            'temperature': 0.7,
            'max_tokens': 1500,
            'top_p': 0.8
        },
        'openai': {
            'model_name': 'gpt-3.5-turbo',
            'temperature': 0.7,
            'max_tokens': 1500,
            'top_p': 0.8
        },
        'volcanoengine': {
            'model_name': 'doubao-pro-32k',
            'temperature': 0.7,
            'max_tokens': 1500,
            'top_p': 0.8
        }
    }
    
    # 评分维度定义
    RATING_DIMENSIONS = [
        '数学基础',
        '英语能力',
        '专业课程',
        '整体表现'
    ]
    
    # 应用配置
    APP_TITLE = '智能学业状态诊断助手'
    APP_PAGE_CONFIG = {
        'page_title': '智能学业诊断助手',
        'page_icon': '📊',
        'layout': 'wide',
        'initial_sidebar_state': 'expanded'
    }
    
    @classmethod
    def validate_api_keys(cls):
        """验证 API 密钥配置"""
        model = cls.DEFAULT_MODEL
        
        if model == 'qwen' and not cls.QWEN_API_KEY:
            raise ValueError('未配置 QWEN_API_KEY')
        elif model == 'zhipu' and not cls.ZHIPU_API_KEY:
            raise ValueError('未配置 ZHIPU_API_KEY')
        elif model == 'openai' and not cls.OPENAI_API_KEY:
            raise ValueError('未配置 OPENAI_API_KEY')
        elif model == 'volcanoengine' and not cls.VOLCANOENGINE_API_KEY:
            raise ValueError('未配置 VOLCANOENGINE_API_KEY')
        
        return True
    
    @classmethod
    def get_model_config(cls, model_type):
        """获取指定模型的配置"""
        return cls.MODEL_CONFIG.get(model_type, cls.MODEL_CONFIG['qwen'])


if __name__ == '__main__':
    print("配置加载成功")
    print(f"默认模型: {Config.DEFAULT_MODEL}")
    print(f"评分维度: {Config.RATING_DIMENSIONS}")
