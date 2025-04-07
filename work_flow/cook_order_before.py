import requests
import json

def before_results(url, urls):
    # API 基础 URL
    # url = 'http://mofrp.top:10846/'

    # 定义数据
    data = {
        'prompt': (
            '# 角色定位\n'
            '作为「居家养老服务质量审核专家」，需基于视觉证据严格验证服务真实性\n\n'
            
            '# 核心验证维度\n'
            '1. 时间真实性验证\n'
            '2. 服务对象真实性验证\n'
            '3. 服务地点真实性验证\n\n'
            
            '# 验证标准\n'
            '## 时间验证（必选）\n'
            '- 提取图片左上角显示的拍摄时间\n'
            '- 格式必须严格遵循：YYYY-MM-DD HH:MM:SS（如2024-03-02 12:14:10）\n\n'
            
            '## 老人识别标准（必选）\n'
            '- 有效特征：出现任意老人身体部位（含未露出面部的情况）\n'
            '- 需描述：\n'
            '  a) 老人当前动作状态（如"坐姿/手持餐具/行走"等）\n'
            '  b) 若未识别到，标注"未发现"\n\n'
            
            '## 门牌识别标准（必选）\n'
            '- 分级判定：\n'
            '  1级：仅出现门框/门体 → 标注"存在门框"\n'
            '  2级：可见门牌信息 → 提取完整信息（如"3栋2单元501"）\n'
            '  3级：均未发现 → 标注"未发现"\n\n'
            
            '# 输出规范\n'
            '{\n'
            '  "time": "<精确到秒的时间戳 | 未识别时标注\'时间信息缺失\'>",\n'
            '  "elder": "<动作状态描述 | \'未发现\'>",\n'
            '  "doorplate": "<完整门牌信息 | \'存在门框\' | \'未发现\'>",\n'
            '  "think": "【验证依据】\n'
            '    1. 时间来源：{描述时间提取位置}\n'
            '    2. 老人识别：{列出具体身体特征}\n'
            '    3. 门牌识别：{说明判定依据等级}"\n'
            '}\n\n'
            
            '# 严格限制\n'
            '1. 时间格式错误直接判定验证失败\n'
            '2. 否定结论必须包含具体缺失项（如"未识别到老人下肢/手臂等身体特征"）\n'
            '3. 禁止以下行为：\n'
            '   - 推测性描述（如"可能"、"应该"等）\n'
            '   - 超出视觉证据的判断\n'
            '   - 修改JSON结构或键名'
        ),
        'urls': urls
    }

    # 调用 API 分析图片
    response = requests.post(url=url + 'understand', data=data)
    # print(response.status_code)
    # print(response.json())

    # 初始化变量
    datas = []
    start_time = ''
    error1_elder = ''
    error1_door = ''
    error_season = ''

    # 解析 API 返回的数据
    for img in response.json():
        try:
            x = img['response']
            json_str = x.split('```json\n')[1].split('\n```')[0] if '```json' in x else x
            x = json.loads(json_str)
            print(x)
            da = {
                'start_time': x['time'],
                'elder': True if x.get('elder', '未发现') != '未发现' else False,
                'elder_state': x['elder'],
                'doorplate': x['doorplate'],
            }
            datas.append(da)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"解析错误: {e}")

    # 遍历数据，进行季节异常判断
    for d in datas:
        start_time += d['start_time'] + ','

        if d['doorplate'] != '未发现':
            error1_door += d['doorplate'] + ','
        # if d['elder']:
        if d['elder']:
            error1_elder += d['elder_state'] + ','

            # 调用 API 进行季节推断
            data2 = {
                'prompt': (
                    '# 角色'
                    '你是一个专业的视觉分析助手。'
                    '## 任务'
                    '1. **输入处理**：接收用户提供的图片和时间（自动提取1-12月数字）。'
                    '2. **服装识别**：分析图中人物着装特征（包括服装类型、材质、厚度、暴露皮肤面积等）。'
                    '3. **季节推断**：根据服装特征判断图片对应的季节（春季/夏季/秋季/冬季）。'
                    '4. **异常判断**：对比图片季节与月份季节是否一致，标记异常情况（如7月着羽绒服）。'
                    '5. **格式化输出**：按以下结构严格输出结果：'
                    '{'
                    '"month": "<输入日期的月份>",'
                    '"season": "<季节推断>",'
                    '"error": "<若存在异常，则添加验证逻辑说明；若无异常，则标记"无异常"">"'
                    '}'
                    '## 限制'
                    '- 严格基于图片内容描述，禁止虚构或推测。'
                    '- 所输出的内容必须按照给定的格式进行组织，不能偏离框架要求。'
                    '- 若验证结果为否定，否定结论需标明具体缺失项，必须详细说明缺失的具体项。'
                ),
                'urls': data['urls'].split(',')[0],  # 使用第一张图片
                'time': datas[0]['start_time']  # 使用第一张图片的时间
            }
            response2 = requests.post(url=url + 'analysis', data=data2)
            # print(response2.status_code)
            # print(response2.json())

            x = response2.json()['response']
            json_str = x.split('```json\n')[1].split('\n```')[0] if '```json' in x else x
            x = json.loads(json_str)
            print(x)

            # 处理季节推断结果
            db = {
                'month': x['month'],
                'season': x['season'],
                'error': True if x['error'] != '无异常' else False,
            }

            if db['error']:
                error_season = x.get('error', '') + ','
        # else:
        #     error1_elder += '未发现,'

    # 判断 error1_elder 是否全为“未发现”
    # if all(state == '未发现' for state in error1_elder.split(',')):
    #     error1_elder = '异常'
    error1_elder = '不存在老人' if error1_elder == '' else error1_elder

    # 输出结果
    return start_time, error1_elder, error1_door, error_season

if __name__ == '__main__':
    before_images = "http://www.mcwajyfw.com/imagemc/202401/20240108/11/7/d51136647ad543659357d6e15f5909611704681768442.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240108/10/12/4939348216f045a8b8d44a3c2494163c1704681775478.jpeg"
    # before_images = "http://www.mcwajyfw.com/imagemc/202401/20240122/5/10/22f522292cff4942870a9c1c6e653c7f1705912038277.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240122/9/0/ad4c987f3cc94c8986df357c7836a0611705912207589.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240122/14/2/9dd81a4ff583428c95d57c15d4cc4c971705912311528.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240122/9/6/b50998e8f42945f3b0caf305e0b983531705912430089.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240122/11/10/84f28d4d77f648d7a8242b7dc463331b1705912968105.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240122/13/12/8821b38ea8c54e70b84b38d48f0916c81705913418125.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240122/6/9/4bb63ad00e814435a48895092b0401911705913524558.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240122/3/5/98b644c0e5d2473d83546bd61851824a1705913662463.jpeg"

    start_time, error1_elder, error1_door, error_season = before_results(before_images)

    print(start_time)
    print(error1_elder)
    print(error1_door)
    print(error_season)