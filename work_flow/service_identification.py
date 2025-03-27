import requests
import json

BASE_URL = "http://mofrp.top:10846/"

# 可配置的 service type 判定规则
SERVICE_RULES = {
    "理发服务": {
        "关键词": ["剪刀", "电推剪", "剃刀", "吹风机", "理发围布", "美发师操作"],
        "场景关键词": ["理发店", "造型台", "护发产品"]
    },
    "做饭服务": {
        "关键词": ["锅具", "食材", "碗筷", "电饭煲", "菜刀", "砧板", "炉灶", "烹饪"],
        "场景关键词": ["厨房", "餐厅", "操作台"]
    }
}

def construct_service_prompt() -> str:
    """构建服务类型判断 prompt"""
    return (
        "# 角色\n"
        "您是「养老院服务类型判断专家」，需在理发服务和做饭服务之间做出精准判定。\n"
        "\n## 技能\n"
        "### 技能 1: 多图特征融合分析\n"
        "1. 综合分析所有图片的以下特征：\n"
        f"   - {SERVICE_RULES['理发服务']['关键词']}\n"
        f"   - {SERVICE_RULES['做饭服务']['关键词']}\n"
        f"   - {SERVICE_RULES['理发服务']['场景关键词']}\n"
        f"   - {SERVICE_RULES['做饭服务']['场景关键词']}\n"
        "2. 判定标准：\n"
        "   - 出现任一理发服务关键词即计+1分\n"
        "   - 出现任一做饭服务关键词即计+1分\n"
        "   - 场景关键词匹配度额外+2分\n"
        "3. 最终判定：\n"
        "   - 总分≥4分且理发得分＞做饭得分 → 理发服务\n"
        "   - 总分≥4分且做饭得分＞理发得分 → 做饭服务\n"
        "   - 其他情况 → 无法判定\n"
        "===回复示例===\n"
        '{"service_type": "<判断结果>", "score": {"hair": <分数>, "cook": <分数>}, "reason": "<简要说明>"}\n'
        "===示例结束==="
    )

def get_image_urls() -> list:
    """获取待分析图片URL"""
    return [
        "http://example.com/haircut1.jpg",
        "http://example.com/haircut2.jpg",
        "http://example.com/cooking1.jpg",
        "http://example.com/cooking2.jpg"
    ]

def analyze_service_type() -> str:
    """主判断流程"""
    try:
        # 构建请求数据
        payload = {
            'prompt': construct_service_prompt(),
            'urls': get_image_urls()
        }

        # 发送 POST 请求
        response = requests.post(f"{BASE_URL}analyze", json=payload, timeout=15)
        response.raise_for_status()

        # 打印服务器返回内容
        print("Response Status Code:", response.status_code)
        print("Response JSON:", response.json())

        # 解析 JSON 数据
        data = response.json()
        if not isinstance(data, list) or not data:
            return "错误: 服务器返回数据格式异常"

        response_text = data[0].get('response', '')
        if not response_text:
            return "错误: 服务器返回数据为空"

        # 解析去掉前后可能的无关字符
        result = json.loads(response_text.strip())

        return f"服务类型: {result.get('service_type', '未知')} | 评分: {result.get('score', {})} | 说明: {result.get('reason', '无')}"
    
    except requests.exceptions.RequestException as e:
        return f"服务判断失败: {str(e)}"
    except json.JSONDecodeError:
        return "错误: 无法解析服务器返回的 JSON"
    except KeyError as e:
        return f"数据格式错误: 缺少字段 {str(e)}"
    except Exception as e:
        return f"系统错误: {str(e)}"

if __name__ == "__main__":
    # 执行服务判断
    service_type = analyze_service_type()
    print(f"最终判定结果: {service_type}")
