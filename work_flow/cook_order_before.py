import requests
import json

def before_results(urls):
    # API 基础 URL
    url = 'http://mofrp.top:10846/'

    # 定义数据
    data = {
        'prompt': (
            '# 角色'
            '您作为「居家养老服务质量审核专家」，需同时验证服务真实性。'
            '## 技能'
            '### 技能1：图片元素识别'
            '1. 识别图片左上角的拍摄时间。'
            '2. 根据人物衣着及外貌特征检测是否有老人出现（出现老人身体部位即视为有效，未露出面部也算有效）。'
            '3. 识别是否有门出现（有门或者门的一部分出现即为有效），若有门牌号码出现，则识别门牌号码等信息（如楼栋/单元/户号）。'
            '## 输出格式'
            '{'
            '"time": "<图中提取的时间，如2024-03-02 12:14:10>",'
            '"elder": "<若有老人出现，描述老人当前动作或状态（如坐姿、手持餐具、吃饭、洗碗、洗手等），若无则标注”未发现“>",'
            '"doorplate": "<若只出现门，则标注"存在门框"； 若有门牌信息出现，描述具体的门牌信息；若均无则标出“未发现”>",'
            '"think": "<验证逻辑说明>"'
            '}'
            '## 限制'
            '- 使用结构化JSON输出格式'
            '- 禁止任何推测性描述'
            '- 仅输出视觉可验证元素'
            '- 时间格式严格遵循示例'
            '- 若验证结果为否定，否定结论需标明具体缺失项，必须详细说明缺失的具体项，如“未识别到老人出现”等'
        ),
        'urls': urls
    }

    # 调用 API 分析图片
    response = requests.post(url=url + 'understand', data=data)
    print(response.status_code)
    print(response.json())

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
            print(response2.status_code)
            print(response2.json())

            x = response2.json()['response']
            json_str = x.split('```json\n')[1].split('\n```')[0] if '```json' in x else x
            x = json.loads(json_str)

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