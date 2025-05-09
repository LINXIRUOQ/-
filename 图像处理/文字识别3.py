from cnocr import CnOcr
from typing import Optional, Union, Collection, Dict, Any
from pathlib import Path
import cv2

def preprocess_image(img_path):
    # 读取图像
    img = cv2.imread(img_path)
    # 转为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 增强对比度
    enhanced = cv2.equalizeHist(gray)
    # 可选：应用高斯模糊或去噪
    denoised = cv2.fastNlMeansDenoising(enhanced, None, 30, 7, 21)
    return denoised
# 正确初始化OCR实例的配置
rec_model_name = ['densenet_lite_136-gru','scene-densenet_lite_136-gru'
    ,'doc-densenet_lite_136-gru' ,'db_mobilenet_v3','ch_PP-OCRv4_server']
ocr = CnOcr(
    rec_model_name='densenet_lite_136-gru',  # 识别模型
    det_model_name='',        # 检测模型
    context='gpu',                           # 使用CPU推理
    rec_model_backend='onnx',                # ONNX后端
    det_model_backend='onnx',                # ONNX后端
    cand_alphabet=None                       # 不限制识别字符集
)
def recognize_text(img_path):
    img_path = img_path
    ocr = CnOcr()
    out = ocr.ocr_for_single_line(img_path)
    return out['text']
if __name__ == '__main__':
    print(recognize_text('wenzhi.png'))
