# coding: utf-8
# @Author: oliver
# @Date:   2019-12-03 17:27:09

import os
import sys
import cv2
import math
import shutil
import numpy as np
from tqdm import tqdm

def rotate(image, angle, scale=1.):
    if int(angle) == 0:
        return image
    elif int(angle) % 90 == 0:
        return np.rot90(image, k=int(angle)//90)
    else:
        w = image.shape[1]
        h = image.shape[0]
        rangle = np.deg2rad(angle)  # angle in radians
        nw = (abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale
        nh = (abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale
        rot_mat = cv2.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)
        rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5,0]))
        rot_mat[0,2] += rot_move[0]
        rot_mat[1,2] += rot_move[1]
        return cv2.warpAffine(image, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))), flags=cv2.INTER_LINEAR).astype(np.uint8)

if __name__ == '__main__':
    images_dir = sys.argv[1]
    output_dir = sys.argv[2]
    angle = sys.argv[3]

    output_dir = os.path.join(output_dir, angle)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_list = os.listdir(images_dir)
    for file in tqdm(file_list):
        file_name = os.path.join(images_dir, file)
        try:
            img = cv2.imread(file_name)
            rotated_img = rotate(img, -float(angle))
            cv2.imwrite(os.path.join(output_dir, file), rotated_img)
        except Exception as e:
            print('{}: {}'.format(file, e))
            continue