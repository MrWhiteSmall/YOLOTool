import json
import os
'''
  "imageHeight": 7000,
  "imageWidth": 4096
'''
def convert_json_to_yolo(json_path, output_path):
    # 打开并读取 JSON 文件
    with open(json_path, 'r',encoding='utf-8') as f:
        data = json.load(f)
    
    h,w = data['imageHeight'],data['imageWidth']
    # 初始化 YOLO 格式的标签内容
    yolo_content = []
    
    # 遍历每个形状（对象）
    for shape in data['shapes']:
        # 获取标签和坐标点
        label = int(shape['label'])
        points = shape['points']
        
        # 将所有坐标转换为字符串格式，并展开列表
        coordinates = [str(point[0]/w) for point in points] + [str(point[1]/h) for point in points]
        
        # 构建 YOLO 格式的一行内容
        yolo_line = f"{label} {' '.join(coordinates)}"
        # print(yolo_line)
        yolo_content.append(yolo_line)
    
    # 将所有内容写入输出文件
    with open(output_path, 'w') as f:
        f.write('\n'.join(yolo_content))

# 使用示例：
# 假设你的 JSON 文件路径是 "input.json"，输出 YOLO 格式的文件是 "output.txt"
input_dir = r'D:\BaiduNetdiskDownload\2025-1-24-芜湖长信TP（重新分类 用于标注）\复检标注图片'
save_dir = r'D:\BaiduNetdiskDownload\2025-1-24-芜湖长信TP（重新分类 用于标注）\复检标注图片'

jsons = os.listdir(input_dir)
from os.path import join as osj
for j in jsons:
    if not j.endswith('.json'):continue
    json_path = osj(input_dir,j)
    lname = os.path.splitext(j)[0]+'.txt'
    save_path = osj(save_dir,lname)
    convert_json_to_yolo(json_path, save_path)
    # break