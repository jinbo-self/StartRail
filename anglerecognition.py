import copy
import math
import time
import cv2
import os
import numpy as np
#from ultralytics import YOLO
import pyautogui
from win32api import Sleep

from function import screenshot
from moni import mouse_moveR


def pyramid_template_matching(image, template, mask=None):
    '''
    金字塔模板匹配
    :param image:
    :param template:
    :param mask:
    :return:
    '''
    result = image.copy()
    # 创建掩码
    if mask is not None:
        mask = mask.astype(np.uint8)
    # 金字塔层级
    # pyramid_levels =1
    best_angle = 0  # 最佳匹配角度
    max_similarity = 0  # 最大相似度
    best_res = 0
    best_rotated_template = ""
    h, w = template.shape[:2]
    scaled_mask = mask.astype(np.uint8)
    scaled_image = image
    scaled_template = template
    # for level in range(pyramid_levels):
    #     # 缩放大图和小图
    #     scaled_image = cv2.resize(image, (0, 0), fx=1 / (2 ** level), fy=1 / (2 ** level))
    #     scaled_template = cv2.resize(template, (0, 0), fx=1 / (2 ** level), fy=1 / (2 ** level))
    #     if mask is not None:
    #         scaled_mask = cv2.resize(mask, (0, 0), fx=1 / (2 ** level), fy=1 / (2 ** level))
    #         scaled_mask = scaled_mask.astype(np.uint8)
    # 旋转模板并进行匹配
    for angle in range(0, 360, 10):
        rotated_mask = rotate_image(scaled_mask, angle)
        rotated_mask[rotated_mask > 1] = 255  # 将灰色也变成白色
        rotated_template = rotate_image(scaled_template, angle)
        #save_rotated_image(rotated_template, "./datas/img", f"{angle}_template")
        #save_rotated_image(rotated_mask, "./datas/img", f"{angle}_mask")
        res = cv2.matchTemplate(cv2.cvtColor(scaled_image, cv2.COLOR_BGR2GRAY),
                                cv2.cvtColor(rotated_template, cv2.COLOR_BGR2GRAY), cv2.TM_CCORR_NORMED,
                                mask=rotated_mask)
        similarity = cv2.minMaxLoc(res)[1]  # 获取匹配相似度
        if similarity > max_similarity:
            max_similarity = similarity
            best_angle = angle
            best_res = res
            best_rotated_template = rotated_template

    best_angle_bk = copy.copy(best_angle)
    start_angle = best_angle_bk - 10
    if start_angle < 0:
        start_angle = 0
        end_angle = start_angle + 10
    else:
        end_angle = start_angle + 20
    for angle in range(start_angle, end_angle, 1):
        rotated_mask = rotate_image(scaled_mask, angle)
        rotated_mask[rotated_mask > 1] = 255  # 将灰色像素值改为黑色像素值
        rotated_template = rotate_image(scaled_template, angle)
        res = cv2.matchTemplate(cv2.cvtColor(scaled_image, cv2.COLOR_BGR2GRAY),
                                cv2.cvtColor(rotated_template, cv2.COLOR_BGR2GRAY), cv2.TM_CCORR_NORMED,
                                mask=rotated_mask)
        similarity = cv2.minMaxLoc(res)[1]  # 获取匹配相似度
        if similarity > max_similarity:
            max_similarity = similarity
            best_angle = angle
            best_res = res
            best_rotated_template = rotated_template

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(best_res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    # 绘制角度
    # cv2.putText(result, f"{int(best_angle)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # 在原始大图上绘制矩形框标记匹配区域,需要展示之后才能画
    cv2.rectangle(result, top_left, bottom_right, (0, 255, 0), 2)
    return result, max_similarity, best_angle, best_rotated_template


def save_rotated_image(rotated_image, save_dir, index):
    save_path = os.path.join(save_dir, f"{index}.png")
    cv2.imwrite(save_path, rotated_image)


def rotate_image(image, angle):
    '''
    将图片旋转多少度
    :param image:
    :param angle:
    :return:
    '''
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, -angle, 1.0)
    rotated_image = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT,
                                   borderValue=(0, 0, 0, 0))
    return rotated_image


def get_tangle_and_distance(A, B):
    """
    计算点B相对于点A的夹角度数，Y轴正半轴为0度和360度。

    参数:
    A -- 点A的坐标，形式为(x, y)。
    B -- 点B的坐标，形式为(x, y)。

    返回:
    angle -- 点B相对于点A的夹角度数。
    """
    # 计算从B到A的向量
    vector_x = B[0] - A[0]
    vector_y = B[1] - A[1]

    # 使用atan2计算向量与Y轴正半轴之间的夹角（弧度）
    angle_radians = math.atan2(vector_x, vector_y)

    # 将弧度转换为度
    angle_degrees = math.degrees(angle_radians)

    # 将角度转换为0到360度的范围
    if angle_degrees < 0:
        angle_degrees += 360

    return angle_degrees





if __name__ == '__main__':
    safe = 0
    cnt = 10
    ang = [1, 1, 3]

    print("开始校准")
    multi = 1
    self_pos_left, self_pos_up, self_pos_right, self_pos_bottom = 122, 134, 160, 172

    self_pos_center_x, self_pos_center_y = self_pos_left + (
            self_pos_right - self_pos_left) / 2, self_pos_up + (self_pos_bottom - self_pos_up) / 2
    img = screenshot(self_pos_center_x - 19, self_pos_center_y - 19, self_pos_center_x + 19,
                     self_pos_center_y + 19)  # 截的自己箭头图片
    template = cv2.imdecode(np.fromfile(file=r"小图.png", dtype=np.uint8), cv2.IMREAD_UNCHANGED)  # 加载透明图
    mask = template[:, :, 3]  # 提取透明度通道作为掩码
    result, _, init_ang, _ = pyramid_template_matching(img, template, mask=mask)  # 获取箭头朝向角度，向上为0度
    lst_ang = init_ang
    print("lst_ang:", lst_ang)
    for i in ang:
        if lst_ang != init_ang and i == 1:
            continue
        ang_list = []
        for j in range(i):
            mouse_moveR(60, fine=3 // i)
            time.sleep(0.2)
            pyautogui.press('w')
            img = screenshot(self_pos_center_x - 19, self_pos_center_y - 19, self_pos_center_x + 19,
                             self_pos_center_y + 19)  # 截的自己箭头图片
            result, _, now_ang, _ = pyramid_template_matching(img, template, mask=mask)  # 获取箭头朝向角度，向上为0度
            print("lst_ang:", lst_ang, "now_ang:", now_ang)
            sub = lst_ang - now_ang
            while sub < 0:
                sub += 360
            ang_list.append(sub)
            lst_ang = now_ang
        ang_list = np.array(ang_list)
        # 十/3次转身的角度
        print(ang_list)
        ax = 0
        ay = 0
        for j in ang_list:
            if abs(j - np.median(ang_list)) <= 3:
                ax += 60
                ay += j
        multi *= ax / ay
    multi += 1e-9
    try:
        if not abs(multi) <= 2:
            multi = 1
    except:
        multi = 1
    angle = str(multi + len(ang) - 1)
    print(angle)
    print("校准完成")




