
import os
import sys
import re
import urllib
import urllib.request
import urllib.parse
from html.parser import HTMLParser

#class AppURLopener(urllib.FancyURLopener):
#    version = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT)";

class MyHTMLParser(HTMLParser):
    '''
    网页解析生成一个HTMLParser的类，然后利用这个类，
    把给定的一个网址中所需要的地址解析并保存在该类中，
    然后利用该类的的地址，下载图片。
    '''
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
        pass
    def handle_starttag(self,tag,attrs):
        #print("Encountered a start tag:",tag)
        if tag == "img":
            s = []
            for (variable, value) in attrs:
                s.append(value)
            #print("ss:",s)
            self.links.append(s)
            s = []
        pass
     
    def handle_endtag(self,tag):
        #print("Encountered a end tag:",tag)
        pass   
    def handle_data(self,data):
        #print("Encountered some data:",data)
        pass

def geturl(url):
    '''
    打开给定的网页，并返回网页的内容,
    python3中来来是以字节码形式返回的，
    可以根据网页编码判定编码为gb2312,是gbk的子集，
    以字符串形式返回。
    '''
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
    req = urllib.request.Request(url=url, headers=headers)  
    return urllib.request.urlopen(req).read() 
 
def continsrc(src):
    '''
    根据网页的内容，找到我们所需要的内容，
    这里主要是有两个需要关注的内容，一个是picture标签，另一个是boxinfo标签。
    '''
    str = src.decode('utf-8');
    inta = str.find("[查看原图]</a><br />")
    #print(inta) #所找的第一个位置点
    intb = str.find("</p><div class=\"vote\"")
    #print(intb) 所找的第二个位置点
    content = str[inta:intb]
    return content
	
def pageinurl(url):
    '''
    这个是把上面的许多功能放在一个函数库里，方便操作。
    作用是给定一个url，自动去解析地址，并自动下载保存图片。
    '''
    src = geturl(url)
    content = continsrc(src)
    parser = MyHTMLParser()
    parser.feed(content)
    parser.close()
    alinks = parser.links
    x = 0
    print(alinks)
    for i in range(len(alinks)):
        #pass
        print(alinks[i][0])
        #print("filename:",alinks[i][0],"fileurl:",alinks[i][1])
		
        headers = [('Host','img0.imgtn.bdimg.com'),
			('Connection', 'keep-alive'),
			('Cache-Control', 'max-age=0'),
			('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
			('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'),
			('Accept-Encoding','gzip,deflate,sdch'),('Accept-Language', 'zh-CN,zh;q=0.8'),('If-None-Match', '90101f995236651aa74454922de2ad74'),
			('Referer','http://image.baidu.com/i?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&word=%E4%BA%A4%E9%80%9A&ie=utf-8'),
			('If-Modified-Since', 'Thu, 01 Jan 1970 00:00:00 GMT')]
        #filename = '%s.jpg' % x
        #data = ('Referer','http://image.baidu.com/i?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&word=%E4%BA%A4%E9%80%9A&ie=utf-8')
		
        urllib.request.urlretrieve(alinks[i][0],data=('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'))
        #headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
        #req = urllib.request.Request(url=alinks[i][0], headers=headers) 
        #urllib._urlopener = AppURLopener();		
        # urllib.request.urlretrieve(alinks[i][0])
        #url = alinks[i][0].encode();
        #req = urllib.request.Request(alinks[i][0], headers=headers) 
        #urllib.request.urlopen(req).urlretrieve()
        
		
		#opener = urllib.request.build_opener()
        #opener.addheaders = headers
        #data = opener.open(alinks[i][0])

# print(data)

        #path = str(x)+".jpg"  
        #f = open(path,"wb")  
        #f.write(data.read())  
        #f.close()
		
        x += 1

    print("ok!!")
	

	
if __name__ == "__main__":
    print("------------------------")
    url = "view-source:http://www.tianqihoubao.com/lishi/tianjin/month/201211.html"
    pageinurl(url)
	
	
	
	
	
	
	
	
	
	
	
	
	
 
