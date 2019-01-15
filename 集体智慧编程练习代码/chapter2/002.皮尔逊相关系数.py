 # A dictionary of movie critics and their ratings of a small
 # set of movies

print('皮尔逊相关系数')

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

print(sim_pearson(recommendations.critics,'Lisa Rose','Gene Seymour'))






















