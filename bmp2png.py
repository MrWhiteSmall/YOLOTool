from PIL import Image
import os
from tqdm import tqdm
def bmp_to_PNG(bmp_path, PNG_path):
    # 打开BMP文件
    with Image.open(bmp_path) as img:
        # 保存为PNG格式
        img.convert("RGB").save(PNG_path, "PNG")
    print(f"成功将 {bmp_path} 转换为 {PNG_path}")

# 示例：批量转换文件夹中的所有BMP文件为PNG
def batch_convert(bmp_folder, PNG_folder,remove_bmp):
    # 如果输出文件夹不存在，创建它
    if not os.path.exists(PNG_folder):
        os.makedirs(PNG_folder)

    # 遍历文件夹中的所有BMP文件
    for filename in tqdm(os.listdir(bmp_folder)):
        if filename.lower().endswith(".bmp"):
            bmp_path = os.path.join(bmp_folder, filename)
            PNG_filename = filename.replace(".bmp", ".png")
            PNG_path = os.path.join(PNG_folder, PNG_filename)
            bmp_to_PNG(bmp_path, PNG_path)
            if remove_bmp:os.remove(bmp_path)

# 示例：批量转换指定文件夹中的BMP文件为PNG
bmp_folder = r"D:\DesktopImages\test"  # 替换为你的BMP文件夹路径
PNG_folder = r"D:\DesktopImages\test2"  # 替换为保存PNG文件的文件夹路径
# 转换PNG后是否移除原有的bmp文件
remove_bmp = False

batch_convert(bmp_folder, PNG_folder,remove_bmp=remove_bmp)
