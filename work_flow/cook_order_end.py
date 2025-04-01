import requests
import json

def end_results(urls):
    url = 'http://mofrp.top:10846/'
    data = {
        'prompt': (
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
        ),
        'urls': urls
    }

    # ========== 请求处理部分 ==========
    response = requests.post(url=url + 'understand', data=data)
    # print(f"状态码: {response.status_code}")
    # print("原始响应:", response.json())

    # ========== 数据解析部分 ==========
    datas = []
    for img in response.json():
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
    end_images = "http://www.mcwajyfw.com/imagemc/202401/20240108/11/7/d51136647ad543659357d6e15f5909611704681768442.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240108/10/12/4939348216f045a8b8d44a3c2494163c1704681775478.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240108/15/14/cfadcad343574d06994b0c805f2e2efb1704690135160.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240108/12/1/0c2b7818be20425eb5c3e7397f24c37a1704690143832.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240108/6/11/0db7fb90fbb947368e66aacd2c8b19901704690153756.jpeg"
    error3_signature, error3_elder, end_time = end_results(end_images)

    print(error3_signature)
    print(error3_elder)
    print(end_time)
