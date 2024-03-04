# -*- coding: utf-8 -*-
import time
import cv2
import numpy as np
def bbbb(big_img,small_img,sim=0.7):


    old_time=time.time()
    g1=cv2.cvtColor(small_img,cv2.COLOR_BGR2GRAY)
    g2=cv2.cvtColor(big_img,cv2.COLOR_BGR2GRAY)

    sift=cv2.SIFT_create(nfeatures=0, nOctaveLayers=10)


    kp1,des1=sift.detectAndCompute(g1,None)
    kp2,des2=sift.detectAndCompute(g2,None)

    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)



    good_matches = []

    for (m,n) in matches:
        if m.distance < sim*n.distance:
            good_matches.append(m)
    print(good_matches)
    if len(good_matches) < 4:
        print("Not enough matching points")
        return None
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    #查找单应性矩阵

    H,mask=cv2.findHomography(src_pts,dst_pts,cv2.RANSAC,5.0)
    matches_mask = mask.ravel().tolist()
    h,w=small_img.shape[:2]

    pts=np.float32([[0,0],[0,h-1],[w-1,h-1],[w-1,0]]).reshape(-1,1,2)

    dst=cv2.perspectiveTransform(pts,H)

    pypts = []
    for npt in dst.astype(int).tolist():
        pypts.append(tuple(npt[0]))

    lt, br = pypts[0], pypts[2]
    middle_point = (lt[0] + br[0]) / 2, (lt[1] + br[1]) / 2  # 计算中心点

    print(dst,time.time()-old_time,middle_point,min(1.0 * matches_mask.count(1) / 10, 1.0))

    #画多边形
    cv2.polylines(big_img, [np.int32(dst)], True, (0, 255, 0),2)
    cv2.imshow("Matched Image", big_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def aaaa(big_img,small_img,sim=0.7):
    # 检查small_img的尺寸
    if small_img.shape[0] < 50 or small_img.shape[1] < 50:
        print("small_img的尺寸太小")
        return None

    g1 = cv2.cvtColor(small_img, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(big_img, cv2.COLOR_BGR2GRAY)

    # 检查g1的尺寸
    if g1.shape[0] <= 0 or g1.shape[1] <= 0:
        print("g1的尺寸小于等于0")
        return None

    orb = cv2.ORB_create(nfeatures=5000, scaleFactor=3.0, nlevels=8)
    kp2, des2 = orb.detectAndCompute(g2, None)
    kp1, des1 = orb.detectAndCompute(g1, None)

    index_params = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=2)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)

    good_matches = []

    for (m, n) in matches:
        if m.distance < sim * n.distance:
            good_matches.append(m)

    if len(good_matches) < 4:
        print("Not enough matching points")
        return None

    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    matches_mask = mask.ravel().tolist()
    h, w = small_img.shape[:2]

    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)

    dst = cv2.perspectiveTransform(pts, H)

    pypts = []
    for npt in dst.astype(int).tolist():
        pypts.append(tuple(npt[0]))

    lt, br = pypts[0], pypts[2]
    middle_point = (lt[0] + br[0]) / 2, (lt[1] + br[1]) / 2  # 计算中心点
    print(middle_point)
    cv2.polylines(big_img, [np.int32(dst)], True, (0, 255, 0), 2)
    cv2.imshow("Matched Image", big_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows
def findImg(big_img,small_img,sim=0.7,min_match_count= 4,threshold=0.7):
    '''
    图片查找_特征匹配_最佳位置
    :param big_img:
    :param small_img:
    :param sim:
    :param min_match_count:
    :param threshold:
    :return: {"result": 中心点, "rectangle": 矩阵信息, "confidence": 0.76,'dst_pot': array(线条信息) 方便 cv2.polylines使用}
    '''
    try:
        return findImgALL(big_img,small_img,sim,maxcnt=1,threshold=threshold,min_match_count=min_match_count)[0]
    except:
        return {}
def findImgALL(big_img, small_img,min_match_count=1, maxcnt=0):
    '''
    使用sift算法进行多个相同元素的查找
    Args:
        im_source(string): 图像、素材
        im_search(string): 需要查找的图片
        threshold: 阈值，当相识度小于该阈值的时候，就忽略掉
        maxcnt: 限制匹配的数量

    Returns:
        A tuple of found [(point, rectangle), ...]
        A tuple of found [{"result": point, "rectangle": rectangle, "confidence": 0.76}, ...]
        rectangle is a 4 points list
    '''
    #sift = cv2.SIFT_create(nfeatures=0, nOctaveLayers=20)
    #small_img = remove_background(small_img)
    # 增加nfeatures的值：通过增加nfeatures参数的值，可以提取更多的特征点。默认情况下，该值为
    # 0，表示提取所有的特征点。你可以逐渐增加这个值，看看是否能够得到更多细节丰富的特征点。
    # 调整edgeThreshold参数：该参数用于控制边缘阈值，即排除边缘特征点的数量。通过减小edgeThreshold的值，
    # 可以允许更多的边缘特征点被提取出来，从而增加特征的细节。
    # 调整sigma参数：sigma 参数用于控制高斯滤波器的标准差，从而影响特征点的尺度范围。较小的sigma值可以提取到更细微的特征，
    # 但也可能导致特征点w数量过多。你可以尝试增大或减小sigma的值，找到适合你任务的最佳取值。
    sift = cv2.SIFT_create(sigma=1.3)
    flann = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 5}, dict(checks=50))
    g1 = cv2.cvtColor(small_img, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(big_img, cv2.COLOR_BGR2GRAY)
    kp_sch, des_sch = sift.detectAndCompute(g1, None)
    if len(kp_sch) < min_match_count:
        return None
    kp_src, des_src = sift.detectAndCompute(g2, None)
    if len(kp_src) < min_match_count:
        return None

    result = []
    while True:
        # 匹配两个图片中的特征点，k=2表示每个特征点取2个最匹配的点
        matches = flann.knnMatch(des_sch, des_src, k=2)
        good = []

        for m, n in matches:
            # 剔除掉跟第二匹配太接近的特征点
            if m.distance < 0.75* n.distance:
                good.append(m)
        if len(good) < min_match_count:
            break
        #print(len(good))
        sch_pts = np.float32([kp_sch[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        img_pts = np.float32([kp_src[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        # M是转化矩阵
        M, mask = cv2.findHomography(sch_pts, img_pts, cv2.RANSAC, 5.0)
        matches_mask = mask.ravel().tolist()
        # 计算四个角矩阵变换后的坐标，也就是在大图中的坐标
        h, w = small_img.shape[:2]
        pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
        try:
            dst = cv2.perspectiveTransform(pts, M)
        except:
            break
        # trans numpy arrary to python list
        # [(a, b), (a1, b1), ...]
        pypts = []
        for npt in dst.astype(int).tolist():
            pypts.append(tuple(npt[0]))
        sim = min(1.0 * matches_mask.count(1) / 10, 1.0)

        X = (pypts[0][0] + pypts[1][0] +  pypts[2][0] +  pypts[3][0]) // 4
        Y = (pypts[0][1] + pypts[1][1] +  pypts[2][1] +  pypts[3][1]) // 4
        middle_point = (X, Y)#计算中心点
        result.append(dict(
            result=middle_point,
            rectangle=pypts,
            confidence=sim,
            dst_pot=[np.int32(dst)]
        ))
        if maxcnt and len(result) >= maxcnt:
            break
        # 符合的特征点存起来 用以后删除
        qindexes, tindexes = [], []
        for m in good:
            #将已经找到的先存起来 后面方便删除
            qindexes.append(m.queryIdx)
            tindexes.append(m.trainIdx)
        def filter_index(indexes, arr):
            r = []
            for i, item in enumerate(arr):
                if i not in indexes:
                    r .append(item)
            return np.array(r )
        #更新数组
        kp_src = filter_index(qindexes,kp_src)
        des_src = filter_index(tindexes,des_src)


    return result








if __name__ == '__main__':
    big_img = cv2.imdecode(np.fromfile(file=r"datas/max_map/蒙德1.png", dtype=np.uint8), cv2.IMREAD_COLOR)  # 加载大图

    small_img = cv2.imdecode(np.fromfile(file=r"datas/img/1704095733.5493054_8.png", dtype=np.uint8), cv2.IMREAD_COLOR)

    ret=findImgALL(big_img,small_img,threshold=0.7)
    #ret = ac.find_all_template(big_img, small_img, threshold=0.5, rgb=True, bgremove=True)
    #aaaa(big_img,small_img,sim=0.6)
    #图片查找_特征匹配_最佳(big_img,small_img)

    result=ret[0]
    for result in ret:
        print(result)
        pos = result['rectangle']
        confidence = result['confidence']
        cv2.polylines(big_img, result['dst_pot'], True, (0, 255, 0), 2)
        # 定义点的颜色和半径
        color = (0, 0, 255)  # 红色
        radius = 5

        # 绘制点
        cv2.circle(big_img, result["result"], radius, color, -1)

    # 显示匹配结果
    cv2.imshow('Matched Image', big_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
