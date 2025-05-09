import time
from ultralytics import YOLO
import os
import cv2
from pathlib import Path
# 设置路径
source = r'C:\Users\67167\Desktop\YOLU\LINXIRUOtarn2\datasets\icon\images\val'  # 可以是单张图片或包含图片的文件夹
save_dir = r'C:\Users\67167\Desktop\YOLU\测试'
output_root = r'C:\Users\67167\Desktop\YOLU\测试'  # 输出根目录
# 确保保存目录存在
os.makedirs(save_dir, exist_ok=True)


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
# 加载模型
model = YOLO('best.pt')
print('---------------------------------------------------------------------------')
# 进行预测并保存结果到指定目录
# 进行预测并保存结果到指定目录
results = model.predict(
    source=source,
    conf=0.1,
    save=True,
    project=save_dir,
    name='',
    exist_ok=True
)

# 遍历所有预测结果（每个result对应一张图片）
for result_idx, result in enumerate(results):
    # 获取当前图片路径
    input_path = result.path
    print(f"\n正在处理第 {result_idx + 1} 张图片：{input_path}")

    # 读取原始图像
    original_image = cv2.imread(input_path)
    if original_image is None:
        print(f"警告：无法读取图像文件，跳过处理：{input_path}")
        continue

    # 提取当前图片的检测结果
    boxes = result.boxes
    names = result.names
    name = 0
    # 遍历当前图片的所有检测框
    for i, box in enumerate(boxes):
        name +=1
        # 解析坐标
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

        # 获取类别信息
        cls_id = int(box.cls[0])
        name = names[cls_id]

        # 打印当前检测框信息
        print(f'图片{result_idx + 1} | 标签{i + 1}号内容:{name} 坐标：[{x1}, {y1}, {x2}, {y2}]')

        # 调用保存函数（使用当前图片文件名）
        save_color_crop(
            image=original_image,
            coords=(x1, y1, x2, y2),
            output_dir=output_root,
            name=name
        )


print("\n所有图片处理完成！")