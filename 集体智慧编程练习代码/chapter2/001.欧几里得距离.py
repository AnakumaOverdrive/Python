 # A dictionary of movie critics and their ratings of a small
 # set of movies

print('欧几里得距离')

from math import sqrt
import recommendations

#d = sqrt(pow(critics['Toby']['Snakes on a Plane'] - critics['Mick LaSalle']['Snakes on a Plane'],2)+pow(critics['Toby']['You, Me and Dupree']-critics['Mick LaSalle']['You, Me and Dupree'],2))
#print(d)
#d = 1 / (1 + sqrt(pow(critics['Toby']['Snakes on a Plane'] - critics['Mick LaSalle']['Snakes on a Plane'],2)+pow(critics['Toby']['You, Me and Dupree']-critics['Mick LaSalle']['You, Me and Dupree'],2)))
#print(d)

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

print(sim_distance(recommendations.critics,'Lisa Rose','Gene Seymour'))









