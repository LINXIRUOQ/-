import cv2
import numpy as np

def find_image_location(b_path, a_path='chongzhi.png',threshold=0.8):
    # 读取图片并校验
    big_image = cv2.imread(b_path)
    small_image = cv2.imread(a_path)
    if big_image is None or small_image is None:
        print("图片读取失败")
        return None

    # 灰度转换
    big_gray = cv2.cvtColor(big_image, cv2.COLOR_BGR2GRAY)
    small_gray = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)

    # 高斯降噪
    big_gray = cv2.GaussianBlur(big_gray, (3, 3), 0)
    small_gray = cv2.GaussianBlur(small_gray, (3, 3), 0)

    # 多尺度匹配参数
    scales = [0.6, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4]
    best_max = (-1, None, (0, 0))  # (max_val, max_loc, (w,h))
    small_h, small_w = small_gray.shape

    for scale in scales:
        # 计算缩放后尺寸
        w = int(small_w * scale)
        h = int(small_h * scale)
        if w <= 0 or h <= 0:
            continue
        if w > big_gray.shape[1] or h > big_gray.shape[0]:
            continue

        # 缩放模板并匹配
        resized = cv2.resize(small_gray, (w, h), interpolation=cv2.INTER_AREA)
        result = cv2.matchTemplate(big_gray, resized, cv2.TM_CCOEFF_NORMED)

        # 获取当前尺度最佳匹配
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if max_val > best_max[0]:
            best_max = (max_val, max_loc, (w, h))

    # 阈值判断
    if best_max[0] >= threshold:
        print(f'匹配成功 最高置信度: {best_max[0]:.2f}')
        max_loc = best_max[1]
        w, h = best_max[2]
        x1, y1 = max_loc
        x2, y2 = x1 + w, y1 + h
        return (x1, y1, x2, y2)
    else:
        print(f'匹配失败 最高置信度: {best_max[0]:.2f}')
        return None

if __name__ == '__main__':
    find_image_location('103.png')