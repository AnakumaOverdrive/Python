from bs4 import BeautifulSoup
from urllib.request import urlopen

html = urlopen("https://www.baidu.com/")
print(html.read())
bsObj = BeautifulSoup(html.read())

print(bsObj.h1)
