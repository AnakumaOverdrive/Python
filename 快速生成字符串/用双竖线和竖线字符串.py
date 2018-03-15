#coding=gbk
#! /usr/bin/python

import os

def encodeUtf8(text):
	return text.encode("utf-8")
	
f = open("JoinStr.txt",encoding='utf-8',errors='ignore');
lines = f.readlines();
f.close();
temp = []

for line in lines:
	s,v = line.split()
	temp.append("%s|%s" % (s,v))

NewLine = '||'.join(temp)

f = open("JoinOutStr.txt","wb+");
f.write(encodeUtf8(NewLine));
f.close();
os.startfile("JoinOutStr.txt"); 