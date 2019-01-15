import re
import jieba

jieba.load_userdict("dict.txt.small")

#构建一个单词列表，这些单词和符号将被忽略
ignorewords = set({'the','of','to','and','a','in','is','it','这','的','到','和','一个','在','是','它','得','地','啊',
' ','"','-','/',':','.','=',';','(',',',')','|','*','，','_','【','】','、','・','.....','“','┆','<','>','《','》',
'{','}','[',']','！','',
 '测试','对','的','内','网','新','果磊','，','张贺','一天','sun','、','洪德','下站','mcu','大','166','瑞','市','外','和','。',
 '四楼','路','一','二','机','（','1','；','2','3','）','专','第','次','分','所','局','楼','铁','城','孟','到','41','-','42','号',
 '后','应','50','万','凌','中','从','因','时','前','都','咱','签','在','保','与','14','已','道','许','地','为','9','日','及','11',
 '需','双','单','7','/','4','74','台','给','谷工','各','断','是','被','讯','飞','并','10','过','将','李','20','苏明开','月','8',':','30',
 '17','孙书记','仪','处','卡','6',',','张跃民','耿小宁','寸','不','10.120','.','232.47','48','509','李建洲','尹建广','李晓楠','会','睿',
 '眼','向','好','至','up','由','了','全','主','9.71','深','宋木楠','ap','无','非','碰','曹','桥','卫','吴庄变','看','?','','甯','',
 '套','占','满','做','门','e','湖','天津','：','上','云','园','控','管','件','拉','布','12','称','连','景','65','天津市','87','易振良',
 '5','天','胡','直','陈','下','个','32','出','按','以','f5','21','c','u','口','通','港','滨','海','点','电','屏','开','幺','南','蔡','高',
 '票','表','且','组','a','本','b','172.20','36.62','未' ,'等'
})
	
def getWordsCn(html):
	"""中文分词"""
	#去除所有HTML标记
	txt = re.compile(r'<[^>]+>').sub('',html)
	#利用结巴分词
	#words = jieba.cut(txt,cut_all = True)
	words = jieba.cut(txt)
	#print(words)
	#转换成小写形式
	return [word.lower() for word in words if word != '']

def getwordcounts(text):
	wc = {}
	try:
		words = getWordsCn(text)
		for word in words:
			wc.setdefault(word,0)
			wc[word] += 1
	except Exception:
		print(' getwordcounts Error',e)
	
	return wc

def clearHiddenChar(text):
	"""去除换行符"""
	return text.replace('\r', '').replace("\n", "").split("\t")
	
def encodeUtf8(text):
	return text.encode("utf-8")
	

result= {}
wordcounts = {}
apcount = {}
eventInfo = [clearHiddenChar(line) for line in open('eventInfo.txt','r',encoding='utf-8',errors='ignore')]
for (level,detail) in eventInfo:
	result.setdefault(level,"")
	result[level]+=detail
	
for (level,text) in result.items():
	wc = {}
	words = getWordsCn(text)
	for word in words:
		if word in ignorewords : continue
		wc.setdefault(word,0)
		wc[word] += 1
	wordcounts[level] = wc
	for word,count in wc.items():
		apcount.setdefault(word,0)
		if count > 1 :
			apcount[word] += 1


			
wordlist = []
for w,bc in apcount.items():
	frac = float(bc) / 4.0
	#if frac >=.25 and frac <=.75:
	if frac >=.75:
		wordlist.append(w)

print(len(wordlist))
	
out = open('text.txt',"wb+")
wordf = open('word.txt',"wb+")
out.write(encodeUtf8('Blog'))
for word in wordlist:
	out.write(encodeUtf8('\t%s' % word.replace('\r', '').replace("\n", "")))
	wordf.write(encodeUtf8('\n%s' % word.replace('\r', '').replace("\n", "")))

out.write(encodeUtf8('\n'))

for blog,wc in wordcounts.items():
	out.write(encodeUtf8(blog))
	for word in wordlist:
		if word in wc:
			out.write(encodeUtf8('\t%d' % wc[word]))
		else:
			out.write(encodeUtf8('\t0'))
	
	out.write(encodeUtf8('\n'))
	

out.close();	

		
