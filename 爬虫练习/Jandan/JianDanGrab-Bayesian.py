from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import time
import random
import datetime

random.seed(datetime.datetime.now())
pages = set()
session = requests.Session();
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection':'keep-alive',
    
    }

def stf(s):
    if s.startswith('0') or '.' in s and len(s.split('.')[-1]) > 2 or s == '0':
        return 0
    
    return float(s)

def CalculateWeight(oo,xx):
    if oo - xx > 100.0:
         s = oo + xx
         print("s:",s)
         return (oo/s)*(1/2)/(xx/s) > 10
    else:
         return False;

    

def getLinks(pageUrl):
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
                print(oo,xx)
                print(CalculateWeight(stf(oo),stf(xx)))
                
    
getLinks("http://jandan.net/pic/page-");

for i in range(9204,9219):
    url = "http://jandan.net/pic/page-" + str(i) + "#comments"
    print(url);
    getLinks(url);
    time.sleep(5);


        





