# Video_Smart_subtitle_captioning
	利用阿里云提供的视频处理接口完成字幕的识别和去除.
## 运行前准备
	1、注册阿里云平台账户，访问[视觉开放平台](https://vision.aliyun.com/?spm=a2cvz.27717767.J_8623776880.1.325234cfi3y47I)获得体验资格或者购买服务
    2、找到个人账户的api_key,将内容填写到Authorize.json当中
	3、将需要处理的视频放入input文件夹中，运行后结果会出现在output文件夹中
## 运行方式1：直接运行入口文件
    main.py   同时运行识别视频字幕保存和去除字幕
    recognition_main.py 识别视频字幕并保存
    Erase_main.py  去除视频字幕
## 运行方式2：将程序打包成可执行文件再运行，打包代码
    pyinstaller --onefile --hidden-import=Intelligent_caption_recognition --hidden-import=EraseVideoSubtitles --hidden-import=tools   --hidden-import=Authorize  --add-data "Authorize.json;."  --name  main  main.py
    pyinstaller --onefile --hidden-import=Intelligent_caption_recognition --hidden-import=tools   --hidden-import=Authorize  --add-data "Authorize.json;."  --name  Recognition  recognition_main.py
    pyinstaller --onefile --hidden-import=EraseVideoSubtitles --hidden-import=tools   --hidden-import=Authorize  --add-data "Authorize.json;."  --name  Erase  Erase_main.py