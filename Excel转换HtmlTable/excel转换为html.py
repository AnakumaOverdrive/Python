import os,uuid,csv,xlrd
	
def IsMergedCell(mergedCells,i,j):
	"""判断是否为合并单元格的起始行和起始列,如果是则返回合并单元格的数组,
	数组包含四个元素（起始行，结束行，起始列，结束列）	"""
	for mergedCell in mergedCells:
		rlo, rhi, clo, chi = mergedCell
		if rlo == i and clo == j:
			return (rhi-rlo,chi-clo)
	return None
	
def IsInMergedCell(mergedCells,i,j):
	"""判断单元格是否在合并单元格内"""
	for mergedCell in mergedCells:
		rlo, rhi, clo, chi = mergedCell
		#当处于合并单元格的第一行第一列的时候
		if mergedCell[0] == i and mergedCell[2] == j :
			return False
		#当处于合并单元格内的时候
		if (rlo <= i and i <= rhi -1) and (clo <= j and j <= chi -1) :
			return True
	return False
	
def WriteFileInfo(fileName,Content):
	"""写入文件内容"""
	f = open(fileName,"w",encoding="utf-8");
	f.write(Content)
	f.close();
	
def GetTdClass(i,j):
	"""根据单元格的行数与列数返回 Td Class 的样式名称"""
	#$return "Td_Class_i"+str(i)+"j"+str(j)
	#return None
	
def GetTrClass(i):
	"""根据单元格的行数与列数返回 Tr Class 的样式名称"""
	#return "Tr_Class_i"+str(i)
	return None
	
def HandleExcel(filename):
	TC_workbook=xlrd.open_workbook(filename)
	first_sheet=TC_workbook.sheet_by_index(0)
	#获得所有行数  
	nrows = first_sheet.nrows  

	#得到所有合并单元格
	#	merged_cells返回的是一个列表，每一个元素是合并单元格的位置信息的数组，
	#	数组包含四个元素（起始行，结束行，起始列，结束列）
	mergedCells = first_sheet.merged_cells

	htmlTable = " <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />";
	htmlTable += " <table border=\"1\">";
	for i in range(0,first_sheet.nrows):
		trClass = GetTrClass(i)
		if trClass != None:
			htmlTable += "<tr class='"+GetTrClass(i)+"'>";
		else:
			htmlTable += "<tr>";
		tr = first_sheet.row_values(i)
		for j in range(len(tr)):
			spanStr = "";
			tdClass = GetTdClass(i,j)
			mc =  IsMergedCell(mergedCells, i,j)
			if mc != None:
				if mc[0] != 1:
					spanStr += 'rowspan="' + str(mc[0]) + '"'
				if mc[1] != 1:
					spanStr += 'colspan ="' + str(mc[1]) + '"'
					
				if tdClass != None:
					htmlTable += "<td class='"+GetTdClass(i,j)+"'"+spanStr+">"+str(tr[j])+"</td>"
				else:
					htmlTable += "<td "+spanStr+">"+str(tr[j])+"</td>"
					
			elif IsInMergedCell(mergedCells, i,j):
				continue
			else:
				if tdClass != None:
					htmlTable += "<td class='"+GetTdClass(i,j)+"'>"+str(tr[j])+"</td>"
				else:
					htmlTable += "<td>"+str(tr[j])+"</td>"
				
		htmlTable += "</tr>";
	htmlTable += "</table>";
	WriteFileInfo(filename+".html",htmlTable)
	
HandleExcel('test1.xlsx')

#if __name__ == '__main__':
	# print(IsInMergedCell(mergedCells, 1,1))
	# print(IsInMergedCell(mergedCells, 2,0))
	# print(IsInMergedCell(mergedCells, 2,1))
	# print(IsInMergedCell(mergedCells, 3,2))
	# print(IsInMergedCell(mergedCells, 3,7))
	# print(IsInMergedCell(mergedCells, 8,9))
	# print(IsInMergedCell(mergedCells, 11,1))
	# print(IsInMergedCell(mergedCells, 11,2))
	# print(IsInMergedCell(mergedCells, 12,2))
	# print(IsInMergedCell(mergedCells, 13,2))
	# print(IsInMergedCell(mergedCells, 14,2))
	# print(IsInMergedCell(mergedCells, 15,2))
	# print(IsInMergedCell(mergedCells, 15,4))
	# print(IsInMergedCell(mergedCells, 15,7))


	# print(IsInMergedCell(mergedCells, 4,2))
	# print(IsInMergedCell(mergedCells, 4,2))
