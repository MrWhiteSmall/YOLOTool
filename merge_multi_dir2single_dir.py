# coding=utf-8
'''2025-3-19
合并多个标注文件夹到一个文件夹
确保 合并的文件中即包含 图片 又包含 标注
'''
import os,shutil
from tqdm import tqdm
from os.path import exists as is_path_exists
from os.path import join as  osj
multi_dirs = [
    r'D:\DesktopDocument\WXWork\1688858163660841\Cache\File\2025-03\SIMO-Light-132C06(XIFEN)',
    r'D:\DesktopDocument\WXWork\1688858163660841\Cache\File\2025-03\SIMO-Light-156F03(XIFEN)',
]
single_dir = r'D:\DesktopDocument\WXWork\1688858163660841\Cache\File\2025-03\All-SIMO-Light(XIFEN)'
if is_path_exists(single_dir):shutil.rmtree(single_dir)
os.makedirs(single_dir)

for md in tqdm(multi_dirs):
    if not is_path_exists(md):
        print(f'{md}不存在')
        continue
    for name in tqdm(os.listdir(md)):
        if os.path.splitext(name)[-1] in ('.jpg','.bmp','.png'):
            img_path = osj(md,name)
            txt_path = osj(md,os.path.splitext(name)[0]+'.txt')
            if is_path_exists(txt_path):
                shutil.copy2(img_path,single_dir)                
                shutil.copy2(txt_path,single_dir)                
