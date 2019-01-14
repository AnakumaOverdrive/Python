import sys,os,uuid,csv,xlrd,json
import datetime

HTMLTMP = """
 <div id="%s"></div>
    <script>
        var data = %s;

        function data2TableStr(data) {
            var matchLetter = /^[a-z|A-Z]+/gi;
            var matchNumber = /\d+$/gi;
            var table = "<table>";
            for (var i = 0; i < data.length; i++) {
                var tr = "<tr>";
                var trData = data[i];
                for (var j = 0; j < trData.length; j++) {
                    var span = "";
                    var content = "";
                    td = trData[j];
                    var tdsplit = td.split("|");
                    for (var k = 0; k < tdsplit.length; k++) {
                        if (k == 0) {
                            content = tdsplit[k];
                        }
                        if (tdsplit[k].match(matchLetter) == "r") {
                            span += " rowspan=" + tdsplit[k].match(matchNumber);
                        }
                        if (tdsplit[k].match(matchLetter) == "c") {
                            span += " colspan=" + tdsplit[k].match(matchNumber);
                        }
                    }
                    if (span != "") {
                        tr += "<td" + span + ">" + content + "</td>";
                    } else {
                        tr += "<td>" + content + "</td>";
                    }
                }
                tr += "</tr>";
                table += tr;
            }
            table += "</table>";
            return table;
        }

        document.getElementById("%s").innerHTML = data2TableStr(data);
    </script>
""";

def IsMergedCell(mergedCells,i,j):
	"""判断是否为合并单元格的起始行和起始列,如果是则返回合并单元格的数组,
	数组包含四个元素（起始行，结束行，起始列，结束列）	"""
	for mergedCell in mergedCells:
		rlo, rhi, clo, chi = mergedCell
		if rlo == i and clo == j:
			return True
	return False
	
def IsInMergedCell(mergedCells,i,j):
	"""判断单元格是否在合并单元格内"""
	for mergedCell in mergedCells:
		rlo, rhi, clo, chi = mergedCell
		#当处于合并单元格的第一行第一列的时候
		#if mergedCell[0] == i and mergedCell[2] == j :
		#	return False
		#当处于合并单元格内的时候
		if (rlo <= i and i <= rhi -1) and (clo <= j and j <= chi -1) :
			return True
	return False
	
def GetMargedCell(mergedCells,i,j):
	""""""
	for mergedCell in mergedCells:
		rlo, rhi, clo, chi = mergedCell
		if (rlo <= i and i <= rhi -1) and (clo <= j and j <= chi -1) :
			return (rlo, rhi, clo, chi)
	return None
	
def WriteFileInfo(fileName,Content):
	"""写入文件内容"""
	f = open(fileName,"w",encoding="utf-8");
	#f = open(fileName,"w");
	f.write(Content)
	f.close();
		
def HandleCellValue(sheet,i,j,worldColNumber = []):
	"""单元格值的处理"""
	cell = sheet.cell(i,j)
	if cell.ctype == xlrd.XL_CELL_TEXT: #类型为文本	a Unicode string
		return cell.value
	if cell.ctype == xlrd.XL_CELL_EMPTY or cell.ctype == xlrd.XL_CELL_BLANK: #类型为空	empty string ''
		return ""
	if cell.ctype == xlrd.XL_CELL_ERROR: #类型为错误类型	int
		#return "int representing internal Excel codes; for a text representation, refer to the supplied dictionary error_text_from_code"
		return ""
	if cell.ctype == xlrd.XL_CELL_BOOLEAN: #类型为布尔值	int; 1 means TRUE, 0 means FALSE
		if cell.value == 0: return "假的"
		elif cell.value == 1: return "真的"
		else: return "boolean:%s" % cell.value
	if cell.ctype == xlrd.XL_CELL_DATE: #类型为时间类型	float
		# @param datemode 0: 1900-based, 1: 1904-based.  
		dt = xlrd.xldate.xldate_as_datetime(cell.value, 0)   #直接转化为datetime对象  
		return dt.strftime("%Y-%m-%d %H:%M:%S")
	if cell.ctype == xlrd.XL_CELL_NUMBER: #类型为数字类型 float
		return HandleCellNumberValue(sheet,i,j,worldColNumber)
		#return cell.value
	return cell

def HandleCellNumberValue(sheet,i,j,worldColNumber):
	"""单元格值是浮点型的处理"""
	cell = sheet.cell(i,j)
	#if j in worldColNumber:
	#	return "%s%%" % int(round(cell.value * 100))
	#return int(cell.value)
	if int(cell.value) == cell.value:
		return int(cell.value)
	else:
		return round(cell.value,2)
	
def FindColByField(sheet,world,maxn = 5):
	"""查询包含字段的列号"""
	fieldcols = []
	nrows = sheet.nrows  #获得所有行数  
	ncols = sheet.ncols	#获得所有列数
	
	if nrows > maxn:
		nrows = maxn
		
	for i in range(nrows):
		for j in range(ncols):
			cell = sheet.cell(i,j)
			if cell.ctype == xlrd.XL_CELL_TEXT:
				if cell.value.find(world) > -1:
					#print(cell.value)
					fieldcols.append(j)
	#去重
	fieldcols = list(set(fieldcols))
	return fieldcols
	
def HandleExcel(filename):
	#使用 formatting_info=True 来复制带有格式的excel,否则追加写后格式会丢失
	#formatting_info=True 只能应用于xls文档，如果是xlsx文档话则需要转换为xls文档。
	#TC_workbook=xlrd.open_workbook(filename,formatting_info=True)
	TC_workbook=xlrd.open_workbook(filename)
	sheet=TC_workbook.sheet_by_index(0)

	nrows = sheet.nrows  #获得所有行数  
	ncols = sheet.ncols	#获得所有列数
	#得到所有合并单元格
	#	merged_cells返回的是一个列表，每一个元素是合并单元格的位置信息的数组，
	#	数组包含四个元素（起始行，结束行，起始列，结束列）
	mergedCells = sheet.merged_cells
	
	#获得含有%的列
	worldColNumber = FindColByField(sheet,'%')
	
	TableJson = [];
	trhead = []
	for i in range(nrows):
		if i == 0:
			trhead = sheet.row_values(0) #获得json key的名称
		else:
			tr = sheet.row_values(i) #获得行的所有数据
			trArray = []
			trJson = {};
			trJson["SerialNumber"] = i
			for j in range(ncols):
				
				#当是合并单元格的时候返回该合并单元格的起始行,结束行,起始列和结束列.
				mc = GetMargedCell(mergedCells, i,j)
				#判断是否存在合并单元格内
				if mc != None:
					rlo, rhi, clo, chi = mc;
					rowspan = {}
					colspan = {}
					#为当前合并单元格生成一个guid
					id = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(mc)))
					
					#行 span 跨度
					rspan = rhi - rlo
					if rspan > 1 :
						scontent = list(range(rlo,rhi))
						rowspan = {"id":id,"span":rspan,"content":scontent}
						
					#列 span 跨度
					cspan = chi - clo
					if cspan > 1 :
						ccontent = trhead[clo:chi]
						colspan = {"id":id,"span":cspan,"content":ccontent}
					
					k = trhead[j]
					
					val = ""
					if IsMergedCell(mergedCells, i,j):
						val = HandleCellValue(sheet,i,j,worldColNumber)
						
				
					trJson[k] = val
					trJson["merge_" + k] = {"row":rowspan,"col":colspan}
				else:
					k = trhead[j]
					
					
					
					trJson[k] = HandleCellValue(sheet,i,j,worldColNumber)
					trJson["merge_" + k] = {}
				#trArray.append(trJson)
			TableJson.append(trJson)
	TableStr = json.dumps(TableJson)
	(filepath,tempfilename) = os.path.split(filename);
	(shotname,extension) = os.path.splitext(tempfilename);
	
	#print(TableStr.encode().decode('unicode-escape'))
	
	WriteFileInfo(filename+".json",TableStr.encode().decode('unicode-escape'))
	
	#TempStr = HTMLTMP % (shotname,TableStr,shotname)
	#WriteFileInfo(filename+".html",TempStr)

# EXCELNAME = "ExcelToJson.xlsx"
# HandleExcel(EXCELNAME)	
	
lines = []
words = input("请将EXCEL文件拖入控制台内,以回车分割文件(单独输入':w')开始执行:\n")

while words != ':w':
	line = lines.append(words)
	words = input()		

for line in lines:
	print("开始处理 "+ line)
	HandleExcel(line)	
	print("完成")
print("全部完成")

