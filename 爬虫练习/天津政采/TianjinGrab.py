from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests,time,random,datetime,math,re,sys,json,urllib,csv

random.seed(datetime.datetime.now())
pages = set()
session = requests.Session();
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection':'keep-alive',
    
    }

RootUrl = "http://www.tjgp.gov.cn"
SjUrl = "http://www.tjgp.gov.cn/portal/topicView.do?method=view&view=Infor&id=1665&ver=2&st=1"
QxUrl = "http://www.tjgp.gov.cn/portal/topicView.do?method=view&view=Infor&id=1664&ver=2"

Returns = []

def getLinks(pageUrl,ids,i=1):
    global pages
    global headers
    global session
    
    req = session.post(pageUrl,headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Referer': pageUrl
    },data = {
        "method":"view",
        "page":i,
        "id":ids,
        "step":1,
        "view":"Infor",
        "st":"1",
        "ldateQGE":"",
        "ldateQLE":""
        })
    try:
        bsObj = BeautifulSoup(req.text,"html.parser")
    except:
        print("没有找到页面")
    else:
        if bsObj == None :
            return

        pagesColumn = bsObj.find("div",{"id":"pagesColumn"})
        if pagesColumn == None:
            pass
        else:
            pagesColumnA = pagesColumn.findAll("a")
            if pagesColumnA != None and len(pagesColumnA) > 2:
                print(pagesColumnA[2].get_text())
                for a in bsObj.find("ul",{"id":"div_ul_1"}).findAll("a"):
                    getContext(RootUrl + a.attrs["href"])
            getLinks(pageUrl,ids,i + 1)
        
        
def getContext(pageUrl):
    global pages
    global headers
    global session
    global Returns
    req = session.post(pageUrl,headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Referer': pageUrl
    })

    try:
        bsObj = BeautifulSoup(req.text,"html.parser")
    except:
        print("没有找到页面")
    else:
        if bsObj == None :
            return
        span_underlines = bsObj.findAll("span",{"class":"underline"})
        if span_underlines == None:
            pass
        else:
            if len(span_underlines) == 3:
                jfName = span_underlines[0].get_text()
                yfName = span_underlines[1].get_text()
                xmName = span_underlines[2].get_text()

                No = "";
                for div_line in  bsObj.findAll("div",{"class":"line"}):
                    #print(div_line.get_text())
                    if div_line.get_text().find("2.项目编号：") != -1:
                        No = div_line.get_text().replace("2.项目编号：","")
                    
                tdContent = "";
                for tr in bsObj.find("table",{"id":"projectBundleList"}).findAll("tr"):
                    #print(sibling) 包号|采购目录|简要技术要求|预算(万元)|
                    if "class" in tr.attrs:
                        pass
                    else:
                        for td in tr.findAll("td"):
                            tdContent += td.get_text() +" "
                        tdContent += "|"

                Returns.append((No,xmName,jfName,yfName,tdContent))
                
        
getLinks(SjUrl,1665);
csvFile = open("天津政采信息-市级.csv","w")
try:
    writer = csv.writer(csvFile)
    writer.writerow(('项目编号','项目名称','委托方','乙方','包号 采购目录 简要技术要求 预算(万元)|...'))
    for line in Returns:
        writer.writerow(line)
finally:
    csvFile.close()

Returns = []

getLinks(QxUrl,1664);
csvFile = open("天津政采信息-区县.csv","w")
try:
    writer = csv.writer(csvFile)
    writer.writerow(('项目编号','项目名称','委托方','乙方','包号 采购目录 简要技术要求 预算(万元)|...'))
    for line in Returns:
        writer.writerow(line)
finally:
    csvFile.close()





