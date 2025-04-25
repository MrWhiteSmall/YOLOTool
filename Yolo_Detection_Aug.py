# this document aug image with horizontal, vertical and rotate 180;
import os,math
from os.path import join as osj
import random
from random import shuffle
from PIL import Image
from tqdm import tqdm
import shutil
import cv2
from utils_aug import *
def create_project_structure(root_dir):
    # 定义需要创建的目录结构
    directories = [
        os.path.join(root_dir, 'temp', 'mask'),
        os.path.join(root_dir, "images", "train"),
        os.path.join(root_dir, "images", "val"),
        os.path.join(root_dir, "labels", "train"),
        os.path.join(root_dir, "labels", "val"),
        os.path.join(root_dir, 'temp', 'save'),
        os.path.join(root_dir, 'temp')
    ]

    # 创建目录
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    print(f"目录结构在 '{root_dir}' 下创建完毕!")
    return directories
def move_files_to_outer_folder(folder_path):
    # 获取文件夹下的所有文件夹和文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 构建文件的原始路径和目标路径
            src_path = os.path.join(root, file)
            dest_path = os.path.join(folder_path, file)
            # 移动文件
            shutil.move(src_path, dest_path)
def remove_empty_dirs(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                print(f"Removed empty directory: {dir_path}")
def Aug(path, aug_path, Aug_methods, Aug_num):
    Aug_method_Names = ['vertical', 'horizontal', 'rotate180', 'anticlockwise90', 'clockwise']
    #创建数据增强子文件夹
    if not os.path.exists(os.path.join(aug_path, Aug_methods[Aug_num])):
        os.makedirs(os.path.join(aug_path, Aug_methods[Aug_num]))
    aug_path = os.path.join(aug_path, Aug_methods[Aug_num])

    cls_docs = os.listdir(path)
    # for cls_doc in cls_docs:
        # files = os.listdir(os.path.join(path, cls_doc))
        # path of reading image
        # cls_path = os.path.join(path, cls_doc)
        # save image and txt with different classes
        # if not os.path.exists(os.path.join(aug_path, cls_doc)):
        #     os.makedirs(os.path.join(aug_path, cls_doc))
    cls_save_path = aug_path
    for file in tqdm(cls_docs):
        if '.ini' in file:
            break
        if '.txt' in file:
            continue
        file_name = file[0:-4]
        img_type = file[-3:]
        img_name = file_name + '.{}'.format(img_type)
        txt_name = file_name + '.txt'
        new_img = file_name + '_{}.{}'.format(Aug_method_Names[Aug_num], img_type)
        new_txt = file_name + '_{}.txt'.format(Aug_method_Names[Aug_num])
        if not os.path.exists(os.path.join(path, img_name)):
            print('image:{} not found'.format(img_name))
            continue
        #图片操作
        img = Image.open(os.path.join(path, img_name)).convert('RGB')
        if Aug_num == 0:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            img.save(os.path.join(cls_save_path, new_img))
        elif Aug_num == 1:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
            img.save(os.path.join(cls_save_path, new_img))
        elif Aug_num == 2:
            img = img.rotate(180)
            img.save(os.path.join(cls_save_path, new_img))
        elif Aug_num == 3:
            img = cv2.imread(os.path.join(path, img_name))
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            cv2.imwrite(os.path.join(cls_save_path, new_img), img)
        elif Aug_num == 4:
            img = cv2.imread(os.path.join(path, img_name))
            img = cv2.flip(cv2.transpose(img), 1)
            cv2.imwrite(os.path.join(cls_save_path, new_img), img)
        else:
            print('Augmentation method not found')
        result = []
        if not os.path.exists(os.path.join(path, txt_name)):
            print(f'Text file: {txt_name} not found, creating an empty file.')
            open(os.path.join(path, txt_name), 'w').close()
        #txt操作
        with open(os.path.join(path, txt_name), encoding='utf-8') as file_obj:
            lines = file_obj.readlines()
            # 逐行读取
            for line in lines:
                number = find_number(line)
                if Aug_num == 0:
                    new_number = Vertical_flip_bbox(number)
                elif Aug_num == 1:
                    new_number = Horizontal_flip_bbox(number)
                elif Aug_num == 2:
                    new_number = rotation180_bbox(number)
                elif Aug_num == 3:
                    new_number = rotate90_bbox(number)
                elif Aug_num == 4:
                    new_number = rotate270_bbox(number)
                else:
                    print('Augmentation method not found')
                result.append(new_number)
            with open(os.path.join(cls_save_path, new_txt), 'w', encoding='utf-8') as new_file_obj:
                for k in range(len(result)):
                    for k_k in range(len(result[k])):
                        new_file_obj.write('{} '.format(result[k][k_k]))
                    new_file_obj.write('\n')
def extract_prefix(file_name):
    # 定义可能的后缀
    suffixes = ['_vertical', '_horizontal', '_rotate180', '_anticlockwise90', '_clockwise']
    
    # 反向查找后缀，找到最后一个匹配的后缀并获取它的位置
    for suffix in suffixes:
        if suffix in file_name:
            # 找到后缀，按_分割，取_前面的一部分
            prefix = file_name.split(suffix)[0]
            return prefix
    
    # 如果没有任何后缀，按.分割，取0号元素
    if '.' in file_name:
        prefix = file_name.split('.')[0]
        return prefix
    
    return None
def select_random_files(file_list, istrain, count=4):
    # 确保 file_list 是一个 NumPy 数组
    file_list = np.array(file_list)
    # file_list_copy=file_list
    selected_table = []
    unselected_table = []
    kill_table=[]
    if istrain:
        #'vertical', 'horizontal', 'rotate180', 'anticlockwise90', 'clockwise'
        for j,files in tqdm(enumerate(file_list)):
            for i, file in enumerate(files):
                if "vertical" not in file and "horizontal" not in file and "rotate180" not in file and "anticlockwise90" not in file and "clockwise" not in file:
                    # kill存入去除原图的文件列表
                    tmp = [files[i]]
                    selected_table.append(tmp)
                    files = np.delete(files, i)
                    kill_table.append(files)
        count -= 1  
    if istrain:
        for files in kill_table:
            if len(files) < count:
                raise ValueError("文件列表中的文件数量少于指定的选择数量")
            
            # 随机选择指定数量的文件
            selected_files = random.sample(list(files), count)
            
            # 获取剩余未被选中的文件
            unselected_files = [file for file in files if file not in selected_files]
            
            # 将选中的文件和未选中的文件分别添加到各自的表中
            selected_table.append(selected_files)
            unselected_table.append(unselected_files)
    else:
        for files in file_list:
            if len(files) < count:
                raise ValueError("文件列表中的文件数量少于指定的选择数量")
            
            # 随机选择指定数量的文件
            selected_files = random.sample(list(files), count)
            
            # 获取剩余未被选中的文件
            unselected_files = [file for file in files if file not in selected_files]
            
            # 将选中的文件和未选中的文件分别添加到各自的表中
            selected_table.append(selected_files)
            unselected_table.append(unselected_files)

    return selected_table, unselected_table

def group_files_by_prefix(folder_path):
    # 初始化一个字典来存储文件名前缀及其对应的文件列表
    file_dict = {}

    # 遍历文件夹中的所有文件和文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 获取文件名前缀
            prefix = extract_prefix(file)
            if prefix and not file.endswith('.txt'):
                # 如果文件名前缀不在字典中，则添加进字典并初始化一个列表
                if prefix not in file_dict:
                    file_dict[prefix] = []
                # 将文件名添加到相应前缀的列表中
                file_dict[prefix].append(file)

    # 初始化一个空列表来存储具有相同前缀的文件列表
    table = []

    # 遍历字典中的值，将文件列表添加到二维表中
    for file_list in file_dict.values():
        table.append(file_list)

    return table
def blocking_mask(ori_img_dir,mask_save_dir,mask_labels):
    save_dir=mask_save_dir
    txt_dir=ori_img_dir
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    files = os.listdir(ori_img_dir)
    for file in tqdm(files):
        if os.path.isdir(osj(ori_img_dir,file)) or \
                'txt' in file:
            continue
        txt_path = os.path.join(txt_dir, file[:-4] + '.txt')
        # 通过img名字在txt路径下找txt文件
        if not os.path.exists(txt_path):
            print('{} has not label,creating the file'.format(file))
            with open(txt_path, 'w') as f:
                pass

        img_path = os.path.join(ori_img_dir, file)
        if not os.path.exists(img_path):
            print(img_path,'error 不存在这个图片文件')
        img = cv2.imread(img_path)
        img_mask = draw_txt_mask(img, os.path.join(txt_dir, file[:-4] + '.txt'), mask_labels)

        cv2.imwrite(os.path.join(save_dir, file), img_mask)  # 保存被遮盖的图片

        filename = file[:-4]
        ori_txt = filename + '.txt'
        save_txt = filename + '.txt'

        ori_txt = os.path.join(txt_dir, ori_txt)
        save_txt = os.path.join(save_dir, save_txt)

        merger_select_label(ori_txt, save_txt, mask_labels) # 筛掉 禁用的 label 比如原类别 1,2,3 mask_label=2 则最后保存在tmp/save下面的就是1，3

def move_selected_and_unselected_files(selected_table, unselected_table, mask_save_dir, directories):
    def move_files(file_list, dest_img_dir, dest_txt_dir):
        for file in file_list:
            src_file = os.path.join(mask_save_dir, file)
            file_ext = os.path.splitext(file)[1]  # 获取文件扩展名
            if file_ext in ['.bmp', '.jpg']:  # 确保处理 .bmp 和 .jpg 文件
                dest_img_file = os.path.join(dest_img_dir, file)
                dest_txt_file = os.path.join(dest_txt_dir, file.replace(file_ext, '.txt'))
                shutil.move(src_file, dest_img_file)
                if os.path.exists(src_file.replace(file_ext, '.txt')):
                    shutil.move(src_file.replace(file_ext, '.txt'), dest_txt_file)

    # 将 selected_table 对应的文件移动到训练文件夹
    for selected_files in selected_table:
        move_files(selected_files, directories[1], directories[3])
    
    # 将 unselected_table 对应的文件移动到验证文件夹
    for unselected_files in unselected_table:
        move_files(unselected_files, directories[2], directories[4])
def process_and_augment_data(path, aug_path, Aug_methods, Aug_nums, mask_labels, count,istrain):
    directories = create_project_structure(aug_path)
    mask_save_dir = directories[0]
    save_dir=directories[5]
    temp=directories[6]
    blocking_mask(path, save_dir, mask_labels) # 筛选一下，把 mask_label中的类别 禁用掉，存入 /tmp/save
    if not os.path.exists(aug_path):
        os.makedirs(aug_path)   

    for Aug_num in Aug_nums:
        Aug(save_dir, mask_save_dir, Aug_methods, Aug_num)
    move_files_to_outer_folder(mask_save_dir)
    move_files_to_outer_folder(temp)
    remove_empty_dirs(temp)
    # directories = create_project_structure(aug_path)
    group = group_files_by_prefix(temp)
    selected_table, unselected_table = select_random_files(group,istrain, count)
    move_selected_and_unselected_files(selected_table, unselected_table, temp, directories)
    shutil.rmtree(temp)

'''
输入1 图片文件夹（包含bmp和label）
输入2 保存文件夹
最终保存为（yolo格式文件夹  images/  labels/）
'''

if __name__ == '__main__':
    # 图片上一级文件夹
    ori_img_dir = r"D:\DesktopDocument\WXWork\1688858163660841\Cache\File\2025-03\All-SIMO-Light"
    save_dir = r"D:\DesktopDocument\WXWork\1688858163660841\Cache\File\2025-03\All-SIMO-Light-Aug"
    Aug_nums = [0, 1, 2,3,4]
    
    split_ratio=[2,1] # train 2/3 val 1/3
    
    if os.path.exists(save_dir):shutil.rmtree(save_dir)
    # directories=create_project_structure(save_dir)
    # mask_save_dir=directories[0]
    Aug_methods = ['vertical', 'horizontal', 'rotate180', 'anticlockwise90', 'clockwise']
    #选择需要哪些数据增强
    #屏蔽的类是多少
    mask_labels = [50]
    #分几类
    count=3
    #是否将原图存入 train
    istrain=True
    # 调用封装的函数
    # process_and_augment_data(ori_img_dir, save_dir, Aug_methods, Aug_nums, mask_labels, count,istrain)
    
    '''
    预处理，先把原始数据都复制到目标目录
    1 在目标文件，根据已有数据做增强  => 增强文件的路径做成目录
    2 合并增强文件和原始文件
    3 按照比例shuffle后分成train val名单
    4 在目标目录创建 文件夹 并move文件
    '''
    def copy_ori_to_target(ori_img_dir,save_dir):
        img_name_list = [os.path.splitext(n)[0] for n in os.listdir(ori_img_dir) 
                    if n.split('.')[-1] in ('bmp','jpg','png')]
        txt_name_list = [os.path.splitext(n)[0] for n in os.listdir(ori_img_dir) 
                    if n.split('.')[-1] in ('txt')]
        sifted_list = [n for n in img_name_list if n in txt_name_list]  # 求两个数组的交集，使
        os.makedirs(save_dir,exist_ok=True)
        img_list = [(osj(ori_img_dir,n),osj(save_dir,n)) 
                    for n in os.listdir(ori_img_dir) 
                    if n.split('.')[-1] in ('bmp','jpg','png') and \
                        os.path.splitext(n)[0] in sifted_list]
        txt_list = [(osj(ori_img_dir,n+'.txt'),osj(save_dir,n+'.txt')) 
                    for n in sifted_list ]
        for ori_path,dst_path in img_list:shutil.copy2(ori_path,dst_path)
        for ori_path,dst_path in txt_list:shutil.copy2(ori_path,dst_path)
        return [os.path.basename(save_path) for _,save_path in img_list]

    def aug_vertical_img(img_path,save_aug_img_path):
        img = Image.open(img_path).convert('RGB')
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img.save(save_aug_img_path)
    def aug_horizontal_img(img_path,save_aug_img_path):
        img = Image.open(img_path).convert('RGB')
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        img.save(save_aug_img_path)
    def aug_rotate180_img(img_path,save_aug_img_path):
        img = Image.open(img_path).convert('RGB')
        img = img.rotate(180)
        img.save(save_aug_img_path)
    def aug_anticlockwise90_img(img_path,save_aug_img_path):
        img = cv2.imread(img_path)
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.imwrite(save_aug_img_path, img)    
    def aug_clockwise_img(img_path,save_aug_img_path):
        img = cv2.imread(img_path)
        img = cv2.flip(cv2.transpose(img), 1)
        cv2.imwrite(save_aug_img_path, img)
    def aug_img(aug_method,img_path,save_aug_img_path):
        ''' 'vertical', 'horizontal', 'rotate180', 'anticlockwise90', 'clockwise' '''
        if aug_method=='vertical':
            aug_vertical_img(img_path,save_aug_img_path)
        elif aug_method=='horizontal':
            aug_horizontal_img(img_path,save_aug_img_path)
        elif aug_method=='rotate180':
            aug_rotate180_img(img_path,save_aug_img_path)
        elif aug_method=='anticlockwise90':
            aug_anticlockwise90_img(img_path,save_aug_img_path)
        elif aug_method=='clockwise':
            aug_clockwise_img(img_path,save_aug_img_path)
        else:
            raise Exception('no this aug method')
    def aug_vertical_txt(txt_path,save_aug_txt_path):
        with open(txt_path, encoding='utf-8') as file_obj:
            data = file_obj.readlines()
        data = [ list(map(float,d.split())) for d in data]
        data = [list(map(str,Vertical_flip_bbox(d))) for d in data]
        with open(save_aug_txt_path,'w') as f:
            f.write( '\n'.join( [ ' '.join(d) for d in data] ) )
    def aug_horizontal_txt(txt_path,save_aug_txt_path):
        with open(txt_path, encoding='utf-8') as file_obj:
            data = file_obj.readlines()
        data = [ list(map(float,d.split())) for d in data]
        data = [list(map(str,Horizontal_flip_bbox(d))) for d in data]
        with open(save_aug_txt_path,'w') as f:
            f.write( '\n'.join( [ ' '.join(d) for d in data] ) )
    def aug_rotate180_txt(txt_path,save_aug_txt_path):
        with open(txt_path, encoding='utf-8') as file_obj:
            data = file_obj.readlines()
        data = [ list(map(float,d.split())) for d in data]
        data = [list(map(str,rotation180_bbox(d))) for d in data]
        with open(save_aug_txt_path,'w') as f:
            f.write( '\n'.join( [ ' '.join(d) for d in data] ) )
    def aug_anticlockwise90_txt(txt_path,save_aug_txt_path):
        with open(txt_path, encoding='utf-8') as file_obj:
            data = file_obj.readlines()
        data = [ list(map(float,d.split())) for d in data]
        data = [list(map(str,rotate90_bbox(d))) for d in data]
        with open(save_aug_txt_path,'w') as f:
            f.write( '\n'.join( [ ' '.join(d) for d in data] ) )  
    def aug_clockwise_txt(txt_path,save_aug_txt_path):
        with open(txt_path, encoding='utf-8') as file_obj:
            data = file_obj.readlines()
        data = [ list(map(float,d.split())) for d in data]
        data = [list(map(str,rotate270_bbox(d))) for d in data]
        with open(save_aug_txt_path,'w') as f:
            f.write( '\n'.join( [ ' '.join(d) for d in data] ) )
    def aug_txt(aug_method,txt_path,save_aug_txt_path):
        ''' 'vertical', 'horizontal', 'rotate180', 'anticlockwise90', 'clockwise' '''
        if aug_method=='vertical':
            aug_vertical_txt(txt_path,save_aug_txt_path)
        elif aug_method=='horizontal':
            aug_horizontal_txt(txt_path,save_aug_txt_path)
        elif aug_method=='rotate180':
            aug_rotate180_txt(txt_path,save_aug_txt_path)
        elif aug_method=='anticlockwise90':
            aug_anticlockwise90_txt(txt_path,save_aug_txt_path)
        elif aug_method=='clockwise':
            aug_clockwise_txt(txt_path,save_aug_txt_path)
        else:
            raise Exception('no this aug method')
    def augment_data(save_dir,Aug_methods, Aug_nums, mask_labels):
        returned_aug_img=[]
        # save_dir中的数据已经能够保证 图片-label 一一对应
        img_list = [n for n in os.listdir(save_dir) 
                    if n.split('.')[-1] in ('bmp','jpg','png')]
        # 原数据先根据mask_labels处理一下
        print('开始增强数据')
        for n in tqdm(img_list):
            txt_path = osj(save_dir,os.path.splitext(n)[0]+'.txt')
            img_path = osj(save_dir,n)
            img = cv2.imread(img_path)
            img_mask = draw_txt_mask(img, txt_path, mask_labels)
            cv2.imwrite(img_path, img_mask)  # 保存被遮盖的图片 
            with open(txt_path ,'r') as f:
                data = f.readlines()
            # 去掉原label中包含mask_label的部分
            i=0
            for j in range(len(data)):
                if int(data[j].split()[0]) in mask_labels: # 取出第一个label 是否存在于mask_labels中
                    continue
                data[i] = data[j]
                i+=1
            data = data[:i]
            with open(txt_path,'w') as f:
                f.write(''.join(data))
            ###### 至此 完成数据的预处理————将masked 的内容在图片上标黑且label中去掉这行内容 ####
            ## 开始增强   对原图增强后存入aug路径
            for aug_id in Aug_nums:
                aug_method = Aug_methods[aug_id]
                save_aug_img_path = osj(save_dir,os.path.splitext(n)[0]+f'{aug_method}'+'.jpg')
                aug_img(aug_method,img_path,save_aug_img_path)
                save_aug_txt_path = osj(save_dir,os.path.splitext(n)[0]+f'{aug_method}'+'.txt')
                aug_txt(aug_method,txt_path,save_aug_txt_path)
                
                # 将增强后的输入存入 返回列表
                returned_aug_img.append(os.path.basename(save_aug_img_path))
        return returned_aug_img
    def merge_ori_aug(ori_file_list,aug_file_list):
        ori_file_list.extend(aug_file_list)
        shuffle(ori_file_list)
        return ori_file_list
    def split_train_val_by_split_ratio(all_file_list,split_ratio):
        if len(split_ratio)!=2:raise Exception('由于分成train val所以这里必须有两个值')
        # 此时传入的 file list 已经是shuffle过的，直接从中取出 split_ration 对应的数据
        train_num = math.ceil(len(all_file_list)*(split_ratio[0]/sum(split_ratio)))
        train_list = all_file_list[:train_num]
        val_list = all_file_list[train_num:]
        return train_list,val_list
    def move_to_yolo_dir_by_lists(save_dir,train_list,val_list):
        ''' 
        save_dir
            images
                train
                val
            labels
                train
                val
        '''
        yolo_image_train_dir = osj(save_dir,'images','train')
        yolo_image_val_dir = osj(save_dir,'images','val')
        yolo_label_train_dir = osj(save_dir,'labels','train')
        yolo_label_val_dir = osj(save_dir,'labels','val')
        os.makedirs(yolo_image_train_dir)
        os.makedirs(yolo_image_val_dir)
        os.makedirs(yolo_label_train_dir)
        os.makedirs(yolo_label_val_dir)
        print('开始分割数据')
        for train_n in tqdm(train_list):
            shutil.move(osj(save_dir,train_n),yolo_image_train_dir)
            shutil.move(osj(save_dir,
                            os.path.splitext(train_n)[0]+'.txt'),yolo_label_train_dir)
        for val_n in tqdm(val_list):
            shutil.move(osj(save_dir,val_n),yolo_image_val_dir)
            shutil.move(osj(save_dir,
                            os.path.splitext(val_n)[0]+'.txt'),yolo_label_val_dir)
    # 返回 list 包含 imgname.ext
    ori_file_list = copy_ori_to_target(ori_img_dir,save_dir)
    # 返回 list 包含 imgname.ext
    aug_file_list = augment_data(save_dir,Aug_methods, Aug_nums, mask_labels)
    all_file_list = merge_ori_aug(ori_file_list,aug_file_list)
    train_list,val_list = split_train_val_by_split_ratio(all_file_list,split_ratio)
    move_to_yolo_dir_by_lists(save_dir,train_list,val_list)