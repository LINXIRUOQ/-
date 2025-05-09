from fontTools.misc.cython import returns
from ultralytics import YOLO
from 对图片进行标注 import annotate_image
import time
def calculate_overlap(tu_box, que_box):
    """计算两个矩形在垂直方向的重叠面积（假设水平已对齐）"""
    # 突的坐标
    x1_tu, y1_tu, x2_tu, y2_tu = tu_box
    # 调整后的缺坐标（水平对齐）
    x1_que, y1_que, x2_que, y2_que = x1_tu, que_box[1], x2_tu, que_box[3]

    # 计算垂直重叠
    y_overlap_start = max(y1_tu, y1_que)
    y_overlap_end = min(y2_tu, y2_que)
    overlap_height = max(0, y_overlap_end - y_overlap_start)

    # 计算重叠面积
    return overlap_height * (x2_tu - x1_tu)
# 加载模型
model_path = r'C:\Users\67167\Desktop\YOLU\YOLOXUNLIAN\ultralytics-8.3.55\ultralytics-8.3.55\runs\detect\train53\weights\best.pt'
yolo = YOLO(model=model_path, task='detect')

# 执行推理
def 滑块验证(tupian):
    results = yolo(
        source=tupian,
        save=True,
        conf=0.2,
    )
    for result in results:
        print(f"\nImage ID: 0")

        if result.boxes is not None:
            # 初始化存储
            max_tu_conf = -1
            best_tu_box = None
            ques = []

            # 第一遍遍历分类
            for box in result.boxes:
                coords = [round(c, 2) for c in box.xyxy.tolist()[0]]
                cls_name = result.names[int(box.cls)]
                conf = round(float(box.conf), 2)

                if cls_name == "突":
                    if conf > max_tu_conf:
                        max_tu_conf = conf
                        best_tu_box = coords
                else:
                    ques.append((coords, conf))

            # 处理最佳突
            obj_id = 0
            if best_tu_box:
                print(f"Object {obj_id}: 突 | Confidence: {max_tu_conf} | BBox: {best_tu_box}")
                obj_id += 1
                tux, tuy, tuz, tuw = best_tu_box

                # 计算最大重叠缺
                max_overlap = 0
                best_que = None
                for que_coords, que_conf in ques:
                    overlap = calculate_overlap(best_tu_box, que_coords)
                    if overlap > max_overlap:
                        max_overlap = overlap
                        best_que = (que_coords, que_conf, overlap)

                # 输出最大重叠结果
                if best_que:
                    orig_coords, conf, area = best_que
                    print(f"\n[最大重叠] 原坐标: {orig_coords} | 置信度: {conf} | 重叠面积: {area:.2f}")
                    cdx, cdy, cdz, cdw = orig_coords
                    tuz = int(tuz)+10
                    tuw = int(tuw)-5
                    cdz = int(cdz)+10
                    cdw = int(cdw)-5
                    annotate_image(
                        input_path=tupian,
                        output_dir=r'.\验证点击验证码后的结果',
                        coordinates=(tuz, tuw),
                        text="头",  # 可选文本标注
                        mark_color="#FF0000",  # 支持十六进制颜色
                        mark_size=8,
                        font_size=18
                    )
                    time.sleep(1)
                    annotate_image(
                        input_path=tupian,
                        output_dir=r'.\验证点击验证码后的结果',
                        coordinates=(cdz, cdw),
                        text="尾",  # 可选文本标注
                        mark_color="#FF0000",  # 支持十六进制颜色
                        mark_size=8,
                        font_size=18)
                    最终点击位置 = f'{tuz}_{tuw}_{cdz}_{cdw}'
                    return 最终点击位置
            # 输出其他缺
            for que_coords, que_conf in ques:
                print(f"Object {obj_id}: 缺 | Confidence: {que_conf} | BBox: {que_coords}")
                obj_id += 1
        else:
            print("未检测到任何目标")

if __name__ == '__main__':
    jkdad=滑块验证('4455cheshi.png')
    print(jkdad)
