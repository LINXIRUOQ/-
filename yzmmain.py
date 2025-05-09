import os
import time
from pathlib import Path
from ultralytics import YOLO
import cv2
from 识别颜色并分类 import detect_objects
from 识别朝向并分类 import detect_objects2
from PIL import Image
from 求重叠面积 import *
from 查找字典中对应的序号的值 import *
import re
from 文字识别3 import recognize_text
from 查找请点击位置 import *
from 对图片进行标注 import annotate_image
# 配置参数
img_path = r'C:\Users\67167\Desktop\验证码识别\20.png'  # 单张图片路径
save_dir = r'C:\Users\67167\Desktop\验证码识别\结果'  # 结果保存目录
crop_dir = r'C:\Users\67167\Desktop\验证码识别\shibie2'  # 新增：裁剪图片保存目录
'''图片预处理
'''
def 图片验证(img_path=img_path):
    from 图片查找所在图片的位置 import find_image_location
    result = find_image_location(img_path)
    x1a, y1a, x2a, y2a = result
    henjiemina = (x2a - x1a) * 15
    zhongjiemina = (y2a - y1a) * 10
    x1a = x1a - henjiemina
    y2a = y2a + zhongjiemina
    from PIL import Image
    def crop_and_save(image_path, x, y, x1, y1):
        img = Image.open(image_path)  # 打开原始图片
        cropped_img = img.crop((x, y, x1, y1))  # 裁剪图片
        cropped_img.save(image_path)  # 覆盖保存原图

    crop_and_save(img_path, x1a, y1a, x2a, y2a)  # 输入裁剪区域的坐标 (x, y, x1, y1)
    original_image = cv2.imread(img_path)
    if original_image is None:
        print(f"警告：无法读取图像文件，跳过处理：{img_path}")
    # 初始化模型
    model = YOLO(r'C:\Users\67167\Desktop\验证码识别\best.pt')
    os.makedirs(save_dir, exist_ok=True)  # 创建结果目录
    os.makedirs(crop_dir, exist_ok=True)  # 新增：创建裁剪目录

    # 执行预测
    print('-' * 60)
    results = model.predict(
        source=img_path,
        conf=0.2,
        save=True,
        project=save_dir,
        name='',
        exist_ok=True
    )
    print('-' * 60)
    '''函数部分'''

    def crop_image(image_path, x, y, x1, y1):
        """
        图片裁剪函数
        :param image_path: 原图路径
        :param x: 左上角X坐标
        :param y: 左上角Y坐标
        :param x1: 右下角X坐标
        :param y1: 右下角Y坐标
        :return: 保存路径
        """
        with Image.open(image_path) as img:
            img.crop((x, y, x1, y1)).save("wenzhi.png")
        return "wenzhi.png"

    def save_color_crop(image, coords, output_dir, name):
        """保存颜色分类裁剪图"""
        # 使用传递的文件夹路径，而不是创建新文件夹
        color_dir = Path(output_dir)

        # 生成新文件名
        new_name = f"{name}.png"
        save_path = color_dir / new_name

        # 执行裁剪并保存
        x1, y1, x2, y2 = coords
        crop_img = image[y1:y2, x1:x2]

        # 确保裁剪区域有效
        if crop_img.size > 0:
            cv2.imwrite(str(save_path), crop_img)
            print(f"已保存到：{save_path}")
        else:
            print(f"警告：无效裁剪区域 {coords}，跳过保存")

    ''''''
    # 解析结果
    result = results[0]  # 直接获取单图结果
    img_name = os.path.basename(img_path)
    orig_img = result.orig_img  # 获取原始图像数据

    # 保存标签文件
    txt_path = os.path.join(save_dir, img_name.replace('.png', '.txt'))
    result.save_txt(txt_path)

    # 输出检测信息
    print(f"图像尺寸：{result.orig_shape}")
    # 在循环前初始化信息存储列表
    detection_info = []
    nameRSRFG = 0
    for i, box in enumerate(result.boxes):
        nameRSRFG += 1
        # 获取目标信息
        cls_id = int(box.cls[0])
        name = result.names[cls_id]
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        conf = box.conf[0].item()

        # 存储检测信息（代替直接打印）
        detection_info.append(
            f" {i + 1}. {name} 置信度：{conf:.2f} 坐标：[{x1}, {y1}, {x2}, {y2}]"
        )
        save_color_crop(
            image=original_image,
            coords=(x1, y1, x2, y2),
            output_dir=crop_dir,
            name=nameRSRFG
        )
    # 在循环外统一输出检测信息
    print(f"检测到 {len(result.boxes)} 个目标：")
    results = detect_objects(crop_dir)
    results2 = detect_objects2(crop_dir)
    print("&" * 60)
    print(detection_info)
    print(results)
    print(results2)
    print("&" * 60)

    # 创建颜色和方向映射字典
    color_map = {}
    direction_map = {}

    for item in results:
        num, color = item.split(": ")
        color_map[num] = color

    for item in results2:  # 新增对results2的处理
        num, direction = item.split(": ")
        direction_map[num] = direction

    # 创建主字典
    your_dict = {}

    for info in detection_info:
        parts = info.strip().split(". ")
        num = parts[0]

        coords_str = info.split("坐标：[")[1].split("]")[0]
        coords = list(map(int, coords_str.split(", ")))

        text = parts[1].split(" 置信度")[0].strip()

        # 获取颜色和朝向
        color = color_map.get(num, "未知颜色")
        direction = direction_map.get(num, "未知朝向")  # 新增方向获取

        your_dict[num] = {
            "zuobiao": coords,
            "yanshe": color,
            "xingzhuang": text,
            "chaoxiang": direction  # 新增朝向字段
        }
    print(your_dict)
    cfgjh = find_target_position(img_path)
    xa, ya, xb, yb = cfgjh
    print(f'识别到的文字区域{xa, ya, xb, yb}')
    crop_image(img_path, xa, ya, xb, yb)
    results = recognize_text('wenzhi.png')
    print(f'识别到的文字为：{results}')
    results = results.replace("凯色", "颜色")  # 把所有的 "苹果" 替换成 "香蕉"
    results = results.replace("正方体", "矩形")  # 把所有的 "苹果" 替换成 "香蕉"
    results = results.replace("潮向", "朝向")  # 把所有的 "苹果" 替换成 "香蕉"
    # 假设这是print(results)的输出
    if results:
        result = results[3:]
        first_two_chars = result[:2]
        if first_two_chars == '托起':
            first_two_charsA = result[4:5]
            first_two_chars = result[6:]
            if first_two_chars == '正方体':
                first_two_chars = '矩形'
            print(f'查找{first_two_charsA}和{first_two_chars}重叠的{first_two_chars}')
            result = find_max_overlap(your_dict, first_two_charsA, first_two_chars)
            print(f'<UNK>{result}')
            if result:
                (id2, id1), area = result
                if area > 0:
                    print(f"最大重叠面积发生在 {first_two_charsA}-{id1} 和 {first_two_chars}-{id2} 之间，面积为 {area}")
                    要点击的位置 = 获取中心点(your_dict, id1)
                else:
                    print(f"没有找到 {first_two_charsA} 和 {first_two_chars} 之间的重叠区域")
            else:
                print("输入形状不存在有效组合")
        elif '色的' in result:
            # 使用正则表达式提取“色”字后面的内容
            match = re.search(r'色的(.*)', result)
            if match:
                result = match.group(1)
                if '体' in result:
                    result = result[0:2]
                print(f'{first_two_chars}+{result}')  # 输出：的球
                xuhaiid = 输入颜色和形状查找序号(your_dict, yanshe=first_two_chars, xingzhuang=result)
                print(xuhaiid)
                要点击的位置 = 获取中心点(your_dict, xuhaiid)
        elif '颜色一样' in result:
            # 提取前两个字
            first_two_chars = result[2:3]
            first_two_charsA = result[10:]
            print(f'判断{first_two_chars}的颜色点击{first_two_charsA}')
            first_two_chars = 输入形状查找颜色(your_dict, first_two_chars)
            xuhaiid = 输入颜色和形状查找序号(your_dict, yanshe=first_two_chars, xingzhuang=first_two_charsA)
            print(xuhaiid)
            要点击的位置 = 获取中心点(your_dict, xuhaiid)
        elif '朝向一样' in result:
            # 提取前两个字
            first_two_chars = result[2:3]
            first_two_charsA = result[10:]
            print(f'判断{first_two_chars}的朝向点击{first_two_charsA}')
            first_two_chars = 输入形状查找朝向(your_dict, first_two_chars)
            xuhaiid = 输入颜色和形状查找序号(your_dict, chaoxiang=first_two_chars, xingzhuang=first_two_charsA)
            print(xuhaiid)
            要点击的位置 = 获取中心点(your_dict, xuhaiid)
        elif first_two_chars == '小写' or first_two_chars == '大写':
            first_two_charsA = result[2:]
            print(first_two_charsA)
            输入颜色和形状查找序号(your_dict, xingzhuang=first_two_charsA)
        elif '向的' in result and '色' in result:
            颜色 = result[:2]
            朝向 = result[2:3]
            形状 = result[7:]
            print(f'颜色：{颜色} 朝向：{朝向} 形状：{形状}')
            if 朝向 == '正':
                朝向 = '正向'
                xuhaiid = 输入颜色和形状查找序号(your_dict, chaoxiang=朝向, xingzhuang=形状, yanshe=颜色)
                if xuhaiid:
                    要点击的位置 = 获取中心点(your_dict, xuhaiid)
                else:
                    print('<UNK>')
            elif 朝向 == '侧':
                朝向 = '右侧向'
                xuhaiid = 输入颜色和形状查找序号(your_dict, chaoxiang=朝向, xingzhuang=形状, yanshe=颜色)
                if xuhaiid:
                    要点击的位置 = 获取中心点(your_dict, xuhaiid)
                else:
                    朝向 = '左侧向'
                    xuhaiid = 输入颜色和形状查找序号(your_dict, chaoxiang=朝向, xingzhuang=形状, yanshe=颜色)
                    if xuhaiid:
                        要点击的位置 = 获取中心点(your_dict, xuhaiid)
        elif '向的' in result:
            first_two_chars = result[:1]
            irst_two_chars = result[5:]
            print(f'方向: {first_two_chars} {irst_two_chars}')
            if first_two_chars == '正':
                first_two_chars = '正向'
            elif first_two_chars == '侧':
                first_two_chars = '右侧向'
                xuhaiid = 输入颜色和形状查找序号(your_dict, chaoxiang=first_two_chars, xingzhuang=irst_two_chars)
                if xuhaiid:
                    要点击的位置 = 获取中心点(your_dict, xuhaiid)
                else:
                    first_two_chars = '左侧向'
                    xuhaiid = 输入颜色和形状查找序号(your_dict, chaoxiang=first_two_chars, xingzhuang=irst_two_chars)
                    if xuhaiid:
                        要点击的位置 = 获取中心点(your_dict, xuhaiid)
        elif '上表面' in result:
            first_two_chars = result[2:4]
            if first_two_chars == '正方':
                first_two_chars = '矩形'
            irst_two_chars = result[8:]
            if irst_two_chars == '数字':
                print(f'遍历查找所有 数字 与 {first_two_chars} 求最大重叠面积，输出id')
                shuzhixuhid = 查找所有的数字对应的_id(your_dict)
                result = find_max_overlap(your_dict, shuzhixuhid, first_two_chars)
                if result:
                    (id2, id1), area = result
                    if area > 0:
                        print(f"最大重叠面积发生在 {shuzhixuhid}-{id1} 和 {first_two_chars}-{id2} 之间，面积为 {area}")
                        要点击的位置 = 获取中心点(your_dict, id2)
                    else:
                        print(f"没有找到 {shuzhixuhid} 和 {first_two_chars} 之间的重叠区域")
                else:
                    print("输入形状不存在有效组合")
            irst_two_chars = result[9:]
            if irst_two_chars == '字母':
                print(f'遍历查找所有 字母 与 {first_two_chars} 求最大重叠面积，输出id')
                shuzhixuhid = 查找所有的字母对应的_id(your_dict)
                shuzhixuhid = 根据列表id找到形状(your_dict, shuzhixuhid)
                print(f'{shuzhixuhid}')
                result = find_max_overlap(your_dict, shuzhixuhid, first_two_chars)
                if result:
                    (id2, id1), area = result
                    if area > 0:
                        print(f"最大重叠面积发生在 {shuzhixuhid}-{id1} 和 {first_two_chars}-{id2} 之间，面积为 {area}")
                        要点击的位置 = 获取中心点(your_dict, id2)
                    else:
                        print(f"没有找到 {shuzhixuhid} 和 {first_two_chars} 之间的重叠区域")
                else:
                    print("输入形状不存在有效组合")
        elif first_two_chars == '数字':
            first_two_chars = result[2:4]
            # 输出结果
            xuhaiid = 输入颜色和形状查找序号(your_dict, yanshe=first_two_chars)
            要点击的位置 = 获取中心点(your_dict, xuhaiid)
        else:
            print(f'报错：图片：{img_path}，识别文字：{result}')
        if 要点击的位置:
            print(f'预处理后图要要点击的位置{要点击的位置}')
            xad, yad = 要点击的位置
            xada = xad + x1a
            yada = yad + y1a
            print(f'原图应该点击的位置为{xada, yada}')
            annotate_image(
                input_path=img_path,
                output_dir=r'.\验证点击验证码后的结果',
                coordinates=(xad, yad),
                text="Target Point",  # 可选文本标注
                mark_color="#FF0000",  # 支持十六进制颜色
                mark_size=8,
                font_size=18
            )
            zzjg = f'{xada}_{yada}'
            return zzjg
        else:
            annotate_image(
                input_path=img_path,
                output_dir=r'.\未验证过',
                coordinates=(10, 10),
                text=results,  # 可选文本标注
                mark_color="#FF0000",  # 支持十六进制颜色
                mark_size=8,
                font_size=18
            )
if __name__ == '__main__':
    图片验证(img_path='emulator-5642linxiruoQ.png')
    time.sleep(111)
    错误列表=[]
    # 定义图片扩展名集合（可根据需要添加）
    image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
    image_exts={'.png'}
    # 输入目标文件夹路径
    folder_path = rf'C:\Users\67167\Desktop\验证码识别'

    # 转换为绝对路径
    abs_path = os.path.abspath(folder_path)

    # 验证路径有效性
    if not os.path.exists(abs_path):
        print(f"错误：路径不存在 - {abs_path}")
    elif not os.path.isdir(abs_path):
        print(f"错误：这不是文件夹 - {abs_path}")
    else:
        # 获取文件夹内所有条目
        entries = os.listdir(abs_path)

        # 筛选图片文件
        image_files = [
            os.path.join(abs_path, f)
            for f in entries
            if os.path.isfile(os.path.join(abs_path, f)) and
               os.path.splitext(f)[1].lower() in image_exts
        ]

        # 按文件名排序
        image_files.sort()

        # 输出结果
        if not image_files:
            print("该文件夹中没有图片文件")
        else:
            print(f"在 {abs_path} 中找到 {len(image_files)} 个图片文件：")
            for idx, path in enumerate(image_files, 1):
                xioaxi = f"{idx}. {path}"
                print(xioaxi)
                try:
                    图片验证(img_path=path)
                except Exception:
                    错误列表.append(xioaxi)
    for _ in 错误列表:
        print(_)

