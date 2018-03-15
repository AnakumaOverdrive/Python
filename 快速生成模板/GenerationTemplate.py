#coding=utf-8
import os,uuid,csv,xlrd

def EpSuffix(fileName,suffixName):
	"""判断传入的文件名与传入的后缀名是否相等"""
	if suffixName == "" or os.path.splitext(fileName)[1].lower() == suffixName.lower():
		return True;
	else :
		return False;

def LocalPathFiles(filterName = "",suffixName = ""):
	"""获得本地路径的文件
	filterName: 指定的文件名
	suffixName: 指定的字符串后缀"""
	files = [];
	path = os.getcwd()
	filelist  = os.listdir(path)
	
	for filename in filelist:
		filepath = os.path.join(path, filename)
		if(os.path.isdir(filepath) != True and EpSuffix(filepath,suffixName)) and filename.lower().find(filterName.lower()) == 0:
			files.append(filename)
	return files

def trimBOM(str):
	"""去掉BOM"""
	try:
		str = str.encode('utf-8').decode('utf-8-sig')
	except:
		pass
	return str

def openAnything(filename):
	"""打开文件并且返回数据"""
	if os.path.isfile(filename): 
		if EpSuffix(filename,".csv"):
			return Csv2Json(filename)
		elif EpSuffix(filename,".xlsx") or EpSuffix(filename,".xls"):
			return Excel2Json(filename)
	else:
		return []
	
def Csv2Json(filename):
	"""将CSV转换为Json对象 注意 CSV文件必须存在header头信息"""
	#获得数据
	header,datas = HandleCSV(filename)
	#转换为Json数据
	jsonArr = GenerationJson(header,datas)
	return jsonArr

def Excel2Json(filename):
	"""将Excel转换为Json对象 注意 Excel文件必须存在header头信息"""
	#获得数据
	header,datas = HandleExcel(filename)
	#转换为Json数据
	jsonArr = GenerationJson(header,datas)
	
	return jsonArr
	
def HandleCSV(filename,isHeader = True):
	"""处理CSV信息"""
	header = []
	datas = []
	i = 0
	with open(filename,"r",encoding="utf-8") as csvfile:
		read = csv.reader(csvfile)
		for row in read:
			if isHeader:
				if i == 0:
					header.extend([trimBOM(r) for r in row])
				else:
					datas.append([trimBOM(r) for r in row])
			else:
				datas.append([trimBOM(r) for r in row])
			i += 1
	
	return header,datas
	
def HandleExcel(filename,isHeader = True):
	"""处理CSV信息"""
	datas = []
	TC_workbook=xlrd.open_workbook(filename)
	first_sheet=TC_workbook.sheet_by_index(0)
	if isHeader:
		header = first_sheet.row_values(0)
		for i in range(1,first_sheet.nrows):
			datas.append(first_sheet.row_values(i))
	else:
		for i in range(first_sheet.nrows):
			datas.append(first_sheet.row_values(i))
			
	return header,datas
	
def GenerationJson(header,datas):
	"""生成Json对象"""
	if len(header) == 0 or len(datas) == 0: 
		print("len(header) == 0 or len(datas) == 0")
		return []
	if len(header) == len(datas[0]):
		jsonArr = []
		for data in datas:
			jsonobj = {}
			for i in range(len(header)):
				jsonobj.setdefault(header[i],"")
				jsonobj[header[i]] = data[i]
			jsonArr.append(jsonobj)	
	else:
		print("GenerationJson Error")
		return []
	return  jsonArr	

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
	
def TemplateDataSource():
	"""获得模板数据"""
	#数据源名称
	dataSourceName = "Data"
	dataSourceFiles = LocalPathFiles(dataSourceName)
	return openAnything(dataSourceFiles[0])

def GenerationTemplate(tmpFileNames,templateData):
	"""根据模板和数据生成代码"""
	for tmpFileName in tmpFileNames:
		#生成的文件名
		txtFileName = tmpFileName[:tmpFileName.rfind(".")]
		
		#获得模板
		templateStr = "".join(GetFileInfo(tmpFileName))
		
		#循环数据信息并且填入模板
		templateContent = ""
		for data in templateData:
			templateContent += templateStr % data
		print(templateContent)

		#写入文件
		WriteFileInfo(txtFileName,templateContent)
		
		#打开文件
		# os.startfile(txtFileName); 
	
#获得所有模板名称
tmpFileNames = LocalPathFiles(suffixName = ".tmp");
#获得模板数据
templateData = TemplateDataSource()
#根据模板和数据生成代码
GenerationTemplate(tmpFileNames,templateData)



	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
		