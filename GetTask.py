# -*- coding: utf-8 -*-
# 引入依赖包
# pip install alibabacloud_viapi20230117
import os
import json
from urllib.request import urlopen
from alibabacloud_tea_openapi.models import Config
from alibabacloud_tea_util.models import RuntimeOptions
from alibabacloud_viapi20230117.client import Client
from alibabacloud_viapi20230117.models import QueryAsyncJobListRequest,GetAsyncJobResultRequest

# 查询异步调用列表
def GetTaskList():
    config = Config(
        # 创建AccessKey ID和AccessKey Secret，请参考https://help.aliyun.com/document_detail/175144.html。
        # 如果您用的是RAM用户的AccessKey，还需要为RAM用户授予权限AliyunVIAPIFullAccess，请参考https://help.aliyun.com/document_detail/145025.html。
        # 从环境变量读取配置的AccessKey ID和AccessKey Secret。运行代码示例前必须先配置环境变量。
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
        # 访问的域名
        endpoint='viapi.cn-shanghai.aliyuncs.com',
        # 访问的域名对应的region
        region_id='cn-shanghai'
    )
    
    query_async_job_list_request = QueryAsyncJobListRequest(
    # start_time='2023-02-23 00:00:00',
    # end_time='2023-02-23 23:00:00',
    # job_id='1299348D-DFF2-5FDA-8C9C-C2D14EBF63F2'
    )
    runtime = RuntimeOptions()
    try:
        # 初始化Client
        client = Client(config)
        response = client.query_async_job_list_with_options(query_async_job_list_request, runtime)
        # 获取整体结果
        # print(response.body)
    except Exception as error:
        # 获取整体报错信息
        print(error)
        # 获取单个字段
        print(error.code)
    result_dict = json.loads(response.body.data.result)
    return result_dict

#查询异步任务状态
def GetTaskState(RequestId):
    config = Config(
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
        # 访问的域名
        endpoint='viapi.cn-shanghai.aliyuncs.com',
        # 访问的域名对应的region
        region_id='cn-shanghai'
    )
    query_async_job_list_request = QueryAsyncJobListRequest(
    # start_time='2023-02-23 00:00:00',
    # end_time='2023-02-23 23:00:00',
        job_id = RequestId
    )
    runtime = RuntimeOptions()
    try:
        # 初始化Client
        client = Client(config)
        response = client.query_async_job_list_with_options(query_async_job_list_request, runtime)
        # 获取整体结果
        # print(response.body)
    except Exception as error:
        # 获取整体报错信息
        print(error)
        # 获取单个字段
        print(error.code)
    # print(response.body)
    # print(type(response.body.data.result[0]))
    # print(response.body.data.result[0].status)
    # # result_dict = json.loads(response.body.data.result)
    # # print(result_dict[0]["Status"])
    # print(1)
    return response.body.data.result[0].status



#查询异步调用结果
def GetTaskResult(RequestId):
    config = Config(
        # 创建AccessKey ID和AccessKey Secret，请参考https://help.aliyun.com/document_detail/175144.html。
        # 如果您用的是RAM用户的AccessKey，还需要为RAM用户授予权限AliyunVIAPIFullAccess，请参考https://help.aliyun.com/document_detail/145025.html。
        # 从环境变量读取配置的AccessKey ID和AccessKey Secret。运行代码示例前必须先配置环境变量。
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
        # 访问的域名
        endpoint='viapi.cn-shanghai.aliyuncs.com',
        # 访问的域名对应的region
        region_id='cn-shanghai'
        )
    #获取结果
    get_async_job_result_request = GetAsyncJobResultRequest(
        job_id= RequestId
    )
    runtime = RuntimeOptions()
    try:
        # 初始化Client
        client = Client(config)
        response = client.get_async_job_result_with_options(get_async_job_result_request, runtime)
        # 获取整体结果
        # print(response.body)
    except Exception as error:
        # 获取整体报错信息
        print(error)
        # 获取单个字段
        print(error.code)
    return response.body
        

