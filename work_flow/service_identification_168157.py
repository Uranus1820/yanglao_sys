import requests
from collections import Counter

def judge_service_type(img_urls, service_type):
    url = 'http://mofrp.top:10846/'
    # img_urls = ",".join(service_img)

    prompt = (
        "# 角色\n"
        "你是一位经验极为丰富的 养老院服务类型判断专家，专注于 理发服务 和 做饭服务 的精准甄别。"
        "凭借深厚的专业知识、海量的实践经验以及敏锐的洞察力，你能够迅速、精准地判定 用户上传的服务图片 是否契合特定的服务类型，并给出最终的 统一判断结果。\n\n"
        "## 技能\n"
        "### 技能 1: 处理一组图片并判断服务类型\n"
        "当接收到用户上传的 一组图片时，需全面分析整组图片的整体信息，而非单独分析单张图片。\n"
        "依据 关键物品、人物动作、场景特征等多方面因素，对整组图片进行综合判断，最终给出 唯一的服务类型结果（理发服务 或 做饭服务）：\n"
        "理发服务：若整组图片中 多数 出现剪刀、电推剪、剃刀、吹风机、理发围布、美发师操作等典型元素，则最终判定为 理发服务。\n"
        "做饭服务：若整组图片中 多数 呈现食物、食材、碗筷餐具、电饭煲等厨房电器、锅具、菜刀、砧板、炉灶、食材烹饪、厨师穿戴等典型元素，则最终判定为 做饭服务。\n"
        "无法判定：若整组图片缺乏明确特征，或包含混合信息，导致无法精准归类，则返回 “无法判定”，并说明主要原因。\n\n"
        "### 技能 2: 输出最终判断结果\n"
        "仅返回最终的统一判断结果，而不单独解析每张图片。\n"
        "若能确定服务类型，则直接输出 “理发服务” 或 “做饭服务”。\n"
        "若无法做出明确归类，则输出 “无法判定，原因：整组图片缺乏明显的理发或做饭特征”。\n\n"
        "## 限制\n"
        "仅 负责 理发服务和做饭服务 的判断，不回答其他养老院服务类型或无关问题。\n"
        "输出仅包含最终统一判断结果，不逐一分析单张图片，必须基于整组图片的整体信息得出明确结论。\n\n"
        # f"以下是用户上传的服务图片：{img_urls}"
    )

    data = {
        'prompt': prompt,
        'urls': img_urls
    }

    try:
        response = requests.post(url + 'understand', data=data)
        results = response.json()  # 一个列表

        print(results)

        service_votes = []

        for item in results:
            text = item['response']
            if any(k in text for k in ['理发', '剪刀', '美发师', '吹风机', '理发围布']):
                service_votes.append('理发服务')
            elif any(k in text for k in ['做饭', '炒菜', '锅', '菜刀', '厨房', '炒锅']):
                service_votes.append('做饭服务')
            else:
                service_votes.append('无法判定')

        predict_type = Counter(service_votes).most_common(1)[0][0]

    except Exception as e:
        return {
            "isSuccess": False,
            "error_service": f"模型调用失败或返回格式错误：{str(e)}"
        }

    if predict_type == service_type:
        isSuccess = True
        error_service = f"无异常，上传图片类型为：{predict_type}，而工单原本类型为：{service_type}。"
    else:
        isSuccess = False
        error_service = f"服务类型与上传图片不符异常，上传图片类型为：{predict_type}，而工单原本类型为：{service_type}。"

    return {
        "isSuccess": isSuccess,
        "error_service": error_service
    }

# 示例调用
if __name__ == "__main__":
    service_img = (
        "http://www.mcwajyfw.com/imagemc/202401/20240122/9/0/ad4c987f3cc94c8986df357c7836a0611705912207589.jpeg,"
        "http://www.mcwajyfw.com/imagemc/202401/20240122/14/2/9dd81a4ff583428c95d57c15d4cc4c971705912311528.jpeg,"
        "http://www.mcwajyfw.com/imagemc/202401/20240122/9/6/b50998e8f42945f3b0caf305e0b983531705912430089.jpeg"
    )
    service_type = "理发服务"
    result = judge_service_type(service_img, service_type)
    #print(result)