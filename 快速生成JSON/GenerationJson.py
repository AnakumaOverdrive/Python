#coding=gbk
#! /usr/bin/python

import uuid
import os

f = open("JoinStr.txt",encoding='utf-8',errors='ignore');
LINES = f.readlines();
f.close();

trArr = []
TrTmp = "{Field:'%s',Name:'%s'}"
for line in LINES:
	s,v = line.split();
	trArr.append(TrTmp % (s,v))

temp = ",".join([ tr for tr in trArr]) 
temp = '[%s]' % temp

f = open("JoinOutStr.txt","w",encoding='utf-8');
f.write(temp);
f.close();
os.startfile("JoinOutStr.txt"); 