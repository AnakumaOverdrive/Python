#! /usr/bin/python
import urllib
import urllib2  

url = 'http://app1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=25&tableName=TABLE25'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'    
headers = { 'User-Agent' : user_agent }    
values = {'Id':'64963'}    
data = urllib.urlencode(values)   


headers = { 'User-Agent' : user_agent }    
data = urllib.urlencode(values)    
req = urllib2.Request(url, data, headers)    
response = urllib2.urlopen(req)    
the_page = response.read()   
print the_page