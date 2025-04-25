import cv2
from PIL import Image, ImageDraw
import json
import os
import numpy as np

def process_annotation(json_path, image_path):
    # 加载 JSON 标注文件
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 读取原始图片（BMP格式）
    img = Image.open(image_path)
    width, height = img.size
    
    # 创建掩码图（mask），初始化为全黑
    mask = Image.new('L', (width, height), 0)  # 'L' 表示8位灰度图
    draw = ImageDraw.Draw(mask)
    # 遍历所有的标注对象
    for shape in data['shapes']:
        # label = shape['label']
        points = shape['points']
        
        polygon = [tuple(point) for point in points]
        draw.polygon(polygon, fill=255)
    
    # 将掩码图转换为 OpenCV 格式并保存为 PNG
    # mask_cv = cv2.cvtColor(np.array(mask), cv2.COLOR_GRAY2BGR)
    mask_path = os.path.splitext(image_path)[0] + '_mask.png'
    # cv2.imwrite(mask_path, np.array(mask))
    mask.save(mask_path)
    
    # 将原始图片从 BMP 转换为 JPG 并保存
    jpg_path = os.path.splitext(image_path)[0] + '.jpg'
    img.save(jpg_path, 'JPEG', quality=100)
    
    print(f"Saved mask to {mask_path}")
    print(f"Saved JPG to {jpg_path}")
    
def process_folder(json_dir, image_dir):
    # 遍历所有 JSON 文件
    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            json_path = os.path.join(json_dir, filename)
            image_name = os.path.splitext(filename)[0] + '.bmp'
            image_path = os.path.join(image_dir, image_name)
            
            # 检查图片是否存在
            if not os.path.exists(image_path):
                print(f"Image {image_name} not found!")
                continue
            
            process_annotation(json_path, image_path)
            # break

# 示例调用
json_folder = f"D:\BaiduNetdiskDownload\\2025-1-24-芜湖长信TP\复检标注图片\\20250120"
image_folder = f"D:\BaiduNetdiskDownload\\2025-1-24-芜湖长信TP\复检标注图片\\20250120"

process_folder(json_folder, image_folder)