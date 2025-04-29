from json import JSONDecodeError
from pprint import pprint
import re
import requests
import json
from flask import Blueprint, jsonify,request,abort
from work_flow.siliconAPI import get_api_inference
bp = Blueprint(name='image_end', import_name=__name__,url_prefix='/image_end')
prompt = (
            '# 角色\n'
            '您作为「双图时序核验专家」，需通过服务前/后双图比对验证服务真实性。\n\n'
            '## 多图处理技能\n'
            '### 技能 1: 次图核验（服务结束时）\n'
            '1. 识别图片左上角拍摄时间。\n'
            '2. 根据人物衣着及外貌特征检测是否有老人出现（出现老人身体部位即视为有效，未露出面部也算有效）。\n'
            '3. 检测是否有签字表出现及是否与老人同框。\n\n'
            '===回复示例===\n'
            '{\n'
            '      "time": <图中提取的时间，如2024-03-02 12:14:10>,\n'
            '      "elder": "<若有老人，描述动作状态（如坐姿、手持餐具、吃饭、洗碗、洗手等），若无则标注”未发现“>",\n'
            '      "signature": "<若出现签字表且签字表与老人同框，则标记"无异常"；若仅出现签字表，则标注"疑似异常"，若均无则标出“异常”>",\n'
            '      "think": "<验证逻辑说明>"\n'
            '}\n'
            '===示例结束===\n\n'
            '## 限制:\n'
            '- 时间格式必须严格遵循示例格式\n'
            '- 禁止任何推测性描述\n'
            '- 老人检测包含部分身体特征\n'
            '- 签字表状态需明确标注同框情况'
            '- JSON格式必须标准规范，结尾不能有逗号。'
)
@bp.route('/end_results', methods=['GET'])
def end_results():
    url = 'http://mofrp.top:10846/'
    API_KEY = 'sk-5ef7d974952841e08eb3d461bd759cc5'
    API_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
    model = "qwen-vl-plus"
    urls=request.args.get('end_images')

    # print(prompt[0])
    # ========== 请求处理部分 ==========
    data = {
        'prompt': prompt,
        'urls': urls
    }
    if API_URL and API_KEY and model:
        response = get_api_inference(API_URL, API_KEY, model, prompt, urls)
    else:
        response = requests.post(url=url + 'understand', data=data).json()
    print(response[0]['response'])

    # ========== 数据解析部分 ==========
    datas = []
    for img in response:
        x = img['response']
        x = json.loads(x[8:-4])
        print(x)
        # 数据转换
        da = {
                'time_valid': False,
                'time': x.get('time', ''),  # 使用 get 方法
                'has_elder': x.get('elder', '未发现') != '未发现',  # 使用 get 方法
                'elder_state': x.get('elder', '未发现'),  # 使用 get 方法
                'signature_status': x.get('signature', '异常'),  # 使用 get 方法
                'think_log': x.get('think', '')  # 使用 get 方法
        }
        datas.append(da)

    error3_signature = ''
    error3_elder = ''
    end_time = ''

    for d in datas:
        # 只需使用已存在的字段
        if d['has_elder']:  # 如果有老人
            error3_elder += d['elder_state'] + ','  # 增加老人状态
        error3_signature += d['signature_status'] + ','  # 始终增加签字表状态

        if d['time']:  # 如果时间存在
            end_time += d['time'] + ','  # 增加时间信息

    # 输出结果
    return error3_signature, error3_elder, end_time

if __name__ == '__main__':
    # end_images = "http://www.mcwajyfw.com/imagemc/202401/20240108/11/7/d51136647ad543659357d6e15f5909611704681768442.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240108/10/12/4939348216f045a8b8d44a3c2494163c1704681775478.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240108/15/14/cfadcad343574d06994b0c805f2e2efb1704690135160.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240108/12/1/0c2b7818be20425eb5c3e7397f24c37a1704690143832.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240108/6/11/0db7fb90fbb947368e66aacd2c8b19901704690153756.jpeg"
    # API_KEY = 'sk-5ef7d974952841e08eb3d461bd759cc5'
    # API_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
    # MODEL = "qwen-vl-plus"
    # url = 'http://mofrp.top:10846/'
    # # error3_signature, error3_elder, end_time = end_results(url, end_images, API_URL, API_KEY, MODEL)
    # end_results(url, end_images, API_URL, API_KEY, MODEL)

    # print(error3_signature)
    # print(error3_elder)
    # print(end_time)

    def normalize_json_quotes(json_str):
        # 第一步：消除所有换行符
        no_newlines_str = json_str.replace('\n', '')
        # 第一步：将所有引号统一转换为英文引号
        normalized_str = no_newlines_str.replace('“', '"').replace('”', '"')

        result = []
        i = 0
        n = len(normalized_str)

        while i < n:
            char = normalized_str[i]

            if char == '"':
                # 检查是否应该保留为英文引号
                # 左引号检查
                is_valid_left = False
                left = i - 1
                while left >= 0 and normalized_str[left] in ' \n\t\r':
                    left -= 1
                if left >= 0 and normalized_str[left] in '{[,:':
                    is_valid_left = True

                # 右引号检查
                is_valid_right = False
                right = i + 1
                while right < n and normalized_str[right] in ' \n\t\r':
                    right += 1
                if right < n and normalized_str[right] in '],}:':
                    is_valid_right = True

                # 确定引号类型
                if is_valid_left and not is_valid_right:
                    # 这是合法的左引号
                    result.append('"')
                elif is_valid_right and not is_valid_left:
                    # 这是合法的右引号
                    result.append('"')
                elif is_valid_left and is_valid_right:
                    # 可能是空字符串""情况
                    result.append('"')
                else:
                    # 需要转换为中文引号
                    # 判断是左引号还是右引号
                    # 查找最近的未闭合的左引号
                    stack = []
                    for j in range(len(result)):
                        if result[j] == '"':
                            if len(stack) > 0 and stack[-1] == 'left':
                                stack.pop()
                            else:
                                stack.append('left')
                        elif result[j] in ('“', '”'):
                            # 忽略中文引号
                            pass

                    if len(stack) > 0 and stack[-1] == 'left':
                        # 有未闭合的左引号，这是右引号
                        result.append('”')
                    else:
                        # 否则是左引号
                        result.append('“')

                i += 1
            else:
                result.append(char)
                i += 1

        return ''.join(result)

    sd = """{
    "elder": "存在老人",
    "assistant": "烹饪",
    "ingredients": "疑似猪肉（用于炖煮） | 猪骨块 (可能)",
    "food": "米饭、炖菜",
    "think": "第一张图片显示了大米被放入电饭煲内。第二张图片展示了水倒入电饭煲里准备蒸制。第三张图片表明正在用电饭煲进行加热操作以完成炊事工作。\n第四张图片展示了一位志愿者正将一块肉类切割成小块放在砧 
板上，这似乎是为后续的食物制作做准备工作的一部分。“第五张图片中有两个人一起用火炉炒菜。”第六张图片是一位老年人手持一碗白米饭的画面，“第七张图片则是在户外环境中一位老人生吃着刚做的饭菜，在旁边有一个大铁里面装有炖好的菜肴"。第八张图片是一个人在清洗餐具或者工具的过程,但没有明确看到与食物相关的活动内容."
}
"""
    sd = normalize_json_quotes(sd)
    print(sd)
    sd = json.loads(sd)
    print(sd)
