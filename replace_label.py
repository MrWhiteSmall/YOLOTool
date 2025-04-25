'''
2025-3-12
现场标注label与实际不一致
根本原因：
    现场关注 缺陷 label 为 7,8...
    labelimg关注 缺陷 下标 为 0,1...
需要将现场 标注文件中的  label 进行替换
比如 现场认为缺陷是 8 并且标注，但是标注文件中 写入的是 0，因为在classes.txt 文件中 下标0的位置对应了 8 这个名称！

1, 读取现场 的 classes.txt 文件 获取 dict = {下标: 名称}
2, 读取 label 文件，替换其中的 下标 为 名称  classid = dict[classid]
3, 替换现场的 classes.txt 为 模型可用的classes.txt

2025-3-30
处理bug
>> readlines 后每个line都自带一个\n 不用 '\n'.join(...)
'''
import os
from os.path import join as osj

process_dir  = r'D:\DesktopDocument\WXWork\1688858163660841\Cache\File\2025-03\156F03撕膜\BMP-Down2'
xianchang_classes = osj(process_dir,'classes.txt')
target_classes =  r'D:\DesktopImages\classes.txt'
label_dir = process_dir


label_paths = [osj(label_dir,n) for n in os.listdir(label_dir) 
               if n.split('.')[-1]=='txt' and n.split('.')[0]!='classes']

# 1, 读取现场 的 classes.txt 文件 获取 dict = {下标: 名称}
dic = {}
with open(xianchang_classes,'r') as f:
    data = f.readlines()
    for k,v in enumerate(data):
        dic[str(k)] = v.split('\n')[0]
    
# 2. 读取 label 文件，替换其中的 下标 为 名称  classid = dict[classid]
for label_path in label_paths:
    with open(label_path,'r') as f:
        data = f.readlines()
    for i in range(len(data)):
        d_split = data[i].split()
        if d_split[0] not in dic:continue
        d_split[0] = dic[d_split[0]]
        data[i] = ' '.join(d_split)
    # print(data)
    with open(label_path,'w') as f:
        f.write( ''.join(data) )

# 3, 替换现场的 classes.txt 为 模型可用的classes.txt
import shutil
shutil.copy2(target_classes,xianchang_classes)