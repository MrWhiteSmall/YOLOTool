import os
from os.path import join as osj
txt_dir = r'D:\DesktopDocument\WXWork\1688858163660841\Cache\File\2025-03\All-SIMO-Light(XIFEN)'
rep_dict={
    '81':'12',
    '82':'13',
    '83':'14',
}
for name in os.listdir(txt_dir):
    if os.path.splitext(name)[-1]=='.txt':
        txt_path = osj(txt_dir,name)
        with open(txt_path,'r') as f:
            data = f.readlines()
        data = [rep_dict[d[:2]]+d[2:] if d[:2] in ('81','82','83') else d for d in data]
        with open(txt_path,'w') as f:
            f.writelines(data)
    