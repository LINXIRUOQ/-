import cv2
import numpy as np


def image_preprocessing(
        input_path,
        output_path,
        # ============= 默认关闭所有处理 =============
        # 基本变换参数（默认不生效）
        resize_target=None,  # 默认不调整尺寸
        rotation_angle=0,  # 默认不旋转
        flip_mode=None,  # 默认不翻转
        crop_region=None,  # 默认不裁剪

        # 颜色调整参数（默认不修改）
        convert_color=None,  # 默认不转换颜色空间
        contrast_alpha=1.0,  # 默认对比度不变
        brightness_beta=0,  # 默认亮度不变

        # 滤波与增强参数（默认关闭）
        gaussian_kernel=(0, 0),  # 默认核大小为0（不模糊）
        canny_threshold=None,  # 默认不进行边缘检测
        clahe_clip=0.0,  # 默认关闭CLAHE

        # 二值化参数（默认关闭）
        binary_thresh=80,  # 默认不二值化
        binary_mode=cv2.THRESH_BINARY,  # 保留参数但默认不触发
        invert_colors=False  # 默认不反色
):
    """
    安全模式图像预处理：默认不修改图片，需显式指定参数才会触发处理
    返回：(处理后的图像, 保存状态)
    """
    # 读取原始图像
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError("图像读取失败，请检查路径和文件格式")

    # ============= 条件处理模块 =============
    # 调整尺寸（仅当指定目标尺寸时触发）
    if resize_target is not None:
        img = cv2.resize(img, resize_target, interpolation=cv2.INTER_LINEAR)

    # 旋转（仅当角度非零时触发）
    if rotation_angle != 0:
        h, w = img.shape[:2]
        M = cv2.getRotationMatrix2D((w / 2, h / 2), rotation_angle, 1)
        img = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REPLICATE)

    # 翻转（仅当指定模式时触发）
    if flip_mode is not None:
        img = cv2.flip(img, flip_mode)

    # 裁剪（仅当指定区域时触发）
    if crop_region is not None:
        x, y, w, h = crop_region
        img = img[y:y + h, x:x + w]

    # 颜色空间转换（仅当指定类型时触发）
    if convert_color is not None:
        img = cv2.cvtColor(img, convert_color)
        # 自动处理单通道图像的维度
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # 对比度/亮度调整（仅当参数变化时触发）
    if contrast_alpha != 1.0 or brightness_beta != 0:
        img = cv2.convertScaleAbs(img, alpha=contrast_alpha, beta=brightness_beta)

    # 高斯模糊（仅当核尺寸有效时触发）
    if gaussian_kernel[0] > 0 and gaussian_kernel[1] > 0:
        img = cv2.GaussianBlur(img, gaussian_kernel, sigmaX=0)

    # Canny边缘检测（需显式指定阈值）
    if canny_threshold is not None:
        edges = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
                          canny_threshold[0], canny_threshold[1])
        img = cv2.merge([edges, edges, edges])

    # CLAHE直方图均衡（仅当clip值>0时触发）
    if clahe_clip > 0:
        clahe = cv2.createCLAHE(clipLimit=clahe_clip, tileGridSize=(8, 8))
        if len(img.shape) == 3:
            channels = cv2.split(img)
            channels = [clahe.apply(ch) for ch in channels]
            img = cv2.merge(channels)
        else:
            img = clahe.apply(img)

    # 二值化（仅当指定阈值时触发）
    if binary_thresh is not None:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
        _, img = cv2.threshold(gray, binary_thresh, 255, binary_mode)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # 反色处理（需显式启用）
    if invert_colors:
        img = cv2.bitwise_not(img)

    # 保存原始/处理后的图像
    success = cv2.imwrite(output_path, img)
    return img, success
if __name__ == "__main__":
    # 默认调用示例：直接复制原图
    processed_img, status = image_preprocessing(
        input_path="4.png",
        output_path="4a.png",
        # 输出文件将与输入文件完全相同
    )