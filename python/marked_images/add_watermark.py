#coding: utf-8

import os
import argparse
from PIL import Image, ImageDraw, ImageFont

def addTransparency(img, factor = 0.3 ):
    img = img.convert('RGBA')
    img_blender = Image.new('RGBA', img.size, (0,0,0,0))
    img = Image.blend(img_blender, img, factor)
    return img


def add_watermark(file_name, output_path):
    try:
        image = Image.open(file_name)
        layer = Image.open('./mask_im/m3.png')
        w, h = image.size
        layer = layer.resize((w, h), Image.ANTIALIAS)
        layer = addTransparency(layer)
        image.paste(layer, (0, 0), layer)
        # font = ImageFont.truetype('SIMYOU.TTF', 15) #linux上的字体：NotoSansCJK-Black.ttc, windows上的字体：SIMYOU.TTF
        # 输出内容
        # '''
        #content = 'Hello World!'
        # 需要先把输出的中文字符转换成Unicode编码形式, python3不需要
        '''
        if not isinstance(content, unicode):
            content = content.decode('utf8')
        '''
        # '''
        #font = ImageFont.truetype('SIMYOU.TTF', 15) #linux上的字体：NotoSansCJK-Black.ttc, windows上的字体：SIMYOU.TTF
        # 字体颜色
        #fillColor = (255, 0, 0)
        # 文字输出位置
        #position = (w-145, h-15)

        #draw = ImageDraw.Draw(image)
        #draw.text(position, content, font=font, fill=fillColor)
        image.save(os.path.join(output_path, os.path.basename(file_name)))
    except Exception as e:
        print('{}: {}'.format(file_name, e))
            
def traversal_dir(dir_path, output_path):
    files = os.listdir(dir_path)
    for file in files:
        file_name = os.path.join(dir_path, file)
        if os.path.isdir(file_name):
            traversal_dir(file_name, output_path)
        else:
            add_watermark(file_name, output_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_path', type=str, help='')
    parser.add_argument('output_path', type=str, help='')
    args = parser.parse_args()

    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)
        
    traversal_dir(args.data_path, args.output_path)

if __name__ == '__main__':
    main()
