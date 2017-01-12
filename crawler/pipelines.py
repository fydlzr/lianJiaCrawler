# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
import MySQLdb
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CrawlerPipeline(object):
	def __init__(self):
		self.urls_seen = set()
		self.con = MySQLdb.connect(host="localhost", user="root", passwd="123456",db="crawler",port=3306)
		self.con.set_character_set('utf8')
		self.cur = self.con.cursor()
		self.cur.execute('SET NAMES utf8;') 
		self.cur.execute('SET CHARACTER SET utf8;')
		self.cur.execute('SET character_set_connection=utf8;')

	def process_item(self, item, spider):
		if item['url'] in self.urls_seen:
			raise DropItem("Duplicate url found")
		# elif item['table'] 
		else:
			self.urls_seen.add(item['url'])
		# self.write2File(item)
		# self.write2Mysql_10000_JS(item)
		# self.write2Mysql_hiapk(item)
		self.write2Mysql_LJ(item)
		return item


	def write2File(self, item):
		filename = 'out/'  + item['url'].split('?')[-1]
		fout = open(filename,'wb')
		fout.write(item['text'])
		fout.close()


	def write2Mysql_10000_BJ(self, item):
		self.cur.execute("insert into 10000zhidao (url, title, keyword, changeTime, clickTime, content) \
			values (%s,%s,%s,%s,%s,%s)",\
			(item['url'], item['title'], item['keyword'], item['changeTime'], item['clickTime'], item['content']))
		self.con.commit()

	def write2Mysql_10000_JS(self, item):
		# self.cur.execute("insert into 10000zhidaoJS (url, title, tag, tagContent) \
		# 	values (%s,%s,%s,%s)",\
		# 	(item['url'], item['title'], item['tag'], item['tagContent']))
		self.cur.execute("""UPDATE 10000zhidaoJS SET tagContent = %s WHERE url = %s""", (item['tagContent'],item['url']))
		self.con.commit()

	def write2Mysql_baidu(self, item):
		self.cur.execute("insert into baiduZhidao (qid, question, ask_time, ask_tags, bestAnswer, otherAnswer) \
			values (%s,%s,%s,%s,%s,%s)",\
			(item['qid'], item['question'], item['ask_time'], item['ask_tags'], item['bestAnswer'], item['otherAnswer']))
		self.con.commit()

	def write2Mysql_c114(self, item):
		try:
			self.cur.execute("insert into c114 (url, title, publish_time, author, source, text) \
				values (%s,%s,%s,%s,%s,%s)",\
				(item['url'], item['title'], item['publish_time'], item['author'], item['source'], item['text']))
			self.con.commit()
		except:
			return
	def write2Mysql_hiapk(self, item):
		try:
			self.cur.execute("insert into hiapk (url, title, parameter) \
				values (%s,%s,%s)",\
				(item['url'], item['title'], item['parameter']))
			self.con.commit()
		except:
			return

	def write2Mysql_LJ(self, item):
		try:
			if len(item)==2:
				self.cur.execute("update lj set DaiKanFanKui=%s where url=%s", (item['DaiKanFanKui'],item['url']))
				self.con.commit()
			else:
				self.cur.execute("insert into LJ (url, district, area, age, unitPrice, \
					price, base, transaction, residentialName, title, school, circle,\
					tags, isOnlyOne, isNormal, registertime,FangYuanTeSe,DaiKanFanKui,FangZhuZiJian) \
					values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",\
					(item['url'],item['district'],item['area'],item['age'],
						item['unitPrice'],item['price'],item['base'],item['transaction'],
						item['residentialName'],item['title'],item['school'],item['circle'],
						item['tags'],item['isOnlyOne'],item['isNormal'],item['registertime'],
						item['FangYuanTeSe'],item['DaiKanFanKui'],item['FangZhuZiJian']))
				self.con.commit()
		except Exception,e:
			print Exception,':',e
			# self.cur.execute("insert into LJ (url) \
			# 	values (%s)",\
			# 	(item['url']))
			# self.con.commit()