# -*- coding: utf-8 -*-  
import cv2
import numpy as np
import datetime

dir_path = "D:\Program Files\opencv\sources\data\lbpcascades" # 配置OpenCV路径
filename = "lbpcascade_frontalface.xml" # 识别模式文件
model_path = dir_path + "/" + filename

#要使用Haar cascade实现，仅需要把库修改为lbpcascade_frontalface.xml
face_cascade = cv2.CascadeClassifier(model_path)	
	
#人脸识别
def GetFaces(imageName):
	"""获得人脸信息"""
	#cv2.imread()：读入图片，共两个参数，第一个参数为要读入的图片文件名，第二个参数为如何读取图片，包括:
	#cv2.IMREAD_COLOR：读入一副彩色图片；
	#cv2.IMREAD_GRAYSCALE：以灰度模式读入图片；
	#cv2.IMREAD_UNCHANGED：读入一幅图片，并包括其alpha通道。
	img = cv2.imread(imageName)
	# 设定灰度
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# 识别面部
	# 识别输入图片中的人脸对象.返回对象的矩形尺寸
	# 函数原型detectMultiScale(gray, 1.2,3,CV_HAAR_SCALE_IMAGE,Size(30, 30))
	# gray需要识别的图片
	# 1.03：表示每次图像尺寸减小的比例
	# 5：表示每一个目标至少要被检测到4次才算是真的目标(因为周围的像素和不同的窗口大小都可以检测到人脸)
	# CV_HAAR_SCALE_IMAGE表示不是缩放分类器来检测，而是缩放图像，Size(30, 30)为目标的最小最大尺寸
	# faces：表示检测到的人脸目标序列
	faces = face_cascade.detectMultiScale(gray, 1.03, 5)
	
	for (x,y,w,h) in faces:
		if w+h>200:#//针对这个图片画出最大的外框
			img2 = cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),4)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = img[y:y+h, x:x+w]
	#cv2.imshow()创建一个窗口显示图片，共两个参数，第一个参数表示窗口名字，可以创建多个窗口中，但是每个窗口不能重名；
	#第二个参数是读入的图片。
	cv2.imshow('img',img)
	#cv2.waitKey()：键盘绑定函数，共一个参数，表示等待毫秒数，将等待特定的几毫秒，看键盘是否有输入，返回值为ASCII值。
	#如果其参数为0，则表示无限期的等待键盘输入。
	cv2.waitKey(0)
	#cv2.destroyAllWindows()：删除建立的全部窗口。
	#cv2.destroyWindows()：删除指定的窗口。
	cv2.destroyAllWindows()
	#cv2.imwrite()：保存图片，共两个参数，第一个为保存文件名，第二个为读入图片。
	cv2.imwrite("head.jpg", img) # 保存图片

	
GetFaces("1.jpg")