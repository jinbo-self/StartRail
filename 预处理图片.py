
import cv2
import numpy as np
from PIL import Image

from function import screenshot


def 预处理图片识别教程标记(img):
    """
    :param img: opencv格式的图片
    """
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pillow_image = Image.fromarray(rgb_image)

    # img = pillow_image.convert("RGBA")  # 转换为RGBA以检测alpha通道（透明度）

    datas = pillow_image.getdata()
    # lower_white = np.array([110, 230, 220,0], dtype=np.uint8)
    # upper_white = np.array([130, 250, 240,255], dtype=np.uint8)
    newData = []
    for item in datas:
        # 通过比较RGB值来判断是否为白色背景#00C6FF
        if 100 < item[0] < 200 and 200 < item[1] < 255 and 200 < item[2] < 255:
            # 设置为透明
            newData.append(item)
        else:
            newData.append((0, 0, 0))

    pillow_image.putdata(newData)
    pillow_image = np.array(pillow_image)
    img_cv2 = cv2.cvtColor(pillow_image, cv2.COLOR_RGB2BGR)
    return img_cv2


if __name__ == "__main__":
    img = 预处理图片识别教程标记(screenshot(0,0,1920,1080))
    cv2.imshow("222",img)
    cv2.waitKey(0)


