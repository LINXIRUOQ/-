import os
import time
from PIL import Image
from ultralytics import YOLO




# 使用函数


# 设置路径
source = r'C:\Users\67167\Desktop\验证码识别\图片'  # 可以是单张图片或包含图片的文件夹
save_dir = r'C:\Users\67167\Desktop\验证码识别\YOLO自动标注后的数据'

# 确保保存目录存在
os.makedirs(save_dir, exist_ok=True)
模型 = rf'C:\Users\67167\Desktop\验证码识别\best.pt'
# 加载模型
model = YOLO(模型)

# 进行预测并保存结果到指定目录
results = model.predict(
    source=source,
    conf=0.4,
    save=True,  # 自动保存带检测框的图片
    project=save_dir,  # 指定保存根目录
    name='',  # 不创建子目录
    exist_ok=True  # 允许覆盖已存在内容
)
# 检查 results 是否为列表
if isinstance(results, list):
    # 取第一个 Results 对象（假设你只处理单张图像）
    result = results[0]
else:
    result = results

# 提取检测结果
boxes = result.boxes
names = result.names
# 遍历所有检测到的目标
for i, box in enumerate(boxes):
    # 获取坐标（xyxy格式）
    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
    # 获取类别ID
    cls_id = int(box.cls[0])
    # 获取类别名称
    name = names[cls_id]
    source = r'C:\Users\67167\Desktop\YOLU\测试\predict\813.png'  # 可以是单张图片或包含图片的文件夹
    print(f'标签{i + 1}号 {name} 位置：左上({x1},{y1}) 右下({x2},{y2})')
# 遍历所有检测结果
for i, result in enumerate(results):
    # 获取当前图片路径
    input_path = result.path
    # 生成保存文件名
    img_name = os.path.basename(input_path)
    txt_name = os.path.splitext(img_name)[0] + ".txt"

    # 保存标签数据
    txt_path = os.path.join(save_dir, txt_name)
    result.save_txt(txt_path)  # 使用内置方法保存YOLO格式标签

    # 打印进度
    print(f"Processed {i + 1}/{len(results)} images | Saved to {txt_path}")
    print(f'-------------------------------------------------------------')
    print(result)

print("所有检测结果已保存至:", save_dir)