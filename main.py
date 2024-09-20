import os
from pathlib import Path
from Authorize import GetAuthorize
import Intelligent_caption_recognition
import EraseVideoSubtitles 
from tools import list_all_files,CheakDirectory


#pyinstaller --onefile --hidden-import=Intelligent_caption_recognition --hidden-import=EraseVideoSubtitles --hidden-import=tools   --hidden-import=Authorize  --add-data "Authorize.json;."  --name  main  main.py


if __name__=="__main__":
    #默认配置文件读取Authorize.json文件的AccessKey ID和AccessKey Secret。用户可以自定义文件路径
    Authorize_dict = GetAuthorize()
    os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'] = Authorize_dict['ACCESS_KEY_ID']
    os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'] = Authorize_dict['ACCESS_KEY_SECRET']
    #第一步,读取文件夹所有视频
    input_directory = './input'    # 替换为你要遍历的文件夹路径
    output_directory = './output'
    CheakDirectory(input_directory)
    CheakDirectory(output_directory)  
    input_files = list_all_files(input_directory)

    #处理一下去掉之前处理过的视频
    #遍历output
    for file in input_files:
        file_stem = Path(file).stem
        file_name = Path(file).name
        output_path = Path(output_directory)
        srt_file = output_path/(file_stem+'.srt')
        txt_file = output_path/(file_stem+'.txt')
        video_file = output_path/file_name
        #识别已经完成了
        if srt_file.exists() and txt_file.exists():
            #擦除没有完成了，#重新擦除 
            if  not video_file.exists():
                EraseVideoSubtitles.GetResultAndSave(file)
            print("%s已经完成请查看ouput文件夹"%file_name)
            input_files.remove(file)
        #识别没有完成
        else:
            #擦除完成
            if video_file.exists():
                #补充识别
                Intelligent_caption_recognition.GetResultAndSave(file)
                print("%s已经完成请查看ouput文件夹"%file_name)
                input_files.remove(file)

    # print(all_files)
    for file in input_files:
        Intelligent_caption_recognition.GetResultAndSave(file)
        EraseVideoSubtitles.GetResultAndSave(file)

    print("处理完成")
    os.system('pause')
 