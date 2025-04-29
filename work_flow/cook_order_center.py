from pprint import pprint
from flask import Blueprint, jsonify,request,abort
import requests
import json
from work_flow.siliconAPI import get_api_inference
prompt = ('# 角色'
           '您是「居家养老服务质量审核专家」，需验证服务真实性。'

           '## 技能'
           '## 技能 1: 图片元素观察'
           '1. 观察是否有用餐的老人出镜。'
           '2. 观察是否有志愿者出镜，注意限制中对志愿者的说明。'
           '3. 观察是否有生食材出现。'
           '4. 观察是否有菜品出现（烹饪中或已装盘）。'
           '===回复示例==='
           '{'
           '    "elder": "<若有老人出境，描述老人状态（如坐姿、手持餐具等），若无则标注“未发现>",'
           '    "assistant": "< 若存在志愿者，描述志愿者行为，若无志愿者或是无关人员则标注“未发现” >",'
           '    "ingredients": "< 若存在生食材分析具体种类（如番茄、牛肉等），若无则标注“未发现” >",'
           '    "food":"<若存在菜品分析菜品原材料（如“番茄炒蛋”需标注番茄、鸡蛋），若无则标注“未发现”>",'
           '    "think": "<思考过程>"'
           '}'
           '===示例结束==='

           '## 限制:'
           '- 严格基于图片内容描述，禁止虚构或推测。'
           '- 所输出的内容必须按照给定的格式进行组织，不能偏离框架要求。'
           '- 无做菜、炒菜、处理食材、与老人同出镜四种情形的人员，算作无关人员。'
           '- 志愿者可以只出镜部分身体，比如正在炒菜的志愿者只露出握着锅铲的手，此刻也算在存在志愿者。'
           '- 志愿者用刀切的食材，也应算作观察到食材，需在ingredients中列出种类。'
           '- 若原材料或食材种类不确定，猜测一个确切种类，并在该种类前面加上"疑似"，比如"疑似面团""。'
           '- 对于图中同一位置的食品，只能归纳到食物和食材其中之一。'
           '- JSON格式必须标准规范，结尾不能有逗号。'
)

@bp.route('/center_results', methods=['GET'])
def center_results():
    API_KEY = 'sk-5ef7d974952841e08eb3d461bd759cc5'
    API_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
    model = "qwen-vl-plus"
    url = 'http://mofrp.top:10846/'
    urls=request.args.get('center_images')
    print(urls)

    prompt = ('# 角色'
              '您是「居家养老服务质量审核专家」，需验证服务真实性。'

              '## 技能'
              '## 技能 1: 图片元素观察'
              '1. 观察是否有用餐的老人出镜。'
              '2. 观察是否有志愿者出镜，注意限制中对志愿者的说明。'
              '3. 观察是否有生食材出现。'
              '4. 观察是否有菜品出现（烹饪中或已装盘）。'
              '===回复示例==='
              '{'
              '    "elder": "<若有老人出境，描述老人状态（如坐姿、手持餐具等），若无则标注“未发现>",'
              '    "assistant": "< 若存在志愿者，描述志愿者行为，若无志愿者或是无关人员则标注“未发现” >",'
              '    "ingredients": "< 若存在生食材分析具体种类（如番茄、牛肉等），若无则标注“未发现” >",'
              '    "food":"<若存在菜品分析菜品原材料（如“番茄炒蛋”需标注番茄、鸡蛋），若无则标注“未发现”>",'
              '    "think": "<思考过程>"'
              '}'
              '===示例结束==='

              '## 限制:'
              '- 严格基于图片内容描述，禁止虚构或推测。'
              '- 所输出的内容必须按照给定的格式进行组织，不能偏离框架要求。'
              '- 无做菜、炒菜、处理食材、与老人同出镜四种情形的人员，算作无关人员。'
              '- 志愿者可以只出镜部分身体，比如正在炒菜的志愿者只露出握着锅铲的手，此刻也算在存在志愿者。'
              '- 志愿者用刀切的食材，也应算作观察到食材，需在ingredients中列出种类。'
              '- 若原材料或食材种类不确定，猜测一个确切种类，并在该种类前面加上"疑似"，比如"疑似面团""。'
              '- 对于图中同一位置的食品，只能归纳到食物和食材其中之一。'
              '- JSON格式必须标准规范，结尾不能有逗号。'
              )

    data = {
        'prompt': prompt,
        'urls': urls
    }
    response = get_api_inference(API_URL, API_KEY, model, prompt, urls)

    img = response[0]
    x = img['response']
    x = json.loads(x[8:-3], strict = False)

    error2_elder = x['elder']
    error2_assistant = x['assistant']
    ingredients = x['ingredients']
    food = x['food']
    think = x['think']

    error2_elder = '未发现老人' if error2_elder == '未发现' else error2_elder
    error2_assistant = '未发现志愿者' if error2_assistant == '未发现' else error2_assistant

    print(error2_assistant)
    print(error2_elder)
    print(ingredients)
    print(food)
    print(think)

    data = {
        'prompt' : ('# 角色'
        '您作为「居家养老服务质量审核专家」，善于根据多维度规则判断养老服务工单是否存在食材逻辑矛盾。'
    
        '## 技能'
        '### 技能 1: 智能化食材一致性校验'
        '1. 建立食材映射关系时允许：'
        '生鲜食材经加工后的形态变化（如肉→肉片，笋→笋片）'
        '调味辅料的合理省略（如熟食列表可能省略盐、酱油等）'
        '同类食材替代（如腊肉归属肉类大分类）'
        '2. 触发异常的条件：'
        '所有的主食材都明显矛盾（如生食材无鱼类但熟食出现鱼片），判断为明显异常;'
        '超过30%关键材料无法建立关联;'
        '两个输入任意一个为空，则判断为异常；'
        '===回复示例==='
        '{'
        '"food_ingre_error": "<若触法异常，则标注"异常"，并附加原因，若无则仅标注“无异常>"'
        '"think": "<思考过程>"'
        '}'
        '===示例结束==='
    
        '## 限制:'
        '- 采用模糊匹配原则，允许食材形态转换和合理损耗'
        '- 重点关注蛋白质来源、主食、蔬菜的三大类匹配度'
        '- 对调味料、香料等非主要成分不做强制对应要求'
        '- 所输出的内容必须按照给定的格式进行组织，不能偏离框架要求。'
    
        '## 食材与菜品信息:'
        '菜品:' + food +
        '食材:' + ingredients),
    }

    if API_URL and API_KEY and model:
        response = get_api_inference(API_URL, API_KEY, model, data)
    else:
        response = requests.post(url=url + 'understand', data=data).json()
    pprint(response)

    x = response[0]
    x = json.loads(x[8:-3])
    print(x)

    food_ingre_error = x['food_ingre_error']

    return food_ingre_error, error2_elder, error2_assistant

if __name__ == "__main__":
    center_images = "http://www.mcwajyfw.com/imagemc/202401/20240108/11/6/f44133e280f94f65a939729b156a019f1704682364557.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240108/3/2/7d863c93d5ef461dbbc2e1e1c97536b61704682383083.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240108/2/5/14a60a448fdb4ccc9ba390045df99b601704683320010.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240108/7/2/1ad7d9d289ac423ebebfc9ec9f05c9ca1704684681614.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240108/7/7/37952d5a447b4d7db145f6ba93a061cb1704686683057.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240108/0/1/1ba1aafdee7e499688015ade35cb7c461704688386457.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240108/0/15/78ec41f177da43d9ba94537b2298e8491704690099395.jpeg,http://www.mcwajyfw.com/imagemc/202401/20240108/1/9/c2078feb365c4775a12266d62f343a5a1704690184238.jpeg"
    API_KEY = 'sk-5ef7d974952841e08eb3d461bd759cc5'
    API_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
    MODEL = "qwen-vl-plus"
    food_ingre_error, error2_elder, error2_assistant = center_results(center_images, API_URL, API_KEY, MODEL)

    print(food_ingre_error)
    print(error2_elder)
    print(error2_assistant)
