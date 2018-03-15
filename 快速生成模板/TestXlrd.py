#coding=utf-8
import xlrd
    
def read_excel_xlrd():
	#file
	TC_workbook=xlrd.open_workbook(r"Data.xlsx")

    #获得所有sheet的名字
	all_sheets_list=TC_workbook.sheet_names()
	print("All sheets name in File:",all_sheets_list)
	
	first_sheet=TC_workbook.sheet_by_index(0)
	print("First sheet Name:",first_sheet.name)
	print("First sheet Rows:",first_sheet.nrows)
	print("First sheet Cols:",first_sheet.ncols)
	
    
    # second_sheet=TC_workbook.sheet_by_name("SheetName_test")
    # print("Second sheet Rows:",second_sheet.nrows)
    # print("Second sheet Cols:",second_sheet.ncols)
	
	#获得首行
	first_row=first_sheet.row_values(0)
	print("First row:",first_row)
	#获得首列
	first_col=first_sheet.col_values(0)
	print("First Column:",first_col)
#read_excel_xlrd();


def HandlerExcel():
	#file
	TC_workbook=xlrd.open_workbook("Data.xlsx")
	first_sheet=TC_workbook.sheet_by_index(0)
	header = first_sheet.row_values(0)
	datas = []
	for i in range(1,first_sheet.nrows):
		datas.append(first_sheet.row_values(i))

	print(header)
	print(datas)
	return header,datas
		
HandlerExcel()		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
	