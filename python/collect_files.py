#coding: utf-8

import os
import cv2
import argparse
import shutil
import sys
import random

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('base_path', type=str, default='')
    parser.add_argument('output_path', type=str, default='')
    args = parser.parse_args()
    return args

def traversal_dir(dir_path, output_path):
    files = os.listdir(dir_path)
    for file_name in files:
        file_path = os.path.join(dir_path, file_name)
        if os.path.isdir(file_path):
            traversal_dir(file_path, output_path)
        else:
            try:
                out_file_name = os.path.join(output_path, file_name)
                while os.path.exists(out_file_name):
                    out_file_name = os.path.join(output_path, ''.join(str(random.choice(range(10))) for _ in range(10)) + file_name)
                shutil.copy(file_path, out_file_name)
            except IOError as e:
                print("Unable to copy file. %s" % e)
                continue
            except:
                print("Unexpected error:", sys.exc_info())
                continue

def main():
    args = parse_args()

    if not os.path.exists(args.base_path):
        raise Exception('[{}] is not exists!'.format(args.base_path))
    if not os.path.isdir(args.base_path):
        raise Exception('[{}] is not a directory'.format(args.base_path))

    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    traversal_dir(args.base_path, args.output_path)
    
    

if __name__ == '__main__':
    main()

