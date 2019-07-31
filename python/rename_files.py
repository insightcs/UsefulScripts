#coding: utf-8
import os
import sys

def main():
    if len(sys.argv) <= 1:
        raise ValueError('Please input data_dir.')
    data_dir = sys.argv[1]
    file_list = os.listdir(data_dir)
    for index, file in enumerate(file_list):
        file_name = os.path.join(data_dir, file)
        if not os.path.isfile(file_name):
            continue

        ext = os.path.splitext(file)[1]
        new_file_name = os.path.join(data_dir, '{:0>6d}'.format(index)+ ext)
        #new_file_name = file_name.replace(' - 副本', '_1')
        try:
            os.rename(file_name, new_file_name)
        except Exception as e:
            print('{}: {}'.format(file, e))
            continue

if __name__ == '__main__':
    main()