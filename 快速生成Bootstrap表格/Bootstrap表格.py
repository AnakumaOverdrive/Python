#coding=gbk
#! /usr/bin/python

def encodeUtf8(text):
	return text.encode("utf-8")
	
f = open("JoinStr.txt",encoding='utf-8',errors='ignore');
LINES = f.readlines();
f.close();

TableTmp = """<table class="table  table-bordered table-condensed table-hover table-striped">
  <tbody>
%s
  </tbody>
</table>"""

TrTmp = """
	<tr>
		<td>%s</td><td>%s</td>
	</tr>"""

trStr = "";
tableStr = "";
for line in LINES:
	s,v = line.split();
	trStr += TrTmp % (s,v)
	
tableStr = TableTmp % trStr

f = open("JoinOutStr.txt","wb+");
f.write(encodeUtf8(tableStr));
f.close();