import feedparser
import re
import jieba
from math import sqrt
from PIL import Image,ImageDraw,ImageFont  
import random

fontMsyh = ImageFont.truetype("msyh.ttc",10)  

def readfile(filename):
	lines = [line for line in open(filename,'r',encoding='utf-8',errors='ignore')]
	
	#第一行是列标题
	colnames = lines[0].strip().split('\t')[1:]
	rownames = []
	data = []
	for line in lines[1:]:
		p = line.strip().split('\t')
		#每行的第一列是行名
		rownames.append(p[0])
		#剩余部分是该行对应的数据
		data.append([float(x) for x in p[1:]])
	return rownames,colnames,data

def pearson(v1,v2):
	#简单求和
	sum1 = sum(v1)
	sum2 = sum(v2)
	
	#求平方和
	sum1Sq = sum([pow(v,2) for v in v1])
	sum2Sq = sum([pow(v,2) for v in v2])
	
	#求乘积之和
	pSum = sum([v1[i] * v2[i] for  i in range(len(v1))])
	
	#计算r
	num = pSum - (sum1*sum2 / len(v1))
	den = sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))
	if den == 0 : return 0
	return 1.0-num/den

def tanimoto(v1,v2):
	"""Tanimoto系数 
返回一个介于1.0和0.0之间的值。
其中1.0代表不存在同时喜欢两件物品的人，
而0.0则代表所有人都同时喜欢两个向量中的物品"""
	c1,c2,shr = 0,0,0
	
	for i in range(len(v1)):
		if v1[i] != 0: c1+=1 #出现在v1中
		if v2[i] != 0: c2+=1 #出现在v2中
		if v1[i] != 0 and v2[i] != 0: shr+=1 #在两个向量中都出现。
		
	return 1.0 -(float(shr)) / (c1+c2-shr)
	
class bicluster:
	"""双聚类"""
	def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
		self.left = left
		self.right = right
		self.vec = vec
		self.id = id
		self.distance = distance
	
def hcluster(row,distance=pearson):
	"""分级聚类"""
	distances = {}
	currentclustid = -1
	
	#最开始的聚类就数据集中的行
	clust = [bicluster(row[i],id=i) for i in range(len(row))]
	print(len(clust))
	while len(clust) > 1:
		lowestpair = (0,1)
		#最近距离
		closest = distance(clust[0].vec,clust[1].vec)
		#print(closest,lowestpair)
		#遍历每一个配对，寻找最小距离
		for i in range(len(clust)):
			for j in range(i+1,len(clust)):
				#用distances来缓存距离的计算值
				if(clust[i].id,clust[j].id) not in distances:
					distances[clust[i].id,clust[j].id] = distance(clust[i].vec,clust[j].vec)
				d = distances[(clust[i].id,clust[j].id)]

				if d < closest :
					closest = d
					lowestpair = (i,j)
				
		#print(closest,lowestpair)
		#计算两个聚类的平均值
		mergevec = [(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i])/2.0 for i in range(len(clust[0].vec))]
		#建立新的聚类
		newcluster = bicluster(mergevec,left=clust[lowestpair[0]],right=clust[lowestpair[1]],distance=closest,id=currentclustid)
	
		#不在原始集合中的聚类，其id为负数
		#print(len(clust),lowestpair[0],lowestpair[1],clust[lowestpair[0]],clust[lowestpair[1]])
		currentclustid -=1
		delItem1 = clust[lowestpair[0]]
		delItem2 = clust[lowestpair[1]]
		clust.remove(delItem1)
		clust.remove(delItem2)
		clust.append(newcluster)
	return clust[0]
	
def printclust(clust,labels=None,n=0):
	"""打印聚类"""
	#利用缩进来建立层级布局
	for i in range(n): print(' ', end=' ')
	if clust.id < 0:
		#负数标记代表这是一个分支
		print('-')
	else:
		#正数标记代表这是一个叶节点
		if labels == None: 
			print(clust.id)
		else:
			print(labels[clust.id])
	#现在开始打印右侧分支和左侧分支
	if clust.left != None:
		printclust(clust.left,labels=labels,n=n+1)
	if clust.right != None:
		printclust(clust.right,labels=labels,n=n+1)
		
def getheight(clust):
	#这是一个叶节点吗？若是，则高度为1
	if clust.left == None and clust.right == None : return 1
	#否则，高度为每个分支的高度之和
	return getheight(clust.left) + getheight(clust.right)
	
def getdepth(clust):
	#一个叶节点的距离是0.0
	if clust.left == None and clust.right == None: return 0
	#y一个枝节点的距离等于左右两侧分支中距离较大者，
	#加上该枝节点自身的距离
	return max(getdepth(clust.left),getdepth(clust.right))+clust.distance
	
def drawdendrogram(clust,labels,jpeg='ckysters.jpg'):
	#高度和宽度
	h = getheight(clust)*30
	w=1200
	depth = getdepth(clust)
	
	#由于宽度是固定的，因此我要需要对距离值做相应的调整
	scaling=float(w-150)/depth
	
	#新建一个白色背景的图片
	img = Image.new('RGB',(w,h),(255,255,255))
	draw = ImageDraw.Draw(img)

	draw.line((0,h/2,10,h/2),fill=(255,0,0))
	
	#画第一个节点
	drawnode(draw,clust,10,(h/2),scaling,labels)
	img.save(jpeg,'JPEG')
	
def drawnode(draw,clust,x,y,scaling,labels):
	#print(clust.id)
	if clust.id < 0:
		h1=getheight(clust.left)*20
		h2=getheight(clust.right)*20
		top=y-(h1+h2)/2
		bottom=y+(h1+h2)/2
		#线的长度
		ll = clust.distance*scaling
		#聚类到其子节点的垂直线
		draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))
		#链接左侧节点的水平线
		draw.line((x,top+h1/2,x+11,top+h1/2),fill=(255,0,0))
		#链接右侧节点的水平线
		draw.line((x,bottom-h2/2,x+11,bottom-h2/2),fill=(255,0,0))
		#调用函数回执左右节点
		drawnode(draw,clust.left,x+11,top+h1/2,scaling,labels)
		drawnode(draw,clust.right,x+11,bottom-h2/2,scaling,labels)
	else:
		#如果这是一个叶节点，则绘制节点的标签
		try:
			draw.text((x+5,y-7),labels[clust.id],(0,0,0),font=fontMsyh)
		except Exception:
			text = ""+str(clust.id)
			draw.text((x+5,y-7),text,(0,0,0),font=fontMsyh)

def rotatematrix(data):
	newdata = []
	for i in range(len(data[0])):
		newrow = [data[j][i] for j in range(len(data))]
		newdata.append(newrow)
	return newdata

def kcluster(rows,distance=pearson,k=4):
	#确定每个点的最小值和最大值
	ranges = [(min([row[i] for row in rows]),max([row[i] for row in rows])) for i in range(len(rows[0]))]
	
	#随机创建k个中心点
	clusters = [
		[
			random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] 
			for i in range(len(rows[0]))
		] 
		for j in range(k)
	]
	
	lastmatches=None
	for t in range(100):
		print('Iteration %d' % t)
		bestmatches = [[] for i in range(k)]
		#print(bestmatches)
		
		#在每一行中寻找距离最近的中心点
		for j in range(len(rows)):
			row = rows[j]
			bestmatch = 0
			for i in range(k):
				d = distance(clusters[i],row)
				if d < distance(clusters[bestmatch],row):
					bestmatch = i
			bestmatches[bestmatch].append(j)
		
		#如果结果与上一次相同，则整个过程结果
		if bestmatches == lastmatches : break
		lastmatches = bestmatches
		#print(bestmatches)
		
		#把中心点移到其所有成员的平均位置处
		for i in range(k):
			avgs = [0.0] * len(rows[0])
			#print(len(avgs),len(bestmatches[i]))
			
			if len(bestmatches[i]) >0:
				for rowid in bestmatches[i]:
					for m in range(len(rows[rowid])):
						#print(row[rowid])
						avgs[m] += rows[rowid][m]
				for j in range(len(avgs)):
					avgs[j] /= len(bestmatches[i])
				#将中心点的数据更新为分配给它的所有项的平均位置
				clusters[i] = avgs
			#print(avgs)
	return bestmatches
	
def scaledown(data,distance=pearson,rate=0.01):
	"""多维缩放"""
	n = len(data)
	
	#每一对数据项之间的真实距离
	realdist = [[(distance(data[i],data[j])) for j in range(n)] for i in range(0,n)]

	outersum = 0.0
	
	#随机初始化节点在二维空间中的起始位置
	loc = [[random.random(),random.random()] for i in range(n)]
	fakedist = [[0.0 for j in range(n)] for i in range(n)]
	
	lasterror = None
	for m in range(0,1000):
		#寻找投影后的距离
		for i in range(n):
			for j in range(n):
				fakedist[i][j] = sqrt(sum([pow(loc[i][x]-loc[j][x],2) for x in range(len(loc[i]))]))
	
		#移动节点
		grad =[[0.0,0.0] for i in range(n)]
		
		totalerror = 0
		for k in range(n):
			for j in range(n):
				if j == k: continue
				#误差值等于目标距离与当前距离之间差值的百分比
				errorterm=(fakedist[j][k]-realdist[j][k])/realdist[j][k]
				#每一个节点都需要根据误差的多少，按比例移离或移向其他节点
				grad[k][0] += ((loc[k][0]-loc[j][0])/fakedist[j][k])*errorterm
				grad[k][1] += ((loc[k][1]-loc[j][1])/fakedist[j][k])*errorterm
				
				#记录总的误差值
				totalerror += abs(errorterm)
		print(totalerror)
		
		#如果节点移动之后的情况变得更糟，则程序结束
		if lasterror and lasterror < totalerror : break
		lasterror = totalerror
	
		#根据rate参数与grad值相乘的结果，移动每一个节点
		for k in range(n):
			loc[k][0] -= rate*grad[k][0]
			loc[k][1] -= rate*grad[k][1]
	return loc
	
def draw2d(data,labels,jpeg='mds2d.jpg'):
	img = Image.new('RGB',(2000,2000),(255,255,255))
	draw = ImageDraw.Draw(img)
	for i in range(len(data)):
		x = (data[i][0]+0.5)*1000
		y = (data[i][1]+0.5)*1000
		draw.text((x,y),labels[i],(0,0,0),font=fontMsyh)
	img.save(jpeg,'JPEG')
#blognames,words,data = readfile('rss.txt')
#clust = hcluster(data)	
#print('#############')
#printclust(clust,labels=blognames)	
#drawdendrogram(clust,blognames,jpeg='blogclust.jpg')
		
#rdata = rotatematrix(data)
#wordclust = hcluster(rdata)		
#drawdendrogram(wordclust,words,jpeg='wordclust.jpg')		
	
#clust = kcluster(data,k=10)
#print('#####################')
#for i in range(10):
#	print([blognames[r] for r in clust[i]])
	
#wants,people,data = readfile('zebo.txt')	
#clust = hcluster(data,distance=tanimoto)
#drawdendrogram(clust,wants,jpeg='wants1.jpg')	
	
	
#blognames,words,data = readfile('text.txt')
#coords = scaledown(data)
#draw2d(coords,blognames,jpeg='blog2d.jpg')	

blognames,words,data = readfile('text.txt')
#print(len(blognames),len(words),len(data))
print("rotatematrix")
rdata = rotatematrix(data)
print("hcluster")
clust = hcluster(rdata)	
print("drawdendrogram")
drawdendrogram(clust,words,jpeg='blogclust.jpg')
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	