import re,math
import jieba

#jieba.load_userdict("dict.txt.big")
jieba.load_userdict("dict.txt.small")
def getwords(doc):
	words =[s.lower() for s in jieba.cut(doc,cut_all = True)]
	#只返回一组不重复的单词
	return dict([(w,1) for w in words])

def sampletrain(c1):
	c1.train('Nobody owns the water.','good')
	c1.train('the quick rabbit jumps fences','good')
	c1.train('buy pharmaceuticals now','bad')
	c1.train('make quick money at the online casino','bad')
	c1.train('the quick brown fox jumps','good')
	
class classifier:
	"""分类过滤
	getfeatures 分类函数,是从即将被归类的内容项中提取出的特征"""
	def __init__(self,getfeatures,filename=None):
		#统计特征/分类组合的数量 记录位于各分类中的不同特征的数量
		#如 {'nobody': {'good': 1}, 'owns': {'good': 1}, 'the': {'good': 3, 'bad': 1}, 'water': {'good': 1}, '': {'good': 1}, 'quick': {'good': 2, 'bad': 1}, 'rabbit': {'good': 1}, 'jumps': {'good': 2}, 'fences': {'good': 1}, 'buy': {'bad': 1}, 'pharmaceuticals': {'bad': 1}, 'now': {'bad': 1}, 'make': {'bad': 1}, 'money': {'bad': 1}, 'in': {'bad': 1}, 'online': {'bad': 1}, 'casino': {'bad': 1}, 'brown': {'good': 1}, 'fox': {'good': 1}}
		self.fc = {}
		#统计每个分类中的文档数量 记录各分类被使用次数的字典
		#如 {'good': 3, 'bad': 2}
		self.cc = {}
		self.getfeatures = getfeatures
		
	def incf(self,f,cat):
		"""增加对特征/分类组合的计数值"""
		self.fc.setdefault(f,{})
		self.fc[f].setdefault(cat,0)
		self.fc[f][cat] += 1
		#print(self.fc)
		
	def incc(self,cat):
		"""增加对某一分类的计数值"""
		self.cc.setdefault(cat,0)
		self.cc[cat] += 1
		#print(self.cc)
		
	def fcount(self,f,cat):
		"""某一特征出现于某一分类中的次数"""
		if f in self.fc and cat in self.fc[f]:
			return float(self.fc[f][cat])
		return 0.0
		
	def catcount(self,cat):
		"""属于某一分类的内容项数量"""
		if cat in self.cc:
			return float(self.cc[cat])
		return 0
		
	def totalcount(self):
		"""所有内容项的数量"""
		return sum(self.cc.values())
		
	def categories(self):
		"""所有分类的列表"""
		return self.cc.keys()
		
	def train(self,item,cat):
		features = self.getfeatures(item)
		#针对该分类为每个特征增加计数值
		for f in features:
			#print(f,cat)
			self.incf(f,cat)
			
		#增加针对该分类的计数值
		self.incc(cat)
	
	def fprob(self,f,cat):
		if self.catcount(cat) ==0: return 0
		#特征在分类中出现的总次数,除以分种类中包含内容项的总数
		return self.fcount(f,cat) / self.catcount(cat)
		
	def weightwdprob(self,f,cat,prf,weight=1.0,ap=0.5):
		#计算当前的概率值
		basicprob = prf(f,cat)
		
		#统计特征在所有分类中出现的次数
		totals = sum([(self.fcount(f,c)) for c in self.categories()])
		
		#计算加权平均
		bp = ((weight*ap)+(totals*basicprob))/(weight+totals)
		return bp

class naivebayes(classifier):
	def __init__(self,getfeatures):
		classifier.__init__(self,getfeatures)
		self.thresholds = {}

	def setthreshold(self,cat,t):
		"""设置阈值"""
		self.thresholds[cat] = t
		
	def getthreshold(self,cat):
		"""获得阈值"""
		if cat not in self.thresholds : return 1.0
		return self.thresholds[cat]
		
	"""贝叶斯方法"""
	def docprob(self,item,cat):
		"""提取特征(单词)并将所有单词的概率值乘以求出整体概率"""
		features = self.getfeatures(item)
		#将所有特征的概率相乘
		p = 1
		for f in features:
			p *= self.weightwdprob(f,cat,self.fprob)
		return p
		
	def prob(self,item,cat):
		"""用于计算分类的概率,并且返回P(文档|分类)与P(分类)的乘积"""
		#P(文档)
		catprob = self.catcount(cat) /self.totalcount()
		#P(文档|分类)
		docprob = self.docprob(item,cat)
		
		return catprob * docprob
	
	def classify(self,item,default=None):
		"""该方法将计算每个分类的概率,从中得出最大值,并将其与次大概率值进行对比,确定是否超过了规定的阈值.
		如果没有任何一个分类满足上述条件,方法就返回默认值"""
		probs = {}
		#寻找概率最大的分类
		max = 0.0 
		for cat in self.categories():
			probs[cat] = self.prob(item,cat)
			if probs[cat] > max:
				max = probs[cat]
				best = cat
		
		#确保概率值超出阈值*次大概率值
		for cat in probs:
			if cat == best: continue
			if probs[cat] * self.getthreshold(best) > probs[best]:
				return default
		return best

class fisherclassifier(classifier):
	"""费舍尔分类"""
	
	def __init__(self,getfeatures):
		classifier.__init__(self,getfeatures)
		self.minimums = {}
		
	def setminimum(self,cat,min):
		"""设置临界值"""
		self.minimums[cat] = min
	
	def getminimum(self,cat):
		"""获取临界值"""
		if cat not in self.minimums: return 0
		return self.minimums[cat]

	def cprob(self,f,cat):
		"""针对特征的分类概率"""
		#特征在该分类中出现的频率
		clf = self.fprob(f,cat)
		if clf == 0 : return 0
		
		#特征在所有分类中出现的频率
		freqsum = sum([self.fprob(f,c) for c in self.categories()])
		
		#概率等于特征在该分类中出现的频率除以总体频率
		p = clf/(freqsum)
		return p
		
	def fisherprob(self,item,cat):
		"""费舍尔概率"""
		#将所有概率值相乘
		p = 1
		features = self.getfeatures(item)
		for f in features:
			p *= (self.weightwdprob(f,cat,self.cprob))
			
		#取自然对数,并乘以-2
		fscore = -2 * math.log(p)
		
		#利用倒置对数卡方函数求得概率
		return self.invchi2(fscore,len(features) * 2)
		
	def invchi2(self,chi,df):
		"""倒置对数卡方函数"""
		m = chi / 2.0
		sum  = term = math.exp(-m)
		for i in range(1, df // 2):
			print(m,i,m/i)
			term *= m / i
			sum += term
		print(min(sum,1.0))
		return min(sum,1.0)
	
	def classify(self,item,default=None):
		#循环遍历并寻找最佳结果
		best = default
		max = 0.0
		for c in self.categories():
			p = self.fisherprob(item,c)
			#确保其超过下限值
			if p > self.getminimum(c) and p > max:
				best = c
				max = p
		return best
			
#c1 = classifier(getwords)
#c1.train('the quick brown fox jumps over the lazy dog','good')
#c1.train('make quick money in the online casino','bad')
# fcount = c1.fcount('quick','good')
# print(fcount)
# fcount = c1.fcount('quick','bad')
# print(fcount)

# c1 = classifier(getwords)
#sampletrain(c1)
#print(c1.totalcount())
#print(c1.categories())
# fprob = c1.weightwdprob('money','good',c1.fprob)
# print(fprob)
# sampletrain(c1)
# fprob = c1.weightwdprob('money','good',c1.fprob)
# print(fprob)

# c1 = naivebayes(getwords)
# sampletrain(c1)
# print(c1.prob('quick rabbit','good'))
# print(c1.prob('quick rabbit','bad'))


# c1 = naivebayes(getwords)
# sampletrain(c1)
# print(c1.classify('quick rabbit',default='unknown'))
# print(c1.classify('quick money',default='unknown'))
# c1.setthreshold('bad',3.0)
# print(c1.classify('quick money',default='unknown'))
# for i in range(10):
	# sampletrain(c1)
# print(c1.classify('quick money',default='unknown'))

# c1 = fisherclassifier(getwords)
# sampletrain(c1)
# print(c1.cprob('quick','good'))
# print(c1.cprob('quick','bad'))
# print(c1.cprob('money','good'))
# print(c1.cprob('money','bad'))
# print(c1.weightwdprob('money','bad',c1.cprob))

# c1 = fisherclassifier(getwords)
# sampletrain(c1)
# print(c1.cprob('quick','good'))
# print(c1.fisherprob('qucik rabbit','good'))
# print(c1.fisherprob('qucik rabbit','bad'))

c1 = fisherclassifier(getwords)
sampletrain(c1)
print(c1.classify('quick rabbit'))
print(c1.classify('money'))
c1.setminimum('bad',0.8)
print(c1.classify('qucik money'))
# print(c1.classify('qucik money'))












		
