# -*- coding: utf-8 -*-  
import cv2
import numpy as np
import datetime

dir_path = "D:\Program Files\opencv\sources\data\haarcascades" # 配置OpenCV路径
#filename = "haarcascade_frontalface_default.xml" # 识别模式文件
filename = "haarcascade_eye_tree_eyeglasses.xml"
model_path = dir_path + "/" + filename

def dist(x1,x2,y1,y2,):
	return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
	
#人脸识别
def gface(image):
	# 创建 classifier
	clf = cv2.CascadeClassifier(model_path)
	# 设定灰度
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# 识别面部
	# 识别输入图片中的人脸对象.返回对象的矩形尺寸
	# 函数原型detectMultiScale(gray, 1.2,3,CV_HAAR_SCALE_IMAGE,Size(30, 30))
	# gray需要识别的图片
	# 1.03：表示每次图像尺寸减小的比例
	# 5：表示每一个目标至少要被检测到4次才算是真的目标(因为周围的像素和不同的窗口大小都可以检测到人脸)
	# CV_HAAR_SCALE_IMAGE表示不是缩放分类器来检测，而是缩放图像，Size(30, 30)为目标的最小最大尺寸
	# faces：表示检测到的人脸目标序列
	faces = clf.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE
	)
	#print("Found {0} faces!".format(len(faces)))
	flag = False;
	# 画方框
	#for (x, y, w, h) in faces:
	#	x1 = x + int(w / 2)
	#	y1 = y + int(h / 2)
	#	cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
	#	cv2.circle(image, (x1,y1), 2, (255, 0, 0), 2)
	#	flag = True

	cv2.rectangle(image, (150 ,100),(450, 400), (0, 255, 0), 2)
	
	if len(faces) == 2 :
		for (x, y, w, h) in faces:
			x1 = x + int(w / 2)
			y1 = y + int(h / 2)
			cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 255), 2)
			cv2.circle(image, (x1,y1), 2, (255, 0, 0), 2)
			print(dist(x,x1,y,y1))
		flag = True
	
	#if flag == True:
	#	now = datetime.datetime.now()
	#	otherStyleTime = now.strftime("%Y-%m-%d %H-%M-%S")  +'.jpg'
	#	cv2.imwrite(otherStyleTime, image)
	#	out.release()
	#	cap.release()
	#	cv2.destroyAllWindows()
	return image
	
cap = cv2.VideoCapture(0) # 从摄像头中取得视频
# 获取视频播放界面长宽
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
# 定义编码器 创建 VideoWriter 对象
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use the lower case
#fourcc = cv2.VideoWriter_fourcc(*'mp4 / MP4 (MPEG-4 Part 14)') 
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (width, height))
while(cap.isOpened()):
	#读取帧摄像头
	ret, frame = cap.read()
	if ret == True:
		#输出当前帧
		frame=gface(frame)
		out.write(frame)
		cv2.imshow('My Camera',frame)
		#键盘按 Q 退出
		if (cv2.waitKey(1) & 0xFF) == ord('q'):
			break
	else:
		break
# 释放资源
out.release()
cap.release()
cv2.destroyAllWindows()