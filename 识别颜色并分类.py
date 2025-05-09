from ultralytics import YOLO
import os


def detect_objects(folder_path, model_path=r'C:\Users\67167\Desktop\验证码识别\closebest.pt'):
    """
    目标检测主函数
    参数：
        folder_path: 需要检测的图片文件夹路径
        model_path: 模型文件路径 (默认'closebest.pt')
    返回：
        list: 包含 "文件名: 类别" 的列表
    """
    # 配置参数
    supported_exts = ['.png', '.jpg', '.jpeg', '.bmp']

    # 加载模型
    model = YOLO(model_path)
    print("✅ 模型加载完成")

    # 存储结果
    results_dict = {}

    # 遍历处理文件
    for filename in [f for f in os.listdir(folder_path)
                     if os.path.splitext(f)[1].lower() in supported_exts]:
        try:
            # 处理文件名
            pure_name = os.path.splitext(filename)[0]  # 去除扩展名

            # 执行预测
            results = model(os.path.join(folder_path, filename))

            # 解析结果
            pred = results[0].probs
            class_name = results[0].names[pred.top1]

            results_dict[pure_name] = class_name

        except Exception as e:
            print(f"⚠ 处理 {filename} 出错: {str(e)}")
            continue

    # 格式化输出结果
    return [f"{k}: {v}" for k, v in results_dict.items()]


if __name__ == '__main__':
    # 使用示例
    input_folder = r'C:\Users\67167\Desktop\验证码识别\shibie2'
    results = detect_objects(input_folder)
    print("识别结果：")
    for item in results:
        print(item)