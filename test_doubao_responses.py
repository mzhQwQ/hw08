import os
import requests
from dotenv import load_dotenv

def test_doubao_responses():
    load_dotenv()
    
    # API KEY 环境变量
    api_key = os.getenv('VOLCANOENGINE_API_KEY')
    # 模型名称
    model_name = os.getenv('VOLCANOENGINE_MODEL_NAME')
    
    if not api_key:
        print("❌ 错误: 请在 .env 文件中配置 VOLCANOENGINE_API_KEY")
        return

    print(f"正在测试豆包 Responses API (REST)...")
    print(f"Model: {model_name}")
    
    url = "https://ark.cn-beijing.volces.com/api/v3/responses"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # 注意：这里使用的是 'input' 而不是 'messages'
    payload = {
        "model": model_name,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "你好，请做个自我介绍。"
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ 测试成功！")
            # 这里的响应结构可能与 chat/completions 不同，打印出来看看
            print(f"响应内容: {result}")
        else:
            print(f"❌ 测试失败")
            print(f"错误详情: {response.text}")
    except Exception as e:
        print(f"❌ 发生异常: {str(e)}")

if __name__ == "__main__":
    test_doubao_responses()
