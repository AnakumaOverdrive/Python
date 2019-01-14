import time,random,math

itemsInfo = {}
#总金额
TotalPrice = 100000
#总工期
TotalTimeLimit = 10
#项目模块名称及权重
Items =[('ItemA',5),
('ItemB',3),
('ItemC',2),
('ItemD',1),
('ItemE',2),
('ItemF',3),
('ItemJ',2),
('ItemH',5)]
#人员姓名及人天成本
PersonnelCost = [('PersonA',800),('PersonB',500),('PersonC',750),('PersonD',900),('PersonE',550),('PersonF',800)]

TotalWeight = 0;
for item in Items:
	TotalWeight +=item[1]

for item in Items:
	itemWeight = item[1] / TotalWeight
	itemsInfo.setdefault(item[0],[])
	itemsInfo[item[0]].append((TotalPrice * itemWeight,TotalTimeLimit * itemWeight))
	#print(item,item[0],item[1])
#print(itemsInfo)


def ProjectCost(sol):
	totalprice = 0
	for	i in range(len(itemsInfo)):
		person = sol[i]
		item = Items[i]
		info = itemsInfo[item[0]]
		#模块的计划成本
		planCost = info[0][0]
		#模块需要天数
		day = info[0][1]
		#人员的每天需要的成本
		personCost = PersonnelCost[person][1]
		#实际成本
		actualCost = personCost * day
		totalprice += actualCost
	return totalprice


def printProjectCost(r):
	obj = {}
	for	i in range(len(itemsInfo)):
		person = r[i]
		item = Items[i]
		print("项目:%s 人员:%s" % (item[0],PersonnelCost[person][0]))
		
	
def randomoptimize(domain,costf):
	"""随机搜索"""
	best = 999999999
	bestr = None
	for i in range(0,1000):
		#创建一个随机解
		r = [random.randint(0,len(PersonnelCost)-1) for _ in range(len(Items))]
		#得到成本
		cost = costf(r)
		
		#与到目前为止的最优解进行比较
		if cost < best:
			best = cost
			bestr = r
	print(r)		
	return r
	
domain = [random.randint(0,len(PersonnelCost)-1) for _ in range(len(Items))]
print(domain)
def test():
	s = randomoptimize(domain,ProjectCost)
	print(ProjectCost(s))
	printProjectCost(s)
	if ProjectCost(s) > 7000: test()
test()

#print(randomlist)


 