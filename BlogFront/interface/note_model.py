# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/25 16:14
 @Author  : CyanZoy
 @File    : note_model.py
 @Describe: 提供查数据接口
 """
from BlogFront.models import *
from collections import defaultdict
import os
import hashlib
import random
from PIL import Image
from PIL import ImageDraw, ImageFont


class Change:
    @staticmethod
    def queryset_to_dic(lab, *args, **kwargs):
        context = defaultdict(list)
        for _ in args:
            for i, j in zip(_, kwargs.values()):
                for k in i:
                    if 'name' in k:
                        if k['name'].lower() == lab:
                            k['color'] = 'active'
                        else:
                            k['color'] = 'tag-unchecked'
                    context[j].append(k)
        return context


class ModelGet:
    @staticmethod
    def note_get_t(name=None):
        """
        @ Create by CyanZoy on 2018/3/25 16:16
        @ Describe: 根据name-笔记本名获取相应笔记
        """
        try:
            if name:
                notename = NoteName.objects.get(name=name)
                return notename.belong_name.all().values()
            else:
                return NoteT.objects.all().values()
        except Exception as e:
            print(e)

    @staticmethod
    def note_get_name():
        """
        @ Create by CyanZoy on 2018/3/25 17:59
        @ Describe: 获取所有笔记类
        """
        try:
            return NoteName.objects.all().values()
        except Exception as e:
            print(e)


class ImageProcess(object):
    """用户处理图片"""
    def __init__(self):
        self.Base_Dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        # 原图
        self.original = self.Base_Dir + '/media/images/'
        # 水印图
        self.machining = self.Base_Dir + '/media/machining/'
        if not os.path.exists(self.machining):
            os.makedirs(self.machining)
        if not os.path.exists(self.original):
            os.makedirs(self.original)

    def image_upload(self, image=None):
        """上传图片
            :return 创建的文件名
        """
        filename = hashlib.md5(str(random.random()).encode(encoding="utf-8")).hexdigest()
        with open(self.Base_Dir+'/media/images/{}.jpg'.format(filename), 'wb') as f:
            f.write(image.read())
        return filename

    def image_add_watermark(self, watermark="https://blog.cyanzoy.top", filename=None):
        """给图片添加水印 默认为域名"""
        i = Image.open(self.original+'{}.jpg'.format(filename))
        draw = ImageDraw.Draw(i)
        assig = int((i.width + i.height) / 200)
        font_size = int(3 * assig) if assig else 5

        font = ImageFont.truetype(self.Base_Dir+'/media/tahoma.ttf', font_size)
        draw.text((i.width - (font_size / 72) * 96 * len(watermark) / 2.5, i.height - font_size / 72 * 96), watermark,
                  fill=(255, 255, 255), font=font)
        i.save(self.machining+'{}.jpg'.format(filename))
        return None


