'''2025-4-1
统一正常图片的名称，用来区别于其他图片
用于增加时间前缀
如果有时间前缀，先删掉这个前缀

方式：
    增加 {time}-name  格式为YYYYMMDD_HHMMSS
'''
process_dir = r'D:\DesktopImages\TP-FUMO\validate\val1\overkill'

import os,re
from os.path import join as osj
from tqdm import tqdm
from datetime import datetime

# 获取当前时间并格式化
time_format = r'%Y%m%d_%H%M%S'
current_time = datetime.now().strftime(time_format)

pattern = r'^\d{8}_\d{6}'
for idx,name in tqdm(enumerate(os.listdir(process_dir))):
    if os.path.isdir( osj(process_dir,name) ):continue
    match_res = re.match(pattern,name)
    if match_res: dst_name =  f'{current_time}_'+name[match_res.end():]
    else:dst_name = f'{current_time}_'+name
    ori_path = osj(process_dir,name)
    dst_path = osj(process_dir,dst_name)
    os.rename(ori_path,dst_path)