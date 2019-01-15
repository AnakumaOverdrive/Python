#coding:gbk
#! /usr/bin/python

import urllib    
import urllib2    
  
url = 'http://app1.sfda.gov.cn/datasearch/face3/base.jsp'    
    
values = {'tableId' : '25',    
          'tableName' : 'TABLE25',    
          'title' : '%B9%FA%B2%FA%D2%A9%C6%B7',
		  'bcId':'124356560303886909015737447882'		  }    
  
data = urllib.urlencode(values) 
req = urllib2.Request(url, data)  
response = urllib2.urlopen(req) 
the_page = response.read()  

