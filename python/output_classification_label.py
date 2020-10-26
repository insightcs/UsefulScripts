# coding: utf-8
# @Author: oliver
# @Date:   2019-12-03 18:54:55

import os
import sys
import cv2
import numpy as np
from tqdm import tqdm

if __name__ == '__main__':
	images_dir = sys.argv[1]
	output_file_name = sys.argv[2]

	file_writer = open(output_file_name, 'ab')
	file_list = os.listdir(images_dir)
	for file in tqdm(file_list):
		file_name = os.path.join(images_dir, file)
		if not os.path.exists(file_name):
			continue
		line = '{}\t{}\n'.format(file, 4)
		file_writer.write(line.encode('utf-8'))
	file_writer.close()
