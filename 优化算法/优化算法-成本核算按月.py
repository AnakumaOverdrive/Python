import time,random,math,numpy

itemsInfo = {}
#总金额
TotalPrice = 1500000
#总工期
TotalTimeLimit = 3
#人员成本
PersonnelCost = 12000
#项目模块名称及权重 
Items =[('基础数据融合平台',9),
('大数据分析平台',8),
('自定义工作流平台',7),
('自定义报表统计平台',5),
('综合数据交换平台',2)]

#人员姓名及人天成本 
#PersonnelCost = [('PersonA',800),('PersonB',500),('PersonC',750),('PersonD',900),('PersonE',550),('PersonF',800)]
#人员成本
#Personnel = ['PersonA','PersonB','PersonC','PersonD','PersonE','PersonF']


print("总金额",TotalPrice)
print("总工期(天)",TotalTimeLimit)
print("人员成本(人月)",PersonnelCost)
print("")

def calculationTotalWeight(Items):
	"""计算模块的总权重"""
	TotalWeight = 0
	for item in Items:
		TotalWeight +=item[1]
	return TotalWeight
	
def randomDistribution():
	itemDay = []
	itemCost = []
	itemPerson = []
	totalTimeDay = 0
	totalItemCost = 0
	p25 = 0
	
	#计算模块的总权重.
	TotalWeight = calculationTotalWeight(Items);
	#根据模块的权重推算用人的天数.天数结果四舍六入五成双.
	for item in Items:
		itemWeight = item[1] / TotalWeight #+ random.uniform(0,0.2)
		
		timeWeight = TotalTimeLimit * itemWeight
		#print(timeWeight)
		itemDay.append([item[0],timeWeight])
		totalTimeDay += timeWeight
		
		costWeight = TotalPrice * itemWeight
		#p75 = costWeight * 0.75
		#p25 += costWeight * 0.25
		itemCost.append([item[0],round(costWeight,-3)])
		totalItemCost += round(costWeight,-3)
		
	#print(itemDay)
	#将推演的天数的总数与实际总数比较,如果多出的天数则随机填入到项目天数中.
	differenceDay = TotalTimeLimit - totalTimeDay
	randomNum = random.randint(0,len(Items)-1);+
	#print(itemDay[randomNum],differenceDay)
	itemDay[randomNum][1] = itemDay[randomNum][1] + differenceDay * 1.0
	#print(itemDay)
	
	#推算成本的总数与实际成本比较,如果多出的成本则随机填入到项目成本中.
	#print(itemCost)
	differenceCost = TotalPrice - totalItemCost
	randomNum = random.randint(0,len(Items)-1);
	#print(itemCost[randomNum],differenceCost)
	itemCost[randomNum][1] = itemCost[randomNum][1] + differenceCost * 1.0
	#print(itemCost)
	
	#print(itemDay)
	#print(itemCost)
	#print(round(p25,-3) / len(Items))
	result = []
	# #根据模块需要的天数,模块成本,人员成本推算所需要的人数.
	for itemi in itemCost:
		key = itemi[0]
		cost = itemi[1]
		for itemj in itemDay:
			if itemj[0] == key:
				day = itemj[1]
				personNum = round(cost / day / PersonnelCost,1)
				reCost = personNum * day * PersonnelCost
				dValue = cost - reCost
				#print([key,cost - dValue,int(day),int(personNum)])
				result.append([key,cost - dValue,day,int(personNum)])
	
	return result
	
def printResults(sol):
	#tempStr = "%+8s\t%+8s\t%+8s\t%+8s\t" 
	tempStr = "%+8s\t%+8s\t%+8s\t" 
	#print(tempStr % ("模块名称","模块单价","工期(月)","人数"))
	print(tempStr % ("模块名称","模块单价","工期(月)"))
	for item in sol:
		#print(tempStr %(item[0],item[1],item[2] ,item[3]))
		print(tempStr %(item[0],item[1],item[2]))
	
#print(round(19888,-3))
	
#randomDistribution();
	

def ProjectCost(sol):
	"""成本函数"""
	pers = []
	#人数数组
	for item in sol:
		if item[3] < 0:
			return 9999
		elif item[2] == 1:
			return 8888
		else:
			pers.append(item[3])
	print(pers,numpy.var(pers),1 / numpy.var(pers))
	variance = numpy.var(pers)
	if variance != 0 :
		return 1 / numpy.var(pers)	
	else:
		return 1
	
# for i in range(10):
	# print("")
	# print(ProjectCost(randomDistribution()));

	
def randomoptimize(domain,costf):
	"""随机搜索"""
	best = 999999999
	bestr = None
	for i in range(0,1000):
		#创建一个随机解
		r = randomDistribution()
		#得到成本
		cost = costf(r)
		#与到目前为止的最优解进行比较
		if cost < best:
			best = cost
			bestr = r	
	#print(best)
	return r
	
domain = randomDistribution()
s = randomoptimize(domain,ProjectCost)
printResults(s)

# def test():
	# s = randomoptimize(domain,ProjectCost)
	# print(ProjectCost(s))
	# printProjectCost(s)
	# if ProjectCost(s) > 7000: test()
# test()

# #print(randomlist)


 