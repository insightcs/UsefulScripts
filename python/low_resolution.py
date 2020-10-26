# coding: utf-8
# @Author: oliver
# @Date:   2019-12-03 14:41:43

import os
import sys
import cv2
import shutil
import numpy as np
from tqdm import tqdm

if __name__ == '__main__':
	images_dir = sys.argv[1]
	output_dir = sys.argv[2]

	file_list = os.listdir(images_dir)
	for file in tqdm(file_list):
		file_name = os.path.join(images_dir, file)
		img = cv2.imread(file_name)
		h, w, _ = img.shape
		if max(h, w) < 500:
			shutil.move(file_name, os.path.join(output_dir, file))