#coding=gbk
#! /usr/bin/python

def encodeUtf8(text):
	return text.encode("utf-8")
	
f = open("JoinStr.txt",encoding='utf-8',errors='ignore');
LINE = "";
while True:
	#global LINE;
	readline = f.readline();
	LINE += readline
	if(len(readline) == 0):
		break;
line1 = ",".join(LINE.split());

line2 = ",".join("'%s'" % s for s in LINE.split());

line3 = ",".join("\"%s\"" % s for s in LINE.split());
f.close();

NewLine = "%s \n\n %s \n\n %s" % (line1,line2,line3)

f = open("JoinOutStr.txt","wb+");
f.write(encodeUtf8(NewLine));
f.close();