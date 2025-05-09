from ultralytics import YOLO
import os
import cv2
import shutil
from tqdm import tqdm
# 配置参数
input_folder = r'C:\Users\67167\Desktop\验证码识别\颜色分类\daifenlei'  # 待识别图片文件夹
output_folder = r'C:\Users\67167\Desktop\验证码识别\结果\predict'  # 结果保存路径
report_txt_path = os.path.join(output_folder, 'prediction_report.txt')  # 文本报告路径
supported_exts = ['.png', '.jpg', '.jpeg', '.bmp']  # 支持的图片格式

# 创建结果目录和分类子目录
os.makedirs(output_folder, exist_ok=True)
class_folders = []  # 根据实际类别名称修改
for folder in class_folders:
    os.makedirs(os.path.join(output_folder, folder), exist_ok=True)

分类模型路径 = r'C:\Users\67167\Desktop\YOLU\YOLOXUNLIAN\ultralytics-8.3.55\ultralytics-8.3.55\runs\classify\chaoxiang\weights\best.pt'
颜色模型路径 = r'C:\Users\67167\Desktop\YOLU\YOLOXUNLIAN\ultralytics-8.3.55\ultralytics-8.3.55\runs\classify\yanshe1\weights\best.pt'

# 加载训练好的模型
model = YOLO(分类模型路径)


def process_folder(folder_path):
    """处理整个文件夹的图片"""
    image_files = [f for f in os.listdir(folder_path)
                   if os.path.splitext(f)[1].lower() in supported_exts]

    results = []

    with tqdm(total=len(image_files), desc="处理进度") as pbar:
        for filename in image_files:
            try:
                img_path = os.path.join(folder_path, filename)

                # 使用OpenCV读取图像
                img_bgr = cv2.imread(img_path)
                if img_bgr is None:
                    raise ValueError("无法读取图像文件")
                img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

                # 进行预测
                pred_results = model(img_rgb)

                # 解析结果
                top1_idx = pred_results[0].probs.top1
                confidence = pred_results[0].probs.top1conf.item()
                class_name = pred_results[0].names[top1_idx]

                # 创建分类子目录
                class_folder = os.path.join(output_folder, class_name)
                os.makedirs(class_folder, exist_ok=True)

                # 保存结果图片到分类目录
                output_path = os.path.join(class_folder, filename)
                cv2.imwrite(output_path, cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR))

                # 记录结果
                results.append({
                    "filename": filename,
                    "pred_class": class_name,
                    "confidence": confidence,
                    "save_path": output_path
                })

            except Exception as e:
                print(f"\n处理文件 {filename} 时出错: {str(e)}")
                results.append({
                    "filename": filename,
                    "pred_class": "ERROR",
                    "confidence": 0.0,
                    "save_path": ""
                })

            pbar.update(1)

    return results


def generate_text_report(results, report_path):
    """生成文本格式报告"""
    with open(report_path, 'w', encoding='utf-8') as f:
        # 写入CSV格式报告
        f.write("文件名,预测类别,置信度,保存路径\n")
        for item in results:
            f.write(f"{item['filename']},{item['pred_class']},{item['confidence']:.4f},{item['save_path']}\n")


if __name__ == '__main__':
    # 执行批量预测
    all_results = process_folder(input_folder)

    # 生成文本报告
    generate_text_report(all_results, report_txt_path)

    print(f"\n处理完成！共处理 {len(all_results)} 张图片")
    print(f"分类结果保存在: {output_folder}")
    print(f"文本报告已生成: {report_txt_path}")