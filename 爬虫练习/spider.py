#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import sys
reload(sys)
sys.setdefaultencoding('UTF-8') 



class spider(object):
	def __init__(self):
		print u"start....."
	
	def getsource(self,url):
		html = requests.get(url)
		print html.text
		return html.text
		
	def changepage(self,url,total_page):	
		now_page = int(re.search('pageNum=(\d+)',url,re.S).group(1))
		page_group = []
		for i in range(now_page,total_page + 1):
			link = re.sub('pageNum=\d+','pageNum=%s' % i,url,re.S)
			page_group.append(link)
		return page_group
	
	def geteveryclass(self,source):
		everyclass = re.findall('(<li deg="".#?</li>)',source,re.S)
		return everyclass
		
	def getinfo(self,eachclass):
		info = {}
		info['title'] =re.search('target="_blank">(.#?)</a>',eachclass,re.S).group(1)
		info['content'] =re.search('</h2><p>(.#?)</p>',eachclass,re.S).group(1)
		timeandlevel = re.findall('<em>(.#?)</em>',eachclass,re.S)
		info['classtime'] = timeandlevel[0]
		info['classlevel'] = timeandlevel[1]
		info['learnnum'] =re.search('"learn-number">(.*?)</em>',eachclass,re.S).group(1)
		return info
	def saveinfo(self,classinfo):
		f = open('info.txt','a')
		for each in classinfo:
			print each['title']
			f.writerlines('title:' + each['title'])
			f.writerlines('content:' + each['content'])
			f.writerlines('classtime:' + each['classtime'])
			f.writerlines('classlevel:' + each['classlevel'])
			f.writerlines('learnnum:' + each['learnnum'])
		f.close()

if __name__ == '__main__':
	classinfo = []
	url = "http://www.jikexueyuan.com/course/?pageNum=1"
	jikespider = spider()
	all_links = jikespider.changepage(url,2)
	for link in all_links:
		print u"page:" + link
		html = jikespider.getsource(link)
		everyclass = jikespider.geteveryclass(html)
		for each in everyclass:
			into = jikespider.getinfo(each)
			classinfo.append(info)
	jikespider.saveinfo(classinfo)