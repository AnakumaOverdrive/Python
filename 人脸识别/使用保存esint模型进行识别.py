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
		self.pca = joblib.load('LearningModel/esint.pca')
		self.clf =  joblib.load('LearningModel/esint.pkl') 


	def predict(self,image):
		"""预测最接近的特征脸"""
		mat = image.reshape(1,-1)
		X = self.pca.transform(mat)
		rdata = self.clf.predict(X)
		return rdata

def TestFun(Eigenfaces,fileName):
	im = Image.open(fileName)
	im = im.convert("L") #数据转换为long类型
	testImg = np.asarray(im, dtype=np.uint8)
	print("预测值 =",Eigenfaces.predict(testImg))
		
ef = Eigenfaces()

TestFun(ef,"TestImg//HB.mx.jpg")
#TestFun(ef,"TestImg//HB.wz.jpg")
TestFun(ef,"TestImg//wangzhe.jpg")
TestFun(ef,"TestImg//geyan.jpg")
TestFun(ef,"TestImg//fr.jpg")
TestFun(ef,"TestImg//lx.jpg")
TestFun(ef,"TestImg//dw.jpg")
TestFun(ef,"TestImg//chen.jpg")
TestFun(ef,"TestImg//cl.jpg")
