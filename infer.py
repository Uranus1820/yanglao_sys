from flask import Blueprint

from work_flow import *
from work_flow.service_identification_168157 import judge_service_type
from database_models import WorkOrderModel, ServiceLogModel
bp = Blueprint(name='infer', import_name=__name__,url_prefix='/infer')

def infer(order_id):
    order_id = order_id
    # order_query = ("select member_id, to_user, start_img, img_url, end_img, service_price " +
    #                    "from work_order, service_log " +
    #                     "where work_order.order_id = service_log.order_id and work_order.order_id = ") + order_id + ";"
    # db.execute(order_query)
    # row = db.fetchall()[0]
    # print(row)
    # member_id = str(row[0])
    # employee_id = row[1]
    # start_img = row[2]
    # img_rul = row[3]
    # end_img = row[4]
    # service_type = row[5]
    # Query using ORM models
    work_order = WorkOrderModel.query.filter_by(id=order_id).first()
    service_log = ServiceLogModel.query.filter_by(order_id=order_id).first()
    member_id = str(work_order.member_id)
    employee_id = work_order.handler
    start_img = service_log.start_img
    img_rul = service_log.img_url
    end_img = service_log.end_img
    service_type = work_order.service_id  # Assuming service_id corresponds to service_price
    print(order_id)
    #url = 'http://hk.mofrp.top:10846/'
    url = 'http://mofrp.top:10846/'
    judge = judge_service_type(url, img_rul, service_type)
    error_wangtu, error_fanpai, think = wangtu_results(url, start_img + ',' + img_rul + ',' + end_img)
    start_time, error1_elder, error1_door, error_season = before_results(url, start_img)
    error2_food_ingre, error2_elder, error2_assistant = center_results(url, img_rul)
    error3_signature, error3_elder, end_time = end_results(url, end_img)
    all_url = {
        "start_img": start_img.split(','),
        "img_rul": img_rul.split(','),
        "end_img": end_img.split(',')
    }
    data={
        "member_id": member_id,
        "employee_id": employee_id,
        "start_time": start_time,
        "end_time": end_time,
        "error1_elder": error1_elder,
        "error1_door": error1_door,
        "error2_food_ingre": error2_food_ingre,
        "error2_elder": error2_elder,
        "error2_assistant": error2_assistant,
        "error3_signature": error3_signature,
        "error3_elder": error3_elder,
        "error_wangtu": error_wangtu,
        "error_fanpai": error_fanpai,
        "error_season": error_season,
        "judge": judge,
        "all_url": all_url
    }
    print(data)
    return data

