#用于设置访问凭证
import json
def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"The file at {filepath} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def GetAuthorize(filepath="./Authorize.json"):
    data = read_file(filepath)
    Authorize = json.loads(data)
    return Authorize

