import threading

import pyautogui
import win32gui
from PIL import Image

from pynput import keyboard
from pynput.keyboard import Key

from function import *
from ultralytics import YOLO

from hookkeymose import HookKeyMose
from pos_get_load import *

# 箭头坐标125.76, 132.09,165.58, 171.91
# if(findstr(61, 281, 340, 312)=="混乱行至深处"):第一个任务
from 预处理图片 import 预处理图片识别教程标记

# 识字
主任务位置 = (61, 281, 340, 312)
子任务位置 = (55, 315, 411, 364)

# 识图
当前分辨率 = (0, 0, 1920, 1080)
战斗标识 = (1565, 1, 1920, 86)  # 待修改确认 YOLO识别
对话标识 = (1565, 1, 1920, 86)  # 待修改确认 YOLO识别
对话点击位置 = (1425, 760)  # 待修改确认
详情位置 = (216, 136, 275, 174)  # ocr识字识别
对话 = (130, 139, 169, 80)  # ocr识字识别 ,识别不了

战斗 = (89, 931, 135, 970)
当前位置 = (52, 9, 155, 49)
F的位置 = (1147, 589, 1560, 658)  # 待修改确认
isPause = False
区域数组 = ["主控舱段", "基座舱段", "支援舱段", "收容舱段"]
启用载体 = (260, 576, 405, 631)
继续启用 =  (1531, 736, 1668, 789)
def 顺序执行(目标坐标数组路径):
    print("开始顺序执行")
    第一次按下 = False
    第二次按下 = False
    if os.path.exists(目标坐标数组路径):
        template = cv2.imdecode(np.fromfile(file=r"小图.png", dtype=np.uint8), cv2.IMREAD_UNCHANGED)  # 加载透明图
        内存坐标x, 内存坐标y = 获取自身坐标()
        目标坐标数组1 = read_coordinates(目标坐标数组路径)
        # 坐标数组长度 = len(目标坐标数组1)
        mask = template[:, :, 3]  # 提取透明度通道作为掩码
        self_pos_center_x, self_pos_center_y = self_pos_left + (
                self_pos_right - self_pos_left) / 2, self_pos_up + (self_pos_bottom - self_pos_up) / 2
        # 裁剪坐标数组，只留下最近的和之后的，获取最近距离的数组下标，返回该下标之后（包括该下标）的值，也就是后半截数组
        # 如果离远离终点的点位近那还是舍弃吧
        print(目标坐标数组1)
        执行完 = False
        for i in range(len(目标坐标数组1)):
            目标坐标数组 = 目标坐标数组1[i]
            img = screenshot(self_pos_center_x - 19, self_pos_center_y - 19, self_pos_center_x + 19,
                             self_pos_center_y + 19)  # 截的自己箭头图片
            # 其实就是目标坐标，懒得改了，就这样

            距离 = math.sqrt((目标坐标数组[0] - 内存坐标x) ** 2 + (目标坐标数组[1] - 内存坐标y) ** 2)
            result, _, 当前角度, _ = pyramid_template_matching(img, template, mask=mask)  # 获取箭头朝向角度，向上为0度
            目标角度 = get_tangle_and_distance((内存坐标x, 内存坐标y), (目标坐标数组[0], 目标坐标数组[1]))
            fault = 2
            print("当前坐标：", 内存坐标x, 内存坐标y, "目标坐标:", 目标坐标数组[0], 目标坐标数组[1])
            setangle(当前角度, 目标角度, fault)
            now_time = time.time()
            while 距离 > 0.3:
                # pyautogui.press('w')
                if 距离<5:
                    pyautogui.keyUp('w')
                    interval = 0.5
                else:
                    pyautogui.keyUp('w')
                    interval = 0
                if abs(当前角度 - 目标角度) > 10:
                    print("开始转角")
                    pyautogui.keyUp('w')
                    img = screenshot(self_pos_center_x - 19, self_pos_center_y - 19, self_pos_center_x + 19,
                                     self_pos_center_y + 19)  # 截的自己箭头图片
                    result, _, 当前角度, _ = pyramid_template_matching(img, template, mask=mask)  # 获取箭头朝向角度，向上为0度
                    setangle(当前角度, 目标角度, fault)
                    sleep(1)
                print("当前角度",当前角度,"目标角度",目标角度)
                img = screenshot(self_pos_center_x - 19, self_pos_center_y - 19, self_pos_center_x + 19,self_pos_center_y + 19)  # 截的自己箭头图片
                result, _, 当前角度, _ = pyramid_template_matching(img, template, mask=mask)  # 获取箭头朝向角度，向上为0度
                内存坐标x, 内存坐标y = 获取自身坐标()
                目标角度 = get_tangle_and_distance((内存坐标x, 内存坐标y), (目标坐标数组[0], 目标坐标数组[1]))
                距离 = calculate_distance(目标坐标数组, (内存坐标x, 内存坐标y))
                Fd = findstr(F的位置)
                if Fd != "" and Fd != "配控装置":
                    pyautogui.keyDown('f')
                    sleep(0.01)
                    pyautogui.keyUp('f')
                if Fd == "配控装置":
                    if 第一次按下 == False or 第二次按下 == False:
                        配空装置位置 = (95.87102509, 102.2781296)
                        内存坐标x, 内存坐标y = 获取自身坐标()
                        距离 = calculate_distance(配空装置位置, (内存坐标x, 内存坐标y))
                        if 距离 < 5 and 第一次按下 == False:
                            pyautogui.press('f')
                            第一次按下 = True
                            break
                        配空装置位置1 = (66.0109024, 98.46126556)
                        内存坐标x1, 内存坐标y1 = 获取自身坐标()
                        距离1 = calculate_distance(配空装置位置1, (内存坐标x1, 内存坐标y1))
                        if 距离1 < 5 and 第二次按下 == False:
                            pyautogui.press('f')
                            第二次按下 = True
                            break
                if interval>0:
                    sleep(interval)
                    pyautogui.press('w')
                else:
                    pyautogui.keyDown("w")
                执行完 = True
            # 遍历数组，走完跳出
            pyautogui.keyUp('w')
            Fd = findstr(F的位置)
            if Fd != "" and Fd!="配控装置":
                pyautogui.press('f')

    else:
        print(f"未找到路径文件:{目标坐标数组路径}")
        mouse_moveR(90)


class StartRailAutoMap(HookKeyMose):
    def __init__(self):
        super().__init__()
        HookKeyMose.__init__(self, hookKey=True)
        self.model = YOLO("best.pt")
        self.走完 = False
        self.cirl = False
        self.map_matrix = []
        self.template = cv2.imdecode(np.fromfile(file=r"小图.png", dtype=np.uint8), cv2.IMREAD_UNCHANGED)  # 加载透明图
    def run(self):
        old_res = False
        new_res = False
        self.on_start = True
        print("自动开始")
        hwnd = win32gui.FindWindow("UnityWndClass", "崩坏：星穹铁道")  # 替换成你实际的窗口句柄
        while True:
            # 这是跳过教程
            print("自动开始")
            sleep(0.01)
            new_res = False
            主任务 = findstr(主任务位置)
            子任务 = findstr(子任务位置)

            print(主任务, 子任务)

            path = "task\\" + 主任务 + "\\" + 子任务 + ".txt"
            if 主任务 == "混乱行至深处" and 子任务 == "协助银狼调查监控室内的终端":
                continue
            if 主任务 == "混乱行至深处" and 子任务 == "然而银狼似乎已经理解了一切":
                continue
            if 主任务 == "混乱行至深处" and 子任务 == "与奇物交互揭开监控室的秘密":
                continue


            # self.自动对话()
            # self.自动战斗()
            当前截图1 = screenshot(当前分辨率[0], 当前分辨率[1], 当前分辨率[2], 当前分辨率[3])

            if 当前截图1 is None:
                continue
            当前截图 = 预处理图片识别教程标记(当前截图1)
            # cv2.imshow("当前截图", 当前截图)
            # cv2.waitKey(0)

            results = self.model(当前截图)  # 对图像进行预测
            print(len(results))
            for r in results:
                boxes = r.boxes  # Boxes object for bbox outputs
                for box in boxes:
                    if r.names[int(np.array(box.cls.cpu())[0])] == "圆形" or \
                            r.names[int(np.array(box.cls.cpu())[0])] == "矩形":
                        print("发现教程标识")
                        临时 = np.array(box.xywh.cpu())[0]
                        pyautogui.keyDown('alt')  # 防止寻路时触发教程
                        sleep(0.5)
                        pyautogui.click(临时[0], 临时[1])
                        sleep(0.5)
                        pyautogui.keyUp('alt')
                        new_res = True

            if findstr(详情位置) == "详情":
                pyautogui.press('c')
            if findstr((868, 881, 1056, 921)) == "点击空白处关闭":
                pyautogui.click(对话点击位置[0], 对话点击位置[1])
            res = findstr((100, 40, 187, 66))
            if res == "教学自录" or res == "任务" or res == "导航" \
                    or res == "界域定锚" or res=="队伍" or res=="等级提升" \
                    or res=="战斗实况" or res=="跃迁" or res=="旅情事记":
                pyautogui.press('esc')
            if findstr(启用载体) == "启用载体":
                pyautogui.click(启用载体[0]+(启用载体[2]-启用载体[0])/2, 启用载体[1]+(启用载体[3]-启用载体[1])/2)
            if findstr(继续启用) == "继续启用":
                pyautogui.click(继续启用[0]+(继续启用[2]-继续启用[0])/2, 继续启用[1]+(继续启用[3]-继续启用[1])/2)
            进行变更 = (1419, 730, 1548, 789)
            if findstr(进行变更) == "进行变更":
                pyautogui.click(1554, 514)
                pyautogui.press('T')
                pyautogui.press('s')
                pyautogui.press('enter')
                pyautogui.click(进行变更[0] + (进行变更[2] - 进行变更[0]) / 2, 进行变更[1] + (进行变更[3] - 进行变更[1]) / 2)
            认证 = (1399, 854, 1561, 895)
            if findstr(认证) == "长按以完成认证":
                # 移动鼠标到指定位置
                pyautogui.moveTo(1481, 761)
                # 按下鼠标左键并保持
                pyautogui.mouseDown()
                time.sleep(5)
                pyautogui.mouseUp()
            角色 = (324, 485, 384, 523)
            if findstr((324, 485, 384, 523))=="角色":
                pyautogui.click(角色[0] + (角色[2] - 角色[0]) / 2, 角色[1] + (角色[3] - 角色[1]) / 2)

            if findstr((1622, 797, 1752, 843))=="选择升级":
                pyautogui.click(1688,998)
            if findstr((1599, 796, 1774, 841))=="提升角色等级":
                pyautogui.click(1688, 998)
            if findstr((873, 804, 1056, 847)) == "点击空白处关闭":
                pyautogui.click(1688, 998)
            if findstr((862, 1002, 1063, 1039)) == "点击空白区域继续":
                pyautogui.click(1688, 998)
            跃迁 = findstr((1234, 821, 1408, 873))
            if 跃迁 == "进行一次跃迁":
                pyautogui.click(1310, 987)
                pyautogui.press('esc')
            if findstr((850, 446, 1125, 493))=="选中右侧敌人作为攻击":
                pyautogui.click(1365, 500)
            old_res = new_res

            # 下面是寻路
            Fd = findstr(F的位置)
            if Fd != "" and Fd!="配控装置":
                isPause = True
                pyautogui.keyDown('f')
                sleep(0.01)
                pyautogui.keyUp('f')
                isPause = False

    def 自动寻路(self):
        print("自动寻路开始")
        while True:
            sleep(0.01)
            跳出当前任务循环 = False
            主任务 = findstr(主任务位置)
            子任务 = findstr(子任务位置)
            print(主任务, 子任务)
            print("panduan")
            path = "task\\" + 主任务 + "\\" + 子任务 + ".txt"
            if 主任务=="混乱行至深处" and 子任务=="协助银狼调查监控室内的终端":
                print("跳过")
                顺序执行(path)
                continue
            if 主任务 == "混乱行至深处" and 子任务 == "然而银狼似乎已经理解了一切":
                print("跳过")
                顺序执行(path)
                continue
            if 主任务 == "混乱行至深处" and 子任务 == "与奇物交互揭开监控室的秘密":
                print("跳过")
                顺序执行(path)
                continue
            if 主任务 == "阴影从未离去" and 子任务 == "找到离开备件库房的方法":
                print("跳过")
                顺序执行(path)
                continue
            print("panduan")
            if os.path.exists(path):
                print("文件存在")
                目标坐标数组路径 = path
                内存坐标x, 内存坐标y = 获取自身坐标()
                if 内存坐标x==0 and 内存坐标y==0:
                    continue
                print("自身坐标：",内存坐标x,内存坐标y)
                目标坐标数组1 = 获取坐标寻路数组(目标坐标数组路径, (内存坐标x, 内存坐标y))
                if len(目标坐标数组1) > 0:
                    print("目标坐标数组：", 目标坐标数组1[0])
                else:
                    continue
                目标坐标数组 = 目标坐标数组1[0]
                # 坐标数组长度 = len(目标坐标数组1)
                mask = template[:, :, 3]  # 提取透明度通道作为掩码
                self_pos_center_x, self_pos_center_y = self_pos_left + (
                        self_pos_right - self_pos_left) / 2, self_pos_up + (self_pos_bottom - self_pos_up) / 2
                # 裁剪坐标数组，只留下最近的和之后的，获取最近距离的数组下标，返回该下标之后（包括该下标）的值，也就是后半截数组
                # 如果离远离终点的点位近那还是舍弃吧
                print("执行数组")
                while True:
                    print("执行数组开始")
                    if len(目标坐标数组1) == 0:
                        break
                    img = screenshot(self_pos_center_x - 19, self_pos_center_y - 19, self_pos_center_x + 19,
                                     self_pos_center_y + 19)  # 截的自己箭头图片
                     # 其实就是目标坐标，懒得改了，就这样
                    距离 = math.sqrt((目标坐标数组[0] - 内存坐标x) ** 2 + (目标坐标数组[1] - 内存坐标y) ** 2)
                    result, _, 当前角度, _ = pyramid_template_matching(img, self.template, mask=mask)  # 获取箭头朝向角度，向上为0度
                    目标角度 = get_tangle_and_distance((内存坐标x, 内存坐标y), (目标坐标数组[0], 目标坐标数组[1]))

                    目标坐标数组1 = 获取坐标寻路数组(目标坐标数组路径, (内存坐标x, 内存坐标y))
                    目标坐标数组 = 目标坐标数组1[0]
                    fault = 2
                    print("当前坐标：", 内存坐标x, 内存坐标y, "目标坐标:", 目标坐标数组[0], 目标坐标数组[1])
                    setangle(当前角度, 目标角度, fault)

                    while 距离 > 0.1:
                        print("循环继续",当前角度, 目标角度)
                        if 距离 < 10:
                            print("慢速前行")
                            pyautogui.keyUp('w')
                            interval = 0.001
                        else:
                            pyautogui.keyUp('w')
                            print("急速飞奔")
                            interval = 0
                        if abs(当前角度 - 目标角度) > 2.0:
                            print("开始转角")
                            pyautogui.keyUp('w')
                            img = screenshot(self_pos_center_x - 19, self_pos_center_y - 19, self_pos_center_x + 19,
                                             self_pos_center_y + 19)  # 截的自己箭头图片
                            result, _, 当前角度, _ = pyramid_template_matching(img, self.template, mask=mask)  # 获取箭头朝向角度，向上为0度

                            setangle(当前角度, 目标角度, fault)
                            sleep(1)
                        # 计算自己与第0个坐标的角度
                        img = screenshot(self_pos_center_x - 19, self_pos_center_y - 19, self_pos_center_x + 19,self_pos_center_y + 19)  # 截的自己箭头图片
                        result, _, 当前角度, _ = pyramid_template_matching(img, self.template, mask=mask)  # 获取箭头朝向角度，向上为0度
                        内存坐标x, 内存坐标y = 获取自身坐标()
                        if 内存坐标x == 0 and 内存坐标y == 0:
                            continue
                        目标角度 = get_tangle_and_distance((内存坐标x, 内存坐标y), (目标坐标数组[0], 目标坐标数组[1]))
                        距离 = calculate_distance(目标坐标数组, (内存坐标x, 内存坐标y))
                        if 主任务 != findstr(主任务位置) or 子任务 != findstr(子任务位置):
                            跳出当前任务循环=True
                            break
                        目标坐标数组1 = 获取坐标寻路数组(目标坐标数组路径, (内存坐标x, 内存坐标y))
                        目标坐标数组 = 目标坐标数组1[0]
                        print("当前坐标：", 内存坐标x, 内存坐标y, "目标坐标:", 目标坐标数组[0], 目标坐标数组[1])
                        print(当前角度,目标角度)
                        if interval > 0:
                            sleep(interval)
                            pyautogui.press('w')
                            sleep(0.1)
                            pyautogui.keyDown("f")
                        else:
                            pyautogui.keyDown("w")
                            pyautogui.keyDown("f")


                    if len(目标坐标数组1)>1:
                        目标坐标数组1 = 目标坐标数组1[1:]
                        目标坐标数组 = 目标坐标数组1[0]
                    # 遍历数组，走完跳出
                    if 跳出当前任务循环:
                        break
                    pyautogui.keyUp('w')
                    pyautogui.keyDown("f")
                    pyautogui.keyUp('f')
            else:
                print(f"未找到路径文件:{path}")
                mouse_moveR(90)

    def 自动跳过教程(self):
        print("自动跳过教程开始")
        old_res = False
        new_res = False
        while True:
            sleep(0.01)
            new_res = False
            当前截图1 = screenshot(当前分辨率[0], 当前分辨率[1], 当前分辨率[2], 当前分辨率[3])

            if 当前截图1 is None:
                continue
            当前截图 = 预处理图片识别教程标记(当前截图1)
            # cv2.imshow("当前截图", 当前截图)
            # cv2.waitKey(0)
            results = self.model(当前截图)  # 对图像进行预测
            print(len(results))
            for r in results:
                boxes = r.boxes  # Boxes object for bbox outputs
                for box in boxes:
                    if r.names[int(np.array(box.cls.cpu())[0])] == "圆形" or \
                            r.names[int(np.array(box.cls.cpu())[0])] == "矩形":
                        print("发现教程标识")
                        临时 = np.array(box.xywh.cpu())[0]
                        pyautogui.keyDown('alt')  # 防止寻路时触发教程
                        sleep(0.5)
                        pyautogui.click(临时[0], 临时[1])
                        sleep(0.5)
                        pyautogui.keyUp('alt')
                        new_res = True
            if new_res != old_res:
                pyautogui.click(对话点击位置[0], 对话点击位置[1])  # 随便点一下
                sleep(0.1)
                pyautogui.click(对话点击位置[0], 对话点击位置[1])  # 随便再点一下
                pyautogui.press('esc')
                sleep(0.1)
                pyautogui.press('esc')
                sleep(0.1)
                pyautogui.press('esc')
                sleep(0.1)
            if findstr(详情位置) == "详情":
                pyautogui.press('c')
            old_res = new_res

    def 自动战斗和对话(self):
        global 当前角度,当前主任务,当前子任务
        print("自动战斗和对话")
        self_pos_center_x, self_pos_center_y = self_pos_left + (
                self_pos_right - self_pos_left) / 2, self_pos_up + (self_pos_bottom - self_pos_up) / 2
        while True:
            sleep(0.01)
            if findstr(当前位置) not in 区域数组:
                screen = ImageGrab.grab()
                # 使用getpixel获取指定坐标(x, y)的颜色
                color1 = screen.getpixel((106, 948))
                color2 = screen.getpixel((115, 941))
                color3 = screen.getpixel((116, 951))
                # 使用getpixel获取指定坐标(x, y)的颜色
                color4 = screen.getpixel((148, 60))
                color5 = screen.getpixel((148, 66))
                color6 = screen.getpixel((152, 66))
                # print(color1, color2, color3)
                # print(color1,color2,color3)
                #战斗
                if color1==(10, 8, 6) and color2==(10, 8, 6) and color3==(10, 8, 6):
                    isPause = True
                    print("识别到自动战斗")
                    #先按大招，再按技能，最后按普攻
                    pyautogui.press('1')

                    pyautogui.press('2')

                    pyautogui.press('3')

                    pyautogui.press('4')

                    pyautogui.press('e')
                    pyautogui.press('e')
                    pyautogui.press('e')
                    pyautogui.press('e')

                    pyautogui.press('q')
                    pyautogui.press('q')
                    pyautogui.press('q')
                    pyautogui.press('q')

                    pyautogui.press('space')
                    pyautogui.press('space')



                    isPause = False
                    sleep(0.01)
                # 判断该颜色是否为白色
                # 白色的RGB值是(255, 255, 255)，这里也可以根据需要调整容差
                #对话
                if color4 == (241, 213, 153) and color5 == (241, 213, 153)  and color6 == (241, 213, 153):
                    isPause = True
                    print("找到对话标识")
                    pyautogui.click(1699, 62)
                    pyautogui.click(对话点击位置[0], 对话点击位置[1])
                    pyautogui.click(对话点击位置[0], 对话点击位置[1])
                    pyautogui.press('space')
                    isPause = False
            else:

                img = screenshot(self_pos_center_x - 19, self_pos_center_y - 19, self_pos_center_x + 19,
                                 self_pos_center_y + 19)  # 截的自己箭头图片
                mask = template[:, :, 3]  # 提取透明度通道作为掩码
                result, _, 当前角度, _ = pyramid_template_matching(img, self.template, mask=mask)  # 获取箭头朝向角度，向上为0度
                当前主任务 = findstr(主任务位置)
                当前子任务 = findstr(子任务位置)




    def on_release(self, key: keyboard.KeyCode):
        """定义释放时候的响应"""

        if key == Key.home:
            pyautogui.keyUp("w")
            os._exit(0)

    def get_window_handle_at_mouse_position(self, ):
        # 获取鼠标当前位置的屏幕坐标
        x, y = pyautogui.position()

        # 获取该坐标处窗口的句柄
        hwnd = win32gui.WindowFromPoint((x, y))

def worker(target):
    ysam = StartRailAutoMap()
    method = getattr(ysam, target)
    method()

if __name__ == '__main__':
    from multiprocessing import Pool

    ysam = StartRailAutoMap()
    thread1 = threading.Thread(target=ysam.自动战斗和对话,args=(1,))
    thread2 = threading.Thread(target=ysam.自动寻路, args = (1,))
    thread1.start()
    thread2.start()
    targets = ['run']
    with Pool(1) as pool:
        pool.map(worker, targets)
    thread1.join()
    thread2.join()
    # ysam = StartRailAutoMap()
    # ysam.run()