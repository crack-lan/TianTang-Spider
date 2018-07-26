# -*- coding: utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import xlwt
class XynSpiderPipeline(object):
    def __init__(self):
        self.workbook=xlwt.Workbook(encoding='utf-8')
        self.sheet=self.workbook.add_sheet(u'天堂图片数据')
        self.sheet.write(0,0,'图片标题')
        self.sheet.write(0,1,'图片分类')
        self.sheet.write(0,2,'下载地址')
        self.count=1
    def __del__(self):
        self.workbook.save(u'天堂网图片信息.xls')
    def process_item(self, item, spider):
        self.sheet.write(self.count, 0, item['name'])
        self.sheet.write(self.count, 1, item['title'])
        self.sheet.write(self.count, 2, item['src'])
        self.count+=1
        return item

class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        url=item['src'][0]
        request=scrapy.Request(
            url=url,
            meta={'item':item}
        )
        return [request]
    def file_path(self, request, response=None, info=None):
        item=request.meta['item']
        name=item['name']

        title=item['title']
        return '%s/%s.jpg'%(title,name)
