from PIL import Image
import numpy as np
import cv2

############# aug image ################
############# aug image ################
############# aug image ################
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
############# End aug image ################
############# End aug image ################
############# End aug image ################


##############  aug label txt ###########
##############  aug label txt ###########
##############  aug label txt ###########
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
############## End aug label txt ###########
############## End aug label txt ###########
############## End aug label txt ###########


# Vertical_flip_bbox
def Vertical_flip_bbox(bbox):
    new_bbox = []
    new_bbox.append(int(bbox[0]))
    o_x, o_y, o_w, o_h = bbox[1], bbox[2], bbox[3], bbox[4]
    new_x = o_x
    new_y = 1 - o_y
    new_bbox.append(new_x)
    new_bbox.append(new_y)
    new_bbox.append(o_w)
    new_bbox.append(o_h)
    return new_bbox


def Horizontal_flip_bbox(bbox):
    new_bbox = []
    new_bbox.append(int(bbox[0]))
    o_x, o_y, o_w, o_h = bbox[1], bbox[2], bbox[3], bbox[4]
    new_x = 1 - o_x
    new_y = o_y
    new_bbox.append(new_x)
    new_bbox.append(new_y)
    new_bbox.append(o_w)
    new_bbox.append(o_h)
    return new_bbox


def rotation180_bbox(bbox):
    new_bbox = []
    new_bbox.append(int(bbox[0]))
    o_x, o_y, o_w, o_h = bbox[1], bbox[2], bbox[3], bbox[4]
    new_x = 1 - o_x
    new_y = 1 - o_y
    new_bbox.append(new_x)
    new_bbox.append(new_y)
    new_bbox.append(o_w)
    new_bbox.append(o_h)
    return new_bbox


# 逆时针
def rotate90_bbox(bbox):
    new_bbox = []
    new_bbox.append(int(bbox[0]))
    o_x, o_y, o_w, o_h = bbox[1], bbox[2], bbox[3], bbox[4]
    new_x = o_y
    new_y = 1 - (o_x)
    new_bbox.append(new_x)
    new_bbox.append(new_y)
    new_bbox.append(o_h)
    new_bbox.append(o_w)
    return new_bbox


# 顺时针
def rotate270_bbox(bbox):
    new_bbox = []
    new_bbox.append(int(bbox[0]))
    o_x, o_y, o_w, o_h = bbox[1], bbox[2], bbox[3], bbox[4]
    new_x = 1 - o_y
    new_y = (o_x)
    new_bbox.append(new_x)
    new_bbox.append(new_y)
    new_bbox.append(o_h)
    new_bbox.append(o_w)
    return new_bbox

# Draw block are with special label
def draw_txt_mask(img, txt_path, mask_labels):
    image_size = img.shape
    height, width = image_size[:2]

    file_handle = open(txt_path)
    cnt_info = file_handle.readlines()
    new_cnt_info = [line_str.replace("\n", "").split(" ") for line_str in cnt_info]

    for new_info in new_cnt_info:
        temp_label = int(new_info[0])
        if temp_label in mask_labels:
            s = []  # 如果需要遮盖，创建一个空列表
            for i in range(1, len(new_info), 2):
                b = []
                for tmp in new_info[i:i + 2]:
                    if tmp != '':
                        b.append(float(tmp))  # x,y/w,h
                if b != []:
                    s.append(b[0])
                    s.append(b[1])
            s = np.array(s)
            x1 = int((float(s[0]) - float(s[2]) / 2) * width)  # x_center - width/2 将归一化之后的数据变回原来的大小
            y1 = int((float(s[1]) - float(s[3]) / 2) * height)  # y_center - height/2
            x2 = int((float(s[0]) + float(s[2]) / 2) * width)  # x_center + width/2
            y2 = int((float(s[1]) + float(s[3]) / 2) * height)  # y_center + height/2
            cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 0, 0), thickness=-1)  # BGR
    return img

