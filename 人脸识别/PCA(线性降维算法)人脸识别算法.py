# -*- coding: utf-8 -*-  
#http://blog.csdn.net/wangyaninglm/article/details/51731989

from numpy import *
import numpy as np
import sys,os
import copy
import cv2
import PIL.Image as Image
import matplotlib.pyplot as plt  

class Eigenfaces(object):
	def __init__(self):
		self.eps = 1.0e-16
		self.X = []
		self.y = []
		self.z = []
		self.Mat=[]
		self.eig_v = 0
		self.eig_vect = 0
		self.mu = 0
		self.projections = [] #预测
		self.dist_metric=0 #距离度量

	def loadimgs(self,path): # 加载图片数据集
		classlabel = 0
		for dirname, dirnames, filenames in os.walk(path):
			for subdirname in dirnames:
				#print(subdirname)
				sub_path = os.path.join(dirname, subdirname)
				#print(sub_path)
				for filename in os.listdir(sub_path):
					#排除非图片类型的文件
					if os.path.splitext(os.path.join(sub_path, filename))[1].lower() != ".db":
						im = Image.open(os.path.join(sub_path, filename))
						im = im.convert("L") #数据转换为long类型
						self.X.append(np.asarray(im, dtype=np.uint8))
						self.y.append(classlabel)
						self.z.append(sub_path)
				classlabel += 1 
				
	# 将图片变为行向量  
	# 生成图片矩阵
	def genRowMatrix(self):
		#np.empty(tupleA) 产生一个tupleA维度大小的矩阵 （并不是你以为的0！！！！）
		self.Mat = np.empty((0, self.X[0].size), dtype=self.X[0].dtype)
		for row in self.X:
			#np.vstack() 垂直方向合拼函数
			#np.asarray()将列表转换成数组
			#reshape方法，可以创建一个改变了尺寸的新数组，原数组的shape保持不变 
			#注意a.reshape((1,-1))和a.reshape((1,2))和a.reshape((-1,1))
			self.Mat = np.vstack((self.Mat, np.asarray(row).reshape(1,-1)))	

	# 计算特征脸 线性降维算法
	def PCA(self, pc_num =0):
		self.genRowMatrix() 
		#.hape属性 数组的形状
		[n,d] = shape(self.Mat)
		#print(n,d)
		if ( pc_num <= 0) or ( pc_num>n):
			pc_num = n
		#mean()求平均值
		self.mu = self.Mat.mean(axis =0)
		#print(self.mu)
		#减去均值
		#self.Mat -= self.mu
		self.Mat = self.Mat - self.mu
		#print(self.Mat)
		if n>d:
			#np.dot(a,b) 计算矩阵的乘积
			XTX = np.dot(self.Mat.T,self.Mat)
			#linalg模块：numpy线性代数模块
			#linalg.eigh() 返回的特征值和特征向量的一个埃尔米特对称矩阵。
			#返回两个对象，包含一个一维数组的值，和一个二维正方形阵列或矩阵（取决于输入型）的对应的特征向量（列）。
			[ self.eig_v , self.eig_vect ] = linalg.eigh (XTX)
		else :
			XTX = np.dot(self.Mat,self.Mat.T)
			#print(XTX)
			[ self.eig_v , self.eig_vect ] = linalg.eigh (XTX)
			#print([ self.eig_v , self.eig_vect ])
		self.eig_vect = np.dot(self.Mat.T, self.eig_vect)
		#print(self.eig_vect)
		#print(n)
		#Python3 range 与 xrange 合拼了
		#for i in xrange(n):
		for i in range(n):
			#norm则表示范数，首先需要注意的是范数是对向量（或者矩阵）的度量，是一个标量（scalar）
			#print(type(i))
			#print(self.eig_vect[:,i])
			#print(linalg.norm(self.eig_vect[:,i]))
			self.eig_vect[:,i] = self.eig_vect[:,i]/linalg.norm(self.eig_vect[:,i])
		#argsort函数返回的是数组值从小到大的索引值 
		idx = np.argsort(-self.eig_v)
		self.eig_v = self.eig_v[idx]
		self.eig_vect = self.eig_vect[:,idx ]       
		self.eig_v = self.eig_v[0:pc_num ].copy () # select only pc_num
		self.eig_vect = self.eig_vect[:,0:pc_num].copy ()
		
	def compute(self):
		"""计算"""
		self.PCA()
		for xi in self.X:
			self.projections.append(self.project(xi.reshape(1,-1))) 	
		#print(self.projections)
			
	def distEclud(self, vecA, vecB):
		"""欧氏距离"""
		return linalg.norm(vecA-vecB)+self.eps 

	def cosSim(self, vecA, vecB):
		"""夹角余弦"""
		return (dot(vecA,vecB.T)/((linalg.norm(vecA)*linalg.norm(vecB))+self.eps))[0,0]
		
	def project(self,XI):
		"""映射"""
		if self.mu is None:
			return np.dot(XI,self.eig_vect)
		return np.dot(XI-self.mu, self.eig_vect) 
		
	def predict(self,XI):
		"""预测最接近的特征脸"""
		minDist = np.finfo('float').max
		minClass = -1
		Q = self.project(XI.reshape(1,-1))
		for i in range(len(self.projections)):
			dist = self.dist_metric(self.projections[i], Q)
			if dist < minDist:
				minDist = dist
				minClass = self.y[i]
		return minClass	
		
	def predict2(self,XI):
		"""预测最接近的特征脸"""
		minDist = np.finfo('float').max
		minClass = -1
		Q = self.project(XI.reshape(1,-1))
		for i in range(len(self.projections)):
			dist = self.dist_metric(self.projections[i], Q)
			if dist < minDist:
				minDist = dist
				minClass = self.z[i]
		return minClass	

	def subplot(self,title, images):
		"""生成特征脸"""
		fig = plt.figure()
		fig.text(.5, .95, title, horizontalalignment='center') 
		for i in range(len(images)):
			ax0 = fig.add_subplot(4,4,(i+1))
			plt.imshow(asarray(images[i]), cmap="gray")
			plt.xticks([]), plt. yticks([]) # 隐藏 X Y 坐标
		plt.show()
		
	def normalize(self, X, low, high, dtype=None):
		"""归一化"""
		X = np.asarray(X)
		minX, maxX = np.min(X), np.max(X)
		X = X - float(minX)
		X = X / float((maxX - minX))
		X = X * (high-low)
		X = X + low
		if dtype is None:
			return np.asarray(X)
		return np.asarray(X, dtype=dtype)
	
	
ef = Eigenfaces()
ef.dist_metric=ef.distEclud
#ef.loadimgs(os.getcwd())	
ef.loadimgs("yalefaces")
#ef.loadimgs("esint")
ef.compute()
E = []
X = mat(zeros((10,10304)))
for i in range(16):
	X = ef.Mat[i*10:(i+1)*10,:].copy()
	# X = ef.normalize(X.mean(axis =0),0,255)
	X = X.mean(axis =0)
	#imgs = X.reshape(112,92)
	imgs = X.reshape(100,100)
	E.append(imgs)
ef.subplot(title="AT&T Eigen Facedatabase", images=E)  


# 创建测试集
testImg = ef.X[30]
#print(testImg)
#cv2.imshow('img',testImg)
print("实际值 =", ef.y[30], "->", "预测值 =",ef.predict(testImg))

im = Image.open("RES.8.BMP")
im = im.convert("L") #数据转换为long类型
testImg = np.asarray(im, dtype=np.uint8)
print("预测值 =",ef.predict2(testImg))
