'''
2025-2-14
数据增强
输入 文件夹（jpg or png）
输出 文件夹
1，flip 图片 上下，左右翻转
2，translate 图片 50像素
'''
from PIL import Image, ImageOps,ImageChops
import os
import json

def get_annotation_path(image_path,json_dir, annotation_suffix=''):
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    annotation_name = f"{base_name}{annotation_suffix}.json"
    return os.path.join(json_dir, annotation_name)
def load_annotation(annotation_path):
    with open(annotation_path, 'r') as f:
        return json.load(f)
def flip_l2r_annotation(annotation, image_width):
    shapes = annotation['shapes']
    for i in range(len(shapes)):
        shape = shapes[i]
        new_points = []
        for (x, y) in shape['points']:
            new_x = image_width - x
            new_y = y
            new_points.append([new_x, new_y])
        annotation['shapes'][i]['points'] = new_points
    return annotation
def flip_t2b_annotation(annotation, image_height):
    shapes = annotation['shapes']
    for i in range(len(shapes)):
        shape = shapes[i]
        new_points = []
        for (x, y) in shape['points']:
            new_x = x
            new_y = image_height - y
            new_points.append([new_x, new_y])
        annotation['shapes'][i]['points'] = new_points
    return annotation
def translate_annotation(annotation, dx, dy):
    # dx = 50  # 水平偏移量
    # dy = 30  # 垂直偏移量

    shapes = annotation['shapes']
    for i in range(len(shapes)):
        shape = shapes[i]
        new_points = []
        for (x, y) in shape['points']:
            new_x = x + dx
            new_y = y + dy
            new_points.append([new_x, new_y])
        annotation['shapes'][i]['points'] = new_points
    return annotation
def save_annotation(annotation, annotation_path):
    with open(annotation_path, 'w') as f:
        json.dump(annotation, f, indent=2)
def clip_annotation(annotation, image_width, image_height):
    for obj in annotation['objects']:
        x1 = max(0, min(obj['bbox'][0], image_width))
        y1 = max(0, min(obj['bbox'][1], image_height))
        width = max(0, min(obj['bbox'][2], image_width - x1))
        height = max(0, min(obj['bbox'][3], image_height - y1))
        obj['bbox'] = [x1, y1, width, height]

def flip(imgpath,json_dir, savedir):
    # 打开图片
    img = Image.open(imgpath)
    
    # 获取文件名和扩展名
    basename = os.path.basename(imgpath)
    name, ext = os.path.splitext(basename)
    end = ''
    
     # 处理标注文件
    annotation_path = get_annotation_path(imgpath,json_dir)
    
    image_width, image_height = img.size
    
    annotation = load_annotation(annotation_path)
    annotation = flip_l2r_annotation(annotation, image_width)
    annotation_output_path = os.path.join(savedir, f"{name}_flipl2r{end}.json")
    save_annotation(annotation, annotation_output_path)
    
    
    annotation = load_annotation(annotation_path)
    annotation = flip_t2b_annotation(annotation, image_height)
    annotation_output_path = os.path.join(savedir, f"{name}_flipt2b{end}.json")
    save_annotation(annotation, annotation_output_path)
    
def translate(imgpath,json_dir, savedir, translate_distance):
    # img = Image.open(imgpath)
    # width, height = img.size
    
    directions = {
        'right': (translate_distance, 0),
        'left': (-translate_distance, 0),
        'down': (0, translate_distance),
        'up': (0, -translate_distance)
    }
    # 处理标注文件
    annotation_path = get_annotation_path(imgpath,json_dir)
    
    
    for direction, (dx, dy) in directions.items():
        annotation = load_annotation(annotation_path)
        annotation = translate_annotation(annotation,dx,dy)
        basename = os.path.basename(imgpath)
        name, ext = os.path.splitext(basename)
        end = ''
        annotation_output_path = os.path.join(savedir, f"{name}_translate_{direction}{end}.json")
        save_annotation(annotation, annotation_output_path)
        

import argparse
from os.path import join as osj
from tqdm import tqdm
if __name__=='__main__':
    # parser = argparse.ArgumentParser(description='图像处理工具')
    # subparsers = parser.add_subparsers(title='可用命令', dest='command')
    
    # # 添加翻转命令
    # flip_parser = subparsers.add_parser('flip', help='翻转图片')
    # flip_parser.add_argument('--input_dir', required=True, help='输入图片路径')
    # flip_parser.add_argument('--savedir', required=True, help='保存目录')
    
    # # 添加平移命令
    # translate_parser = subparsers.add_parser('translate', help='平移图片')
    # translate_parser.add_argument('--input_dir', required=True, help='输入图片路径')
    # translate_parser.add_argument('--savedir', required=True, help='保存目录')
    # translate_parser.add_argument('--distance', type=int, default=10, help='平移距离，默认为10像素')
    
    # args = parser.parse_args()
    
    # input_dir = args.input_dir
    # save_dir = args.savedir
    
    # imgnames = os.listdir(input_dir)

    # for imgname in tqdm(imgnames):
    #     imgpath = osj(input_dir,imgname)
    #     if args.command == 'flip':
    #         flip(imgpath, save_dir)
    #     elif args.command == 'translate':
    #         translate(imgpath, save_dir, args.distance)

        
    input_dir = 'D:\\DesktopImages\\mvTP\\Abnormal'
    json_dir = 'D:\\DesktopImages\\mvTP\\Json'
    save_dir = 'D:\\DesktopImages\\mvTP\\Json-translate'
    
    imgnames = os.listdir(input_dir)
    distance = 50

    for imgname in tqdm(imgnames):
        imgpath = osj(input_dir,imgname)
        # if args.command == 'flip':
        # flip(imgpath,json_dir, save_dir)
        # elif args.command == 'translate':
        translate(imgpath,json_dir, save_dir, distance)
        # if input()=='n':break
