'''2025-3-23
统一正常图片的名称，用来区别于其他图片

方式：
    增加normal-{num}-前缀
'''
unify_name = lambda num:f'normal-{num}-'

process_dir = r'D:\DesktopImages\TP-FUMO\TP-FUMO-easy-slice-unlabeled\part'

import os,re
from os.path import join as osj
from tqdm import tqdm

pattern = r'normal-\d*-'
for idx,name in tqdm(enumerate(os.listdir(process_dir))):
    if os.path.isdir( osj(process_dir,name) ):continue
    match_res = re.match(pattern,name)
    if match_res: dst_name = name.replace(match_res.group(),unify_name(idx))
    else:dst_name = unify_name(idx)+name
    ori_path = osj(process_dir,name)
    dst_path = osj(process_dir,dst_name)
    os.rename(ori_path,dst_path)