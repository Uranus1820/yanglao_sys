from flask import Blueprint, jsonify,request,abort
import json
from datetime import datetime
from database_models import WorkOrderModel, ServiceModel,ServiceLogModel
import requests

from infer import infer
from work_flow.logic import logic

bp = Blueprint(name='work_order', import_name=__name__,url_prefix='/work_order')
# 接收前端工单号并返回对应数据
@bp.route('/list')
def get_all_order_id():
    data = {"list": [], "total": []}
    page = int(request.args.get('currentPage', 1))  # 获取页码，默认为第一页
    per_page = int(request.args.get('size', 10))  # 获取每页显示的数据量，默认为 10 条

    if request.args.get('orderId'):
        order_id = request.args.get('orderId', 0, type=int)
        query = WorkOrderModel.query
        if order_id > 0:
            query = query.filter(WorkOrderModel.id >= order_id)
        query = query.order_by(WorkOrderModel.id.asc())
        # 调用 paginate 进行分页
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        # 获取当前页的数据
        orders = pagination.items
        data['total'] = pagination.total
        for order in orders:
            service = get_work_orderByid(order.id, order.service_id)
            service_model = ServiceModel.query.filter_by(id=order.service_id).first()
            service_name = service_model.name if service_model else "未知"
            flag = 1
            if service is None:
                flag = 0
            order_data = {
                "orderId": order.id,
                "no": order.no,
                "member": order.member_id,
                "serviceId": order.service_id,
                "projectType": service_name,
                "flag": flag
            }
            data['list'].append(order_data)

        return jsonify(data)
    elif request.args.get('order'):
        order_name=request.args.get('order')
        pagination=ServiceLogModel.query.filter(ServiceLogModel.service_content.like(f"%{order_name}%")).paginate(page=page, per_page=per_page,error_out=False)
        orders = pagination.items
        data['total'] = pagination.total
        for order in orders:
            service = get_work_orderByid(order.order_id, order.id)
            member_id=WorkOrderModel.query.filter_by(id=order.order_id).first().member_id
            handler=WorkOrderModel.query.filter_by(id=order.order_id).first().handler
            flag = 1
            if service is None: flag = 0
            order_data = {
                "orderId": order.order_id,
                #"no": order.no,
                "handler": handler,
                "member": member_id,
                "serviceId": order.id,
                "projectType": order.service_content,
                "flag": flag
            }
            data['list'].append(order_data)
        return jsonify(data)
    else:
        orders=[]
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
                "handler": order.handler,
                "member": order.member_id,
                "serviceId": order.service_id,
                "projectType": service_name,
                "flag":flag
            }
            data['list'].append(order_data)



    return jsonify(data)


@bp.route('/infer', methods=['GET'])
def infering():
    """
    返回id进行infer
    """
    order_ids = request.args.get('order_id')  # '3888,3889'
    orderId = order_ids.split(',')
    print(orderId)
    #orderId=["540549"]
    correct = len(orderId)
    orders={
        "correct":correct,
        "suspect":len(orderId)-correct,
        "error":len(orderId)-correct,
        "suspect_info":[],
        "error_info":[],
        "error_url":[]
    }
    for i in orderId:
        data=infer(i)
        error=logic(data)
        if error["abnormal_count"]:
            correct-=1
            orders["error_info"].append({"id":i,"error":error["abnormal_info"]})
            orders["error_url"].append({"id":i,"url":error["abnormal_url"]})
            #orders["error_info"].append({"id":i,"error":error["abnormal_info"],"url":error["abnormal_url"]})

    orders["correct"]=correct
    orders["suspect"]=0
    orders["error"]=len(orderId)-correct

    print(orders)

    return jsonify(orders), 200




@bp.route('/member_id/<int:serviceId>', methods=['GET'])
def get_order_by_serviced(member_id):
    order = WorkOrderModel.query.filter_by(member_id=member_id).first()
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

