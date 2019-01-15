from math import tanh
import sqlite3

def dtanh(y):
	return 1.0 - y*y

class searchnet:
	def __init__(self,dbname):
		self.con = sqlite3.connect(dbname)
		
	def __del__(self):
		self.con.close()
	
	def dbcommit(self):
		self.con.commit()
		
	#创建数据库表
	def maketables(self):
		self.con.execute('create table hiddennode(create_key)')
		self.con.execute('create table wordhidden(fromid,toid,strength)')
		self.con.execute('create table hiddenurl(fromid,toid,strength)')
		self.dbcommit()

	def getstrength(self,fromid,toid,layer):
		"""判断链接强度
		对于从单词层到隐藏层的链接，其默认值将为 -0.2。所以在默认情况下，
		附加单词将会对处于隐藏层的节点在活跃度上产生轻微的负面影响。
		对于从隐藏层到URL的链接而言，方法返回的默认值为0"""
		if layer == 0: table = 'wordhidden'
		else: table = 'hiddenurl'
		res = self.con.execute('select strength from %s where fromid = %d and toid=%d ' %(table,fromid,toid)).fetchone()
		if res == None:
			if layer == 0: return -0.2
			if layer == 1: return 0
		return res[0]

	def setstrength(self,fromid,toid,layer,strength):
		"""用以判断链接是否已存在，并利用新的强度值更新链接或创建链接"""
		if layer == 0: table = 'wordhidden'
		else: table = 'hiddenurl'
		res = self.con.execute('select rowid from %s where fromid=%d and toid=%d' %(table,fromid,toid)).fetchone()
		if res == None:
			self.con.execute('insert into %s (fromid,toid,strength) values(%d,%d,%f)' %(table,fromid,toid,strength)) 
		else:
			rowid = res[0]
			self.con.execute('update %s set strength=%s where rowid=%d' % (table,strength,rowid))

	def generatehiddennode(self,wordids,urls):
		"""生成隐藏层 
		每传入一组以前从未见过的单词组合，该函数就会在隐藏层中建立一个新的节点。
		随后，函数会为单词与隐藏节点之间，以及查询节点与由查询所返回的URL结果之间，建立其具有默认权重的链接"""
		if len(wordids) > 3: return None
		#检查我们是否已经为这组单词建好了一节点
		createkey = '_'.join(sorted([str(wi) for wi in wordids]))
		res = self.con.execute("select rowid from hiddennode where create_key='%s'" % createkey).fetchone()
		
		#如果没有，则建立之
		if res == None:
			cur = self.con.execute("insert into hiddennode(create_key) values('%s')" % createkey)
			hiddenid = cur.lastrowid
			#设置默认权重
			for wordid in wordids:
				self.setstrength(wordid,hiddenid,0,1.0/len(wordids))
			for urlid in urls:
				self.setstrength(hiddenid,urlid,1,0.1)
			self.dbcommit()

	def getallhiddenids(self,wordids,urlids):
		"""从隐藏层中找出与某项查询相关的所有节点"""
		l1 = {}
		for wordid in wordids:
			cur = self.con.execute('select toid from wordhidden where fromid=%d ' % wordid)
			for row in cur: l1[row[0]] = 1
		for urlid in urlids:
			cur = self.con.execute('select fromid from hiddenurl where toid=%d' % urlid)
			for row in cur: l1[row[0]] = 1
		
		return list(l1.keys())

	def setupnetwork(self,wordids,urlids):
		"""该函数为searchnet类定义了多个实例变量，包括：单词列表、查询节点及URL，每个节点的输出级别，
		以及每个节点间连接的权重值"""
		#值列表
		self.wordids = wordids
		self.hiddenids = self.getallhiddenids(wordids,urlids)
		self.urlids = urlids
		
		#节点输出
		self.ai = [1.0] * len(self.wordids)
		self.ah = [1.0] * len(self.hiddenids)
		self.ao = [1.0] * len(self.urlids)
		
		#建立权重矩阵
		self.wi = [[self.getstrength(wordid,hiddenid,0) for hiddenid in self.hiddenids ] for wordid in self.wordids]
		self.wo = [[self.getstrength(hiddenid,urlid,1) for urlid in self.urlids ] for hiddenid in self.hiddenids]
		
	def feedforward(self):
		"""前馈算法，算法接受一列输入，将其推入网络，然后返回所有输出层节点的输出结果"""
		#查询单词是仅有的输入
		for i in range(len(self.wordids)):
			self.ai[i] = 1.0
		
		#隐藏层节点的活跃程度
		for j in range(len(self.hiddenids)):
			sum = 0.0
			for i in range(len(self.wordids)):
				sum = sum + self.ai[i] * self.wi[i][j]
				print("self.ai[%s]=%s self.wi[%s][%s]=%s \nsum=%s" % (i,self.ai[i],i,j,self.wi[i][j],sum))
			self.ah[j] = tanh(sum)
			print("self.ah[%s] = %s \n###########################" % (j,self.ah[j]))
		
		#输入层节点的活跃程度
		for k in range(len(self.urlids)):
			sum = 0.0
			for j in range(len(self.hiddenids)):
				sum = sum + self.ah[j] * self.wo[j][k]
				print("self.ah[%s]=%s self.wo[%s][%s]=%s \nsum=%s" % (j,self.ah[i],j,k,self.wo[i][j],sum))
			self.ao[k] = tanh(sum)
			print("self.ao[%s] = %s \n###########################" % (j,self.ah[j]))
		return self.ao[:]
		
	def getresult(self,wordids,urlids):
		self.setupnetwork(wordids,urlids)
		return self.feedforward()
		
	def backPropagate(self,targets, N=0.5):
		"""反向传播函数
		反向传播算法的执行步骤：
		对于输出层的每个节点：
		1.计算节点当前输出结果与期望结果之间的差距
		2.利用dtanh函数确定节点的总输入需要如何改变
		3.改变每个外部回指链接的强度值，其值域链接的当前强度及学习速率成一定比例
		对于每个隐藏层中的节点：
		1.将每个输出链接的强度值乘以其目标节点所需的该变量，再累加求和，从而改变节点的输出结果
		2.使用dtanh函数确定节点的总输入所需的该变量
		3.改变每个输入链接的强度值，其值于链接的当前强度及学习速率成一个比例。
		"""
		#计算输出层的误差
		output_deltas = [0.0] * len(self.urlids)
		for k in range(len(self.urlids)):
			error = targets[k] - self.ao[k]
			output_deltas[k] = dtanh(self.ao[k]) * error
			
		#计算隐藏层的误差
		hidden_deltas = [0.0] * len(self.hiddenids)
		for j in range(len(self.hiddenids)):
			error = 0.0 
			for k in range(len(self.urlids)):
				error = error + output_deltas[k] * self.wo[j][k]
			hidden_deltas[j] = dtanh(self.ah[j]) * error
			
		#更新输出权重
		for j in range(len(self.hiddenids)):
			for k in range(len(self.urlids)):
				change = output_deltas[k] * self.ah[j]
				self.wo[j][k] = self.wo[j][k] + N*change
				
		#更新输入权重
		for i in range(len(self.wordids)):
			for j in range(len(self.hiddenids)):
				change = hidden_deltas[j] * self.ai[i]
				self.wi[i][j] = self.wi[i][j] + N*change

	def trainquery(self,wordids,urlids,selectedurl):
		#如有必要，生成一个隐藏节点
		self.generatehiddennode(wordids,urlids)
		
		self.setupnetwork(wordids,urlids)
		self.feedforward()
		targets = [0.0] * len(urlids)
		targets[urlids.index(selectedurl)] = 1.0
		self.backPropagate(targets)
		self.updatedatabase()
		
	def updatedatabase(self):
		#将值存入数据库中
		for i in range(len(self.wordids)):
			for j in range(len(self.hiddenids)):
				
				self.setstrength(self.wordids[i],self.hiddenids[j],0,self.wi[i][j])
		for j in range(len(self.hiddenids)):
			for k in range(len(self.urlids)):
				self.setstrength(self.hiddenids[j],self.urlids[k],1,self.wo[j][k])
		self.dbcommit()
	
mynet = searchnet('nn.db')
#mynet.maketables()
wWorld,wRiver,wBank = 101,102,103
uWorldBank,uRiver,uEarth = 201,202,203
#mynet.generatehiddennode([wWorld,wBank],[uWorldBank,uRiver,uEarth])
#result = mynet.getresult([wWorld,wBank],[uWorldBank,uRiver,uEarth])

#mynet.trainquery([wWorld,wBank],[uWorldBank,uRiver,uEarth],uWorldBank)
#result = mynet.getresult([wWorld,wBank],[uWorldBank,uRiver,uEarth])
#print(result)

allurls = [uWorldBank,uRiver,uEarth]
#for i in range(30):
#	mynet.trainquery([wWorld,wBank],allurls,uWorldBank)
#	mynet.trainquery([wRiver,wBank],allurls,uRiver)
#	mynet.trainquery([wWorld],allurls,uEarth)

result = mynet.getresult([wWorld,wBank],allurls)
print(result)	

#result = mynet.getresult([wRiver,wBank],allurls)
#print(result)	

#result = mynet.getresult([wWorld],allurls)
#print(result)	



























































