import matplotlib.pyplot as plt
import json
def get_annotation_path(image_path,json_dir, annotation_suffix=''):
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    annotation_name = f"{base_name}{annotation_suffix}.json"
    return os.path.join(json_dir, annotation_name)
def load_annotation(annotation_path):
    with open(annotation_path, 'r') as f:
        return json.load(f)
def show(imgpath,json_path):
    # 读取并显示图像
    img = plt.imread(imgpath)
    plt.imshow(img)

    data = load_annotation(json_path)
    # 绘制标注点
    for shape in data['shapes']:
        points = shape['points']
        x_coords = [point[0] for point in points]
        y_coords = [point[1] for point in points]
        plt.plot(x_coords, y_coords, 'r-', linewidth=2)

    plt.axis('off')
    plt.show()
    
imgdir= 'D:\\DesktopImages\\mvTP\\Abnormal-translate'
jsondir = 'D:\\DesktopImages\\mvTP\\Json-translate'
import os
imgs = os.listdir(imgdir)
from os.path import join as osj
for img in imgs:
    imgpath = osj(imgdir,img)
    jsonpath = get_annotation_path(imgpath,jsondir)
    show(imgpath,jsonpath)
    # break
    