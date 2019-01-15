
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
    ��ҳ��������һ��HTMLParser���࣬Ȼ����������࣬
    �Ѹ�����һ����ַ������Ҫ�ĵ�ַ�����������ڸ����У�
    Ȼ�����ø���ĵĵ�ַ������ͼƬ��
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
    �򿪸�������ҳ����������ҳ������,
    python3�����������ֽ�����ʽ���صģ�
    ���Ը�����ҳ�����ж�����Ϊgb2312,��gbk���Ӽ���
    ���ַ�����ʽ���ء�
    '''
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
    req = urllib.request.Request(url=url, headers=headers)  
    return urllib.request.urlopen(req).read() 
 
def continsrc(src):
    '''
    ������ҳ�����ݣ��ҵ���������Ҫ�����ݣ�
    ������Ҫ����������Ҫ��ע�����ݣ�һ����picture��ǩ����һ����boxinfo��ǩ��
    '''
    str = src.decode('utf-8');
    inta = str.find("[�鿴ԭͼ]</a><br />")
    #print(inta) #���ҵĵ�һ��λ�õ�
    intb = str.find("</p><div class=\"vote\"")
    #print(intb) ���ҵĵڶ���λ�õ�
    content = str[inta:intb]
    return content
	
def pageinurl(url):
    '''
    ����ǰ��������๦�ܷ���һ������������������
    �����Ǹ���һ��url���Զ�ȥ������ַ�����Զ����ر���ͼƬ��
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
	
	
	
	
	
	
	
	
	
	
	
	
	
 
