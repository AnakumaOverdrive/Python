from random import random,randint
import math
import optimization
from pylab import *

def wineprice(rating,age):
	"""葡萄酒价格"""
	peak_age = rating - 50
	
	#根据等级来计算价格
	price = rating / 2
	if age > peak_age:
		#经过"峰值年",后续5年里其品质将会变差
		price = price * (5 - (age-peak_age))
	else:
		#价格在接近"峰值年"时会增加到原值的5倍
		price = price * (5 * ((age + 1) / peak_age))
		
	if price < 0: price=0
	return price
	
def wineset1():
	rows = []
	for i in range(300):
		#随机生成年代和等级
		rating = random() * 50 + 50
		age = random() * 50
		
		#得到一个参考价格
		price = wineprice(rating,age)
		
		#增加"噪声"
		price *= (random() * 0.2 + 0.9)
		
		#加入数据集
		rows.append({'input':(rating,age),'result':price})
	
	return rows
	
def euclidean(v1,v2):
	"""欧几里得距离"""
	d = 0.0
	for i in range(len(v1)):
		d+=(v1[i]-v2[i])**2
	return math.sqrt(d)
	
def getdistances(data,vec1):
	distancelist = []
	for i in range(len(data)):
		vec2 = data[i]['input']
		distancelist.append((euclidean(vec1,vec2),i))
	distancelist.sort()
	return distancelist
	
def knnestimate(data,vec1,k=5):
	"""k最近邻算法的估计"""
	#得到经过排序的距离值
	dlist = getdistances(data,vec1)
	avg = 0.0
	
	#对前k项结果求平均
	for i in range(k):
		idx = dlist[i][1]
		avg += data[idx]['result']
	avg = avg / k
	return avg
	
def inverseweight(dist,num=1.0,const=0.1):
	"""反函数"""
	#print("%s / (%s + %s) = %s" %( num,dist,const,num / (dist+const)))
	return num / (dist+const)
	
def subtractweight(dist,const = 1.0):
	"""减法函数"""
	if dist > const:
		return 0
	else:
		return const - dist
		
def gaussian(dist,sigma=10.0):
	"""高斯函数"""
	return math.e ** (-dist**2/(2*sigma**2))
	
def weightedknn(data,vec1,k=5,weightf=gaussian):
	"""权重knn"""
	#得到距离
	dlist = getdistances(data,vec1)
	avg = 0.0
	totalweight= 0.0
	
	#得到加权平均值
	for i in range(k):
		dist = dlist[i][0]
		idx = dlist[i][1]
		weight = weightf(dist)
		#avg += data[idx]['result'] #书籍中的勘误.
		avg += weight*data[idx]['result']
		totalweight += weight
	if totalweight == 0 : return 0
	avg = avg / totalweight
	#print(avg)
	return avg
	
def dividedata(data,test=0.05):
	"""拆分数据集"""
	trainset = []
	testset = []
	for row in data:
		if random() < test:
			testset.append(row)
		else:
			trainset.append(row)
	return trainset,testset
	
def testalgorithm(algf,trainset,testset):
	error = 0.0
	for row in testset:
		guess = algf(trainset,row['input'])
		error += (row['result'] - guess) ** 2
	#print(error , len(testset),error / len(testset))
	return error / len(testset)
	
def crossvalidate(algf,data,trials=100,test=0.1):
	"""交叉验证"""
	error = 0.0
	for i in range(trials):
		trainset,testset = dividedata(data,test)
		error += testalgorithm(algf,trainset,testset)
	#print(error , trials,error / trials)
	return error / trials

def wineset2():
	rows = []
	for i in range(300):
		#随机生成年代和等级
		rating = random() * 50 + 50
		age = random() * 50
		
		#通道号
		aisle = float(randint(1,20))
		#瓶子的大小 毫升
		bottlesize = [375.0,750.0,1500.0,3000.0][randint(0,3)]
		
		#得到一个参考价格
		price = wineprice(rating,age)
		price *= (bottlesize / 750 )
		#增加"噪声"
		price *= (random() * 0.9 + 0.2)
		
		#加入数据集
		rows.append({'input':(rating,age,aisle,bottlesize),'result':price})
	
	return rows

def rescale(data,scale):
	"""重新调整"""
	scaledddata = []
	for row in data:
		scaled = [ scale[i] * row['input'][i] for i in range(len(scale))]
		scaledddata.append({'input':scaled,'result':row['result']})
	return scaledddata
	
def createcostfunction(algf,data):
	def costf(scale):
		sdata = rescale(data,scale)
		return crossvalidate(algf,sdata,trials=10)
	return costf
	
weightdomain = [(0,20)] * 4


def wineset3():
	rows = wineset1()
	for row in rows:
		if random() < 0.5:
			#葡萄酒是从折扣店购得的
			#row['result'] *= 0.5
			row['result'] *= 0.6
	return rows
	
def probguess(data,vec1,low,high,k=5,weightf=gaussian):
	""""""
	dlist = getdistances(data,vec1)
	nweight = 0.0
	tweight = 0.0
	
	for i in range(k):
		dist = dlist[i][0]
		idx = dlist[i][1]
		weight = weightf(dist)
		v = data[idx]['result']
		
		#当前数据点位于指定范围内吗
		if v >= low and  v <= high:
			nweight += weight
		tweight+=weight
	if tweight == 0 : return 0
	
	#概率等于位于指定范围内的权重值除以所有权重值
	return nweight / tweight
	
def cumulativegrabh(data,vec1,high,k=5,weightf=gaussian):
	t1 = arange(0.0,high,0.1)
	cprob = array([probguess(data,vec1,0,v,k,weightf) for v in t1])
	plot(t1,cprob)
	show()
	
def probabilitygraph(data,vec1,high,k=5,weightf=gaussian,ss=5.0):
	"""概率图"""
	#建立一个代表价格的值域范围
	t1 = arange(0.0,high,0.1)
	
	#得到整个值域范围内的所有概率
	probs = [probguess(data,vec1,v,v+0.1,k,weightf) for v in t1]
	
	#通过加上近邻概率的高斯计算结果,对概率值做平滑处理
	smoothed = []
	for i in range(len(probs)):
		sv = 0.0
		for j in range(0,len(probs)):
			dist = abs(i-j) * 0.1
			weight = gaussian(dist,sigma = ss)
			sv += weight * probs[j]
		smoothed.append(sv)
	smoothed = array(smoothed)
	
	plot(t1,smoothed)
	show()
	
	
#print(wineset1())
# print(wineprice(95.0,3.0))
# print(wineprice(95.0,8.0))
# print(wineprice(95.0,1.0))
# print(wineprice(99.0,1.0))

# data = wineset1()
# v1 = data[0]['input']
# v2 = data[1]['input']
# print(v1)
# print(v2)
# print(euclidean(v1,v2))

# data = wineset1()
# print(knnestimate(data,(95.0,3.0)))
# print(knnestimate(data,(99.0,3.0)))
# print(knnestimate(data,(99.0,5.0)))
# print(wineprice(99.0,5.0)) #得到实际价格
# print(knnestimate(data,(99.0,5.0),k=5)) #尝试更少的近邻
# print(knnestimate(data,(99.0,5.0),k=4)) #尝试更少的近邻
# print(knnestimate(data,(99.0,5.0),k=3)) #尝试更少的近邻
# print(knnestimate(data,(99.0,5.0),k=2)) #尝试更少的近邻
# print(knnestimate(data,(99.0,5.0),k=1)) #尝试更少的近邻

# print(subtractweight(0.1))
# print(inverseweight(0.1))
# print(gaussian(0.1))
# print(gaussian(1.0))
# print(subtractweight(1.0))
# print(inverseweight(1.0))
# print(gaussian(3.0))

# data = wineset1()
# print(wineprice(99.0,5.0))
# print(knnestimate(data,(99.0,5.0)))
# print(weightedknn(data,(99.0,5.0)))

#data = wineset1()
# print(crossvalidate(knnestimate,data))

# def knn3(d,v): return knnestimate(d,v,k=3)
# print(crossvalidate(knn3,data))

# def knn1(d,v): return knnestimate(d,v,k=1)
# print(crossvalidate(knn1,data))

# print(crossvalidate(weightedknn,data))
# def knninverse(d,v): 
	# return weightedknn(d,v,weightf=inverseweight)
# print(crossvalidate(knninverse,data))

#data = wineset2()
#print(data)

# def knn3(d,v): return knnestimate(d,v,k=3)
# print(crossvalidate(knn3,data))
# print(crossvalidate(weightedknn,data))

# sdata = rescale(data,[10,10,0,0.5])
# print(crossvalidate(knn3,data))
# print(crossvalidate(weightedknn,data))

#costf = createcostfunction(knnestimate,data)
# result = optimization.annealingoptimize(weightdomain,costf,step=2)
# print(result)
#[17, 13, 0, 20]

# result = optimization.geneticoptimize(weightdomain,costf,step=2)
# print(result)
#[7, 6, 5, 13]

#不对称分布
# data = wineset3()
# print(wineprice(99.0,20.0))
# print(weightedknn(data,[99.0,20.0]))

#估计概率密度
# data = wineset3()
# print(probguess(data,[99,20],40,80))
# print(probguess(data,[99,20],80,120))
# print(probguess(data,[99,20],120,1000))
# print(probguess(data,[99,20],30,1200))

#绘制概率分布
# a = array([1,2,3,4])
# b = array([4,3,2,1])
# plot(a,b)
# show()
# t1 = arange(0.0,10.0,0.1)
# print(t1)
# plot(t1,sin(t1))
# show()

data = wineset3()
# cumulativegrabh(data,(1,1),120)

probabilitygraph(data,(1,1),6)



























