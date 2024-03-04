from time import sleep

import pyautogui

from anglerecognition import *
from function import screenshot, findstr
from moni import mouse_moveR, mouse_moveR1
from 内存操作 import 获取自身坐标

self_pos_left, self_pos_up, self_pos_right, self_pos_bottom = 122, 134, 160, 172



def 最近寻路走过去(主任务, 子任务, template):
    pass


def is_point_between_2d(point, end1, end2):
    """计算该点是否在两点之间"""
    dist_total = calculate_distance(end1, end2)
    dist_1 = calculate_distance(point, end1)
    dist_2 = calculate_distance(point, end2)
    # 如果点到两端点的距离之和等于两端点之间的距离（允许一定的误差）
    return abs(dist_1 + dist_2 - dist_total) < 1

def setangle(angle_now, angle_target, fault=10,fun=0):
    angle_diff = abs(angle_now - angle_target)
    if angle_diff <= fault:
        return
    if angle_diff > 50:
        pyautogui.keyUp('w')
    if abs(angle_diff) >= fault:
        angle_diff = int((angle_target - angle_now) % 360)
        if angle_diff > 180:
            fangxiang = -1
            angle_diff = 360 - angle_diff
        else:
            fangxiang = 1
        if abs(angle_diff < fault):
            return
        print(f"调整视角 相差:{fangxiang * angle_diff}° 当前:{angle_now}° 目标:{angle_target}°  ")
        if fun==1:
            mouse_moveR1(int(fangxiang *5* angle_diff))
        mouse_moveR(int(fangxiang * angle_diff))


def read_coordinates(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            x, y = line.strip().split(',')
            coordinates.append((float(x), float(y)))
    return coordinates


# 计算两点之间的欧氏距离
def calculate_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)


# 找到与给定坐标距离最近的坐标的序号
def find_nearest_coordinate_index(coordinates, target_coord):
    """找到与给定坐标距离最近的坐标的序号"""
    min_distance = float('inf')
    nearest_index = -1
    for i, coord in enumerate(coordinates):
        distance = calculate_distance(coord, target_coord)
        if distance < min_distance:
            min_distance = distance
            nearest_index = i
    return nearest_index


def 获取坐标寻路数组(file_path, target_coord,get=True):
    """参数为路径和自身坐标(x,y)"""
    # 读取坐标
    coordinates = read_coordinates(file_path)

    # 找到最近的坐标序号
    nearest_index = find_nearest_coordinate_index(coordinates, target_coord)

    # 删除序号之前的坐标
    coordinates = coordinates[nearest_index:]

    print(f"保留的坐标：{coordinates}")

    if get and len(coordinates) > 1 and is_point_between_2d(target_coord, coordinates[0], coordinates[1]):
            print("切换近距离坐标")
            coordinates = coordinates[1:]
    return coordinates


if __name__ == '__main__':
    template = cv2.imdecode(np.fromfile(file=r"小图.png", dtype=np.uint8), cv2.IMREAD_UNCHANGED)  # 加载透明图
    最近寻路走过去("task\\混乱行至深处\\穿过长廊成功进入空间站内部.txt", template)
