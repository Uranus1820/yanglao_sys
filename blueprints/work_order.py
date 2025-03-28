from flask import Blueprint, jsonify,request,abort
import json
from datetime import datetime
from database_models import WorkOrderModel, ServiceModel,ServiceLogModel
import requests

bp = Blueprint(name='work_order', import_name=__name__,url_prefix='/work_order')
# 接收前端工单号并返回对应数据
@bp.route('/list')
def get_all_order_id():
    data = {"list": [], "total": []}
    orders=[]
    page = int(request.args.get('currentPage', 1))  # 获取页码，默认为第一页
    per_page = int(request.args.get('size', 10))  # 获取每页显示的数据量，默认为 10 条
    pagination = WorkOrderModel.query.paginate(page=page, per_page=per_page,error_out=False)  # 使用 paginate() 方法进行分页查询，不抛出异常
    orders = pagination.items
    data['total'] = pagination.total
    for order in orders:
        service = get_work_orderByid(order.id, order.service_id)
        service_name=ServiceModel.query.filter_by(id=order.service_id).first().name
        if service_name is None:
            service_name="未知"
        else:
            service_name=service_name
        flag=1
        if service is None: flag=0
        order_data = {
            "orderId": order.id,
            "no": order.no,
            "serviceId": order.service_id,
            "projectType": service_name,
            "flag":flag
        }
        data['list'].append(order_data)

    return jsonify(data)


@bp.route('/infer/<order_id>', methods=['GET'])
def infer(order_id):
    print(order_id)
    orderId = [int(x) for x in order_id.split(',')]
    orders=[]
    for id in orderId:
        orders.append(ServiceLogModel.query.filter_by(id=id).first().to_dict())



    print(orders)

    return jsonify(orders.to_dict()), 200




@bp.route('/serviceId/<int:serviceId>', methods=['GET'])
def get_order_by_serviced(serviceId):
    order = ServiceModel.query.filter_by(service_id=serviceId).first()
    print(order)

@bp.route('/assistant/<int:assistant>', methods=['GET'])
def get_order_by_assistant(assistant):
    order = WorkOrderModel.query.filter_by(handler=assistant).first()
    print(order)


def get_work_orderByid(order_id,service_id):
    # 从订单表中获取订单信息
    #print_red(order_id)
    # 获取每个订单的详细信息和相关图片
    service = ServiceLogModel.query.filter_by(order_id=order_id).first()
    if not service:
        return None
    startImgs = []
    if service.start_img is not None:
        startImgs.extend(service.start_img.split(','))

    imgUrls = []
    if service.img_url is not None:
        imgUrls.extend(service.img_url.split(','))

    endImgs = []
    if service.end_img is not None:
        endImgs.extend(service.end_img.split(','))

    # 拼接最终返回的JSON数据
    data = {
        "orderId": order_id,
        "serviceId": service_id,
        ""
        "startLocation": service.start_location,
        "location": service.location,
        "endLocation": service.end_location,
        "startTime": service.start_time,
        "endTime": service.end_time,
        "startImg": startImgs,  # 返回对应的图片信息（多个图片的JSON数据）
        "imgUrl": imgUrls,
        "endImg": endImgs
    }
    #print_red(data)
    return data
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

