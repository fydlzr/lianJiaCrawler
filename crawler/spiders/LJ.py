# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import scrapy
from bs4 import BeautifulSoup as bs
from scrapy.http import Request
from scrapy.spider import BaseSpider
from crawler.items import LJCrawlerItem
from selenium import selenium
import re, urllib,urllib2,json

findhouseID = re.compile('http://bj.lianjia.com/ershoufang/(\d{12}).html')

seen = set()
for line in open('ljCrawled.txt'):
    seen.add(line.strip())


class LJSpider(scrapy.Spider):
    name = "LJ"
    allowed_domains = [] 

    # http://bj.lianjia.com/ershoufang/pg2co32sf1l2l3l4p5p6/
    # 70-90 http://bj.lianjia.com/ershoufang/co32sf1l2l3l4a3p5p6/
    #http://bj.lianjia.com/ershoufang/pg2sf1l2l3l4a3p5p6/
    urls = []
    # ped = set([1,3,4,7,9,12,13,18,20,21,22,24,25,26,30,31,33,35,36,37,39,40,43,46,47,50,51,52,53,54,55,57,58,59,60,
    #     61,62,63,64,66,68,71,72,73,74,75,76,78,79,80,85,86,88,90,91,92,93,94,95,96,97,100,11,27,32,28,41,44,69,17,
    #     5,98,83,45,29,48,70,99,49,82,67,77,15,19,16,42,65,81,8,84,56,23,38,14,2,6,10,87,34,89])

    for i in xrange(1,101):
        # if i in ped: continue
        urls.append('http://bj.lianjia.com/ershoufang/pg' + str(i) + 'sf1l2l3l4a3p5p6/')

    # for line in open('todo.txt','r'):
    #     line = line.strip()
    #     if line in seen:continue
    #     urls.append('http://bj.lianjia.com/ershoufang/' + line + '.html')
        # break
    start_urls = tuple(urls)
    
    def parse(self, response):
        fo = open('pages.txt','a')
        if 'pg' in response.url:
            houseIds = set(findhouseID.findall(response.body))
            print '========='+str(len(houseIds))+'============'
            print houseIds
            fo.write(response.url+'\n')
            fo.close()
            fout = open('todo.txt','a')
            for hid in houseIds:
                if hid in seen:continue
                # hid ='101101055559'
                fout.write(hid+'\n')
                yield Request('http://bj.lianjia.com/ershoufang/' + hid + '.html' ,
                        callback=self.parse)
                # break
            fout.close()
        else:
            soup = bs(response.body,'html5lib')
            item = LJCrawlerItem()

            item['url'] = response.url
            # try:
            item['title'] = soup.find('h1', class_='main').get_text()

            # //price
            # price=soup.find('div',class_='price')
            # item['price']=price.find('span', class_='total').get_text()
            # item['unitPrice']=price.find('div',class_='text').find('div',class_='unitPrice').get_text()
            # item['tax'] = price.find('div',class_='text').find('div',class_='tax').get_text()
            

            areaName = soup.find('div', class_='areaName')
            t = areaName.find('span', class_='info').get_text()
            ss = t.split()
            item['district']= ' '.join(ss[:-1])
            item['circle'] = ss[-1];


            communityName = soup.find('div', class_='communityName')
            t = communityName.find(class_='info').get_text()
            item['residentialName']= t

            item['age'] = soup.find('div', class_='area').find('div', class_='subInfo').get_text()


            # 基本信息
            introContent = soup.find('div', class_='introContent')
            base = introContent.find('div', class_='base').find('div', class_='content')
            lis = base.find('ul').find_all('li')
            kv = {}
            for li in lis:
                key = li.find('span').get_text()
                val = li.get_text()
                kv[key] = val.replace(key,'')
            item['base'] = json.dumps(kv, ensure_ascii=False).encode('utf-8')
            # 交易信息
            transaction = introContent.find('div', class_='transaction').find('div', class_='content')
            lis = transaction.find('ul').find_all('li')
            kv = {}
            for li in lis:
                key = li.find('span').get_text()
                val = li.get_text()
                kv[key] = val.replace(key,'')
            item['transaction'] = json.dumps(kv, ensure_ascii=False).encode('utf-8')
            # item['base'] = ''
            # item['transaction'] =''


            # 房源标签
            tags = soup.find('div', class_='tags clear')
            if tags!=None:
                tags = tags.find('div',class_='content').find_all('a')
                item['tags'] = ' '.join(t.get_text() for t in tags)
            else:
                item['tags'] = ""
            # 唯一
            # taxCalc=soup.find('div', id='taxCalculator').find('div', class_='option')
            pos1= response.body.find("require(['ershoufang/sellDetail/detailV3']")
            pos2 = response.body.find('cityId',pos1)
            info =response.body[pos1:pos2]
            
            if '不唯一' in info:
                item['isOnlyOne']='不唯一'
            else:
                item['isOnlyOne']='唯一'
            # 满二满五
            if '满五年' in info:
                item['registertime'] = '满五年'
            elif '未满两年' in info:
                item['registertime'] = '未满两年'
            else:
                item['registertime'] = '满两年'
            # 普或非普
            if '非普通'in info:
                item['isNormal'] ='非普通住宅'
            else:
                item['isNormal'] = '普通住宅'
            # price
            p1 = info.find("area")
            p2 = info.find(",",p1)
            item['area'] = info[p1+6:p2-1]
            p1 = info.find(r"totalPrice:'")
            p2 = info.find("',",p1)
            item['price'] = info[p1+12:p2]
            p1 = info.find(r"price:'")
            p2 = info.find("',",p1)
            item['unitPrice'] = info[p1+7:p2]


            bbody= response.body.replace('幼儿园,小学,中学,大学','').replace('<!-- 对口学校 -->','')
            # 学区
            if '学区' in bbody or '中学' in bbody or '小学' in bbody or \
            '初中' in bbody or '学校' in bbody or '高中' in bbody:
                item['school'] = '是(可能是)'
            else:
                item['school'] = '否'

            tese = soup.find('div', class_='introContent showbasemore')
            if tese!=None:
                item['FangYuanTeSe'] = re.subn('\s+', ' ', tese.get_text())[0]
            else:
                item['FangYuanTeSe'] =''
            daikan = soup.find('div', class_='daikan_content')
            if daikan!=None:
                item['DaiKanFanKui'] = re.subn('\s+', ' ', daikan.get_text())[0]
            else:
                item['DaiKanFanKui']=''
            zijian = soup.find('div', class_='newwrap shuofang')
            if zijian!=None:
                zijian = zijian.find('div', class_='bd').find('div', class_='txt')
                item['FangZhuZiJian'] = re.subn('\s+', ' ', zijian.get_text())[0]
            else:
                item['FangZhuZiJian']=''


            yield item

            # except:
            #     print 'ERROR!!'*10
            #     return


     