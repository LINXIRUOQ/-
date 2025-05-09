import time
import requests
import os
ip = 'aaa'
with open('变量设置.txt', 'r', encoding='utf-8') as file:
    # 遍历文件中的每一行
    for line in file:
        # 去除每行的空白字符（如换行符），并执行赋值操作
        exec(line.strip())
        print(line.strip())
url = f'http://{ip}:5000/upload'
def shangchuanwenj(file_path):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
        print("上传结果:", response.text)
def linuxxiazhai(filename):
    url = f'http://{ip}:5000/download/{filename}'
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f'已成功下载文件: {filename}')
if __name__ == '__main__':
    pass