#coding=gbk
#! /usr/bin/python
#-*-encoding:utf-8-*-

import os
import sys
import string

def startdir():
	result = [];
	list = os.listdir(os.getcwd())
	for line in list:
		if os.path and (line.find('.jpg') != -1 or line.find('.png') != -1  or line.find('.bmp') != -1 ):
			result.append((line,line));
	#result.sort()
	return  '\n\r'.join('<label>%s</label><br /><img src="%s" /><br />' % (s,v) for s,v in result)

def gifdir():
	result = [];
	list = os.listdir(os.getcwd())
	for line in list:
		if os.path and (line.find('.gif')  != -1 ):
			result.append((line,line));
	#result.sort()
	return  '\n\r'.join('<label>%s</label><br /><img src="%s" /><br />' % (s,v) for s,v in result)
	
temp = """
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-cn">
<head>
<script type="text/javascript">
</script>
</head>
<body>
 %s
</body>
</html>
"""

f = open("SeeStartImage.html","w");
html = temp % startdir()
f.write(html);
f.write("\n\n");
f.close();


f = open("SeeGifImage.html","w");
html = temp % gifdir()
f.write(html);
f.write("\n\n");
f.close();






