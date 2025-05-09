import pyautogui
import time


# 截取屏幕并保存
def capture_screenshot(save_path="screenshot.png"):
    screenshot = pyautogui.screenshot()  # 截屏
    screenshot.save(save_path)  # 保存图片


# 模拟鼠标点击
def click_mouse():
    pyautogui.click()  # 默认点击当前鼠标位置


# 主程序
def main(bibidjad):
    bibidjad = f'{bibidjad}.png'
    # 先截取屏幕并保存
    capture_screenshot(bibidjad)
    print("截屏已保存为 screenshot.png")

    # 等待一小会儿，确保截图已经保存

    # 然后模拟点击鼠标
    click_mouse()
    print("已在当前屏幕位置点击鼠标左键")


if __name__ == "__main__":
    bibidjad = 300
    time.sleep(5)
    while True:
        bibidjad+=1
        main(bibidjad)
        time.sleep(1)
        if bibidjad == 600:
            break
