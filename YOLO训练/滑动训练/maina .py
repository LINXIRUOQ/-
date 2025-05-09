from ultralytics import YOLO
def main():
    model = YOLO(model=r'C:\Users\67167\Desktop\YOLU\YOLOXUNLIAN\ultralytics-8.3.55\ultralytics-8.3.55\yolo11n.pt')
    # '''颜色分类/m'''
    # model.train(
    #     data=r'C:\Users\67167\Desktop\YOLU\YOLOXUNLIAN\ultralytics-8.3.55\ultralytics-8.3.55\yanshefenl.yaml',  # 确保YAML文件路径正确
    #     epochs=200,
    #     batch=16,
    #     imgsz=64,
    #     workers=4,
    #     lr0=0.01,
    #     hsv_h=0.0,  # 关闭色相增强
    #     hsv_s=0.0,  # 关闭饱和度增强
    #     hsv_v=0.0,  # 关闭明度增强
    #     erasing=0.0  # 禁用随机擦除
    # )
    '''m/缺口滑块'''
    model.train(
        data='icon.yaml',
        workers=4,
        epochs=500,  # 增加训练轮次（精确定位需要更长时间）
        batch=16,  # 增大batch size（方向固定意味着数据变化较少
        # scale=0.5,  # 添加尺度增强（50%-150%缩放）
        # hsv_s=0.3,  # 饱和度增强
        # hsv_v=0.3,  # 明度增强
        # fliplr=0.0,  # 关闭水平翻转（方向固定）
        # patience=20,  # 增加早停耐
        # degrees=0.0,#旋转
        # mosaic = 0.0,#马赛克
        # lr0 = 0.01,  # 明确设置初始学习率
        # lrf = 0.1,  # 最终学习率
    )


    ''' 识别权重/m模型
    '''
    # model.train(
    # data='icon.yaml',
    # workers=4,
    # # optimizer = 'SGD',  # 改用 SGD 优化器
    # lr0 = 0.01,  # 初始学习率提升
    # lrf = 0.1,  # 学习率衰减幅度增大（最终 lr=0.01*0.1=0.001）
    # momentum = 0.937,  # SGD 标准动量值
    # weight_decay = 0.0003,  # 降低权重衰减强度
    # dropout = 0.0,  # 关闭 Dropout（小模型通常无需）
    # label_smoothing = 0.05,  # 减少标签平滑强度
    # # 训练策略
    # epochs = 200,  # 小模型需更多轮次充分训练
    # batch = 16,  # 增大 Batch Size（需显存充足）
    # # warmup_epochs = 2,  # 缩短学习率预热
    # patience = 30,  # 早停耐心减少
    # amp = True,  # 保持混合精度加速
    # )
    '''11s大模型'''
    # model.train(data='icon.yaml',
    #             workers=4,
    #             optimizer='AdamW',  # 替换为 AdamW 优化器（更适合小数据集）
    #             lr0=0.00015,  # 初始学习率
    #             lrf=0.01,  # 最终学习率 = lr0 * lrf（余弦退火）
    #             momentum=0.9,  # 动量参数（SGD 必需）
    #             warmup_epochs=3,  # 学习率预热 3 epochs
    #             epochs=100,
    #             batch=16,  # 增
    #             imgsz=640,  #
    #             amp=True,
    #             pretrained=True,
    #             weight_decay=0.0005,
    #             dropout=0.2,  # 启用 Dropout
    #             label_smoothing=0.1,  # 标签平滑（应对类别不平衡）
    #             patience=30,  # 早停法：30 epochs 无改善则终止
    #             save_period=10,  # 每 10 epochs 保存一次模型
    #
    #             )
if __name__ == "__main__":
    # Windows 多进程必需的保护
    import multiprocessing
    multiprocessing.freeze_support()  # 若生成 exe 需要此句
    main()