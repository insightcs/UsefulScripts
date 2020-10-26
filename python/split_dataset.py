# coding: utf-8
# @Author: oliver
# @Date:   2019-12-03 19:23:15

import os
import sys
import cv2
import random
import numpy as np
from tqdm import tqdm

if __name__ == '__main__':
	labels_file = sys.argv[1]
	output_dir = sys.argv[2]

	with open(labels_file, 'rb') as file_reader:
		lines = file_reader.readlines()

	true_lines = [] 
	for line in lines:
		data = line.decode('utf-8').strip()
		if len(data) == 0:
			continue
		true_lines.append(line)

	random.shuffle(true_lines)

	num_examples = len(true_lines)

	num_valid = int(np.ceil(num_examples * 0.1))

	valid_list = true_lines[:num_valid]
	train_list = true_lines[num_valid:]

	file_writer = open(os.path.join(output_dir, 'train_labels.txt'), 'wb')
	for line in train_list:
		file_writer.write(line)
	file_writer.close()

	file_writer = open(os.path.join(output_dir, 'valid_labels.txt'), 'wb')
	for line in valid_list:
		file_writer.write(line)
	file_writer.close()

