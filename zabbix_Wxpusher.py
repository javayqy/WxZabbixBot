#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import sys

appToken = 'YOURTOKEN'

#获取用户列表
def get_user(appToken):
    # Wxpusher API配置
    api_url = "https://wxpusher.zjiecode.com/api/fun/wxuser/v2"

    # 请求参数
    params = {
        "appToken": appToken,
        "page": 1,  
        "pageSize": 20, 
    }

    # 发送请求
    response = requests.get(api_url, params=params)

    # 处理响应
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("success"):
            user_records = response_data.get("data").get("records")
            # for user in user_records:
            # print(f"UID: {user['uid']}")
            uid_array = [user['uid'] for user in user_records]
            print("所有UID数组:", uid_array)
        else:
            print("查询用户列表失败")
    else:
        print(f"查询用户列表失败，HTTP状态码：{response.status_code}")
    return uid_array

#信息转为字典
# def parse_alarm_info(alarm_info):
    # alarm_dict = {}
    # lines = alarm_info.strip().split('\n')
    # for line in lines:
    #     parts = line.split(':', 1)
    #     if len(parts) == 2:
    #         key, value = parts
    #         value = value.rstrip(',')  # 去除末尾的逗号
    #         alarm_dict[key.strip()] = value.strip()
    #     else:
    #         # 处理无法分割成两部分的行，可以选择忽略或进行其他处理
    #         print(f"警告：无法解析的行 - {line}")
    # return alarm_dict

#提取标题
# # def getTitle(alarm_dict):
#     pc = alarm_dict.get("告警主机")
#     print(pc)
#     return pc

#输出消息
def msg(text,userList):
    
    # Wxpusher API配置
    api_url = "https://wxpusher.zjiecode.com/api/send/message"

    # 构建消息
    message_data = {
        "msgtype": "text",
        "appToken": appToken,
        "content": text,
        "summary": 'zabbix报警',
        "contentType": 1,
        "uids": userList,
        "verifyPay": False,
    }

    # 发送消息
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    response = requests.post(api_url, json.dumps(message_data), headers=headers)

    # 处理响应
    if response.status_code == 200:
        response_data = json.loads(response.text)
        if response_data.get("success"):
            for send_status in response_data.get("data"):
                if send_status.get("code") == 1000:
                    print(f"消息发送成功给用户UID: {send_status.get('uid')}")
                else:
                    print(f"消息发送失败给用户UID: {send_status.get('uid')}. 错误消息: {send_status.get('status')}")
        else:
            print("消息发送失败。")
    # else:
    #     print(f"消息发送失败，HTTP状态码：{response.status_code}")
    #     # print(response.text)

if __name__ == '__main__':
    # 告警消息
    text = sys.argv[1]
    # text_dict = parse_alarm_info(text)
    # print (text_dict)
    userlist = get_user(appToken=appToken)
    msg(text=text,userList=userlist)