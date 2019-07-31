#coding: utf-8

import os
import argparse

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('base_path', type=str, default='')
	parser.add_argument('output_path', type=str, default='')
	args = parser.parse_args()
	return args

def main():
	args = parse_args()

	if not os.path.exists(args.base_path):
		raise Exception('[{}] is not exists!'.format(args.base_path))
	if not os.path.isdir(args.base_path):
		raise Exception('[{}] is not a directory'.format(args.base_path))
	
	files = os.listdir(args.base_path)
	with open(args.output_path, 'w') as file_writer:
		for file_name in files:
			file_path = os.path.join(args.base_path, file_name)
			file_writer.write('{}\n'.format(file_path))

if __name__ == '__main__':
	main()

