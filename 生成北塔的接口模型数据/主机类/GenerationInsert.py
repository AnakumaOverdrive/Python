#coding=utf-8
import os,uuid,csv

def EpSuffix(fileName,suffixName):
	"""判断传入的文件名与传入的后缀名是否相等"""
	if(os.path.splitext(fileName)[1].lower() == suffixName.lower()):
		return True;
	else :
		return False;

def LocalPathFiles(suffixName = ".csv"):
	"""获得本地路径的文件"""
	files = [];
	path = os.getcwd()
	filelist  = os.listdir(path)
	for filename in filelist:
		filepath = os.path.join(path, filename) 
		#如果是文件夹则递归
		if(os.path.isdir(filepath) != True and EpSuffix(filepath,suffixName)):
			files.append(filename)
	return files

INSERT = "INSERT INTO T_BTS_InterfaceMode(Id,ModelType,Number,ManageClass,SubItem,FieldName,FieldValue,FieldType,IndicatorName,UnitName,Remarks,IsDelete) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'); \n" 
# f = open("JoinOutStr.txt","w",encoding="utf-8");
# with open("Windows.csv","r",encoding="utf-8") as csvfile:
	# read = csv.reader(csvfile)
	# for i in read:
		# files = (str(uuid.uuid1()),'Windows',i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],'1')
		# print(insert % files)
		# f.write(insert % files);
# f.close();
# os.startfile("JoinOutStr.txt"); 

csvFileNames = LocalPathFiles();
for csvFileName in csvFileNames:
	txtFileName = csvFileName[:csvFileName.find(".")] + ".txt"
	f = open(txtFileName,"w",encoding="utf-8");
	with open(csvFileName,"r",encoding="utf-8") as csvfile:
		read = csv.reader(csvfile)
		for i in read:
			files = (str(uuid.uuid1()),csvFileName[:csvFileName.find(".")],i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],'1')
			print(INSERT % files)
			f.write(INSERT % files);
	f.close();
	os.startfile(txtFileName); 
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
		