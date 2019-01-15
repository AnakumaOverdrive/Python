from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests,time,random,datetime,math,re,sys,json,urllib

random.seed(datetime.datetime.now())
pages = set()
session = requests.Session();
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection':'keep-alive',
    
    }
key423 = "KYPBZ-GI53D-ULA4B-HZE6C-6V5WS-YKBLJ"
key527 = "CKZBZ-PRGWX-DOW46-7VVD3-426P3-TSFD4"
keyzj = "Z6QBZ-OONRX-ZOH44-742TE-2EHPK-ORBYT"
queryUrl = "http://apis.map.qq.com/ws/geocoder/v1/?address=%(address)s&key="+key423


def Address2Location(address):
    time.sleep(0.21);
    pageUrl = queryUrl % {"address":urllib.parse.quote(address)}
    response = urlopen(pageUrl).read().decode("utf-8")

    responseJson = json.loads(response)
    if responseJson.get("status") == 0 :
        result = responseJson.get("result")
        title = result.get("title")
        lng = result.get("location").get("lng")
        lat = result.get("location").get("lat")
        return "|"+str(lng)+"|"+str(lat) +"|"+title
    else:
        return "|"+""+"|"+"" +"|"+""

def getLinks(pageUrl,pageNum="0"):
    global pages
    global headers
    global session
    Returns = []
    
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
        if len(bsObj.findAll("ul",{"class":"list"})) == 0:
            return
        ul = bsObj.find("ul",{"class":"list"})
        fd = open("天津黄页信息.txt","a")
        for li in ul.findAll("li"):
            try:
                name = li.find("a").get_text()
                lists = str(li).split("<br/>")
                if len(lists) > 2:
                    strs = lists[1]
                    tel = strs[strs.index("】")+1:strs.rindex("【")]
                    address  = strs[strs.rindex("】")+1:]
                    strwrite = name + "|" + tel + "|"+address+Address2Location(address) +"\n\r"
                    fd.write(strwrite)
            except:
                print(pageUrl)
                print(li)
        fd.close()

URL= "http://www.85781.com/tianjin/index_"
RANGENUM = range(967,973)

for i in RANGENUM:
    url = URL + str(i) + ".html"
    print(url);
    getLinks(url,str(i));

#s = Address2Location("天津市南开区密云路裕达欣园")
#print(s)
#Address2Location("12313")





