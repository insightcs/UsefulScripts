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

def traversal_dir(dir_path, md5_set):
    files = os.listdir(dir_path)
    for file_name in files:
        file_path = os.path.join(dir_path, file_name)
        if os.path.isdir(file_path):
            traversal_dir(file_path, md5_set)
        else:
            file_md5 = md5sum(file_path)
            try:
                if file_md5 in md5_set.keys():
                    #print('='*50)
                    #print(md5_set.get(file_md5))
                    #print(file_name)
                    os.remove(file_path)
                else:
                    md5_set.update({file_md5: file_path})
            except Exception as e:
                print('{}: {}'.format(file_path, e))
                continue

def main():
    if len(sys.argv) < 2:
        raise ValueError('Invalid input parameters!')
    data_dir = sys.argv[1]
    md5_set = {}
    traversal_dir(data_dir, md5_set)

if __name__ == '__main__':
    main()