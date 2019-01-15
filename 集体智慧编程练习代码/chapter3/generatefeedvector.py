import feedparser
import re
import jieba

def getwordcounts(url):
	"""返回一个RSS订阅源的标题和包含单词计数情况的字典"""
	#解析订阅源
	d = feedparser.parse(url)
	wc = {}
	
	#寻缘遍历所有的文章条目
	for e in d.entries:
		#print(e)
		#print('######################')
		if 'summary' in e: 
			summary = e.summary
		else:
			summary = e.description
			
		#提取一个单词列表
		#words = e.title+' '+summary
		try:
			words = getWordsCn(e.title+' '+summary)
			for word in words:
				wc.setdefault(word,0)
				wc[word] += 1
		except Exception:
			print(' getwordcounts Error',e)
	try:
		return d.feed.title,wc
	except Exception:
		print(d)
		return d.title,wc
def getwords(html):
	""""""
	#去除所有HTML标记
	txt = re.compile(r'<[^>]+>').sub('',html)
	#利用所有非字母字符拆分出单词
	words = re.compile(r'[^A-Z^a-z]+').split(txt)
	#print(words)
	#转换成小写形式
	return [word.lower() for word in words if word != '']
	
def getWordsCn(html):
	"""中文分词"""
	#去除所有HTML标记
	txt = re.compile(r'<[^>]+>').sub('',html)
	#利用结巴分词
	words = jieba.cut(txt,cut_all = True)
	#print(words)
	#转换成小写形式
	return [word.lower() for word in words if word != '']
#print(getwordcounts('http://jandan.net/feed'))
#print(getwordcounts('http://rss.slashdot.org/Slashdot/slashdot'))

apcount = {}
wordcounts = {}
feedlist = [line for line in open('feedlist.txt')]
for feedurl in feedlist:
	print(feedurl)
	title,wc = getwordcounts(feedurl)
	wordcounts[title] = wc
	for word,count in wc.items():
		apcount.setdefault(word,0)
		if count > 1 :
			apcount[word] += 1
	#break;

wordlist = []
for w,bc in apcount.items():
	frac = float(bc) / len(feedlist)
	#print(bc,len(feedlist),frac)
	if frac > 0.1 and frac < 0.5:
		wordlist.append(w)

#print(apcount)
print('######################')
#print(wordcounts)
print('######################')
#print(wordlist)
print('######################')
		
out = open('text.txt',"w")
out.write('Blog')
for word in wordlist:
	out.write('\t%s' % word.replace('\r', '').replace("\n", ""))
out.write('\n')

for blog,wc in wordcounts.items():
	try:
		out.write(blog)
		for word in wordlist:
			try:
				if word in wc:
					out.write('\t%d' % wc[word])
				else:
					out.write('\t0')
			except Exception:
				print("word Error")
		out.write('\n')
	except Exception:
		print("blog,wc Error")

out.close();	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	