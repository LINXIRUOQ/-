from 服务器 import shangchuanwenj
from 图片查找所在图片的位置 import find_image_location
from 数据库 import update_data,get_by_id
from 查找请点击位置 import find_target_position
import os
import re
from pathlib import Path  # 添加这行导入
import time
emulator_address = '4455'
nidipanding ='cheshi'

def remove_special_chars(text: str) -> str:
    """去除字符串中的 : 和 _"""

    # 方法 1: 使用 replace() 链式替换
    # return text.replace(':', '').replace('_', '')

    # 方法 2: 使用列表推导式
    # return ''.join([c for c in text if c not in {':', '_'}])

    # 方法 3: 使用 str.translate()
    # translation_table = str.maketrans('', '', ':_')
    # return text.translate(translation_table)

    # 方法 4: 使用正则表达式
    import re
    return re.sub(r'[:_]', '', text)
# 测试示例
def rename_image(old_path: str, new_name: str, overwrite: bool = False) -> str:
    """安全重命名图片文件

    :param old_path: 原始文件完整路径
    :param new_name: 新文件名（建议包含扩展名）
    :param overwrite: 是否覆盖已存在文件
    :return: 新文件路径（若失败返回空字符串）
    """
    try:
        old_file = Path(old_path)

        # 自动保留原扩展名（如果新名称未指定）
        if not os.path.splitext(new_name)[1]:
            new_name += old_file.suffix

        new_file = old_file.with_name(new_name)

        # 处理已存在文件
        if new_file.exists():
            if overwrite:
                new_file.unlink()  # 删除已存在文件
            else:
                # 自动添加序号 new_photo(1).png
                base = new_file.stem
                suffix = new_file.suffix
                counter = 1
                while new_file.exists():
                    new_file = new_file.with_name(f"{base}({counter}){suffix}")
                    counter += 1

        old_file.rename(new_file)
        return str(new_file)

    except Exception as e:
        print(f"重命名失败: {e}")
        return ""
def 过验证码(emulator_address,nidipanding):
    print(f'<AAAAAAAA>进入过验证码<AAAAAAAA>')
    ole = 'li1_1.png'
    xin = f'{emulator_address}_{nidipanding}.png'
    xin = remove_special_chars(xin)
    print(xin)
    try:
        os.remove(xin)
    except Exception as e:
        print(e)
    rename_image(ole, xin)
    data = get_by_id(xin)
    状态 = data['zhuangtai']
    可用次数 = data['keyongcishuo']
    可用次数 = 可用次数 - 1
    if data:
        print("\n查询结果：")
        print(f"ID: {data['id']}")
        print(f"使用次数: {data['cishuo']}")
        print(f"剩余次数: {data['keyongcishuo']}")
        print(f"状态: {data['zhuangtai']}")
        print(f'进入到图形验证码判断,上传图片')
        shangchuanwenj(xin)
        update_data(xin, 1, 可用次数, 1, None)
        yzmzt = True
        if yzmzt == True:
            for _ in range(120):
                time.sleep(0.5)
                data = get_by_id(xin)
                print(data)
                状态 = data['zhuangtai']
                if 状态 == 0:
                    点击位置 = data['remark']
                    print(点击位置)
                    return 点击位置
    else:
        print("<UNK>")
        pass
if __name__ == '__main__':
    过验证码(emulator_address,nidipanding)




