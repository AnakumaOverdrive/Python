from bs4 import BeautifulSoup
import requests
#from urlparse import urljoin
from urllib.parse import urljoin
import sqlite3
import jieba
import nn

mynet = nn.searchnet('nn.db')

session = requests.Session();
#请求头
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection':'keep-alive',
}

#构建一个单词列表，这些单词和符号将被忽略
ignorewords = set({'the','of','to','and','a','in','is','it','这','的','到','和','一个','在','是','它','得','地','啊',
' ','"','-','/',':','.','=',';','(',',',')','|','*','，','_','【','】','、','・','.....','“','┆','<','>','《','》',
'{','}','[',']','！',''})

class crawler:
	#初始化crawler类并传入数据库名称
	def __init__(self,dbname):
		self.con = sqlite3.connect(dbname)
		
	def __del__(self):
		self.con.close()
	
	def dbcommit(self):
		self.con.commit()
		
	#辅助函数，用于获取条目的id,并且如果条目不存在，就将其加入数据库中
	def getentryid(self,table,field,value,createnew=True):
		cur = self.con.execute("select rowid from %s where %s='%s' " % (table,field,value))
		res = cur.fetchone()
		if res == None:
			cur = self.con.execute("insert into %s (%s) values('%s')" % (table,field,value))
			return cur.lastrowid
		else:
			return res[0]

	#为每个网页建立索引
	def addtoindex(self,url,soup):
		if self.isindexed(url): return
		print('Indexing %s' % url)
		
		#获取每个单词
		text = self.gettextonly(soup)
		#print('####################################')
		#print(text)
		#print('####################################')
		words = self.separatewords(text)
		#得到URL的ID
		urlid = self.getentryid('urllist','url',url)
		
		#将每个单词与该URL关联
		try:
			for i in range(len(words)):
				word = words[i]
				#print(word,word in ignorewords)
				if word in ignorewords : continue
				wordid = self.getentryid('wordlist','word',word)
				self.con.execute('insert into wordlocation(urlid,wordid,location) values(%d,%d,%d)' % (urlid,wordid,i))
		except:
			pass
	#从一个HTML网页中提取文字（不带标签的）
	def gettextonly(self,soup):
		#print(soup)
		v = soup.string
		if v == None:
			c = soup.contents
			resulttext = ''
			for t in c:
				#t = str(t,'utf-8')
				subtext = self.gettextonly(t)
				resulttext += subtext #+ '\n'
			return resulttext
		else:	
			return v.strip()
		
	#根据任何非空白字符进行分词处理
	def separatewords(self,text):
		words = jieba.cut(text,cut_all = False)
		lowerWord =  [word.lower() for word in words if word != '']
		return lowerWord
		
	#如果url已经建过索引，则返回true
	def isindexed(self,url):
		u = self.con.execute("select rowid from urllist where url = '%s' " %url).fetchone()

		if u != None:
			#检查它是否已经被检索过了
			v = self.con.execute('select * from wordlocation where urlid=%d ' % u[0]).fetchone()
			if v != None: return True
		return False
	
	#添加一个关联两个网页的链接
	def addlinkref(self,urlFrom,urlTo,linkText):
		words=self.separatewords(linkText)
		fromid=self.getentryid('urllist','url',urlFrom)
		toid=self.getentryid('urllist','url',urlTo)
		if fromid==toid: return
		cur=self.con.execute("insert into link(fromid,toid) values (%d,%d)" % (fromid,toid))
		linkid=cur.lastrowid
		for word in words:
			if word in ignorewords: continue
			wordid=self.getentryid('wordlist','word',word)
			self.con.execute("insert into linkwords(linkid,wordid) values (%d,%d)" % (linkid,wordid))
			
	#从一小组网页开始进行广度优先检索，直至某一给定深度，期间为网页建立索引
	def crawl(self,pages,depth=2):
		for i in range(depth):
			newpages=set()
			for page in pages:
				try:
					c = session.get(page,headers = {
						'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
						'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
						'Connection':'keep-alive',
						'Referer': page
					})
				except:
					print('Could not open %s' % page)
					continue
				soup = BeautifulSoup(c.text,"html.parser")
				self.addtoindex(page,soup)
				
				links = soup.findAll("a")
				for link in links:
					if 'href' in link.attrs:
						url = urljoin(page,link['href'])
						if url.find("'") != -1:continue
						url = url.split('#')[0] #去掉位置部分
						if url[0:4] == 'http' and not self.isindexed(url):
							newpages.add(url)
							#pass
							#print(url)
						linkText = self.gettextonly(link)
						self.addlinkref(page,url,linkText)
						
				self.dbcommit()
			pages=newpages
		
	#创建数据库表
	def createindextables(self):
		self.con.execute('create table urllist(url)')
		self.con.execute('create table wordlist(word)')
		self.con.execute('create table wordlocation(urlid,wordid,location)')
		self.con.execute('create table link(fromid integer,toid integer)')
		self.con.execute('create table linkwords(wordid,linkid)')
		self.con.execute('create index wordidx on wordlist(word)')
		self.con.execute('create index urlidx on urllist(url)')
		self.con.execute('create index wordurlidx on wordlocation(wordid)')
		self.con.execute('create index urltoidx on link(toid)')
		self.con.execute('create index urlfromidx on link(fromid)')
		self.dbcommit()

	def calculatpagerank(self,iterations=20):
		"""计算PageRank值"""
		#清除当前的PageRank表
		self.con.execute('drop table if exists pagerank')
		self.con.execute('create table pagerank(urlid primary key,score)')
		
		#初始化每个url，令其PageRank值为1
		self.con.execute('insert into pagerank select rowid,1.0 from urllist')
		self.dbcommit()
		#阻尼因子
		d = 0.85
		for i in range(iterations):
			print('iterations %d' % (i))
			for (urlid,) in self.con.execute('select rowid from urllist'):
				pr = 1-d
				
				#循环遍历指向当前网页的所有其他网页
				for (linker,) in self.con.execute('select distinct fromid from link where toid=%d' % urlid):
					#得到链接源对应网页的PageRank值
					linkingpr = self.con.execute('select score from pagerank where urlid = %d ' %linker).fetchone()[0]
					
					#根据链接源，求得总的链接数
					linkingcount = self.con.execute('select count(*) from link where fromid=%d ' % linker).fetchone()[0]
					#PageRank值的计算
					pr+=0.85*(linkingpr/linkingcount)
					print(linkingpr,linkingcount,pr)
				self.con.execute('update pagerank set score=%f where urlid=%d ' %(pr,urlid))
			self.dbcommit()
					
class searcher:
	def __init__(self,dbname):
		self.con = sqlite3.connect(dbname)
		
	def __del__(self):
		self.con.close()
		
	def getmatchrows(self,q):
		"""得到匹配的行"""
		#构造查询的字符串
		fieldlist = 'w0.urlid'
		tablelist = ''
		clauselist = ''
		wordids = []
		#根据空格拆分单词
		words = q.split(' ')
		tablenumber = 0
		
		for word in words:
			#获取单词的ID
			wordrow = self.con.execute("select rowid from wordlist where word = '%s' " % word).fetchone()
			if wordrow != None:
				wordid = wordrow[0]
				wordids.append(wordid)
				if tablenumber > 0 :
					tablelist += ' '
					clauselist += ' and  '
					clauselist += 'w%d.urlid=w%d.urlid and ' % (tablenumber - 1,tablenumber)
				fieldlist += ',w%d.location' % tablenumber
				tablelist += 'wordlocation w%d,' % tablenumber
				clauselist += 'w%d.wordid=%d' %(tablenumber,wordid)
				tablenumber += 1
		if len(tablelist) > 0:
			tablelist = tablelist[0:len(tablelist)-1]
		#根据各个组分，建立查询
		fullquery = 'select %s from %s where %s ' % (fieldlist,tablelist,clauselist)
		print(fullquery)
		cur = self.con.execute(fullquery)
		rows = [row for row in cur]
		
		return rows,wordids

	def getscoredlist(self,rows,wordids):
		"""该方法将接受查询请求，将获取的行集置于字典中，并以格式化列表的形式显示输出。"""
		totalscores = dict([(row[0],0.0) for row in rows])
		
		#此处是稍后放置评价函数的地方
		#使用单词频度评价函数
		#weights = [(1.0,self.frequencyscore(rows))]
		#使用文档位置评价函数
		#weights = [(1.0,self.locationscore(rows))]
		
		#使用几种度量分别匹配不同的权重
		weights=[(1.0,self.locationscore(rows)), 
             (1.0,self.frequencyscore(rows)),
             (1.0,self.pagerankscore(rows)),
             (1.0,self.linktextscore(rows,wordids)),
             (5.0,self.nnscore(rows,wordids))]
			 
		#print(weights)
		for (weight,scores) in weights:
			for url in totalscores:
				#print(weight,scores[url],weight * scores[url])
				totalscores[url] = weight * scores[url]

		return totalscores
		
	def geturlname(self,id):
		return self.con.execute("select url from urllist where rowid=%d" % id).fetchone()[0]
	
	def query(self,q):
		rows,wordids = self.getmatchrows(q)
		scores = self.getscoredlist(rows,wordids)
		rankedscores = sorted([(score,url) for (url,score) in scores.items()],reverse=True)
		for (score,urlid) in rankedscores[0:20]:
			print('%f\t%s' % (score,self.geturlname(urlid)))
		return wordids,[r[1] for r in rankedscores[0:10]]
		
			
	def normalizescores(self,scores,smallIsBetter=0):
		"""归一化函数
		令事情变得复杂化的是，有的评价方法分值越大越好，而有的则分值越小越好。
		为了对不同方法的返回值结果进行比较，我们需要一种对结果进行归一化处理的方法，
		即，令它们具有相同的值域及变化方向
		"""
		vsmall = 0.00001 #避免被零整除
		if smallIsBetter:
			#分值越小越好
			minscore = min(scores.values())
			return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) in scores.items()])
		else:
			#分值越大越好
			maxscore = max(scores.values())
			if maxscore == 0: maxscore = vsmall
			return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])
	
	def frequencyscore(self,rows):
		"""单词频度
		该函数建立了一个字段，其中包含了为行集中每个唯一的URL ID所建的条目，
		函数还对每个单词的出现次数进行了计数，随后又对评价值做了归一化处理。
		（在本例中，分值越大越好），并返回结果。
		"""
		counts = dict([(row[0],0) for row in rows])
		for row in rows: counts[row[0]] +=1
		return self.normalizescores(counts)
		
	def locationscore(self,rows):
		"""文档位置"""
		locations = dict([(row[0],1000000) for row in rows])
		for row in rows:
			loc = sum(row[1:])
			if loc < locations[row[0]]:
				locations[row[0]] = loc
		return self.normalizescores(locations,smallIsBetter=1)
	
	def distancescore(self,rows):
		"""单词距离"""
		#如果仅有一个单词，则得分都一样
		if len(rows[0]) <= 2: return dict([(row[0],1.0)] for row in rows)
		
		#初始化字典，并填入一个很大的数
		mindistace = dict([(row[0],1000000) for row in rows])
		for row in rows:
			dist =sum([abs(row[i] - row[i-1]) for i in range(2,len(row))])
			if dist < mindistace[row[0]] : mindistace[row[0]] = dist
		return self.normalizescores(mindistace,smallIsBetter=1)
	
	def inboundlinkscore(self,rows):
		"""简单计数"""
		uniqueurls = set([row[0] for row in rows])
		inboundcount = dict([(u,self.con.execute('select count(*) from link where toid=%d' % u).fetchone()[0]) for u in uniqueurls])
		return self.normalizescores(inboundcount)
		
	def pagerankscore(self,rows):
		"""PageRank值"""
		rpageranks = dict([(row[0],self.con.execute('select score from pagerank where urlid=%d' % row[0]).fetchone()[0]) for row in rows])
		maxrank = max(rpageranks.values())
		normalizescores = dict([(u,float(l)/maxrank) for (u,l) in rpageranks.items()])
		
		return normalizescores
		
	def linktextscore(self,rows,wordids):
		"""利用链接文本"""
		linkscores = dict([(row[0],0) for row in rows])
		for wordid in wordids:
			cur = self.con.execute('select link.fromid,link.toid from linkwords,link where wordid=%d and linkwords.linkid = link.rowid ' % wordid)
			for (fromid,toid) in cur:
				if  toid in linkscores:
					pr = self.con.execute('select score from pagerank where urlid=%d' % fromid).fetchone()[0]
					linkscores[toid] += pr
		maxscore=max(linkscores.values())
		normalizescores = dict([(u,float(l)/maxscore) for (u,l) in linkscores.items()])
		return normalizescores
			
	def nnscore(self,rows,wordids):
		"""神经网络"""
		#获得一个唯一的URL ID构成的有序列表
		urlids = [urlid for urlid in set([row[0] for row in rows])]
		nnres = mynet.getresult(wordids,urlids)
		scores=dict([(urlids[i],nnres[i]) for i in range(len(urlids))])
		return self.normalizescores(scores)
			
pages = ['http://www.85781.com/beijing/index_1.html']
#初始化创建数据库		
crawler = crawler('searchindex.db')
#创建表
#crawler.createindextables()
#爬取数据
#crawler.crawl(pages)
#计算PageRank值
#crawler.calculatpagerank()

e = searcher('searchindex.db')
#result = e.getmatchrows('天津')
#print(result)
wordids, = e.query('天津')
#mynet.trainquery(result)
print(result)


print('end')		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		