import time,random,math

# people = [('Seymour','BOS'),
# ('Franny','DAL'),
# ('Zooey','CAK'),
# ('Walt','MIA'),
# ('Buddy','ORD'),
# ('Les','OMA')]

# destination = 'LGA'

# flights = {}

# for line in open('schedule.txt'):
	# origin,dest,depart,arrive,price = line.strip().split(',')
	# flights.setdefault((origin,dest),[])
	# #将航班详情添加到航班列表中
	# flights[(origin,dest)].append((depart,arrive,int(price)))

def getminutes(t):
	x = time.strptime(t,'%H:%M')
	return x[3]*60 + x[4]

def printschedule(r):
	for d in range(int(len(r)/2)):
		name = people[d][0]
		origin = people[d][1]
		out = flights[(origin,destination)][r[d]]
		ret = flights[(destination,origin)][r[d+1]]
		print('%10s%10s %5s-%5s $%3s %5s-%5s $%3s' %(name,origin,out[0],out[1],out[2],ret[0],ret[1],ret[2]))

def schedulecost(sol):
	"""进度成本"""
	totalprice = 0
	#最晚到达时间
	latestarrival = 0
	#最早离开时间
	earlinestdep = 24 * 60

	for d in range(int(len(sol) / 2)):
		#得到往程航班和返程航班
		origin = people[d][1]
		outbound = flights[(origin,destination)][int(sol[d])]
		reurnf = flights[(destination,origin)][int(sol[d+1])]
		
		#总价格等于所有往程航班和返程航班之和
		totalprice += outbound[2]
		totalprice += reurnf[2]
		
		#记录最晚到达时间和最早离开时间
		if latestarrival < getminutes(outbound[1]): latestarrival = getminutes(outbound[1])
		if earlinestdep > getminutes(reurnf[0]): earlinestdep = getminutes(reurnf[0])
		

	#每个人必须在机房等待直到最后一个人到达为止
	#他们也必须在相同时间达到,并等候他们的返程航班
	totalwait = 0
	for  d in range(int(len(sol) / 2)):
		origin = people[d][1]
		outbound = flights[(origin,destination)][int(sol[d])]
		reurnf = flights[(destination,origin)][int(sol[d+1])]
		totalwait += latestarrival-getminutes(outbound[1])
		totalwait += getminutes(reurnf[0]) - earlinestdep
		#print(outbound[1],latestarrival-getminutes(outbound[1]), reurnf[0],getminutes(reurnf[0]) - earlinestdep)
	
	#这个题解要求多付一天的汽车租用费用吗?如果是,则费用为50美元
	if latestarrival > earlinestdep: totalprice += 50
	
	return totalprice + totalwait
	
def randomoptimize(domain,costf):
	"""随机搜索"""
	best = 999999999
	bestr = None
	for i in range(0,1000):
		#创建一个随机解
		r = [random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
		#得到成本
		cost = costf(r)
		
		#与到目前为止的最优解进行比较
		if cost < best:
			best = cost
			bestr = r
			
	return r

def hillclimb(domain,costf):
	"""爬山法"""
	#创建一个随机解
	sol = [random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
	
	#主循环
	while 1:
		#创建相邻解的列表
		neighbors=[]
		for j in range(len(domain)):
			#在每个方向上相对于原值偏离一点
			if sol[j] > domain[j][0]:
				neighbors.append(sol[0:j]+[sol[j]-1] + sol[j+1:])
			if sol[j] < domain[j][1]:
				neighbors.append(sol[0:j]+[sol[j]+1] + sol[j+1:])
		
		#在相邻解中寻找最优解
		current = costf(sol)
		best = current
		for j in range(len(neighbors)):
			cost = costf(neighbors[j])
			if cost < best:
				best = cost
				sol = neighbors[j]
		if best == current:
			break
	return sol
	
def annealingoptimize(domain,costf,T=10000.0,cool=0.99,step=1):
	"""退火优化"""
	#随机初始化值
	vec = [random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
	
	while T > 0.1:
		#选择一个索引值
		i = random.randint(0,len(domain) -1)

		#选择一个改变索引值的方向
		dir = random.randint(-step,step)
		
		#创建一个代表题解的新列表,改变其中一个值
		vecb = vec[:]
		vecb[i] += dir
		if vecb[i] < domain[i][0]: vecb[i] = domain[i][0]
		elif vecb[i] > domain[i][1]: vecb[i] = domain[i][1]
		
		#计算当前成本和新的成本
		ea = costf(vec)
		eb = costf(vecb)
		
		#它是更好的解吗?或者是趋向最优解的可能的临界解吗?
		if (eb < ea or random.random() < pow(math.e,-(eb-ea) /T)):
			vec = vecb
			
		#降低温度
		T = T*cool
		
	return vec

def geneticoptimize(domain,costf,popsize=100,step=1,mutprob=0.5,elite=0.2,mexiter=20):
	"""遗传算法优化
	popsize	种群大小
	mutprob	种群的新成员是由变异而非交叉得来的概率
	elite	种群中被认为是优解且被允许传入下一代的部分
	mexiter	需运行多少代"""
	#变异操作
	def mutate(vec):
		i = random.randint(0,len(domain)-1)
		if domain[i][0] == domain[i][1]:
			return vec
		else:
			if vec[i] > domain[i][0]:
				return vec[0:i] + [vec[i]-step] + vec[i+1:]
			else:
				return vec[0:i] + [vec[i]+step] + vec[i+1:]
	
	#交叉操作
	def crossover(r1,r2):
		i = random.randint(1,len(domain)-2)
		return r1[0:i]+r2[i:]
		
	#构造初始种群
	pop = []
	for i in range(popsize):
		vec = [random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
		pop.append(vec)
	
	#每一代中有多少胜出者
	topelite = int(elite * popsize)
	
	#主循环
	for i in range(mexiter):
		scores = [ (costf(v),v) for v in pop]
		scores.sort()
		ranked = [ v for (s,v) in scores]
		
		#从纯粹的胜出者开始
		pop = ranked[0:topelite]
		
		#添加变异和配对的胜出者
		while len(pop) < popsize:
			if random.random() < mutprob:
				#变异
				c = random.randint(0,topelite)
				pop.append(mutate(ranked[c]))
			else:
				#交叉
				c1 = random.randint(0,topelite)
				c2 = random.randint(0,topelite)
				pop.append(crossover(ranked[c1],ranked[c2]))
		
		#打印当前最优值
		#print(scores[0][0])
	return scores[0][1]
		
#print(flights)

#s = [1,4,3,2,7,3,6,3,2,4,5,3]
#print(schedulecost(s))
#printschedule(s)

#domain = [(0,9)] *(len(people)*2)

# def test():
	
	# s = randomoptimize(domain,schedulecost)
	# print(schedulecost(s))
	# printschedule(s)
	# if schedulecost(s) > 3500: test()
#test()

#s = hillclimb(domain,schedulecost)
#print(schedulecost(s))
#printschedule(s)

#s = annealingoptimize(domain,schedulecost)
#print(schedulecost(s))
#printschedule(s)

#s = geneticoptimize(domain,schedulecost)
#print(schedulecost(s))
#printschedule(s)


























