#coding: utf-8

import os
import sys

data_dir = 'D:/OCR/营业执照/端到端测试集标注/marked_images/template2'
file_list = os.listdir(data_dir)
file_writer = open('license_template2.txt', 'w')
for file in file_list:
	file_name = os.path.join(data_dir, file)
	if not os.path.exists(file_name):
		continue
	file_writer.write('{}\n'.format(file))
	file_writer.write('id:\n')
	file_writer.write('name:\n')
	file_writer.write('enterprise:\n')
	file_writer.write('address:\n\n')
file_writer.close()
