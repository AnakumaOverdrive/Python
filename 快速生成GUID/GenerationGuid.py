#coding=gbk
#! /usr/bin/python

import uuid
import os

std1 = ""
std2 = ""

guidArr = []


for i in range(0,50):
	guidArr.append(str(uuid.uuid1()) )
f = open("JoinOutStr.txt","w");
guid1 = "\n".join(["%s" % guid for guid in guidArr])
guid2 = "\n".join(["%s" % guid.replace('-','') for guid in guidArr])
guid3 = "\n".join(["{%s}" % guid for guid in guidArr])
guid4 = "\n".join(["{%s}" % guid.replace('-','') for guid in guidArr])
f.write(guid1);
f.write("\n\n")
f.write(guid2);
f.write("\n\n")
f.write(guid3);
f.write("\n\n")
f.write(guid4);
f.close();
os.startfile("JoinOutStr.txt"); 