# -*- coding: utf-8 -*-

import scrapy
import os
import urllib
from urllib import request
from xsd.items import xsdItem

class xsdSpider(scrapy.Spider):
    name = 'xsd'

    def start_requests(self):
        yield scrapy.Request(url='http://xsdau.com.au/main/home/product/5a571f8dee6a622f28939e33',meta={'page': False},callback=self.parse)

    def parse(self, response):
        with open((os.path.join('url.txt')), 'r') as f1:
            data = f1.read()
        urls = data.split('\n')
        for url in urls:
            url = 'http://xsdau.com.au/main/home/product/'+url
            yield scrapy.Request(url=url,callback=self.parse_detail)

    def parse_detail(self,response):
        item = xsdItem()
        title = response.css('#ybq-page-header > ui-view > div.ybq-tab.ng-scope.layout-align-center-center.layout-row > div > a:nth-child(7)::text').extract()[0]
        price = response.css('#ybq-page-header > ui-view > div:nth-child(2) > div > div.flex > div.price-sec > div > div.ad-order-price.ng-binding::text').extract()[0]

        if response.css('#ybq-page-header > ui-view > div:nth-child(2) > div > div.flex > div:nth-child(5) > pre::text'):
            description = response.css('#ybq-page-header > ui-view > div:nth-child(2) > div > div.flex > div:nth-child(5) > pre::text').extract()[0]
        else:
            description = ""
        cid = response.css('#ybq-page-header > ui-view > div.ybq-tab.ng-scope.layout-align-center-center.layout-row > div > a:nth-child(3)::text').extract()[0]
        brand = response.css('#ybq-page-header > ui-view > div.ybq-tab.ng-scope.layout-align-center-center.layout-row > div > a:nth-child(5)::text').extract()[0]
        image = response.css('#ybq-page-header > ui-view > div:nth-child(2) > div > div:nth-child(1) > img::attr(src)').extract()[0][2:]

        if response.css('#ybq-page-header > ui-view > div:nth-child(2) > div > div.flex > div:nth-child(15)'):
            imagediv = response.css(
                '#ybq-page-header > ui-view > div:nth-child(2) > div > div.flex > div:nth-child(15)').extract()[0]
        else:
            imagediv = ""

        item['title'] = title  # //*[@id="ybq-page-header"]/ui-view/div[1]/div/a[4]
        item['price'] = "".join(price.split())  # //*[@id="ybq-page-header"]/ui-view/div[2]/div/div[2]/div[2]/div/div[1]
        item['description'] = description  # //*[@id="ybq-page-header"]/ui-view/div[2]/div/div[2]/div[5]/pre
        item['cid'] = cid  # //*[@id="ybq-page-header"]/ui-view/div[1]/div/a[2]
        item['brand'] = brand  # //*[@id="ybq-page-header"]/ui-view/div[1]/div/a[3]
        item['imagediv'] = imagediv  # (selector) #ybq-page-header > ui-view > div:nth-child(2) > div > div.flex > div:nth-child(14) > img:nth-child(1)
        item['image']=image
        print(item)
        yield item

        file_path = '/Users/mac/Desktop/xsd/'

        try:
            if not os.path.exists(file_path + title):
                # print ('', file_path+name, 'not exist ')
                # os.mkdir(file_path)
                os.makedirs(file_path + title)
            # 获得图片后缀
            file_suffix = os.path.splitext(image)[1]
            # 拼接图片名（包含路径）     :/images/banana/banana.jpg
            filename = '{}{}{}{}'.format(file_path + title, os.sep, title, file_suffix)
            # 下载图片，并保存到文件夹中
            urllib.request.urlretrieve('http://'+image, filename=filename)
            # urllib.urlretrieve(image, filename=filename)
        except IOError as e:
            print('I/O operation failed', e)
        except Exception as e:
            print('error ：', e)
