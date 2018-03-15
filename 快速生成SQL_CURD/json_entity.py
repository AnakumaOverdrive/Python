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

ParamVerificationTemp = """string %s = GetParaValue(dic, "%s");
if (string.IsNullOrEmpty(%s))
{
	return DecryptReturnObj("-1", "", "参数 %s(%s) 为必填项");
}
"""
ParamStatement = "var entity = new XXXXXX();\n";
ParamTranTemp = """entity.%s = GetParaValue(dic, "%s"); //%s
"""

ParamVerification = ""
ParamTran=""
Content = ""
for link in LINES:
	if len(link) == 2 :
		f = link[0]
		uf = f[0].upper() + f[1:]
		lf = f[0].lower() + f[1:]
		r = link[1]
		ParamTran += ParamTranTemp % (uf,uf,r)
		ParamVerification += ParamVerificationTemp % (lf,uf,lf,r,uf)
ParamTran = ParamStatement + ParamTran
Content = ParamVerification + ParamTran
print(Content)


f = open("JoinOutStr.txt","w");
f.write(Content);
f.write("\n");
f.close();

os.startfile("JoinOutStr.txt"); 

