from work_flow import *
import requests
import mysql.connector
from mysql.connector import Error

from work_flow.service_identification_168157 import judge_service_type


def infer(order_id):
    order_id = '540549'
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host='47.99.65.68',
            port=3306,
            database='yanglao',
            user="dhgxjbgs",
            password="D23@#hGb",
        )
        if conn.is_connected():
            cursor = conn.cursor()

        order_query = ("select member_id, to_user, start_img, img_url, end_img, service_price " +
                       "from work_order, service_log " +
                        "where work_order.order_id = service_log.order_id and work_order.order_id = ") + order_id + ";"
        cursor.execute(order_query)
        row = cursor.fetchall()[0]

        #print(row)

        member_id = str(row[0])
        employee_id = row[1]
        start_img = row[2]
        img_rul = row[3]
        end_img = row[4]
        service_type = row[5]

        judge = judge_service_type(img_rul, service_type)
        error_wangtu, error_fanpai, think = wangtu_results(start_img + ',' + img_rul + ',' + end_img)
        start_time, error1_elder, error1_door, error_season = before_results(start_img)
        error2_food_ingre, error2_elder, error2_assistant = center_results(img_rul)
        error3_signature, error3_elder, end_time = end_results(end_img)


        print("结果")
        print("开始时间"+start_time)               #2024-03-02 12:14:10
        print("结束时间"+end_time)                 #2024-03-02 11:27:52,2024-03-02 12:14:10,2024-03-02 12:14:10,
        print("error1_elder"+error1_elder)             #不存在老人
        print("error1_door"+error1_door)              #存在门框
        print("error2_food_ingre"+error2_food_ingre)        #异常，疑似红烧肉需要猪肉等蛋白质来源，而食材列表仅包含疑似土豆，缺乏关键蛋白质来源。
        print("error2_elder"+error2_elder)             #未发现老人
        print("error2_assistant"+error2_assistant)         #未发现志愿者
        print("error3_signature"+error3_signature)         #无异常,异常,异常,
        print("error3_elder"+error3_elder)             #发现老人，坐姿，手持餐具,
        print("error_wangtu"+error_wangtu)             #无异常,
        print("error_fanpai"+error_fanpai)             #无异常,
        print("error_season"+error_season)             #无输出
        print(judge)   #{'isSuccess': False, 'error_service': '服务类型与上传图片不符异常，上传图片类型为：理发服务，而工单原本类型为：煮正餐26.0。'}

    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    infer('540549')

