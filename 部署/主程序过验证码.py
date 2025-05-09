import time

from 数据库 import update_data,get_by_id,get_all_status,get_all_status_with_id,view_all_data,view_all_data1
from 服务器 import linuxxiazhai
from yzmmain import 图片验证
from 识别滑块验证 import 滑块验证
from 查找请点击位置 import find_target_position
返回值 = None
循环次数 = 0
gdajj = view_all_data1()
数据库全部数据 = view_all_data()
while True:
    time.sleep(0.4)
    循环次数 += 1
    zhong = get_all_status()
    print(f'循环次数：{循环次数}值：{zhong}')
    dfghj = 0
    for item in zhong:
        if item == 1:
            device_id = gdajj[dfghj]
            print(f"发现第 {dfghj+1} 号设备 | ID: {device_id}")
            data = get_by_id(device_id)
            可用次数 = data['keyongcishuo']
            linuxxiazhai(device_id)
            过验证 = find_target_position(device_id, target_text='请点击')
            if 过验证:
                print(f'图形验证码')
                try:
                    点击位置 = 图片验证(device_id)
                    返回值 = 点击位置
                except Exception as e:
                    print(e)
                update_data(device_id, 0, 可用次数, 0, 返回值)
            else:
                print(f'滑动验证码')
                返回值 = 滑块验证(device_id)
                print(返回值)
                update_data(device_id, 0, 可用次数, 0, 返回值)
        dfghj += 1