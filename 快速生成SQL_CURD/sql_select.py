#coding=gbk
#! /usr/bin/python
import os ;
#import commands;

f = open("JoinStr.txt");
LINES = [];
while True:
	readline = f.readline();
	LINES.append(readline.split())
	if(len(readline) == 0):
		break;
f.close();	

ParamDescTemp = "/// <param name=\"%s\">%s</param>\n"

MethodTemp = """public ReturnTable GetXXXXXX(PageSplit split, %s){
%s
}"""

SelectTemp = """DataQuery query = new DataQuery();
query.SQLText = "SELECT * FROM XXXXX where 1=1"; 
 """;
 
QueryParamTemp = """//%s
if (!String.IsNullOrEmpty(%s))
{
	query.SQLText += " and %s = @%s";
	query.WhereParameters.Add(new WhereParameter("@%s", %s));
}
"""
InParam = "";
QueryParam = ""
ParamDesc = "";
for link in LINES:
	if len(link) == 2 :
		f = link[0]
		uf = f[0].upper() + f[1:]
		lf = f[0].lower() + f[1:]
		r = link[1]
		QueryParam += QueryParamTemp % (r,lf,uf,uf,uf,lf)
		InParam += "string %s," % lf
		ParamDesc += ParamDescTemp % (lf,r)
QueryParam += """query.PageView = split;
//query.OrderByString = "";

ReturnTable rt = new ReturnTable();
rt.Table = BaseData.ExecuteDataTable(query);
rt.PageInfo = query.PageView;
return rt;
"""
SelectTemp += QueryParam
Method = MethodTemp %(InParam , SelectTemp)
ParamDesc += Method
print(ParamDesc)


f = open("JoinOutStr.txt","w");
f.write(ParamDesc);
f.write("\n");
f.close();

os.startfile("JoinOutStr.txt"); 

