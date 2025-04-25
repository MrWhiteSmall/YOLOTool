'''2025-3-22
对图片和txt相互校验
取出两者的交集，其他名称 都删除
'''
data_dir=r'D:\DesktopImages\数据集汇总\圆形薄片'
import os
from os.path import join
from tqdm import tqdm
names = os.listdir(data_dir)
imgnames = [n for n in names if os.path.splitext(n)[-1] in ('.png','.jpg','.jpeg','.bmp')]
txtnames = [os.path.splitext(n)[0] for n in names    if os.path.splitext(n)[-1] in ('.txt')]
sifted =   [os.path.splitext(n)[0] for n in imgnames if os.path.splitext(n)[0]  in txtnames]
will_rm_imgnames = [n for n in imgnames if os.path.splitext(n)[0] not in sifted]
will_rm_txtnames = [n+'.txt' for n in txtnames if n not in sifted]
for n in tqdm(will_rm_imgnames):os.remove(join(data_dir,n))
for n in tqdm(will_rm_txtnames):os.remove(join(data_dir,n))
