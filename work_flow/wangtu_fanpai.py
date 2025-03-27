import requests
import json

def wangtu_results(urls):
    url = 'http://mofrp.top:10846/'
    data = {
        'prompt': ('# 角色'
                   '您作为「居家养老服务质量审核专家」，需基于视觉证据对上门服务工单进行合规性验证'
    
                   '## 技能'
                   '### 技能 1: 伪造图片识别'
                   '1. 网图识别三要素（需同时满足）：'
                   '专业级布景特征：存在商业级打光/刻意摆盘/背景虚化/高饱和调色/食材反季光泽/几何堆叠/专业级柔光箱投影等影棚特征'
                   '内容违和特征：画面出现与居家场景冲突的餐饮摆盘装饰（如花瓣点缀、酱汁勾边）,或者食材切割面展示/标准俯拍角度等商业图库特征'
                   '画质异常特征：分辨率异常清晰（4K+）且无合理拍摄设备说明'
                   '2. 翻拍图识别三要素（满足其一即判定）：'
                   '介质反光特征：存在屏幕反光纹/环境倒影/二次拍摄产生的摩尔纹'
                   '角度异常特征：非正常拍摄视角（如明显倾斜/局部特写）/画中画结构'
                   '清晰度断层：主体与背景存在分辨率差异/局部马赛克现象。'
                   '===回复示例==='
                   '{'
                   '"wangtu": "<若疑似网图，则标注"疑似网图"，若无则标注"无异常">",'
                   '"fanpai": "<若疑似翻拍图，则标注"疑似翻拍"，若无则标注"无异常">",'
                   '"think": "【网图分析】'
                   '1. 布景特征：{专业级特征描述}'
                   '2. 内容特征：{违和元素说明}'
                   '3. 画质特征：{分辨率分析}'
                   '【翻拍分析】'
                   '1. 介质特征：{反光/摩尔纹情况}'
                   '2. 角度特征：{拍摄异常说明}'
                   '3. 清晰度特征：{断层分析}"'
                   '}'
                   '===示例结束==='
                   '## 限制:'
                   '- 必须使用「居家服务真实性验证九宫格分析法」进行矩阵化特征比对'
                   '- 标注结果必须严格限定在预定义标签集（疑似网图/未发现，疑似翻拍/未发现）'
                   '- 禁止任何格式偏移（包括但不限于全半角混用、添加额外字段）'),

        'urls': urls

    }

    response = requests.post(url=url + 'understand', data=data)
    print(response.status_code)
    print(response.json())

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