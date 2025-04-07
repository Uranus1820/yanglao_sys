from datetime import datetime
import json

from torch import last_error

# 定义判断是否异常的关键词
abnormal_keywords = ["异常", "不存在", "未发现"]
normal_keywords=["无异常"]
def logic(data):
    abnormal_info = []
    abnormal_count = 0
    for key, value in data.items():
        if key.startswith("error"):  # 只处理 error 开头的字段
            # 判断是否包含异常关键词
            if any(word in value for word in normal_keywords):
                continue
            if any(word in value for word in abnormal_keywords):

                abnormal_info.append({"key":error_mapping[key],"value":value})
                abnormal_count += 1

    # start_time = datetime.strptime(data["start_time"].rstrip(','), "%Y-%m-%d %H:%M:%S")
    # last_time=data["end_time"]
    # print(last_time)
    # end_time_list = [t for t in last_time.split(',') if t.strip()]
    # end = datetime.strptime(end_time_list[-1], "%Y-%m-%d %H:%M:%S")
    #
    # # 计算时间差
    # time_difference = end - start_time
    # hours = time_difference.seconds // 3600
    # if hours > 3:
    #     abnormal_info.append({"key": "error_time", "value": "服务时间为：" + str(hours) + "异常"})
    #     abnormal_count+=1

    result = {
        "abnormal_count": abnormal_count,
        "abnormal_info": abnormal_info,
        "abnormal_url":data["all_url"]
    }
    return result
error_mapping = {
    "error2_food_ingre": "服务中：食材不匹配异常",
    "error2_elder": "服务中：无老人异常",
    "error2_assistant": "服务中：无志愿者异常",
    "error1_elder": "服务前：不存在老人异常",
    "error_season": "着装与季节不符异常",
    "error_service": "上传图片与服务不符异常",
    "error_wang_fan": "网图、翻拍异常",
    "error1_door": "服务前：缺门牌号异常",
    "error_duration": "服务时长异常",
    "error3_signature": "服务后：签字表异常",
    "error3_elder": "服务后，不存在老人异常",
    "judge":"服务类型与上传图片不符异常"
}
