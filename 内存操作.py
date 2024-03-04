import ctypes
import struct
import math
# 定义所需的Windows API和结构
from ctypes import wintypes
from ctypes.wintypes import DWORD, HMODULE, HANDLE, MAX_PATH

import win32gui
import win32process

OpenProcess = ctypes.WinDLL('kernel32', use_last_error=True).OpenProcess
ReadProcessMemory = ctypes.WinDLL('kernel32', use_last_error=True).ReadProcessMemory
CloseHandle = ctypes.WinDLL('kernel32', use_last_error=True).CloseHandle

EnumProcessModules = ctypes.windll.psapi.EnumProcessModules
EnumProcessModules.argtypes = [HANDLE, ctypes.POINTER(HMODULE), DWORD, ctypes.POINTER(DWORD)]
EnumProcessModules.restype = ctypes.c_bool

GetModuleFileNameEx = ctypes.windll.psapi.GetModuleFileNameExA
GetModuleFileNameEx.argtypes = [HANDLE, HMODULE, ctypes.c_char_p, DWORD]
GetModuleFileNameEx.restype = DWORD

PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
PROCESS_VM_READ = 0x0010
SIZE_T = ctypes.c_size_t
国服基址 = 0x7FFB2235F58C  # 偏移为104，198
# 偏移为104，198
基址 = 0x7FFB25080000


def get_pid_by_window_title_and_class(title, class_name):
    # 定义一个回调函数，用于枚举窗口
    def enum_windows_proc(hwnd, lParam):
        # 检查窗口标题和类名是否匹配
        if win32gui.IsWindowVisible(hwnd) and title == win32gui.GetWindowText(
                hwnd) and class_name == win32gui.GetClassName(hwnd):
            # 获取窗口所属的进程ID
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            lParam.append(pid)  # 将PID添加到列表中

    pids = []
    # 枚举所有窗口，并对每个窗口调用回调函数
    win32gui.EnumWindows(enum_windows_proc, pids)

    return pids


# 通用基址 = "unityplayer.dll"+01DD5D68
pids = get_pid_by_window_title_and_class("崩坏：星穹铁道", "UnityWndClass")  # 这玩意儿返回的是个数组。。。。
process_handle = OpenProcess(PROCESS_ALL_ACCESS, False, pids[0])
if not process_handle:
    print("Failed to open process")

modules = (HMODULE * 1024)()
needed = DWORD()
module_name = "unityplayer.dll"
通用基址 = 0
# 枚举进程中的所有模块
if EnumProcessModules(process_handle, modules, ctypes.sizeof(modules), ctypes.byref(needed)):
    for i in range(needed.value // ctypes.sizeof(HMODULE)):
        mod_name = (ctypes.c_char * MAX_PATH)()
        if GetModuleFileNameEx(process_handle, modules[i], mod_name, MAX_PATH):
            if module_name.lower() in mod_name.value.decode().lower():
                # 找到指定模块，返回其基址
                通用基址 = modules[i]
通用基址 = 0x01DD5D68 + 通用基址


def 获取自身坐标():
    """3D游戏应该获取的是XZ坐标才对，为了让代码方便理解，这里写XY"""
    float_value_x, float_value_y = 0, 0
    try:
        一级偏移 = bytes_to_int(read_process_memory(通用基址)) + 0x8
        二级偏移 = bytes_to_int(read_process_memory(一级偏移)) + 0x4C
        address = 二级偏移
        float_value_x = bytes_to_float(read_process_memory(address,4))
        float_value_y = bytes_to_float(read_process_memory(address + 8,4))
        return float_value_x, float_value_y
    except Exception as e:
        print("获取坐标失败，可能未刷新:", e)
        return float_value_x, float_value_y


import ctypes


class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [("BaseAddress", ctypes.c_void_p),
                ("AllocationBase", ctypes.c_void_p),
                ("AllocationProtect", ctypes.c_ulong),
                ("RegionSize", ctypes.c_size_t),
                ("State", ctypes.c_ulong),
                ("Protect", ctypes.c_ulong),
                ("Type", ctypes.c_ulong)]


def query_memory_accessible(process_handle, address):
    mbi = MEMORY_BASIC_INFORMATION()
    MEM_COMMIT = 0x1000  # 内存已被提交
    address = ctypes.c_void_p(address)
    if ctypes.windll.kernel32.VirtualQueryEx(process_handle, address, ctypes.byref(mbi), ctypes.sizeof(mbi)):
        # 检查内存状态是否为MEM_COMMIT，如果是，则表示内存可以访问
        if mbi.State == MEM_COMMIT:
            return True  # 内存可以访问
        else:
            return False  # 内存不可访问或保留
    else:
        print("VirtualQueryEx failed")
        return False  # VirtualQueryEx调用失败，假定内存不可访问


def read_process_memory(address, size=8):
    """读取内存，指定地址"""
    # 打开目标进程
    pids = get_pid_by_window_title_and_class("崩坏：星穹铁道", "UnityWndClass")  # 这玩意儿返回的是个数组。。。。

    process_handle = OpenProcess(PROCESS_ALL_ACCESS, False, pids[0])
    if not process_handle:
        raise ctypes.WinError(ctypes.get_last_error())

    # 为读取的数据分配缓冲区
    buffer = ctypes.create_string_buffer(size)
    bytes_read = SIZE_T(0)
    # 读取进程内存
    if query_memory_accessible(process_handle, address):
        if not ReadProcessMemory(process_handle, ctypes.c_void_p(address), buffer, size, ctypes.byref(bytes_read)):
            CloseHandle(process_handle)
            raise ctypes.WinError(ctypes.get_last_error())

        # 关闭进程句柄
    CloseHandle(process_handle)

    # 返回读取的数据
    return buffer.raw


def bytes_to_float(data, double_precision=False):
    """将字节串转换为浮点数。

    参数:
    data -- 字节串。
    double_precision -- 如果为True，则解析为双精度浮点数；否则为单精度。
    """
    if double_precision:
        return struct.unpack('d', data)[0]  # 解析为双精度浮点数
    else:
        return struct.unpack('f', data)[0]  # 解析为单精度浮点数


def bytes_to_int(data):
    """将字节串转换为浮点数。

    参数:
    data -- 字节串。
    """

    return struct.unpack('Q', data)[0]  # 无符号整数


def calculate_angle(A, B):
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
    # 示例：读取特定进程的内存
    x, y = 获取自身坐标()

    print(x, y)
