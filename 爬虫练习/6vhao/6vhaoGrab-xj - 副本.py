from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import time
import random
import datetime

f = open("喜剧电影下载链接.txt","w");
random.seed(datetime.datetime.now())


def getLinks(pageUrl):
    global f
    try:
        html = urlopen(pageUrl)
        bsObj = BeautifulSoup(html.read(),"html.parser")
    except:
        print("没有找到页面")
    else:
        if(bsObj == None):
            return
        if len(bsObj.findAll("div",{"class":"listInfo"})) == 0:
            return

        for div in bsObj.findAll("div",{"class":"listInfo"}):
            if div == None:
                return
            a = div.find("a")

            if 'href' in a.attrs:
                title = a.attrs["href"]+'  '+a.attrs["title"]
                print(title)
                try:
                    f.write(title+"\n");
                    analysisSubPage(a.attrs["href"])
                except:
                    pass

def analysisSubPage(url):
    global f
    try:
        html = urlopen(url)
        bsObj = BeautifulSoup(html.read(),"html.parser")
    except:
        print("没有找到页面")
    else:
        if(bsObj == None):
            return
        table = bsObj.find("table",{"bgcolor":'#0099cc'})
        if(table == None):
            return
        for a in table.findAll("a"):
            if 'href' in a.attrs:
                #print(a.attrs["href"])
                try:
                    f.write(a.attrs["href"]+"\n");
                except:
                    pass
        print("----------------------------------")
        f.write("----------------------------------\n");

for i in range(1,41):
    url = "";
    if i == 1:
        url = "http://www.6vhao.net/dy1/index.html"
    else:
        url = "http://www.6vhao.net/dy1/index_" + str(i) + ".html"
    getLinks(url)

f.close()

        





