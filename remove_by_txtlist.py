'''2025-4-1
给定txt名单
给定处理dir

根据名单找dir中同名文件，然后删除
'''
from os.path import join as osj
from tqdm import tqdm
import os
txtlist_path = r'D:\DesktopImages\TP-FUMO\validate\ok2cls\record.txt'
process_dir = r'D:\DesktopImages\TP-FUMO\validate\images'

with open(txtlist_path,'r') as f:
    will_remove_list = f.readlines()
will_remove_list = [n.strip() for n in will_remove_list]
for n in tqdm(will_remove_list):
    if n in will_remove_list:
        os.remove(osj(process_dir,n))