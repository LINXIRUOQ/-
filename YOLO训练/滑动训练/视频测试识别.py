import time

from ultralytics import YOLO
model = rf'C:\Users\67167\Desktop\YOLU\YOLOXUNLIAN\ultralytics-8.3.55\ultralytics-8.3.55\runs\detect\train53\weights\best.pt'

yolo = YOLO(
    model =model,
    task='detect',
)
图片 =rf'C:\Users\67167\Desktop\验证码识别\8.png'
屏幕 =r'screen'
results = yolo(source=图片,
               save = True,
               conf=0.2,
               )
