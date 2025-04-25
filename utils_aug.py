import os
from PIL import Image, ImageDraw
import numpy as np
from tqdm import tqdm
import json
import shutil
import re
import cv2


# 从输入字符串中提取数字，并将它们转换为浮点数并四舍五入到小数点后六位，最后返回处理后的数字列表。
def find_number(str_):
    number = re.findall(r"\d+\.?\d*", str_)
    for i in range(len(number)):
        number[i] = round(float(number[i]), 6)
    return number

# Vertical_flip_bbox
def Vertical_flip_bbox(bbox):
    new_bbox = []
    new_bbox.append(int(bbox[0]))
    o_x, o_y, o_w, o_h = bbox[1], bbox[2], bbox[3], bbox[4]
    new_x = o_x
    new_y = 1 - o_y
    new_bbox.append(new_x)
    new_bbox.append(new_y)
    new_bbox.append(o_w)
    new_bbox.append(o_h)
    return new_bbox


def Horizontal_flip_bbox(bbox):
    new_bbox = []
    new_bbox.append(int(bbox[0]))
    o_x, o_y, o_w, o_h = bbox[1], bbox[2], bbox[3], bbox[4]
    new_x = 1 - o_x
    new_y = o_y
    new_bbox.append(new_x)
    new_bbox.append(new_y)
    new_bbox.append(o_w)
    new_bbox.append(o_h)
    return new_bbox


def rotation180_bbox(bbox):
    new_bbox = []
    new_bbox.append(int(bbox[0]))
    o_x, o_y, o_w, o_h = bbox[1], bbox[2], bbox[3], bbox[4]
    new_x = 1 - o_x
    new_y = 1 - o_y
    new_bbox.append(new_x)
    new_bbox.append(new_y)
    new_bbox.append(o_w)
    new_bbox.append(o_h)
    return new_bbox


# 逆时针
def rotate90_bbox(bbox):
    new_bbox = []
    new_bbox.append(int(bbox[0]))
    o_x, o_y, o_w, o_h = bbox[1], bbox[2], bbox[3], bbox[4]
    new_x = o_y
    new_y = 1 - (o_x)
    new_bbox.append(new_x)
    new_bbox.append(new_y)
    new_bbox.append(o_h)
    new_bbox.append(o_w)
    return new_bbox


# 顺时针
def rotate270_bbox(bbox):
    new_bbox = []
    new_bbox.append(int(bbox[0]))
    o_x, o_y, o_w, o_h = bbox[1], bbox[2], bbox[3], bbox[4]
    new_x = 1 - o_y
    new_y = (o_x)
    new_bbox.append(new_x)
    new_bbox.append(new_y)
    new_bbox.append(o_h)
    new_bbox.append(o_w)
    return new_bbox

# Draw block are with special label
def draw_txt_mask(img, txt_path, mask_labels):
    image_size = img.shape
    height, width = image_size[:2]

    file_handle = open(txt_path)
    cnt_info = file_handle.readlines()
    new_cnt_info = [line_str.replace("\n", "").split(" ") for line_str in cnt_info]

    for new_info in new_cnt_info:
        temp_label = int(new_info[0])
        if temp_label in mask_labels:
            s = []  # 如果需要遮盖，创建一个空列表
            for i in range(1, len(new_info), 2):
                b = []
                for tmp in new_info[i:i + 2]:
                    if tmp != '':
                        b.append(float(tmp))  # x,y/w,h
                if b != []:
                    s.append(b[0])
                    s.append(b[1])
            s = np.array(s)
            x1 = int((float(s[0]) - float(s[2]) / 2) * width)  # x_center - width/2 将归一化之后的数据变回原来的大小
            y1 = int((float(s[1]) - float(s[3]) / 2) * height)  # y_center - height/2
            x2 = int((float(s[0]) + float(s[2]) / 2) * width)  # x_center + width/2
            y2 = int((float(s[1]) + float(s[3]) / 2) * height)  # y_center + height/2
            cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 0, 0), thickness=-1)  # BGR
    return img


def merger_select_label(ori, txt_file, b_lables):
    ori_file_handle = open(ori)

    cnt_info = ori_file_handle.readlines()
    new_cnt_info = [line_str.replace("\n", "").split(" ") for line_str in cnt_info]
    new_infos = []
    for info in new_cnt_info:
        if int(info[0]) in b_lables:
            continue
        new_info = []
        for i in range(len(info)):
            new_info.append(info[i])
        new_infos.append(new_info)
    with open(txt_file, 'a', encoding='utf-8') as new_file_obj:
        for k in range(len(new_infos)):
            for k_k in range(len(new_infos[k])):
                new_file_obj.write('{} '.format(new_infos[k][k_k]))
            new_file_obj.write('\n')
    print('write file {} to file {} merge complete!'.format(ori, txt_file))

