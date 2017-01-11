# -*- coding: utf-8 -*-
import re
import MySQLdb
# str = '''
# '''
# print re.subn('\s+', '\t', str)[0]

con = MySQLdb.connect(host="localhost", user="root", passwd="123456",db="crawler",port=3306)
con.set_character_set('utf8')
cur = con.cursor()
cur.execute('SET NAMES utf8;') 
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')
print cur.execute('select url from LJ')
results = cur.fetchall()
fout = open('ljCrawled.txt','w')
for row in results:
	str = row[0].strip()
	str = str.replace('http://bj.lianjia.com/ershoufang/','').replace('.html', '')
	fout.write(str+'\n')
fout.close()


for line in open('proxy.txt','r'):
	ss = line.strip().replace('Cn\t','').split('\t')
	if len(ss)<5:continue
	print ('{"ip_port" : "' + ss[0]+':'+ss[1]+'"},')
