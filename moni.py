import ctypes
# 定义鼠标相关常量
import time

import cv2
import numpy as np
import pyautogui
import win32api
import win32con


from function import screenshot

MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000


# 定义MOUSEINPUT结构体
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


# 定义INPUT结构体
class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT)]

    _fields_ = [("type", ctypes.c_ulong),
                ("input", _INPUT)]


# 鼠标相对移动函数
def mouse_moveR1(dx, dy=0):
    # 构造输入事件列表
    inputs = []
    inputs.append(INPUT(type=0, input=INPUT._INPUT(
        mi=MOUSEINPUT(dx=dx, dy=dy, mouseData=0, dwFlags=MOUSEEVENTF_MOVE, time=0, dwExtraInfo=None))))

    # 发送输入事件
    ctypes.windll.user32.SendInput(len(inputs), ctypes.byref(inputs[0]), ctypes.sizeof(INPUT))
def mouse_move(x, fine=1):
    if x > 30 // fine:
        y = 30 // fine
    elif x < -30 // fine:
        y = -30 // fine
    else:
        y = x
    dx = int(16.5 * y * 2.06) #缩放倍率2.03
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, 0)  # 进行视角移动
    time.sleep(0.5 * fine)
    if x != y:
        mouse_move(x - y, fine)
def mouse_moveR(X):
    X=X/2
    mouse_move(X)

if __name__=="__main__":
    time.sleep(3)
    mouse_moveR(360)