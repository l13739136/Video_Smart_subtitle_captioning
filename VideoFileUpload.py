# pip install oss2
# pip install aliyun-python-sdk-viapiutils
# pip install viapi-utils

#视频文件上传，返回URL
from viapi.fileutils import FileUtils
import os

def VideoFileUpload(FilePath,FileType):
    file_utils = FileUtils(os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'], os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'])
    # 场景一，使用本地文件，第一个参数为文件路径，第二个参数为生成的url后缀，但是并不能通过这种方式改变真实的文件类型，第三个参数True表示本地文件模式
    oss_url = file_utils.get_oss_url(FilePath, FileType, True)
    # 场景二，使用任意可访问的url，第一个url，第二个参数为生成的url后缀，但是并不能通过这种方式改变真实的文件类型，第三个参数False表示非本地文件模式
    # oss_url = file_utils.get_oss_url("https://viapi-test-bj.oss-cn-beijing.aliyuncs.com/viapi-3.0domepic/ocr/RecognizeBankCard/yhk1.jpg", "jpg", False)
    # 生成的url，可用于调用视觉智能开放平台的能力
    # print(oss_url)
    return oss_url