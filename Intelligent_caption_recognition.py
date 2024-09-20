#https://help.aliyun.com/zh/viapi/developer-reference/api-video-actor-staff-table-recognition?spm=5176.28426678.J_HeJR_wZokYt378dwP-lLl.101.6a295181pyhxi4&scm=20140722.S_help@@%E6%96%87%E6%A1%A3@@431204.S_BB1@bl+RQW@ag0+BB2@ag0+os0.ID_431204-RL_%E8%A7%86%E9%A2%91%E5%AD%97%E5%B9%95%E8%AF%86%E5%88%AB-LOC_search~UND~helpdoc~UND~item-OR_ser-V_3-P0_15
# -*- coding: utf-8 -*-
# 引入依赖包
# pip install alibabacloud_videorecog20200320
import os
import time
import json
from tqdm import tqdm
from pathlib import Path
from urllib.request import urlopen
from alibabacloud_tea_openapi.models import Config
from alibabacloud_tea_util.models import RuntimeOptions
from alibabacloud_videorecog20200320.client import Client
from alibabacloud_videorecog20200320.models import RecognizeVideoCastCrewListAdvanceRequestParams,RecognizeVideoCastCrewListAdvanceRequest
#本地
from GetTask import GetTaskResult,GetTaskState
from tools import SaveFile,DownloadFile

#异步调用,1、提交任务
def SubmitTask(FilePath):
    config = Config(
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
        # 访问的域名
        endpoint='videorecog.cn-shanghai.aliyuncs.com',
        # 访问的域名对应的region
        region_id='cn-shanghai'
    )
    #场景一：文件在本地
    stream = open(FilePath, 'rb')
    param_type = RecognizeVideoCastCrewListAdvanceRequestParams(type="subtitles")
    recognize_video_cast_crew_list_request = RecognizeVideoCastCrewListAdvanceRequest(
        video_url_object=stream,
        params=[    param_type   ]
    )
    runtime = RuntimeOptions()
    try:
        # 初始化Client
        client = Client(config)
        response = client.recognize_video_cast_crew_list_advance(recognize_video_cast_crew_list_request, runtime)
        # 获取整体结果
        print(response.body)
    except Exception as error:
        # 获取整体报错信息
        print(error)
        # 获取单个字段
        print(error.code)
        # tips: 可通过error.__dict__查看属性名称

    # 关闭流
    stream.close()
    return response.body.request_id


#异步调用,2、查看异步结果
def GetResult(recognition_id):
    response_body = GetTaskResult(recognition_id)
    result_dict = json.loads(response_body.data.result)
    Results = result_dict['subtitlesResults'][0]['subtitlesAllResults']
    ResultsUrl = result_dict['subtitlesResults'][0]['subtitlesAllResultsUrl']
    return Results,ResultsUrl

#查看异步结果,并保存
def GetResultAndSave(file):
    print("正在处理%s"%file)
    recognition_id  = SubmitTask(file)
    file_stem = Path(file).stem
    file_name = Path(file).name
    #大约2-3分钟左右
    print("%s大约等待2-3分钟"%file)
    # 总共的时间间隔
    total_steps = 90
    # 使用 tqdm 显示进度条
    for i in tqdm(range(total_steps), desc="Processing"):
        time.sleep(1)  # 每步暂停 1 秒
    while True :
        state = GetTaskState(recognition_id)
        if state == "PROCESS_SUCCESS":
            Results , ResultsUrl = GetResult(recognition_id)
            SaveFile(Results,"./output/%s.txt"%file_stem)
            print("正在保存%s字幕srt文件"%file_stem)
            DownloadFile(ResultsUrl,"./output/%s.srt"%file_stem)
            break
        elif state == "PROCESSING":
            print("正在处理%s请稍等"%file_name)
            time.sleep(15)
        else:
            print("任务异常，%s视频文件中断"%file_name)
            break
       
    
# if __name__ == "__main__":
    # VideOCR_config = Config(
    # # 创建AccessKey ID和AccessKey Secret，请参考https://help.aliyun.com/document_detail/175144.html。
    # # 如果您用的是RAM用户的AccessKey，还需要为RAM用户授予权限AliyunVIAPIFullAccess，请参考https://help.aliyun.com/document_detail/145025.html。
    # # 从环境变量读取配置的AccessKey ID和AccessKey Secret。运行代码示例前必须先配置环境变量。
    # access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
    # access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
    # # 访问的域名
    # endpoint='videorecog.cn-shanghai.aliyuncs.com',
    # # 访问的域名对应的region
    # region_id='cn-shanghai'
    # )

    # FilePaht = "./input/test01.mp4"
    # RequestId = SubmitTask(FilePaht,VideOCR_config)

    # RequestId = "6D473748-9CA8-57C9-8C58-A3F774028820"
    # response_body = GetTaskResult(RequestId)
    # result_dict = json.loads(response_body.data.result)
    # print(type(result_dict['subtitlesResults'][0]))
    # print(len(result_dict['subtitlesResults']))
    # print(result_dict['subtitlesResults'][0]['subtitlesAllResults'])
    # print(result_dict['subtitlesResults'][0]['subtitlesAllResultsUrl'])
    # print(result.data.result)
    # #字母下载地址
    # srt_url = result.Data.SubtitlesResults.SubtitlesAllResultsUrl
    # print(srt_url)
    # data = result.Data.SubtitlesResults
    # print(result)