 # A dictionary of movie critics and their ratings of a small
 # set of movies

print('推荐物品')

critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

from math import sqrt
from decimal import *

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

print(getRecommendations(critics,'Toby',similarity=sim_pearson))
print('#########################')
print(getRecommendations(critics,'Toby',similarity=sim_distance))
















