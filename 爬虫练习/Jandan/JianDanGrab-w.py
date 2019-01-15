from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests,time,random,datetime,math,re

random.seed(datetime.datetime.now())
pages = set()
session = requests.Session();
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection':'keep-alive',
    
    }

def downImage(src,prefix = ""):
    global session
    req = session.get(src,headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Referer': src
    })
    req = session.get(src,headers = headers)
    fileName = prefix + src[src.rindex("/")+1:]
    print(fileName)
    with open(fileName,"wb") as code:
        code.write(req.content)
    time.sleep(0.1);

def CalculateWeight(oo,xx):
    return int(oo) - int(xx) >200

def RandallWilson(u,v):
    n = u + v
    if n == 0 :
        return False
    else:
        z = 1.96
        phat = u / n
        score = (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n))/n)) / ( 1 + z * z /n)
        return score > 0.9

def Wilson(u,v):
    n = u + v
    if n == 0 :
        return 0
    else:
        z = 1.96
        phat = u / n
        score = (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n))/n)) / ( 1 + z * z /n)
        return score

def GetMiddleStr(content,startStr,endStr):
    patternStr = r'%s(.+?)%s'%(startStr,endStr)
    p = re.compile(patternStr,re.IGNORECASE)
    m= re.match(p,content)
    if m:
        return m.group(1)
		
		
def getLinks(pageUrl,pageNum="0"):
    global pages
    global headers
    global session
    req = session.get(pageUrl,headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Referer': pageUrl
    })
    try:
        bsObj = BeautifulSoup(req.text,"html.parser")
    except:
        print("没有找到页面")
    else:
        if(bsObj == None):
            return
        if len(bsObj.findAll("div",{"class":"vote"})) == 0:
            return

        for div in bsObj.findAll("div",{"class":"vote"}):
            if div == None:
                return
            if 'id' in div.attrs:
                oo = div.find("a",{"class":"acvclick acv4"}).find_next_sibling().get_text()
                xx = div.find("a",{"class":"acvclick acva"}).find_next_sibling().get_text()
                if RandallWilson(float(oo),float(xx)):
                    img = div.parent.find("a",{"class":"view_img_link"})
                    if img == None:
                        return
                    if 'href' in img.attrs:
                        wilsonStr = round(Wilson(float(oo),float(xx)),2)
                        prefix = "[{1}_{2}-{3}_p{0}]".format(pageNum,wilsonStr,oo,xx)
                        imgeurl = img.attrs["href"];
                        downImage(imgeurl,prefix);

URL= "http://jandan.net/pic/page-"
RANGENUM = range(9435,9440)

#URL= "http://jandan.net/ooxx/page-"
#RANGENUM = range(2030,2040)
                                        
#getLinks(URL);

for i in RANGENUM:
    url = URL + str(i) + "#comments"
    print(url);
    getLinks(url,str(i));
    time.sleep(5);


        





