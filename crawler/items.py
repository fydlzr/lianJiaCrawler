# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduzhidaocrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    qid = scrapy.Field()  # 问题id
    question = scrapy.Field() #ask_title
    ask_time = scrapy.Field()  # 提问时间
    ask_tags = scrapy.Field()  # 问题tags标签，暂以 "," 分隔
    bestAnswer = scrapy.Field()
    otherAnswer = scrapy.Field()

class c114CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()  
    title = scrapy.Field() 
    publish_time = scrapy.Field() 
    author = scrapy.Field()
    source = scrapy.Field()
    text = scrapy.Field()

class hiapkCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()  
    title = scrapy.Field() 
    parameter = scrapy.Field() 

class byrCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()  
    text = scrapy.Field()  

class A10000ZhidaoCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()  
    title = scrapy.Field()  
    tag = scrapy.Field()  
    tagContent = scrapy.Field()  

class A10000ZhidaoCrawlerItem_BJ(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()  
    title = scrapy.Field()  
    keyword = scrapy.Field()  
    changeTime = scrapy.Field()  
    clickTime = scrapy.Field()  
    content = scrapy.Field()  

class LJCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    district = scrapy.Field()
    area = scrapy.Field()
    age = scrapy.Field()
    unitPrice = scrapy.Field()
    price = scrapy.Field()
    base = scrapy.Field()
    transaction = scrapy.Field()
    residentialName = scrapy.Field()
    title = scrapy.Field()
    school = scrapy.Field()
    circle = scrapy.Field()
    tags = scrapy.Field()
    isOnlyOne = scrapy.Field()
    isNormal = scrapy.Field()
    registertime = scrapy.Field()
    FangYuanTeSe = scrapy.Field()
    DaiKanFanKui = scrapy.Field()
    FangZhuZiJian = scrapy.Field()

        