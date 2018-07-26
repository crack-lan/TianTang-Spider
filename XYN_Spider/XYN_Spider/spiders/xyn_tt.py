# -*- coding: utf-8 -*-
import scrapy

from ..items import XynSpiderItem
class XynTtSpider(scrapy.Spider):
    name = 'xyn_tt'
    allowed_domains = ['ivsky.com']
    start_urls = ['http://www.ivsky.com/tupian/ziranfengguang/']

    def parse(self, response):
        hrefs=response.xpath('//div[@class="il_img"]/a/@href').extract()
        for href in hrefs:
            hturl='http://www.ivsky.com'+href
            yield scrapy.Request(
                url=hturl,
                callback=self.get_n
            )
        next=response.xpath('//a[@class="page-next"]/@href').extract_first('')
        if next:
            next_url='http://www.ivsky.com'+next
            yield scrapy.Request(next_url)
    def get_n(self,response):
        title=response.xpath('//h1/text()').extract_first('')
        tthrefs=response.xpath('//li/p/a/@href').extract()
        for tthref in tthrefs:
            htturl='http://www.ivsky.com'+tthref
            yield scrapy.Request(
                url=htturl,
                meta={'title':title},
                callback=self.pic
            )
        pic_next = response.xpath('//a[@class="page-next"]/@href').extract_first('')
        if pic_next:
            next_url = 'http://www.ivsky.com' + pic_next
            yield scrapy.Request(
                next_url,
                callback=self.get_n)
    def pic(self,response):
        name=response.xpath('//h1/text()').extract_first('')
        src=response.xpath('//div[@class="pic"]/div[@id="pic_con"]/div[1]/img/@src').extract_first('')
        title=response.meta['title']
        xyn_tt=XynSpiderItem()
        xyn_tt['name']=name
        xyn_tt['title']=title
        xyn_tt['src']=[src]
        yield xyn_tt