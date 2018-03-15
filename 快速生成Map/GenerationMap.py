import os ;

def lowerCamel(str):
	"""转换首字母小写的驼峰命名"""
	newKey = [len(str)]
	newKey[0] = str[0].lower()
	newKey[1:] = str[1:]
	return ''.join(newKey)

f = open("JoinStr.txt");
lines = f.readlines();
f.close();

paramArr,jsArr,mbArr,jsColArr,funArr = [],[],[],[],[]

for line in lines:
	try:
		k,v = line.strip().split('\t')
	except:
		k = line.strip().split('\t')
		v = ''
	paramArr.append('mapParam.put("%s", %s);//%s '% (lowerCamel(k),lowerCamel(k),v))
	jsArr.append("%s:'',// %s" % (lowerCamel(k),v))
	mbArr.append("""<!--%s-->
<if test="%s != null and %s != ''">
	 and %s = #{%s}
</if>""" % (v,lowerCamel(k),lowerCamel(k),lowerCamel(k),lowerCamel(k)))
	jsColArr.append("""{
	field : '%s',
	width : 80,
	title : '%s,
	sort : true'
}""" % (lowerCamel(k),v))
	funArr.append("String %s," % lowerCamel(k))

param = '\n'.join(paramArr)
param += """
mapParam.put("_isPageView", page !=0 && limit !=0);// 是否分页
mapParam.put("_begin", (page - 1) * limit + 1);// 起始行
mapParam.put("_end", page * limit);// 结束行"""

jsPara = '\n'.join(jsArr)

mbPara = '\n'.join(mbArr)
jsColPara = '\n'.join(jsColArr)
funPara = ''.join(funArr)

layTable = """var table = layui.table;
table.render({
	elem : '#Datagrid',
	cellMinWidth : 80, //全局定义常规单元格的最小宽度，layui 2.2.1 新增
	cols :[[%s]]
	""" % jsColPara
	
mbXml = """
<select id="selectXXXXXXXXX" resultType="java.util.Map"	parameterType="java.util.Map">
<if test="_isPageView==true and _begin != null and _begin != '' and _end != null and _end != '' or _begin == 0 or _end == 0">
	select * from (SELECT *,ROW_NUMBER() OVER(ORDER BY orderbyID DESC) AS
	AllowPagingId
	FROM ( select *, 1 as orderbyID from (
</if>
//SQL SELECT
<where>
%s
</where>
<if test="_isPageView == true and _begin != null and _begin != '' and _end != null and _end != ''  or _begin == 0 or _end ==0">
	) as t1 ) as t2 ) as t3 where AllowPagingId between #{_begin}
	and #{_end}
</if>
</select>
"""	% mbPara


f = open("JoinOutStr.txt","w");
f.write(funPara);
f.write("\n\n\n");
f.write(param);
f.write("\n\n\n");
f.write(jsPara);
f.write("\n\n\n");
f.write(mbXml);
f.write("\n\n\n");
f.write(layTable);
f.close();

os.startfile("JoinOutStr.txt"); 
