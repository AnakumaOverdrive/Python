import os
from xml.dom import minidom

def EpSuffix(fileName,suffixName):
	"""判断传入的文件名与传入的后缀名是否相等"""
	if(os.path.splitext(fileName)[1].lower() == suffixName.lower()):
		return True;
	else :
		return False;
		
def getXmlFileName():
	result = []
	list = os.listdir(os.getcwd())
	for line in list:
		if os.path and (EpSuffix(line,".xml") or EpSuffix(line,".XML")):
			result.append(line);
	return result;
	
def CheckXmlRepeatId(fileName):
	result = {}
	nodes = []
	xmldoc = minidom.parse(fileName).documentElement
	nodes.extend(xmldoc.getElementsByTagName("resultMap"))
	nodes.extend(xmldoc.getElementsByTagName("insert"))
	nodes.extend(xmldoc.getElementsByTagName("delete"))
	nodes.extend(xmldoc.getElementsByTagName("update"))
	nodes.extend(xmldoc.getElementsByTagName("select"))
	for	obj in nodes:
		result.setdefault(obj.getAttribute("id"),0)
		result[obj.getAttribute("id")] += 1
	return [ (fileName,v,result[v]) for v in result if result[v] != 1 ]

	
def PrintError(errors):
	print("%30s\t%s\t%s"%('XML文件名称','ID名称','重复出现的次数'))
	for filename,idname,count in errors:
		print("%30s\t%30s\t%s" %(filename,idname,count))
	
errors = []
for filename in getXmlFileName():
	errors.extend(CheckXmlRepeatId(filename))

PrintError(errors)

	