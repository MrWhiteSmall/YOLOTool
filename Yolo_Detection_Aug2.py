# this document aug image with horizontal, vertical and rotate 180;
''' 2025-3-15
输入1 图片文件夹（包含bmp/jpg/png和label）
输入2 保存文件夹
      最终保存为（yolo格式文件夹  images/train | val 、  labels/train | val）
      
2025-3-30
更改分配train val逻辑，每一张图及其增强应该在两边的数据中都有体现
'''

import os,math
from os.path import join as osj
import random
from tqdm import tqdm
import shutil
import cv2
from utils_aug2 import *

'''
预处理，先把原始数据都复制到 【目标文件夹】
1 在【目标文件夹】，根据已有数据做增强  => 增强文件的路径做成目录
2 合并增强文件 列表 和 原始文件 列表
3 按照比例shuffle后分成train val名单
4 在目标目录创建 文件夹 并move文件
'''
def start_process():
    # 输入1 图片文件夹（包含bmp/jpg/png和label）
    ori_img_dir = r"D:\DesktopImages\TP-FUMO\TP-FUMO-mixed-sifted"
    # 输入2 保存文件夹
    save_dir = r"D:\DesktopImages\TP-FUMO\All-FUMO-mixed-Aug"
    ####### 增强方法 目录 #############
    Aug_methods = ['vertical', 'horizontal', 'rotate180', 'anticlockwise90', 'clockwise']
    ###### 增强方法 选择 ############
    Aug_nums = [0, 1]
    ### train val 划分比例，此处必须为两个值 ##
    split_ratio=[1,1] # train 2/3数据量 val 1/3数据量
    
    # 若存咋该文件夹，删除原来的文件夹
    if os.path.exists(save_dir):shutil.rmtree(save_dir)
    # 屏蔽的类是多少（此处的屏蔽，后续操作为：
    #               在图片上将此label的区域【涂抹】成“黑色” 
    #               + 
    #               yolo的txt标签中【删除】这个label）
    mask_labels = [50]
    
    
    ''' !!!!!!!! 正式开始处理 !!!!!!!!!!! '''
    ''' !!!!!!!! 正式开始处理 !!!!!!!!!!! '''
    ''' !!!!!!!! 正式开始处理 !!!!!!!!!!! '''
    ## # 预处理，先把原始数据都复制到目标目录
    # 返回 list 包含 imgname.ext
    ori_file_list = copy_ori_to_target(ori_img_dir,save_dir)
    ## 1 在目标文件，根据已有数据做增强  => 增强文件的路径做成目录
    # 返回 list 包含 imgname.ext
    aug_file_list = augment_data(save_dir,Aug_methods, Aug_nums, mask_labels)
    ## 2 合并增强文件和原始文件
    ## 3-30修改 ： 保证每张图都训练过
    # all_file_list = merge_ori_aug(ori_file_list,aug_file_list)
    train_list = ori_file_list  # 3-30修改 ： 保证每张图都训练过
    ## 3 按照比例shuffle后分成train val名单
    train_list_aug,val_list = split_train_val_by_split_ratio(aug_file_list,split_ratio)
    train_list.extend(train_list_aug)
    ## 4 在目标目录创建 文件夹 并move文件
    move_to_yolo_dir_by_lists(save_dir,train_list,val_list)



# 预处理，先把原始数据都复制到目标目录
def copy_ori_to_target(ori_img_dir,save_dir):
    img_name_list = [os.path.splitext(n)[0] for n in os.listdir(ori_img_dir) 
                if n.split('.')[-1] in ('bmp','jpg','png')]
    txt_name_list = [os.path.splitext(n)[0] for n in os.listdir(ori_img_dir) 
                if n.split('.')[-1] in ('txt')]
    sifted_list = [n for n in img_name_list if n in txt_name_list]  # 求两个数组的交集，使
    os.makedirs(save_dir,exist_ok=True)
    img_list = [(osj(ori_img_dir,n),osj(save_dir,n)) 
                for n in os.listdir(ori_img_dir) 
                if n.split('.')[-1] in ('bmp','jpg','png') and \
                    os.path.splitext(n)[0] in sifted_list]
    txt_list = [(osj(ori_img_dir,n+'.txt'),osj(save_dir,n+'.txt')) 
                for n in sifted_list ]
    for ori_path,dst_path in img_list:shutil.copy2(ori_path,dst_path)
    for ori_path,dst_path in txt_list:shutil.copy2(ori_path,dst_path)
    return [os.path.basename(save_path) for _,save_path in img_list]
# 1 在目标文件，根据已有数据做增强  => 增强文件的路径做成目录
def augment_data(save_dir,Aug_methods, Aug_nums, mask_labels):
    returned_aug_img=[]
    # save_dir中的数据已经能够保证 图片-label 一一对应
    img_list = [n for n in os.listdir(save_dir) 
                if n.split('.')[-1] in ('bmp','jpg','png')]
    # 原数据先根据mask_labels处理一下
    print('开始增强数据')
    for n in tqdm(img_list):
        txt_path = osj(save_dir,os.path.splitext(n)[0]+'.txt')
        img_path = osj(save_dir,n)
        img = cv2.imread(img_path)
        img_mask = draw_txt_mask(img, txt_path, mask_labels)
        cv2.imwrite(img_path, img_mask)  # 保存被遮盖的图片 
        with open(txt_path ,'r') as f:
            data = f.readlines()
        # 去掉原label中包含mask_label的部分
        i=0
        for j in range(len(data)):
            if int(data[j].split()[0]) in mask_labels: # 取出第一个label 是否存在于mask_labels中
                continue
            data[i] = data[j]
            i+=1
        data = data[:i]
        with open(txt_path,'w') as f:
            f.write(''.join(data))
        ###### 至此 完成数据的预处理————将masked 的内容在图片上标黑且label中去掉这行内容 ####
        ## 开始增强   对原图增强后存入aug路径
        for aug_id in Aug_nums:
            aug_method = Aug_methods[aug_id]
            save_aug_img_path = osj(save_dir,os.path.splitext(n)[0]+f'{aug_method}'+'.jpg')
            aug_img(aug_method,img_path,save_aug_img_path)
            save_aug_txt_path = osj(save_dir,os.path.splitext(n)[0]+f'{aug_method}'+'.txt')
            aug_txt(aug_method,txt_path,save_aug_txt_path)
            
            # 将增强后的输入存入 返回列表
            returned_aug_img.append(os.path.basename(save_aug_img_path))
    return returned_aug_img
# 2 合并增强文件和原始文件
def merge_ori_aug(ori_file_list,aug_file_list):
    ori_file_list.extend(aug_file_list)
    # shuffle(ori_file_list)
    # 3-30 更改  
    # 1 sorted
    # 2 此时每张图的名称应该是 [A,A-hori,A-ver...]
    ori_file_list = sorted(ori_file_list)
    return ori_file_list
# 3 按照比例shuffle后分成train val名单
def split_train_val_by_split_ratio(file_list,split_ratio):
    if len(split_ratio)!=2:raise Exception('由于分成train val所以这里必须有两个值')
    # 此时传入的 file list 已经是shuffle过的，直接从中取出 split_ration 对应的数据
    # train_num = math.ceil(len(file_list)*(split_ratio[0]/sum(split_ratio)))
    train_num = math.ceil(3/2 * len(file_list)*(split_ratio[0]/sum(split_ratio))) - len(file_list)//2
    train_list = file_list[:train_num]
    val_list = file_list[train_num:]
    return train_list,val_list
# 4 在目标目录创建 文件夹 并move文件
def move_to_yolo_dir_by_lists(save_dir,train_list,val_list):
    ''' 
    save_dir
        images
            train
            val
        labels
            train
            val
    '''
    yolo_image_train_dir = osj(save_dir,'images','train')
    yolo_image_val_dir = osj(save_dir,'images','val')
    yolo_label_train_dir = osj(save_dir,'labels','train')
    yolo_label_val_dir = osj(save_dir,'labels','val')
    os.makedirs(yolo_image_train_dir)
    os.makedirs(yolo_image_val_dir)
    os.makedirs(yolo_label_train_dir)
    os.makedirs(yolo_label_val_dir)
    print('开始分割数据')
    for train_n in tqdm(train_list):
        shutil.move(osj(save_dir,train_n),yolo_image_train_dir)
        shutil.move(osj(save_dir,
                        os.path.splitext(train_n)[0]+'.txt'),yolo_label_train_dir)
    for val_n in tqdm(val_list):
        shutil.move(osj(save_dir,val_n),yolo_image_val_dir)
        shutil.move(osj(save_dir,
                        os.path.splitext(val_n)[0]+'.txt'),yolo_label_val_dir)


if __name__ == '__main__':
    start_process()