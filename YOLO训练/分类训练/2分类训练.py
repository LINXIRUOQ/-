from ultralytics import YOLO
import multiprocessing


def main():
    # 加载预训练分类模型（推荐使用官方分类模型）
    model = YOLO(r"yolo11n-cls.pt")  # 使用官方YOLOv8分类模型

    # 训练参数配置
    model.train(
        data=r"C:\Users\67167\Desktop\yanzhengmashibie\YOLODirectiontrain",
        epochs=500,  # 减少训练轮次（颜色分类相对简单）
        imgsz=224,
        batch=16,  # 增大批大小（需根据GPU显存调整）
        workers=4,  # 自动设置最优workers数
        optimizer="Adam",  # 使用Adam优化器
        lr0=2e-4,  # 折中学习率
        hsv_h=0.0,  # 保持原始色调
        hsv_s=0.2,  # 允许20%饱和度变化
        hsv_v=0.2,  # 允许20%亮度变化
        degrees=0,  # 禁用旋转（验证码通常方向固定）
        fliplr=0.0,  # 禁用水平翻转（验证码通常无镜像需求）
        flipud=0.0,  # 禁用垂直翻转
        mosaic=0.0,  # 禁用马赛克增强
        perspective=0.0005,  # 极轻微透视变换（模拟视角差异）
        shear=0,  # 允许1度剪切变换
        mixup=0.0,  # 禁用混合增强
        copy_paste=0.0,  # 禁用复制粘贴
        name="chaoxiang",
        pretrained=True,  # 使用预训练权重
        patience=20,  # 早停机制（10轮无改进停止训练）
        device="0" , # 指定使用GPU（如果有）
        dropout = 0.2,  # 增强正则化
        weight_decay = 0.001,  # 控制过拟合
        single_cls = False  # 确保多分类模式
    )


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()