from pycocotools.coco import COCO
import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv
from os.path import join as osj
 
img_dir = r'D:\DesktopImages\mvCOCO-Det-TP-Aug\images'
coco_json = r'D:\DesktopImages\mvCOCO-Det-TP-Aug\annotations\train.json'

# 加载COCO格式的标注文件
coco=COCO(coco_json)

imgIds = coco.getImgIds() # 获取所有的image id，可以选择参数 coco.getImgIds(imgIds=[], catIds=[])
# imgIds = coco.getImgIds(imgIds=[0, 1, 2]) # 获得image id 为 0，1，2的图像的id
# imgIds = coco.getImgIds(catIds=[0, 1, 2]) # 获得包含类别 id 为0，1，2的图像
 
annIds = coco.getAnnIds(catIds=[0, 1, 2]) # 获得类别id为0，1，2的标签
annIds = coco.getAnnIds(imgIds=imgIds[0]) # 获得和image id对应的标签
 
catIds = coco.getCatIds(catNms=['0']) # 通过类别名筛选
catIds = coco.getCatIds(catIds=[0, 1, 2]) # 通过id筛选
catIds = coco.getCatIds(supNms=[]) # 通过父类的名筛选


print('类别信息')
cats_name = coco.loadCats(ids=catIds)
print(cats_name)
 
print('\n标签信息:')
anns = coco.loadAnns(annIds)
bboxes = np.array([i['bbox'] for i in anns]).astype(np.int32)
cats = np.array([i['category_id'] for i in anns])
print(anns)
print('\n从标签中提取的Bounding box:')
print(bboxes)
 
print('图像')
imgIdx = imgIds[0]
img = coco.loadImgs([imgIdx]) # 读取图片信息
img = cv.imread( osj(img_dir , img[0]['file_name']) )
# 绘制bounding box
for i in range(len(bboxes)):
    p1 = bboxes[i][0:2]
    p2 = bboxes[i][0:2] + bboxes[i][2:4]
    
    cv.rectangle(img, (p1[0], p1[1]), (p2[0], p2[1]), (255, 0, 0))
plt.figure(figsize=(8, 8))
plt.imshow(img)
cv.imwrite('./res.jpg',img)
plt.show()