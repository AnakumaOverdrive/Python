# -*- coding: utf-8 -*-  
#LinearSVC+PCA分类识别人脸 结合 获取人脸灰度图(带翻转) 两个Dome实现

from numpy import *
import numpy as np
import sys,os
import PIL.Image as Image
import matplotlib.pyplot as plt  
from sklearn import svm
from sklearn import decomposition
import cv2
import datetime,time

dir_path = "D:\Program Files\opencv\sources\data\haarcascades" # 配置OpenCV路径
filename = "haarcascade_frontalface_default.xml" # 识别模式文件
model_path = dir_path + "/" + filename

def HorizontalFlip(img):
	"""翻转图片
	http://www.cnblogs.com/xianglan/archive/2010/12/25/1916982.html"""
	height = img.shape[0]  
	width = img.shape[1]
	iLR = np.zeros(img.shape, np.uint8)  
	for i in range(height):
		for j in range(width):
			#iUD[height-1-i,j] = img[i,j]	#垂直
			iLR[i,width-1-j] = img[i,j]		#水平
			#iAcross[h-1-i,w-1-j] = image[i,j]	#对角
	return iLR
	
class Eigenfaces(object):
	def __init__(self):
		self.images = []
		self.y = []
		self.z = []
		self.Mat=[]
		self.MatPCA = []
		self.clf = svm.LinearSVC() #线性分类
		self.pca = decomposition.PCA(n_components=15) #降维
		#self.pca = decomposition.PCA(n_components='mle') #将自动选取特征个数n，使得满足所要求的方差百分比。

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
		self.clf.fit(self.MatPCA,self.z) 
		#self.clf.fit(self.Mat,self.z) 
		
	def predict(self,image):
		"""预测最接近的特征脸"""
		mat = image.reshape(1,-1)
		#非降维处理
		#rdata = self.clf.predict(mat)
		#降维处理
		X = self.pca.transform(mat)
		rdata = self.clf.predict(X)
		return rdata

	#人脸识别
def FaceRecognition(image,width,height,Eigenfaces):
	faceText = ""
	# 创建 classifier
	clf = cv2.CascadeClassifier(model_path)
	# 设定灰度
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#识别
	faces = clf.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE
	)
	#在视频中央绘制一个200 * 200像素的方框,用于辅助截图
	#cx = int(width / 2) -100
	#cy = int(height / 2) -100
	#cv2.rectangle(image, (cx,cy), (cx+200, cy+200), (0, 255, 0), 2)
	#cv2.circle(image, (int(width / 2),int(height / 2)), 1, (255, 0, 0), 2)
	
	#绘制人脸识别边框
	for (x, y, w, h) in faces:
		cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
		try:
			crop = image[y:y+h,y:x+w] 
			#会出现尺寸错误
			res=cv2.resize(crop,(100,100),interpolation=cv2.INTER_CUBIC)
			#设置为灰度图
			for x in res:  
				for y in x:
					y[0]=y[1]=y[2]=y[0]*0.299+y[1]*0.587+y[2]*0.114
			#将Opencv Image 转换成 PIL Image 对象
			rheight, rwidth, channels = res.shape
			pimg = Image.frombytes("RGB", (rheight, rwidth), res.tostring()) 
			pimg = pimg.convert("L") #数据转换为long类型
			testImg = np.asarray(pimg, dtype=np.uint8)
			#输出预测结果
			faceText = str(ef.predict(testImg))
		except:
			faceText = ""
	#页面水平翻转
	image = HorizontalFlip(image)
	#视频页面输出
	cv2.putText(image,faceText , (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)	
	cv2.putText(image, datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
	return image

#训练
ef = Eigenfaces()
ef.loadimgs("esint")
ef.compute()

cap = cv2.VideoCapture(0) # 从摄像头中取得视频
# 获取视频播放界面长宽
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

#模拟测试
#TestFun(ef,"TestImg//HB.mx.jpg")

while(cap.isOpened()):
	#读取帧摄像头
	ret, frame = cap.read()
	if ret == True:
		cusImg = frame.copy()
		#输出当前帧
		cusImg=FaceRecognition(cusImg,width,height,ef)
		cv2.imshow('My Camera',cusImg)
		#键盘按 Q 退出
		if (cv2.waitKey(1) & 0xFF) == ord('q'):
			break;
		elif (cv2.waitKey(1) & 0xFF) == ord('w') or (cv2.waitKey(1) & 0xFF) == ord('W'):
			break
		elif (cv2.waitKey(1) & 0xFF) == 27:
			break
	else:
		break
# 释放资源
cap.release()
cv2.destroyAllWindows()