'''

处理逻辑：
    1. 遍历图片和标注，获得 每张图片 对应的  类型
    2. 对类型 数量 从高到低 排序
    3. 遍历此时的图片  check [其对应的类型是否已经满足satisfy 所需数量]
                        if True  则 跳过这张图片
                        else  将此图Add，且Update当前类型  数量
'''

import os,shutil
from tqdm import tqdm
from os.path import exists as is_path_exists
from os.path import join as  osj

data_dir = r'D:\DesktopImages\TP-FUMO\TP-FUMO-mixed'
dst_dir =  r'D:\DesktopImages\TP-FUMO\TP-FUMO-mixed-sifted'
satisfication = {
    0:0,
    1:0,
    2:80,
    3:0,
    4:0,
    5:0,
    6:0,
    7:80,
    8:80,
    9:0,
    10:0,
    11:0,
    12:0,
    13:0,
    14:0,
}


if is_path_exists(dst_dir):shutil.rmtree(dst_dir)
os.makedirs(dst_dir)
static_dict = {}
### 1. 遍历图片和标注，获得 每张图片 对应的  类型
for name in tqdm(os.listdir(data_dir)):
    if os.path.splitext(name)[-1] in ('.jpg','.png','.bmp'):
        img_file = osj(data_dir,name)
        txt_file = osj(data_dir,os.path.splitext(name)[0]+'.txt')
        if not is_path_exists(txt_file):continue
        
        # 获得 每张图片 对应的  类型 
        with open(txt_file,'r') as f:
            types = set( [int( d.split()[0] ) for d in f.readlines()] )
        static_dict[(img_file,txt_file)]=types

### 2. 对类型 数量 从高到低 排序
static_dict = dict(sorted(static_dict.items(),key=lambda x: -len(x[1])))  # 对 len(value) 进行排序

# 当 满足条件时，satistication 中的value  都  <= 0
def check_satisfy_by_data_type(data_type,satisfication):
    for dt in data_type:
        if satisfication[dt] > 0 : return False  # 只要有一个类型 数量上还没有满足，就返回False
    return True
### 3. 遍历此时的图片  check [其对应的类型是否已经满足satisfy 所需数量]
for k,v in tqdm(static_dict.items()):
    ### if True  则 跳过这张图片
    if check_satisfy_by_data_type(v, satisfication): continue
    ### else  将此图Add，且Update当前类型  数量
            # 将此图Add
    img_file,txt_file = k
    shutil.copy2(img_file,dst_dir)
    shutil.copy2(txt_file,dst_dir)
                        # Update当前类型  数量   
    for data_type in v: # type(v) = set()
        satisfication[data_type]-=1  # 遍历每一个类型  减去1 说明 图片将被加入
