from flask import Blueprint, jsonify
import json
from datetime import datetime

bp = Blueprint(name='work_order', import_name=__name__,url_prefix='/work_order')
# 接收前端工单号并返回对应数据
@bp.route('/orderId/<int:order_id>', methods=['GET'])
def get_work_order(order_id):

    print(order_id)



    # response = call_coze_api(order_id)
    # #faiden=face_identify(order_id)
    # data_json = json.loads(response['data'])  # 解析嵌套的 JSON 字符串
    # orderInfo = {
    #     "order_id": data_json["order_id"],
    #     "member_id": data_json["member_id"],
    #     "start_time": data_json["start_time"],
    #     "end_time": data_json["end_time"]
    # }
    # print(orderInfo)
    # data = []
    # for k, v in data_json.items():
    #     if k.startswith("error"):  # 只处理 "error" 开头的 key
    #         t = False
    #         if isinstance(v, str) and "无异常" in v:
    #             t = True
    #         if k== "error2_elder"or k== "error2_assisstant"or k== "error1_door"or k== "error3_elder" or k== "error1_elder":
    #             for item in v:
    #                 if item!="未发现":
    #                     t=True
    #         if t or v=="" or v==[]:
    #
    #             continue
    #         else :
    #             data.append({"key": k, "value": v})  # 存入符合条件的项
    # start_time = datetime.strptime(orderInfo["start_time"], "%Y-%m-%d %H:%M:%S")
    # end_time = datetime.strptime(orderInfo["end_time"], "%Y-%m-%d %H:%M:%S")
    # # 计算时间差
    # time_difference = end_time - start_time
    # hours = time_difference.seconds // 3600
    # if hours > 3:
    #     data.append({"key": "error_duration", "value": "服务时间为："+str(hours)+"异常"})
    #
    # msg=0
    # if any((d["key"] == "error2_food_ingr" or d["key"] == "error2_elder" or d["key"] == "error2_assisstant" ) for d in data):
    #     msg=2
    # elif len(data)>=1:
    #     msg=1
    # else:
    #     msg=0
    #
    # url= {"before_imgs": data_json["before_imgs"], "center_imgs": data_json["center_imgs"], "end_imgs":data_json["end_imgs"]}
    #
    # data=[{"key": error_mapping.get(item["key"], item["key"]), "value": item["value"]} for item in data]
    #
    # res={
    #     'msg':msg,
    #     'data':data,
    #     'orderInfo':orderInfo,
    #     'url':url
    # }
    # return jsonify(res), 200




error_mapping = {
    "error2_food_ingr": "服务中：食材不匹配异常",
    "error2_elder": "服务中：无老人异常",
    "error2_assisstant": "服务中：无志愿者异常",
    "error1_elder": "服务前：不存在老人异常",
    "error_season": "着装与季节不符异常",
    "error_service": "上传图片与服务不符异常",
    "error_wang_fan": "网图、翻拍异常",
    "error1_door": "服务前：缺门牌号异常",
    "error_duration": "服务时长异常",
    "error3_signature": "服务后：签字表异常",
    "error3_elder": "服务后，不存在老人异常",
}

