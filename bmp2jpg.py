from PIL import Image
import os
from tqdm import tqdm
def bmp_to_jpg(bmp_path, jpg_path):
    # 打开BMP文件
    with Image.open(bmp_path) as img:
        # 保存为JPG格式
        img.convert("RGB").save(jpg_path, "JPEG")
    print(f"成功将 {bmp_path} 转换为 {jpg_path}")

# 示例：批量转换文件夹中的所有BMP文件为JPG
def batch_convert(bmp_folder, jpg_folder,remove_bmp):
    # 如果输出文件夹不存在，创建它
    if not os.path.exists(jpg_folder):
        os.makedirs(jpg_folder)

    # 遍历文件夹中的所有BMP文件
    for filename in tqdm(os.listdir(bmp_folder)):
        if filename.lower().endswith(".bmp"):
            bmp_path = os.path.join(bmp_folder, filename)
            jpg_filename = filename.replace(".bmp", ".jpg")
            jpg_path = os.path.join(jpg_folder, jpg_filename)
            bmp_to_jpg(bmp_path, jpg_path)
            if remove_bmp:os.remove(bmp_path)

# 示例：批量转换指定文件夹中的BMP文件为JPG
bmp_folder = r"D:\DesktopImages\test"  # 替换为你的BMP文件夹路径
jpg_folder = r"D:\DesktopImages\test3"  # 替换为保存JPG文件的文件夹路径
# 转换jpg后是否移除原有的bmp文件
remove_bmp = False

batch_convert(bmp_folder, jpg_folder,remove_bmp=remove_bmp)
