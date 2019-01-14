import MySQLdb,json

class MySqlHandle:
	def __init__(self,host,db,user,passwd,port = 3306,charset='utf8'):
		self.host = host
		self.db = db
		self.user = user
		self.passwd = passwd
		self.port = port
		self.charset = charset
		self.TableStructures = {}
	
	def ExecuteSql(self,sql):
		"""执行SQL语句,并且返回执行结果."""
		conn= MySQLdb.connect(host=self.host,port = self.port,user=self.user,passwd=self.passwd,db =self.db,charset=self.charset)
		cur = conn.cursor()
		results = None
		try:
		   # 执行SQL语句
		   cur.execute(sql)
		   # 获取所有记录列表
		   results = cur.fetchall()
		   
		except Exception as e:
			print("发生了异常",e.message)
		finally:
			conn.close();
		return results
		
	def GetTableNameSentence(self):
		"""获得数据库中所有表名的语句"""
		return """select TABLE_NAME as tableName,TABLE_COMMENT as tableComment 
from information_schema.tables 
where table_schema='%s' and table_type='base table'; """ % (self.db)
	
	def GetTableStructureSentence(self,TableName):
		"""获得表结构的语句"""
		return """select
col.TABLE_SCHEMA,
col.TABLE_NAME,
col.ORDINAL_POSITION as COLUMN_ID,
col.COLUMN_NAME,
col.COLUMN_COMMENT as COLUMN_COMMENTS,
col.DATA_TYPE,
col.CHARACTER_MAXIMUM_LENGTH as DATA_LENGTH,
col.IS_NULLABLE as NULLABLE,
col.COLUMN_DEFAULT as DATA_DEFAULT,
col.COLUMN_KEY as PRIMARY_KEY,
if(tab.auto_increment is not null and col.COLUMN_KEY = 'PRI',1,0) as IsIndentity
from information_schema.columns col
join information_schema.TABLES tab on col.table_name = tab.table_name and col.TABLE_SCHEMA = tab.TABLE_SCHEMA
where col.TABLE_SCHEMA = '%s' and col.table_name = '%s';""" % (self.db,TableName)

	def QueryTableName(self):
		"""查询所有表名"""
		return self.ExecuteSql(self.GetTableNameSentence())

	def PreloadTableStructures(self):
		"""预先加载有所表结构"""
		tableNameInfos = self.QueryTableName();
		for tableNameInfo in tableNameInfos:
			tableName,tableComment = tableNameInfo
			self.QueryTableStructure(tableName)
			
	def QueryTableStructure(self,TableName):
		"""查询表结构"""
		self.TableStructures.setdefault(TableName,None)
		if self.TableStructures[TableName] == None:
			#print(TableName , "For the first time")
			tableStructures = self.GetTableStructureSentence(TableName)
			self.TableStructures[TableName] = self.ExecuteSql(tableStructures)
		return self.TableStructures[TableName]

	def __GetTableColumnsInfo(self,TableName):
		"""私有方法 获得表中列的信息."""
		primaryKeyNames = []
		columnNames = []
		tableStructure = self.QueryTableStructure(TableName)
		for row in tableStructure:
			schema,tableName,columnId,columnName,columnComment,dataType,dataLength,isNullable,dataDefaule,primaryKey,isIndentity = row
			if primaryKey == "PRI":
				primaryKeyNames.append(columnName)
			else:
				columnNames.append(columnName)
		return (primaryKeyNames,columnNames)
	
	def GetInsertSentence(self,TableName):
		"""获得插入语句"""
		sqlSentence = "insert into %s(%s) values(%s); "
		columnNames = []
		columnValues = []
		tableStructure = self.QueryTableStructure(TableName)
		for row in tableStructure:
			schema,tableName,columnId,columnName,columnComment,dataType,dataLength,isNullable,dataDefaule,primaryKey,isIndentity = row
			columnNames.append(columnName)
			columnValues.append("%s");
		return sqlSentence % (TableName,",".join(columnNames),",".join(columnValues))
		
	def GetDeleteSentence(self,TableName):
		"""获得删除的语句"""
		sqlSentence = "delete from %s where %s; "
		primaryKeyNames = []
		tableStructure = self.QueryTableStructure(TableName)
		for row in tableStructure:
			schema,tableName,columnId,columnName,columnComment,dataType,dataLength,isNullable,dataDefaule,primaryKey,isIndentity = row
			if primaryKey == "PRI":
				primaryKeyNames.append(columnName + " = %s")
		return sqlSentence % (TableName," and ".join(primaryKeyNames))
		
	def GetUpdateSentence(self,TableName):
		"""获得更新的语句"""
		sqlSentence = "update %s set %s where %s; "
		columnNames = []
		primaryKeyNames = []
		tableStructure = self.QueryTableStructure(TableName)
		for row in tableStructure:
			schema,tableName,columnId,columnName,columnComment,dataType,dataLength,isNullable,dataDefaule,primaryKey,isIndentity = row
			if primaryKey == "PRI":
				primaryKeyNames.append(columnName + " = %s")
			else:
				columnNames.append(columnName + " = %s")
		return sqlSentence % (TableName,", ".join(columnNames)," and ".join(primaryKeyNames))
		
	def GetQuerySentence(self,TableName):
		"""获得查询语句"""
		sqlSentence = "select * from %s where %s; "
		columnNames = []
		tableStructure = self.QueryTableStructure(TableName)
		for row in tableStructure:
			schema,tableName,columnId,columnName,columnComment,dataType,dataLength,isNullable,dataDefaule,primaryKey,isIndentity = row
			columnNames.append(columnName + " = %s")
				
		return sqlSentence % (TableName," and ".join(columnNames))
	
insertSentence = "insert into aa(%s) values(%s); "
	
def HandleJson(filename):
	f = open(filename,encoding='utf-8',errors='ignore');
	filecontent = f.readlines();
	f.close();
	
	jsonstr = "".join(filecontent)
	#转换为json对象
	jsondatas = json.loads(jsonstr)
	
	sqlSentence = []
	# for json in jsondatas:
		# for item in json:
			# columsNames = []
			# columsValues = []
			
	
	#处理json数组中的第一个对象的key的名称
	columsNames = []
	for item in jsondatas[0]:
		columsNames.append(item)
	
	insertColums = ",".join(columsNames)
	
	for jsondata in jsondatas:
		columsValues = []
		for item in columsNames:
			columsValues.append("'"+str(jsondata[item]).replace("'",'"')+"'")
		insertValues = ",".join(columsValues)
		sqlSentence.append(insertSentence % (insertColums,insertValues))
	
	print(sqlSentence[0])
	
JSONNAME = "file.xlsx.json"
HandleJson(JSONNAME)	
	
# lines = []
# words = input("请将EXCEL文件拖入控制台内,以回车分割文件(单独输入':w')开始执行:\n")

# while words != ':w':
	# line = lines.append(words)
	# words = input()		

# for line in lines:
	# print("开始处理 "+ line)
	# HandleExcel(line)	
	# print("完成")
# print("全部完成")