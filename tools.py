import requests
from pathlib import Path

def SaveFile(text,filename):
    """
    将文本保存到指定文件中。

    参数:
    text (str): 要保存的文本内容。
    filename (str): 文件名，默认为 'output.txt'。
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(str(text))
        print(f'文本已成功保存到文件: {filename}')
    except Exception as e:
        print(f'保存文件时出错: {e}')

def DownloadFile(url,save_filename):
    # 发送 GET 请求下载文件
    response = requests.get(url, stream=True)
    # 将内容写入本地文件
    with open(save_filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:  # 过滤掉保持活动的新块
                file.write(chunk)
        print(f'文本已成功保存到文件: {save_filename}')

#检查文件夹是否存在，不存在则创建
def CheakDirectory(directory):
    # 定义文件夹路径
    folder_path = Path(directory)
    # 检查文件夹是否存在
    if not folder_path.exists():
        # 如果不存在，则创建文件夹
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f'创建文件夹: {folder_path}')
   

def list_all_files(directory):
    """
    遍历指定文件夹及其子文件夹，列出所有文件的路径。
    
    参数:
    directory (str or Path): 目标文件夹路径。
    
    返回:
    list: 包含所有文件路径的列表。
    """
    path = Path(directory)
    return [str(file) for file in path.rglob('*') if file.is_file()]
