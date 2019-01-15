# -*- coding: utf-8 -*-  
#http://blog.csdn.net/mingtian715/article/details/54380623

from numpy import *
import numpy as np
import sys,os
#import PIL.Image as Image,ImageDraw
from PIL import Image,ImageDraw
import matplotlib.pyplot as plt  
from sklearn import svm
from sklearn import decomposition
import cv2

class Eigenfaces(object):
	def __init__(self):
		self.images = []
		self.y = []
		self.z = []
		self.foldername = []
		self.Mat=[]
		self.MatPCA = []
		self.clf = svm.LinearSVC() #线性分类
		self.pca = decomposition.PCA(n_components=150) #降维

	def loadimgs(self,path):
		"""加载图片数据集"""
		classlabel = 0
		for dirname, dirnames, filenames in os.walk(path):
			for subdirname in dirnames:
				sub_path = os.path.join(dirname, subdirname)
				for filename in os.listdir(sub_path):
					#排除非图片类型的文件
					if os.path.splitext(os.path.join(sub_path, filename))[1].lower() != ".db":
						im = Image.open(os.path.join(sub_path, filename))
						im = im.convert("L") #数据转换为long类型
						self.images.append(np.asarray(im, dtype=np.uint8))
						self.y.append(classlabel)
						self.z.append(sub_path)
						self.foldername.append(subdirname)
				classlabel += 1 
	
	def genRowMatrix(self):
		"""将图片变为行向量 生成图片矩阵"""
		self.Mat = np.empty((0, self.images[0].size), dtype=self.images[0].dtype)
		for row in self.images:
			self.Mat = np.vstack((self.Mat, np.asarray(row).reshape(1,-1)))		
	
	def PCA(self):
		"""用主成分分析降维"""
		self.pca.fit(self.Mat)
		self.MatPCA = self.pca.transform(self.Mat)
		
	def compute(self):
		self.genRowMatrix() 
		self.PCA()
		#从数据中学习
		self.clf.fit(self.MatPCA,self.foldername) 
		
	def predict(self,image):
		"""预测最接近"""
		mat = image.reshape(1,-1)
		X = self.pca.transform(mat)
		rdata = self.clf.predict(X)
		return rdata

def TestFun(Eigenfaces,fileName):
	im = Image.open(fileName)
	im = im.convert("L") #数据转换为long类型
	testImg = np.asarray(im, dtype=np.uint8)
	print("预测值 =",Eigenfaces.predict(testImg))
	return Eigenfaces.predict(testImg)
	
	
class VerificationCode(object):
	def __init__(self):
		self.Images = []
		self.ImagPath = []
		self.ImageName = []
		self.threshold = 90 #阈值
		self.table = []
		self.TwoValueImages = [] #二值化图片
		self.ClearNoiseImages =[] #降噪图片

	def loadimgs(self,path):
		"""加载图片数据集"""
		for dirname, dirnames, filenames in os.walk(path):
			for filename in filenames:
				if os.path.splitext(os.path.join(dirname, filename))[1].lower() != ".db":
					im = Image.open(os.path.join(dirname, filename))
					im = im.convert("L") #数据转换为long类型
					#self.Images.append(np.asarray(im, dtype=np.uint8))
					self.Images.append(im)
					self.ImagPath.append(dirname)
					self.ImageName.append(filename)
					
	def getPixel(self,image,x,y,G,N):  
	# G: Integer 图像二值化阀值   
	# N: Integer 降噪率 0 <N <8   
	# Z: Integer 降噪次数  
		L = image.getpixel((x,y))  
		if L > G:  
			L = True  
		else:  
			L = False  
	  
		nearDots = 0  
		if L == (image.getpixel((x - 1,y - 1)) > G):  
			nearDots += 1  
		if L == (image.getpixel((x - 1,y)) > G):  
			nearDots += 1  
		if L == (image.getpixel((x - 1,y + 1)) > G):  
			nearDots += 1  
		if L == (image.getpixel((x,y - 1)) > G):  
			nearDots += 1  
		if L == (image.getpixel((x,y + 1)) > G):  
			nearDots += 1  
		if L == (image.getpixel((x + 1,y - 1)) > G):  
			nearDots += 1  
		if L == (image.getpixel((x + 1,y)) > G):  
			nearDots += 1  
		if L == (image.getpixel((x + 1,y + 1)) > G):  
			nearDots += 1  
	  
		if nearDots < N:  
			return image.getpixel((x,y-1))  
		else:  
			return None  
			
	def initTable(self):
		for i in range(256):
			if i < self.threshold:
				self.table.append(0)
			else:
				self.table.append(1)
				
	def TwoValuePro(self):
		"""二值化图片"""
		self.initTable()
		for image in self.Images:
			out = image.point(self.table, '1')
			#out.show()
			self.TwoValueImages.append(out)
			
	def ClearNoise(self):  
		"""降噪点"""
		self.TwoValuePro()
		for image in self.TwoValueImages:
			draw = ImageDraw.Draw(image) 
			for x in range(1,image.size[0] - 1):
				for y in range(1,image.size[1]-1):
					color = self.getPixel(image,x,y,140,1)
					c = str(color)
					if color != None: 
						draw.point((x,y),c)	

			self.ClearNoiseImages.append(image)	  

	def Forecast(self,Eigenfaces):
		"""预测"""
		self.ClearNoise()
		for i in range(len(self.ClearNoiseImages)):
			ChildImgs = crop(self.ClearNoiseImages[i]);
			ForecastValue = "";
			for childImg in ChildImgs:
				childImg = childImg.convert("L") #数据转换为long类型
				testImg = np.asarray(childImg, dtype=np.uint8)
				try:
					ForecastValue +=Eigenfaces.predict(testImg)[0]
				except:
					ForecastValue +='X'
			#print(ForecastValue,self.ImagPath[i],self.ImageName[i])
			os.rename(os.path.join(self.ImagPath[i], self.ImageName[i]),os.path.join(self.ImagPath[i], ForecastValue+".jpg"))
				
				

def crop(img):
	"""切图原理
	1.图片的大小 100 * 50
	2.左白 11 上白 8 右白 11 下白 8
	3.数字大小 19  字间距 3
	"""
	ChildImg = []  
	for i in range(4):
		x = 11 + i * (19 + 1)  # 见原理图 调整字间距为1
		y = 8
		child_img = img.crop((x, y, x + 18, y + 30))
		ChildImg.append(child_img)	
	return ChildImg

ef = Eigenfaces()
ef.loadimgs("ITSSFont")
ef.compute()
vc = VerificationCode()
vc.loadimgs("unknown")
vc.Forecast(ef)