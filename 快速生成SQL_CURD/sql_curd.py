#coding=gbk
#! /usr/bin/python
import os ;
#import commands;

f = open("JoinStr.txt");
LINE = "";
while True:
	readline = f.readline();
	LINE += readline
	if(len(readline) == 0):
		break;
pointLine = ",".join(LINE.split());
atLine = ",".join(["@%s" % s for s in LINE.split()]);
# if
whereList = "\n".join([ 'if (!string.IsNullOrEmpty(%s))\n{\n\tsqlStr += " and %s like @%s ";\n\tparam.Add(new OracleParameter(":%s", "%%" + %s + "%%"));\n}' % (s,s,s,s,s) for s in LINE.split()]);
whereList2 = "\n".join([ 'if (!string.IsNullOrEmpty(%s))\n{\n\tstrSql.Append(" and %s like @%s ");\n\tParameters.Add("@%s", "%%" + %s + "%%");\n}' % (s,s,s,s,s) for s in LINE.split()]);
# OracleParameter
#paramLine = ";\n".join(['param.Add(new OracleParameter("%s", XXXXX.%s))' % (s,s) for s in LINE.split()]);
paramLine = ";\n".join(['Parameters.Add("%s", model.%s)' % (s,s) for s in LINE.split()]);
# update
updateLine = ",".join([' %s=@%s' % (s,s) for s in LINE.split()]);
f.close();

# 
insert = "INSERT INTO XXXXX(%s) VALUES(%s) \n" % (pointLine,atLine);
select = "SELECT %s FROM XXXXX \n " % pointLine;
update = "UPDATE XXXXX SET %s WHERE 1=1 \n" % updateLine;


#outtext = "%s \n %s \n %s \n %s \n %s" %(select,insert,update,paramLine,whereList);

f = open("JoinOutStr.txt","w");
#f.write(outtext);
f.write(select);
f.write("\n");
f.write(insert);
f.write("\n");
f.write(update);
f.write("\n");
f.write(paramLine);
f.write("\n");
f.write(whereList);
f.write("\n");
f.write(whereList2);
f.close();


#cmd = "notepad JoinOutStr.txt";
#os.system(cmd) 
os.startfile("JoinOutStr.txt"); 
#os.startfile("Microsoft Excel.xlsx");

