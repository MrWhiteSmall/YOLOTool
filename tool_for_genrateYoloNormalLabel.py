'''
输入1 图片文件夹 （用于获得文件名称）
输入2 label文件夹
输出 空白label txt文件
'''
'''
输入1 图片文件夹（包含bmp和label）
输入2 保存文件夹
最终保存为（yolo格式文件夹  images/  labels/）
'''


input_dir = r'D:\DesktopImages\TP-FUMO\validate\val1\overkill'
save_dir = r'D:\DesktopImages\TP-FUMO\validate\val1\overkill'
import os
from tqdm import tqdm
imgs = os.listdir(input_dir)
from os.path import join as osj
for j in tqdm(imgs):
    lname = os.path.splitext(j)[0]+'.txt'
    save_path = osj(save_dir,lname)
    # 创建文件
    with open(save_path,'w') as f:
        pass
    # break