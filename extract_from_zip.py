import os
import shutil
from tqdm import tqdm
import zipfile
from os.path import join as osj

def extract_from_zip(zip_path,dst_path):
    # 打开ZIP文件
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # 解压文件到指定目录
        zip_ref.extractall(dst_path)
def move_files_to_outer_folder(folder_path,dst_folder_path):
    # 获取文件夹下的所有文件夹和文件
    for root, dirs, files in os.walk(folder_path):
        for file in tqdm(files):
            # 构建文件的原始路径和目标路径
            src_path = os.path.join(root, file)
            dest_path = os.path.join(dst_folder_path, file)
            # 移动文件
            shutil.move(src_path, dest_path)
            
            
src_dir=r"D:\BaiduNetdiskDownload\2025-1-24-芜湖长信TP\OK料\工位二撕膜\明场"
dst_path=r"D:\BaiduNetdiskDownload\2025-1-24-芜湖长信TP\OK料\工位二撕膜\明场"
# 如果有 zip 先全部提取
# 获取所有ZIP文件列表
zip_files = [file for file in os.listdir(src_dir) if file.endswith('.zip')]
for zip_file in tqdm(zip_files):
    extract_from_zip( osj(src_dir,zip_file),dst_path )
# 检查剩余文件夹中是否还有文件，都move出来
move_files_to_outer_folder(src_dir,dst_path)