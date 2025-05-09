import time

from ultralytics import YOLO


yolo = YOLO(
    model =r'C:\Users\67167\Desktop\YOLU\YOLOXUNLIAN\ultralytics-8.3.55\ultralytics-8.3.55\runs\detect\train38\weights\best.pt',
    task='detect',
)
time.sleep(2)
results = yolo(source='screen',
               save = True,
               conf=0.4,
               )
