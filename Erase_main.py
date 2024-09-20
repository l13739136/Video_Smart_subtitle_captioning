import os
from pathlib import Path
from Authorize import GetAuthorize
from EraseVideoSubtitles import GetResultAndSave
from tools import list_all_files,CheakDirectory

#pyinstaller --onefile --hidden-import=EraseVideoSubtitles --hidden-import=tools   --hidden-import=Authorize  --add-data "Authorize.json;."  --name  Erase  Erase_main.py

if __name__=="__main__":
    #默认配置文件读取Authorize.json文件的AccessKey ID和AccessKey Secret。用户可以自定义文件路径
    Authorize_dict = GetAuthorize()
    os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'] = Authorize_dict['ACCESS_KEY_ID']
    os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'] = Authorize_dict['ACCESS_KEY_SECRET']

    input_directory = './input'    # 替换为你要遍历的文件夹路径
    output_directory = './output'  
    CheakDirectory(input_directory)
    CheakDirectory(output_directory)
    input_files = list_all_files(input_directory)

    #处理一下去掉之前处理过的视频
    for file in input_files:
        file_stem = Path(file).stem
        file_name = Path(file).name
        output_path = Path(output_directory)
        video_file = output_path/file_name
        #识别已经完成了
        if video_file.exists():
            print("%s已经完成请查看ouput文件夹"%file_name)
            input_files.remove(file)

    # print(all_files)
    # for file in input_files:
    #     GetResultAndSave(file)  #按照文件依次处理，可能存在一定问题，比如耗时满，需要等待其他任务完成再提交，不会产生浪费
    
    for file in input_files:
        GetResultAndSave(file)

    print("视频处理完成")
    os.system('pause')  