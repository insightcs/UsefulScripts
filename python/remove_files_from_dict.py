#coding: utf-8

import os
import cv2
import argparse
import shutil
import sys
import random

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path1', type=str, default='')
    parser.add_argument('path2', type=str, default='')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    if not os.path.exists(args.path1):
        raise Exception('[{}] is not exists!'.format(args.path1))
    if not os.path.isdir(args.path2):
        raise Exception('[{}] is not a directory'.format(args.path2))

    file_list = os.listdir(args.path1)
    file_set = set()
    for file in file_list:
        file_set.add(os.path.splitext(file)[0])

    for file in os.listdir(args.path2):
        name = os.path.splitext(file)[0]
        if name in file_set:
            os.remove(os.path.join(args.path2, file))

if __name__ == '__main__':
    main()

