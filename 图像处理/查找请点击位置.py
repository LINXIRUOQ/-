import time

from cnocr import CnOcr


def find_target_position(img_path, target_text='请点击'):
    """
    查找目标文字区域的左上角坐标
    返回格式：(x, y) 或 None（未找到时）
    """
    ocr = CnOcr(
        rec_model_name='doc-densenet_lite_136-gru',
        det_model_name='ch_PP-OCRv3_det',
        context='cpu'
    )

    results = ocr.ocr(img_path)

    for res in results:
        text = res['text']

        # 模糊匹配（解决OCR可能出现的符号问题）
        if target_text in text.replace(' ', '').replace('.', ''):
            print(res['position'])
            # 取四边形坐标的第一个点（左上角）
            x, y = res['position'][0]
            m, z = res['position'][2]
            x = x -10
            y = y -10
            m = m +20
            z = z +10
            print(x, y, m, z)
            return (int(x), int(y),int(m), int(z))  # 转为整数坐标

    return None  # 未找到目标


# 使用示例
if __name__ == "__main__":
    aaa = time.time()
    luj=rf'C:\Users\67167\Desktop\jiaoben\jiaobenxin\QYC\20250506_143424.png'
    position = find_target_position(luj)
    bbb = time.time()
    ccc = bbb - aaa
    print(ccc)

