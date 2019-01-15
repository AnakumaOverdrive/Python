 # A dictionary of movie critics and their ratings of a small
 # set of movies
critics = {
	'Lisa Rose': {
		'Lady in the Water': 2.5,
		'Snakes on a Plane': 3.5,
		'Just My Luck': 3.0,
		'Superman Returns': 3.5,
		'You, Me and Dupree': 2.5,
		'The Night Listener': 3.0
	},
	'Gene Seymour': {
		'Lady in the Water': 3.0,
		'Snakes on a Plane': 3.5,
		'Just My Luck': 1.5,
		'Superman Returns': 5.0,
		'The Night Listener': 3.0,
		'You, Me and Dupree': 3.5
	},
	'Michael Phillips': {
		'Lady in the Water': 2.5,
		'Snakes on a Plane': 3.0,
		'Superman Returns': 3.5,
		'The Night Listener': 4.0
	},
	'Claudia Puig': {
		'Snakes on a Plane': 3.5,
		'Just My Luck': 3.0,
		'The Night Listener': 4.5,
		'Superman Returns': 4.0,
		'You, Me and Dupree': 2.5
	},
	'Mick LaSalle': {
		'Lady in the Water': 3.0,
		'Snakes on a Plane': 4.0,
		'Just My Luck': 2.0,
		'Superman Returns': 3.0,
		'The Night Listener': 3.0,
		'You, Me and Dupree': 2.0
	},
	'Jack Matthews': {
		'Lady in the Water': 3.0,
		'Snakes on a Plane': 4.0,
		'The Night Listener': 3.0,
		'Superman Returns': 5.0,
		'You, Me and Dupree': 3.5
	},
	'Toby': {
		'Snakes on a Plane': 4.5,
		'You, Me and Dupree': 1.0,
		'Superman Returns': 4.0
	}
}

from math import sqrt
import csv

def transformPrefs(prefs):
	"""转换函数"""
	result = {}
	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item,{})
			#将物品和人员对调
			result[item][person] = prefs[person][item]
	return result;
	
def sim_distance(perfs,person1,person2):
	"""返回一个有关person1与person2的基于距离的相似度评价 (欧几里得距离)"""
	si={} #得到shared_items的列表
	for item in perfs[person1]:
		#print(item)
		if item in perfs[person2]:
			si[item] = 1
	#如果两者没有共同之处，则返回0
	if len(si) == 0: return 0
	
	#计算所有差值的平方和
	sum_of_squares = sum([
		pow(perfs[person1][item]-perfs[person2][item],2) 
		for item in perfs[person1] if item in perfs[person2]
	]);

	return 1 / (1 + sqrt(sum_of_squares));
	
def sim_pearson(perfs,person1,person2):
	"""返回一个有关person1与person2的基于距离的相似度评价 (皮尔逊相关系数)"""
	si={} #得到shared_items的列表
	for item in perfs[person1]:
		#print(item)
		if item in perfs[person2]:
			si[item] = 1
	
	#得到列表元素的个数
	n = len(si)
	
	#如果两者没有共同之处，则返回0
	if n == 0: return 0
	
	#对所有偏好求和
	sum1 = sum([perfs[person1][it] for it in si])
	sum2 = sum([perfs[person2][it] for it in si])
	
	#求平方和
	sum1Sq =sum([pow(perfs[person1][it],2) for it in si ])
	sum2Sq =sum([pow(perfs[person2][it],2) for it in si ])
	
	#求乘积之和
	pSum = sum([perfs[person1][it] * perfs[person2][it] for it in si])
	
	#计算皮尔逊评价值
	num = pSum - (sum1*sum2/n);
	den = sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
	if den ==0: return 0
	
	r = num/den
	return r;

def sim_tonimoto(prefs,person1,person2):
	"""返回一个有关person1与person2的基于距离的相似度评价 (杰卡德系数)"""
	si={} #得到shared_items的列表
	for item in prefs[person1]:
		#print(item)
		if item in prefs[person2]:
			si[item] = 1
			
	#如果两者没有共同之处，则返回0
	if len(si) == 0: return 0
	
	na = len(prefs[person1])
	nb = len(prefs[person2])
	nc = len([ v for v in prefs[person1] if v in prefs[person2]])
	t = float(nc)/(na + nb - nc)
	
	return t;
	
def topMatches(perfs,person,n=5,similarity=sim_pearson):
	"""从反映偏好的字典中返回最为匹配者
	返回结果的个数和相似度函数均为可选参数"""
	scores = [(similarity(perfs,person,other),other) for other in perfs if other != person]
	
	#队列表进行排序，评价值最高者排在最前面
	scores.sort() #升序排序
	scores.reverse() #颠倒列表 --> 降序排序
	return scores[0:n]

def calculatsSimilarItems(prefs,n=10):
	"""计算物品相似项"""
	#建立字典，以给出与这些物品最为相近的所有其他物品
	result = {} 
	#以物品为中心对偏好矩阵实施倒置处理
	itemPrefs = transformPrefs(prefs)
	c=0
	for item in itemPrefs:
		#针对大数据集更新状态变量
		c+=1
		if c%100 ==0 :print("%d / %d" % (c,len(itemPrefs)))
		#寻找最为相近的物品
		scores = topMatches(itemPrefs,item,n=n,similarity = sim_distance)
		result[item] = scores
	return result;
	
def calculatsSimilarUsers(prefs,n=10):
	"""计算用户的相似项"""
	#建立字典，以给出与这些物品最为相近的所有其他物品
	result = {}
	c=0
	for item in prefs:
		#针对大数据集更新状态变量
		c+=1
		if c%100 ==0 :print("%d / %d" % (c,len(prefs)))
		#寻找最为相近的用户
		scores = topMatches(prefs,item,n=n,similarity = sim_distance)
		result[item] = scores
	return result;	
	
def getRecommendations(prefs,person,similarity=sim_pearson):
	"""利用所有他人评价值的加权平均，为某人提供建议"""
	totals = {}
	simSums = {}
	for other in prefs:
		#不要和自己作比较
		if other == person : continue
		sim = similarity(prefs,person,other)
		#print(sim)
		#忽略评价值为零或小于零的情况
		if sim <= 0 : continue	
		for item in prefs[other]:
			#只对自己还未曾看过的影片进行评价
			if item not in prefs[person] or prefs[person][item] == 0:
				#相似度*评价值
				totals.setdefault(item,0)#如果字典中包含有给定键，则返回该键对应的值，否则返回为该键设置的值。
				totals[item] += prefs[other][item] * sim

				#相似度之和
				simSums.setdefault(item,0)
				simSums[item] += sim;
				
	#建立一个归一化的列表
	rankings = [(total/simSums[item],item) for item,total in totals.items()]
		
	#返回经过排序的列表
	rankings.sort();
	rankings.reverse();
	return rankings;
	
def getRecommendedItems(prefs,itemMatch,user):
	"""获得推荐项"""
	userRatings = prefs[user]
	scores = {}
	totalSim = {}
	print(userRatings)
	#循环遍历由当前用户评分的物品
	for (item,rating) in userRatings.items():
		#循环遍历与当前物品相近的物品
		for (similarity,item2) in  itemMatch[item]:
			#如果该用户已经对当前物品做过评价，则将其忽略
			print(item2)
			print(item2 in userRatings)
			if item2 in userRatings: continue
			
			#评价值与相似度的加权之和
			scores.setdefault(item2,0)
			scores[item2] += similarity * rating
			
			#全部相似度之和
			totalSim.setdefault(item2,0)
			totalSim[item2] += similarity
	
	#将每个合计值除以加权和，求出平均值
	rankings = [(score/totalSim[item],item) for item,score in scores.items()]

	#按最高值到最低值的顺序，返回评分结果
	rankings.sort()
	rankings.reverse()
	return rankings
	
def getRecommendedUsers(prefs,itemMatch,user):
	"""获得推荐项"""
	totals = {}
	simSums = {}
	
	for (sim,other) in itemMatch[user]:
		for item in prefs[other]:
			if item not in prefs[user] or prefs[user][item] == 0:
				#相似度*评价值
				totals.setdefault(item,0)#如果字典中包含有给定键，则返回该键对应的值，否则返回为该键设置的值。
				totals[item] += prefs[other][item] * sim

				#相似度之和
				simSums.setdefault(item,0)
				simSums[item] += sim;
	
	#建立一个归一化的列表
	rankings = [(total/simSums[item],item) for item,total in totals.items()]
		
	#返回经过排序的列表
	rankings.sort();
	rankings.reverse();
	return rankings;
#itemsim = calculatsSimilarItems(critics)
#print(getRecommendedItems(critics,itemsim,'Toby'))	

def loadMovieLens(path='data/movielens'):
	""""""
	#获取影片的标题
	movies={}
	csv_reader = csv.reader(open(path+'/movies.csv'))
	for line in csv_reader:
		id = line[0]
		title = line[1]
		movies[id] = title

	#加载数据
	prefs = {}
	csv_reader = csv.reader(open(path+'/ratings.csv')) 
	header=True
	for line in csv_reader:
		#跳过首行
		if header == True :
			header = False
			continue;
		user = line[0]
		movieid = line[1]
		rating = float(line[2])
		prefs.setdefault(user,{})
		prefs[user][movies[movieid]]= rating
	return prefs

#装载数据
#prefs = loadMovieLens();	
#用户的评分	
#print(prefs['87'])
#基于用户的推荐
#print(getRecommendations(prefs,'87')[0:5])
#基于物品的推荐
#itemsim = calculatsSimilarItems(prefs)
#print(getRecommendations(prefs,'87')[0:5])

#itemsim = calculatsSimilarItems(critics)
#print(getRecommendedItems(critics,itemsim,'Toby'))	

#print(getRecommendations(critics,'Toby',similarity=sim_tonimoto))
#itemsim = calculatsSimilarUsers(critics)
#print(getRecommendedUsers(critics,itemsim,'Toby'))		
	
	
	
	
	
	
	
	
	
	
	
	