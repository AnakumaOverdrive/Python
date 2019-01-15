 # A dictionary of movie critics and their ratings of a small
 # set of movies

print('匹配最佳人员')

from math import sqrt
import recommendations

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

def topMatches(perfs,person,n=5,similarity=sim_pearson):
	"""从反映偏好的字典中返回最为匹配者
	返回结果的个数和相似度函数均为可选参数"""
	scores = [(similarity(perfs,person,other),other) for other in perfs if other != person]
	
	#队列表进行排序，评价值最高者排在最前面
	scores.sort() #升序排序
	scores.reverse() #颠倒列表 --> 降序排序
	return scores[0:n]


print(topMatches(recommendations.critics,'Toby',n=6))
print('##############################')
movies = recommendations.transformPrefs(recommendations.critics);
print(topMatches(movies,'Superman Returns',n=6))

















