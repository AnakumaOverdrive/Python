# -*- coding: utf-8 -*-  
#http://blog.csdn.net/mingtian715/article/details/54380623

from numpy import *
import numpy as np
import sys,os
import PIL.Image as Image
import matplotlib.pyplot as plt  
from sklearn import svm
from sklearn import decomposition
import cv2
from sklearn.externals import joblib

class Eigenfaces(object):
	def __init__(self):
		self.images = []
		self.y = []
		self.z = []
		self.Mat=[]
		self.MatPCA = []
		self.clf = svm.LinearSVC() #线性分类
		self.pca = decomposition.PCA(n_components=15) #降维

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
		self.clf.fit(self.MatPCA,self.z) 
		joblib.dump(self.pca, 'LearningModel/esint.pca') 
		joblib.dump(self.clf, 'LearningModel/esint.pkl') 

ef = Eigenfaces()
ef.loadimgs("esint")
ef.compute()
