import xml.etree.ElementTree as ET

def convert_xml_to_yolo(xml_path, output_txt_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 获取图片的宽高
    width = int(root.find(".//size/width").text)
    height = int(root.find(".//size/height").text)

    # 打开输出的TXT文件
    with open(output_txt_path, 'w') as f:
        # 遍历所有object标签
        for obj in root.findall(".//object"):
            # 获取标签名称（类别）
            class_name = obj.find("name").text
            # 这里假设类别2是索引1，类别3是索引2，按需修改
            class_idx = int(class_name)   # 如果类别是数字，直接减1作为类别索引

            # 获取bounding box坐标
            xmin = int(obj.find(".//bndbox/xmin").text)
            ymin = int(obj.find(".//bndbox/ymin").text)
            xmax = int(obj.find(".//bndbox/xmax").text)
            ymax = int(obj.find(".//bndbox/ymax").text)

            # 计算 YOLO 格式坐标
            x_center = (xmin + xmax) / 2 / width
            y_center = (ymin + ymax) / 2 / height
            bbox_width = (xmax - xmin) / width
            bbox_height = (ymax - ymin) / height

            # 写入文件（YOLO 格式）
            f.write(f"{class_idx} {x_center} {y_center} {bbox_width} {bbox_height}\n")

# 示例：将xml文件转换为yolo格式txt
# xml_file = 'your_file.xml'  # 替换为你的XML文件路径
# txt_file = 'output.txt'     # 替换为你希望保存的txt路径

# convert_xml_to_yolo(xml_file, txt_file)


input_dir = r'D:\DesktopDocument\WXWork\1688858163660841\Cache\File\2025-03\2025-03-17  156F03\BMP-Down2'
save_dir = r'D:\DesktopDocument\WXWork\1688858163660841\Cache\File\2025-03\2025-03-17  156F03\BMP-Down2'
import os
from tqdm import tqdm
xmls = os.listdir(input_dir)
from os.path import join as osj
for j in tqdm(xmls):
    if not j.endswith('.xml'):continue
    xml_path = osj(input_dir,j)
    lname = os.path.splitext(j)[0]+'.txt'
    save_path = osj(save_dir,lname)
    convert_xml_to_yolo(xml_path, save_path)
    # break