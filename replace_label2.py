'''
2025-3-30
快速替换标注
输入1 {'ori_label':'target_label'...}
输入2 处理的label文件夹
读取文件中的 label 进行替换（原地）

处理bug
>> readlines 后每个line都自带一个\n 不用 '\n'.join(...)
'''
import os
from os.path import join as osj
from tqdm import tqdm

# 输入1 {'ori_label':'target_label'...}
replace_dict={
    '9':'7',
    '10':'8',
}
# 输入2 处理的label文件夹
process_dir  = r'D:\DesktopImages\TP-FUMO\TP-FUMO-mixed'

label_paths = [osj(process_dir,n) for n in os.listdir(process_dir) 
               if n.split('.')[-1]=='txt' and n.split('.')[0]!='classes']
    
#  读取 label 文件，替换其中的 下标 为 名称  classid = dict[classid]
for label_path in tqdm(label_paths):
    with open(label_path,'r') as f:
        data = f.readlines()
        data = [d for d in data if d != "\n"]
    for i in range(len(data)):
        d_split = data[i].split()
        if d_split[0] not in replace_dict:continue
        d_split[0] = replace_dict[d_split[0]]
        data[i] = ' '.join(d_split)
    # print(data)
    with open(label_path,'w') as f:
        f.write( ''.join(data) )
