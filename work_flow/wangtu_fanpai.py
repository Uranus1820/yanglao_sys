import requests
import json

def wangtu_results(url, urls):
    # url = 'http://mofrp.top:10846/'
    data = {
        'prompt': (
            '# 角色定义\n'
            '您作为「居家养老服务质量审核专家」，负责基于视觉证据对上门服务工单进行真实性核查\n\n'
            
            '# 核心任务\n'
            '使用「居家服务真实性验证九宫格分析法」对图片进行矩阵化特征比对，完成以下判定：\n'
            '1. 商业网图识别\n'
            '2. 翻拍图片识别\n\n'
            
            '# 识别标准\n'
            '## 商业网图判定标准（需同时满足3项）\n'
            '1. 专业布景特征：存在以下任一特征\n'
            '   - 商业级打光/刻意摆盘\n'
            '   - 背景虚化/高饱和调色\n'
            '   - 食材反季光泽/几何堆叠\n'
            '   - 专业级柔光箱投影等影棚特征\n'
            '2. 内容违和特征：存在以下任一特征\n'
            '   - 与居家场景冲突的餐饮摆盘装饰（花瓣点缀/酱汁勾边）\n'
            '   - 食材切割面展示/标准俯拍角度等商业图库特征\n'
            '3. 画质异常特征：\n'
            '   - 分辨率异常清晰（4K+）且无合理拍摄设备说明\n\n'
            
            '## 翻拍图判定标准（满足任一即可）\n'
            '1. 介质反光特征：存在以下任一特征\n'
            '   - 屏幕反光纹/环境倒影\n'
            '   - 二次拍摄产生的摩尔纹\n'
            '2. 角度异常特征：\n'
            '   - 非正常拍摄视角（明显倾斜/局部特写）\n'
            '   - 画中画结构\n'
            '3. 清晰度断层：\n'
            '   - 主体与背景存在分辨率差异\n'
            '   - 局部马赛克现象\n\n'
            
            '# 输出规范\n'
            '必须严格按以下格式输出（包括标点符号）：\n'
            '{\n'
            '  "wangtu": "<"疑似网图"|"无异常">",\n'
            '  "fanpai": "<"疑似翻拍"|"无异常">",\n'
            '  "think": "【网图分析】\n'
            '    1. 布景特征：{具体特征描述}\n'
            '    2. 内容特征：{具体违和元素}\n'
            '    3. 画质特征：{分辨率情况}\n'
            '    【翻拍分析】\n'
            '    1. 介质特征：{反光情况}\n'
            '    2. 角度特征：{拍摄视角分析}\n'
            '    3. 清晰度特征：{断层说明}"\n'
            '}\n\n'
            
            '# 严格限制\n'
            '1. 必须使用九宫格分析法进行矩阵比对\n'
            '2. 结果标签仅允许使用预定义值（疑似网图/无异常，疑似翻拍/无异常）\n'
            '3. 禁止任何格式偏移（包括但不限于）：\n'
            '   - 全半角混用\n'
            '   - 添加额外字段\n'
            '   - 修改输出结构'
        ),

        'urls': urls

    }

    response = requests.post(url=url + 'understand', data=data)
    # print(response.status_code)
    # print(response.json())

    datas = []
    for img in response.json():
        x = img['response']
        x = json.loads(x[8:-4])
        print(x)


    da = {
            'wangtu': True if x['wangtu'] != '无异常' else False,
            'wangtu_state':x['wangtu'],
            'fanpai': True if x['fanpai'] != '无异常' else False,
            'fanpai_state': x['fanpai'],
            'think': x['think'],
                }
    datas.append(da)

    error2_wangtu = ''
    error2_fanpai = ''
    think = ''

    for d in datas:
        if d['wangtu'] != '无异常':
            error2_wangtu += d['wangtu_state'] + ','
        if d['fanpai'] != '无异常':
            error2_fanpai += d['fanpai_state'] + ','
        if d['think']:
            think += d['think'] + ','

    return error2_wangtu, error2_fanpai, think

if __name__ == '__main__':
    wangtu_images = ("http://www.mcwajyfw.com/imagemc/202401/20240108/11/7/d51136647ad543659357d6e15f5909611704681768442.jpeg,"
                    "http://www.mcwajyfw.com/imagemc/202401/20240108/10/12/4939348216f045a8b8d44a3c2494163c1704681775478.jpeg,"
                    "http://www.mcwajyfw.com/imagemc/202401/20240108/11/6/f44133e280f94f65a939729b156a019f1704682364557.jpeg,"
                    "http://www.mcwajyfw.com/imagemc/202401/20240108/3/2/7d863c93d5ef461dbbc2e1e1c97536b61704682383083.jpeg,"
                    "http://www.mcwajyfw.com/imagemc/202401/20240108/2/5/14a60a448fdb4ccc9ba390045df99b601704683320010.jpeg,"
                    "http://www.mcwajyfw.com/imagemc/202401/20240108/7/2/1ad7d9d289ac423ebebfc9ec9f05c9ca1704684681614.jpeg,"
                    "http://www.mcwajyfw.com/imagemc/202401/20240108/7/7/37952d5a447b4d7db145f6ba93a061cb1704686683057.jpeg,"
                    "http://www.mcwajyfw.com/imagemc/202401/20240108/0/1/1ba1aafdee7e499688015ade35cb7c461704688386457.jpeg,"
                    "http://www.mcwajyfw.com/imagemc/202401/20240108/0/15/78ec41f177da43d9ba94537b2298e8491704690099395.jpeg,"
                    "http://www.mcwajyfw.com/imagemc/202401/20240108/1/9/c2078feb365c4775a12266d62f343a5a1704690184238.jpeg,"
                    "http://www.mcwajyfw.com/imagemc/202401/20240108/15/14/cfadcad343574d06994b0c805f2e2efb1704690135160.jpeg,"
                    "http://www.mcwajyfw.com/imagemc/202401/20240108/12/1/0c2b7818be20425eb5c3e7397f24c37a1704690143832.jpeg,"
                    "http://www.mcwajyfw.com/imagemc/202401/20240108/6/11/0db7fb90fbb947368e66aacd2c8b19901704690153756.jpeg")
    error2_wangtu, error2_fanpai, think = wangtu_results(wangtu_images)

    print(error2_wangtu)
    print(error2_fanpai)
    print(think)