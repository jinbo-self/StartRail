import time

import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
from paddleocr import PaddleOCR
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

def screenshot(left, top, right, bottom):
    """获取指定坐标的截图,输入左上和右下角坐标"""
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    # 将Pillow图像转换为numpy数组
    img_np = np.array(screenshot)
    # 将RGB格式转换为BGR格式，以便于OpenCV处理
    img_cv2 = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    return img_cv2

def findstr(位置):
    """获取指定坐标图片的文字"""
    left, top, right, bottom = 位置[0],位置[1],位置[2],位置[3]
    try:
        img = screenshot(left, top, right, bottom)

        ocr = PaddleOCR()
        result = ocr.ocr(img, cls=False)
        # print(result)
        for line in result:
            for i in line:
                return i[-1][0]
    except:
        print(left, top, right, bottom)
        return ""


if __name__=="__main__":
    F的位置 = (850, 446, 1125, 493)  # 待修改确认
    print(findstr(F的位置))
