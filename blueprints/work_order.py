from flask import Blueprint, jsonify
import json
from datetime import datetime
from database_models import WorkOrderModel, ServiceModel,ServiceLogModel

bp = Blueprint(name='work_order', import_name=__name__,url_prefix='/work_order')
# 接收前端工单号并返回对应数据
@bp.route('/orderId/<int:order_id>', methods=['GET'])
def get_work_order(order_id):
    print(order_id)
    order = ServiceLogModel.query.filter_by(id=order_id).first()
    print(order.to_dict())

    return jsonify(order.to_dict()), 200
@bp.route('/serviceId/<int:serviceId>', methods=['GET'])
def get_order_by_serviced(serviceId):
    order = ServiceModel.query.filter_by(service_id=serviceId).first()
    print(order)

@bp.route('/assistant/<int:assistant>', methods=['GET'])
def get_order_by_assistant(assistant):
    order = WorkOrderModel.query.filter_by(handler=assistant).first()
    print(order)


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

