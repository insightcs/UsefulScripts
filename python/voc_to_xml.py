#coding: utf-8

import os
import re
import sys

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from xml.dom import minidom


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('labels_path', type=str, default='')
    parser.add_argument('images_path', type=str, default='')
    parser.add_argument('output_path', type=str, default='')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    file_list = os.listdir(args.labels_path)
    for file in file_list:
        file_name = os.path.join(args.labels_path, file)
        tree = ET.ElementTree()
        tree.parse(file_name)
        root = tree.getroot()

        filename_node = root.find('filename')
        path_node = root.find('path')
        size_node = root.find('size')
        objs = root.findall('object')
        object_list = []
        for obj in objs:
            obj.remove(obj.find('pose'))
            obj.remove(obj.find('truncated'))
            obj.remove(obj.find('difficult'))
            object_list.append(obj)

        new_root = ET.Element('doc')
        path = ET.SubElement(new_root, 'path')
        path.text = os.path.join(args.images_path, filename_node.text).replace('/', '\\')

        outputs = ET.SubElement(new_root, 'outputs')
        if len(object_list) != 0:
            objects = ET.SubElement(outputs, 'object')
            for object_node in object_list:
                object_node.tag = 'item'
                objects.append(object_node)

        time_labeled = ET.SubElement(new_root, 'time_labeled')
        time_labeled.text = '1559538378672' if len(object_list) != 0 else '0'
        labeled = ET.SubElement(new_root, 'labeled')
        labeled.text = 'true' if len(object_list) != 0 else 'false'
        if size_node:
            new_root.append(size_node)

        xml_string = ET.tostring(new_root)
        tree = minidom.parseString(xml_string)
        xml_string = tree.toxml().replace('\t', '').replace('\r', '').replace('\n', '')
        tree = minidom.parseString(xml_string)
        xml_string = tree.toprettyxml()
        file_name = os.path.join(args.output_path, file)
        with open(file_name, 'w') as file_writer:
            file_writer.write(xml_string)

if __name__ == '__main__':
    main()