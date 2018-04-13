from itertools import groupby

def GetFileInfo(fileName):
	"""读取文件信息"""
	f = open(fileName,encoding='utf-8',errors='ignore');
	contents = f.readlines();
	f.close();
	return contents
	
	
def WriteFileInfo(fileName,Content):
	"""写入文件内容"""
	f = open(fileName,"w",encoding="utf-8");
	f.write(Content)
	f.close();

filename = 'ds'	
	
def BuildHtmlTable():
	ds = GetFileInfo(filename+".txt")
	htmlTable = " <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /><table border=\"1\">";
	for d in ds:
		if d.strip() != "":
			htmlTable += "<tr>";
			tr = d.split(",");
			for td in tr:
				if td.find('|') > -1 :
					tmp = td.replace('\n','').split('|')
					
					span = [''.join(list(g)) for k, g in groupby(tmp[1], key=lambda x: x.isdigit())]

					spanStr = "";
					if len(span) == 2:
						if span[0].lower() == "r":
							spanStr = 'rowspan="' + span[1] + '"'
						if span[0].lower() == "c":
							spanStr = 'colspan ="' + span[1] + '"'
					if len(span) == 4:
						if span[0].lower() == "r":
							spanStr += 'rowspan="' + span[1] + '"'
						if span[0].lower() == "c":
							spanStr += 'colspan ="' + span[1] + '"'
							
						if span[2].lower() == "r":	
							spanStr += ' rowspan="' + span[3] + '"'
						if span[2].lower() == "c":
							spanStr += ' colspan ="' + span[3] + '"'

					htmlTable += "<td "+spanStr+">"+tmp[0]+"</td>"

				else:
					htmlTable += "<td>"+td+"</td>"
				#print(tr,tr.find('|'))
			#print(d)
			htmlTable += "</tr>";
	htmlTable += "</table>";
	WriteFileInfo(filename+".html",htmlTable)
	
BuildHtmlTable()