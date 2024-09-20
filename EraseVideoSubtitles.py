# -*- coding: utf-8 -*-
# 引入依赖包
# pip install alibabacloud_videoenhan20200320
import os
from pathlib import Path
import time
import json
from tqdm import tqdm
from urllib.request import urlopen
from moviepy.editor import VideoFileClip
from alibabacloud_tea_openapi.models import Config
from alibabacloud_tea_util.models import RuntimeOptions
from alibabacloud_videoenhan20200320.client import Client
from alibabacloud_videoenhan20200320.models import EraseVideoSubtitlesAdvanceRequest
from GetTask import GetTaskResult,GetTaskState
from tools import DownloadFile



#异步调用,1、提交任务
def SubmitTask(FilePath):
    config = Config(
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
        # 访问的域名
        endpoint='videoenhan.cn-shanghai.aliyuncs.com',
        # 访问的域名对应的region
        region_id='cn-shanghai'
        )
        #场景一：文件在本地
    stream = open(FilePath, 'rb')
    erase_video_subtitles_request  = EraseVideoSubtitlesAdvanceRequest(
            video_url_object=stream,
            bx=0,
            by=0,
            bw=1,
            bh=1,
            
    )
    runtime = RuntimeOptions()
    try:
        # 初始化Client
        client = Client(config)
        response = client.erase_video_subtitles_advance(erase_video_subtitles_request, runtime)
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
def GetResult(Erase_id):
    response_body = GetTaskResult(Erase_id)
    result_dict = json.loads(response_body.data.result)
    ResultsUrl = result_dict['VideoUrl']
    return ResultsUrl

#上传任务查看异步结果,并保存,按照文件为单位依次处理
def GetResultAndSave(file):
    print("正在处理%s"%file)
    # 加载视频文件
    video = VideoFileClip(file)
    # 获取视频时长（以秒为单位）
    duration = video.duration
    Erase_id  = SubmitTask(file)
    file_name = Path(file).name
    #大约10-12分钟左右
    print("%s大约等待10-12分钟"%file)
    # 总共的时间间隔,视频时长+90s
    total_steps = int(duration)+90
    # 使用 tqdm 显示进度条
    for i in tqdm(range(total_steps), desc="Processing"):
        time.sleep(1)  # 每步暂停 1 秒
    while True :
        state = GetTaskState(Erase_id)
        if state == "PROCESS_SUCCESS":
            ResultsUrl = GetResult(Erase_id)
            print("正在保存处理后的%s视频文件"%file_name)
            DownloadFile(ResultsUrl,"./output/%s"%file_name)
            break
        elif state == "PROCESSING":
            print("正在处理%s请稍等"%file_name)
            time.sleep(20)
        else:
            print("任务异常，%s视频文件中断"%file_name)
            break
        
        