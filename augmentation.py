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

def flip(imgpath, savedir):
    # 打开图片
    img = Image.open(imgpath)
    
    # 左右翻转
    flipped_left_right = img.transpose(Image.FLIP_LEFT_RIGHT)
    
    # 上下翻转
    flipped_top_bottom = img.transpose(Image.FLIP_TOP_BOTTOM)
    
    # 获取文件名和扩展名
    basename = os.path.basename(imgpath)
    name, ext = os.path.splitext(basename)
    end = ''
    if name.endswith('_mask'):
        name = name[:-len('_mask')]
        end = '_mask'
    
    # 保存左右翻转后的图片
    save_path_lr = os.path.join(savedir, f"{name}_flipl2r{end}{ext}")
    flipped_left_right.save(save_path_lr)
    
    # 保存上下翻转后的图片
    save_path_tb = os.path.join(savedir, f"{name}_flipt2b{end}{ext}")
    flipped_top_bottom.save(save_path_tb)

import numpy as np
#平移
import cv2
def translateImg(imgpath, x, y):
    image = cv2.imread(imgpath)
    M = np.float32([[1, 0, x], [0, 1, y]])
    shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    return Image.fromarray(shifted)
def translate(imgpath, savedir, translate_distance):
    img = Image.open(imgpath)
    
    directions = {
        'right': (translate_distance, 0),
        'left': (-translate_distance, 0),
        'down': (0, translate_distance),
        'up': (0, -translate_distance)
    }
    
    for direction, (dx, dy) in directions.items():
        offset_img = translateImg(imgpath, dx, dy)
        # print(offset_img.size)
        
        # 构建文件名
        basename = os.path.basename(imgpath)
        name, ext = os.path.splitext(basename)
        end = ''
        if name.endswith('_mask'):
            name = name[:-len('_mask')]
            end = '_mask'
        save_path = os.path.join(savedir, f"{name}_translate_{direction}{end}{ext}")
        offset_img.save(save_path)


import argparse
from os.path import join as osj
from tqdm import tqdm
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='图像处理工具')
    subparsers = parser.add_subparsers(title='可用命令', dest='command')
    
    # 添加翻转命令
    flip_parser = subparsers.add_parser('flip', help='翻转图片')
    flip_parser.add_argument('--input_dir', required=True, help='输入图片路径')
    flip_parser.add_argument('--savedir', required=True, help='保存目录')
    
    # 添加平移命令
    translate_parser = subparsers.add_parser('translate', help='平移图片')
    translate_parser.add_argument('--input_dir', required=True, help='输入图片路径')
    translate_parser.add_argument('--savedir', required=True, help='保存目录')
    translate_parser.add_argument('--distance', type=int, default=10, help='平移距离，默认为10像素')
    
    args = parser.parse_args()
    
    input_dir = args.input_dir
    save_dir = args.savedir
    
    imgnames = os.listdir(input_dir)

    for imgname in tqdm(imgnames):
        imgpath = osj(input_dir,imgname)
        if args.command == 'flip':
            flip(imgpath, save_dir)
        elif args.command == 'translate':
            translate(imgpath, save_dir, args.distance)
        # break

        
