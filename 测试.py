import numpy as np
from ultralytics import YOLO
from function import screenshot


if __name__ == '__main__':
    model = YOLO("best.pt")
    results = model("")  # 对图像进行预测
    print(len(results))
    for r in results:
        boxes = r.boxes  # Boxes object for bbox outputs
        for box in boxes:
            print("坐标:", np.array(box.xyxy.cpu())[0], "类别序号:", int(np.array(box.cls.cpu())[0]), "类别:",
                  r.names[int(np.array(box.cls.cpu())[0])])

    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        result.show()  # display to screen
        result.save(filename='result.jpg')  # save to disk