#coding: utf-8

import os
import re
import io
import argparse
import requests
import tqdm
import json
import random
import numpy as np

def get_urls(args):
    with open(args.filename, 'r', encoding='utf-8') as file_reader:
        data = json.load(file_reader)
        
    url_list = []
    if args.data_type == 'video':
        url_template = 'http://tianchi-competition.oss-cn-hangzhou.aliyuncs.com/531798/%s/%s/%s.mp4'
    else:
        url_template = 'http://tianchi-competition.oss-cn-hangzhou.aliyuncs.com/531798/%s/%s/%s.npy'

    for video in data.keys():
        url = url_template % (args.subset, args.data_type, video)
        url_list.append(url)
    return url_list


def download_data(url_list, output_path, log_path):
    error_log_writer = open(log_path, 'a')
    for url in tqdm.tqdm(url_list, dynamic_ncols=True):
        file_name = url.split('/')[-1]
        output_filename = os.path.join(output_path, file_name)
        try:
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
            response = requests.get(url, headers=headers)
        except requests.exceptions.RequestException:
            error_log_writer.write('Time out: {}\n'.format(url))
            continue
        else:
            response.encoding = 'UTF-8'
            with open(output_filename, 'wb') as file_writer:
                file_writer.write(response.content)
    error_log_writer.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='')
    parser.add_argument('output_path', type=str, help='')
    parser.add_argument('--subset', type=str, default='train', help='')
    parser.add_argument('--data_type', type=str, default='video', help='')
    parser.add_argument('--log_path', type=str, default='error.log', help='')
    args = parser.parse_args()

    output_path = os.path.join(args.output_path, args.subset, args.data_type)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    url_list = get_urls(args)
    download_data(url_list[:10000], output_path, args.log_path)

if __name__ == '__main__':
    main()


