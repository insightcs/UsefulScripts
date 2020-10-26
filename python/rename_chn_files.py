#coding: utf-8
import re
import os
import sys
import string
import random

def is_chinese(string):
    for ch in string:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def main():
    if len(sys.argv) <= 1:
        raise ValueError('Please input data_dir.')
    data_dir = sys.argv[1]
    file_list = os.listdir(data_dir)
    for index, file in enumerate(file_list):
        file_name = os.path.join(data_dir, file)
        if not os.path.isfile(file_name):
            continue
        if not is_chinese(file):
            continue

        ext = os.path.splitext(file)[1]
        new_file_name = os.path.join(data_dir, ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20)) + ext)
        while os.path.exists(new_file_name):
            new_file_name = os.path.join(data_dir, ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20)) + ext)
        #new_file_name = file_name.replace(' - 副本', '_1')
        try:
            os.rename(file_name, new_file_name)
        except Exception as e:
            print('{}: {}'.format(file, e))
            continue

if __name__ == '__main__':
    main()