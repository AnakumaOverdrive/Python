from pylab import *

class matchrow:
	def __init__(self,row,allnum=False):
		if allnum:
			self.data = [float(row[i]) for i in range(len(row)-1)]
		else:
			self.data = row[0:len(row)-1]
		self.match = int(row[len(row)-1])
		
def loadmatch(f,allnum=False):
	rows = []
	for line in open(f):
		rows.append(matchrow(line.split(','),allnum))
	return rows
	
agesonly = loadmatch('agesonly.csv',allnum=True)
matchmaker = loadmatch('matchmaker.csv')

def plotagematches(rows):
	xdm,ydm = [r.data[0] for r in rows if r.match == 1], [r.data[1] for r in rows if r.match == 1]
	xdn,ydn = [r.data[0] for r in rows if r.match == 0], [r.data[1] for r in rows if r.match == 0]
	
	plot(xdm,ydm,'go')
	plot(xdn,ydn,'r+')
	
	averages = lineartrain(agesonly)
	plot(averages[1],averages[0])
	
	show()

def lineartrain(rows):
	"""线性分类"""
	averages = {}
	counts = {}
	
	for row in rows:
		#得到该坐标点所属的分类
		cl = row.match
		
		averages.setdefault(cl,[0.0] * (len(row.data)))
		counts.setdefault(cl,0)
	
		#将该坐标点加入averages中
		for i in range(len(row.data)):
			averages[cl][i] += float(row.data[i])
			
		#记录每个分类中有多少坐标点
		counts[cl] += 1
	
	#将综合除以计数值求得平均值
	for cl,avg in averages.items():
		for i in range(len(avg)):
			avg[i] /= counts[cl]
	
	return averages
	
def dotproduct(v1,v2):
	"""点积
	所谓点积是指,针对两个向量,将第一个向量中每个值域第二个向量中的对应值相乘,
	然后再将所得的每个乘积相加,最后得到一个总的结果.
	点积也可以用两个向量的长度乘积,再乘以两者夹角的余弦求得."""
	return sum([v1[i] * v2[i] for i in range(len(v1))])
	
def veclength(v):
  return sum([p**2 for p in v])
	
def dpclassify(point,avgs):
	"""点积分类
	class = sign((x - (m0+m1)/2) * (m0 - m1))
	相乘后的结果为:
	class = sign(xm0 - xm1 + (m0m0-m1m1)/2)
	class
	"""
	b =(dotproduct(avgs[1],avgs[1]) - dotproduct(avgs[0],avgs[0]))/2
	y = dotproduct(point,avgs[0]) - dotproduct(point,avgs[1]) + b
	if y > 0: return 0
	else: return 1
	
def yesno(v):
	if v == 'yes': return 1
	elif v == 'no': return -1
	else: return 0
	
def matchcount(interset1,interset2):
	l1 = interset1.split(':')
	l2 = interset2.split(':')
	x = 0
	for v in l1:
		if v in l2: x += 1
	return x
	
def milesdistance(a1,a2):
	return 0

def loadnumerical():
	oldrows = loadmatch('matchmaker.csv')
	newrows = []
	for row in oldrows:
		d = row.data
		data = [float(d[0]),yesno(d[1]),yesno(d[2]),float(d[5]),yesno(d[6]),yesno(d[7]),matchcount(d[3],d[8]),milesdistance(d[4],d[9]),row.match]
		newrows.append(matchrow(data))
	return newrows
		
	
def scaledata(rows):
	""""""
	low = [99999999.0] * len(rows[0].data)
	high = [-999999999.0] * len(rows[0].data)
	#寻找最大值和最小值
	for row in rows:
		d = row.data
		for i in range(len(d)):
			if d[i] < low[i]: low[i] = d[i]
			if d[i] > high[i]: high[i] = d[i]
			
	#对数据进行缩放处理的函数
	def scaleinput(d):
		#return [(d[i] - low[i]) / (high[i] - low[i]) for i in range(len(low))]
		size = len(d)
		data = [0.0] * size
		for i in range(size):
			if high[i] == low[i]:
				data[i] = 1.0
			else:
				data[i] = (d[i] - low[i]) / (high[i] - low[i])
		return data
		
	
	#对所有数据进行缩放处理
	newrows = [matchrow(scaleinput(row.data)+[row.match]) for row in rows]
	
	#返回新的数据和缩放处理函数
	return newrows,scaleinput
	
def rbf(v1,v2,gamma = 20):
	"""径向基函数"""
	dv = [v1[i]-v2[i] for i in range(len(v1))]
	l = veclength(dv)
	return math.e ** (-gamma * l)
	
def nlclassify(point,rows,offset,gamma=10):
	"""非线性分类"""	
	sum0 = 0.0
	sum1 = 0.0
	count0 = 0
	count1 = 0
	
	for row in rows:
		if row.match == 0:
			sum0 += rbf(point,row.data,gamma)
			count0 += 1
		else:
			sum1 += rbf(point,row.data,gamma)
			count1 += 1
	y = (1.0 / count0) * sum0 - (1.0 / count1) * sum1 + offset
	if y > 0: return 0
	else: return 1

def getoffset(rows,gamma = 10):
	l0 = []
	l1 = []
	for row in rows:
		if row.match == 0: l0.append(row.data)
		else: l1.append(row.data)
		
	sum0 = sum(sum([rbf(v1,v2,gamma) for v1 in l0]) for v2 in l0)
	sum1 = sum(sum([rbf(v1,v2,gamma) for v1 in l1]) for v2 in l1)
	
	return (1.0/(len(l1) ** 2)) * sum1 - (1.0/len(l0) ** 2) * sum0
	

from sklearn import svm
#import numpy as np 
# X= [[1,0,1],[-1,0,-1]]   #训练集  
# y = [1,-1]   # 分类数据  
# clf = svm.SVC(C=10)  # 分类器  
# m = clf.fit(X, y)  # 训练SCV模型 
# print(m)
#result = clf.predict([[-0.8,-1]]) # 预测测试验本的分类  
#print(result)  # 分类
# print clf.support_vectors_  #支持向量 
# print clf.support_  # 支持向量的指标
# print clf.n_support_  # 每个类的支持向量数
	

#plotagematches(agesonly)

#线性分类
# avgs = lineartrain(agesonly)
# print(averages)
# print(dpclassify([30,30],avgs))
# print(dpclassify([30,25],avgs))
# print(dpclassify([25,40],avgs))
# print(dpclassify([48,20],avgs))

# numericalset = loadnumerical()
# scaledset,scalef = scaledata(numericalset)
# avgs = lineartrain(scaledset)
# print(numericalset[0].data)
# print(numericalset[0].match)
# print(dpclassify(scalef(numericalset[0].data),avgs))
# print(numericalset[11].match)
# print(dpclassify(scalef(numericalset[11].data),avgs))

#核技法
# offset = getoffset(agesonly)
# print(offset)
# print(nlclassify([30,30],agesonly,offset))
# print(nlclassify([30,25],agesonly,offset))
# print(nlclassify([25,40],agesonly,offset))
# print(nlclassify([48,20],agesonly,offset))

# numericalset = loadnumerical()
# scaledset,scalef = scaledata(numericalset)
# ssoffset = getoffset(scaledset)

# print(numericalset[0].match)
# print(nlclassify(scalef(numericalset[0].data),scaledset,ssoffset))
# print(numericalset[1].match)
# print(nlclassify(scalef(numericalset[1].data),scaledset,ssoffset))
# print(numericalset[2].match)
# print(nlclassify(scalef(numericalset[2].data),scaledset,ssoffset))

# newrow = [28.0,-1,-1,26.0,-1,1,2,0.8] #男士不想要小孩,而女士想要
# print(nlclassify(scalef(newrow),scaledset,ssoffset))

# newrow = [28.0,-1,1,26.0,-1,1,2,0.8] #双发都想要小孩
# print(nlclassify(scalef(newrow),scaledset,ssoffset))













