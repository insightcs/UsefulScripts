#coding: utf-8
import os
import sys
from hashlib import md5

def md5sum(filename):
    md5_obj = md5()
    file_reader = open(filename, 'rb')
    md5_obj.update(file_reader.read())
    file_reader.close()
    return md5_obj.hexdigest()

def main():
	if len(sys.argv) < 2:
		raise ValueError('Invalid input parameters!')
	data_dir = sys.argv[1]
	md5_set = {}
	file_list = os.listdir(data_dir)
	for file in file_list:
	    file_name = os.path.join(data_dir, file)
	    if not os.path.isfile(file_name):
	        continue
	    file_md5 = md5sum(file_name)
	    try:
	        if file_md5 in md5_set.keys():
	        	#print('='*50)
	        	#print(md5_set.get(file_md5))
	        	#print(file_name)
	            os.remove(file_name)
	        else:
	            md5_set.update({file_md5:file_name})
	    except Exception as e:
	        print('{}: {}'.format(file, e))
	        continue

if __name__ == '__main__':
	main()