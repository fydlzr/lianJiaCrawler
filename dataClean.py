# -*- coding: utf-8 -*-
import json

def getTax(price, area, man2,man5,weiyi,gongFang,jingShi1,jingShi2):
	price = 0.9*price #网签价
	tax = 0.0

	if jingShi1:
		tax += 0.1*price
	if jingShi2:
		tax += 0.03*price

	# 个税
	if gongFang:
		tax += 0.01*price
	else:
		if not weiyi:
			if man5:
				tax += 0.2 * (price - 0.3*price)
			elif man2:
				tax += 0.2 * (price - 0.6*price)
			else:
				tax += 0.2 * (price - 0.7*price)
	# 契税
	if area>90:
		tax += price*0.015
	else:
		tax += price*0.01
	# 增值税
	if not man2:
		tax += price * 0.056
	tax = round(tax,2)
	# print tax
	return str(tax)

def reorder(line):
	man2 = False
	man5 = False
	weiyi = False
	gongFang = False
	jingShi1 = False
	jingShi2 = False

	ss = line.strip('\n').split('\t')
	# print len(ss)
	out = [ss[0]]
	out += ss[1].split()
	if len(out)==2:out.append(' ')
	out.append(ss[2])
	out.append(ss[11])
	out += [ss[3].split('/')[0].replace('年建','')]
	out += ss[4:6]


	base = json.loads(ss[6])
	out.append(base[u'装修情况'].encode('utf-8'))
	out.append(base[u'房屋朝向'].encode('utf-8'))
	out.append(base[u'所在楼层'].encode('utf-8'))
	out.append(base[u'房屋户型'].encode('utf-8'))
	out.append(base[u'梯户比例'].encode('utf-8'))
	out.append(base[u'建筑类型'].encode('utf-8'))

	tran = json.loads(ss[7])
	out.append(tran[u'交易权属'].encode('utf-8'))
	if '一类' in out[-1]:
		jingShi1 = True
	elif '二类' in out[-1]:
		jiangShi2 = True
	elif '已购公房' in out[-1]:
		gongFang = True

	out.append(tran[u'挂牌时间'].encode('utf-8'))
	out.append(tran[u'上次交易'].encode('utf-8'))

	out.append(ss[8])
	out.append(ss[10])
	out.append(ss[13])
	if '不唯一'==ss[13]:
		weiyi = False
	else:
		weiyi = True

	out.append(ss[15])
	if '满五年'==ss[15]:
		man5 = True
		man2 = True
	elif '未满两年'==ss[15]:
		man2 = False
		man5 = False
	else:
		man2 = True
		man5 = False

	out.append(ss[14])
	out.append(ss[12])
	out.append(getTax(float(ss[5]), float(ss[2]), man2,man5,weiyi,gongFang,jingShi1,jingShi2))

	out.append(ss[16])
	out.append(ss[17])
	out.append(ss[18])
	return out

def myFilter(out):
	# out[18] 唯一

	#税 太高
	if float(out[23])/float(out[7]) >0.1 or float(out[23])>25:
		# print 'tax too High'
		return False
	# 是否有学区
	if out[18]=='否':
		# print 'no school'
		return False
	# 房龄
	if out[5]!='未知' and int(out[5])<1996:
		# print 'age<1996'
		return False
	# 朝向
	if '南' not in out[9]: 
		# print 'direction: No South'
		return False
	# 价格
	if float(out[7])>700:
		return False

	if '六环' in out[4]: return False

	return True


if __name__=='__main__':
	fout = open('output.txt','w')
	c = 0
	filted = 0
	for line in open('lj.txt','r'):
		if c%1000 == 0:print c
		c+=1
		out = reorder(line)
		# print '\t'.join(out)

		if not myFilter(out): 
			filted += 1
			continue
		
		fout.write('\t'.join(out)+'\n')
		# break
	fout.close()
	print 'filted =' + str(filted)