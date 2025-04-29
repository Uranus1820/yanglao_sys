import json

import requests
from openai import OpenAI


def get_api_inference(API_URL, API_KEY, model, prompt, imgs):
    """
    Function to get inference from the API.

    Args:
        api_key (str): The API key for authentication.
        model (str): The model to use for inference.
        messages (list): The messages to send to the API.

    Returns:
        response: The API response.
    """
    imgs = imgs.split(',')
    messages = [
        {
            "role": "user",
            "content": prompt
        },
        {
            "role": "user",
            "content": []
        }
    ]
    for img in imgs:
        messages[1]['content'].append(
                    {
                        "type": "image_url",
                        "image_url": {'url': img}
                    }
        )
    try:
        client = OpenAI(
            # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
            api_key=API_KEY,
            base_url=API_URL,
        )
        print(messages)
        completion = client.chat.completions.create(
            model=model,
            # 此处以qwen-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=messages,
            response_format={"type": "text"},
            # "temperature": 0.7,
            # "max_tokens": 1024,
        )
        response = json.loads(completion.model_dump_json())
        print(response)
        return [{'response': item['message']['content']} for item in response['choices']]
    except Exception as e:
        print(f"[bold red]API请求失败: {str(e)}[/]")
        return None
