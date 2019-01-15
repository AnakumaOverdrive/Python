# -*- coding: utf-8 -*-  
import cv2
import numpy as np
import datetime,time
import PIL.Image as Image

dir_path = "D:\Program Files\opencv\sources\data\haarcascades" # 配置OpenCV路径
filename = "haarcascade_frontalface_default.xml" # 识别模式文件
#filename = "haarcascade_eye_tree_eyeglasses.xml"
model_path = dir_path + "/" + filename

#font = cv2.InitFont(cv2.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8) #Creates a font

def dist(x1,x2,y1,y2,):
	return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
	
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
	
#人脸识别
def gface(image,width,height):
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
	
	#在视频中央绘制一个200 * 200像素的方框,用于辅助截图
	cx = int(width / 2) -100
	cy = int(height / 2) -100
	cv2.rectangle(image, (cx,cy), (cx+200, cy+200), (0, 255, 0), 2)
	cv2.circle(image, (int(width / 2),int(height / 2)), 1, (255, 0, 0), 2)
	
	#绘制人脸识别边框
	#for (x, y, w, h) in faces:
	#	cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
	#	print(dist(x,cx,y,cy),dist(x+w,cx+200,y+h,cy+200))
		
	#if flag == True:
	#	now = datetime.datetime.now()
	#	otherStyleTime = now.strftime("%Y-%m-%d %H-%M-%S")  +'.jpg'
	#	cv2.imwrite(otherStyleTime, image)
	#	out.release()
	#	cap.release()
	#	cv2.destroyAllWindows()
	return HorizontalFlip(image)
	
cap = cv2.VideoCapture(0) # 从摄像头中取得视频
# 获取视频播放界面长宽
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
while(cap.isOpened()):
	#读取帧摄像头
	ret, frame = cap.read()
	if ret == True:
		cusImg = frame.copy()
		#输出当前帧
		cusImg=gface(cusImg,width,height)
		cv2.imshow('My Camera',cusImg)
		#键盘按 Q 退出
		#if (cv2.waitKey(1) & 0xFF) == ord('q'):
		if (cv2.waitKey(1) & 0xFF) == ord('q'):
			#break
		#if (cv2.waitKey(1)) == ord('w'):
			#print(ord('q'),hex(ord('q')))
			#print(ord('w'),hex(ord('w')))
			cx = int(width / 2) -100 #220
			cy = int(height / 2) -100 #140
			#print(cx,cy) 
			#vis = frame.copy()
			crop = frame[cy:cy+200,cx:cx+200] 
			#crop = frame[140:140+200,220:220+200] 
			#将图片大小修改100 * 100
			res=cv2.resize(crop,(100,100),interpolation=cv2.INTER_CUBIC)
			#套用算法： r=g=b=(0.30r+0.59g+0.11b) 得到最合理灰度图
			#亮度方程: 0.299r+0.587g+0.114b
			for x in res:  
				for y in x:
					y[0]=y[1]=y[2]=y[0]*0.299+y[1]*0.587+y[2]*0.114  
			newFileName = "Face"+time.strftime('%Y%m%d%H%M%S')+".jpg"
			cv2.imwrite(newFileName, res) # 保存图片
			print(newFileName)
			#im = Image.open(frame)
			#break;
		if (cv2.waitKey(1) & 0xFF) == ord('w') or (cv2.waitKey(1) & 0xFF) == ord('W'):
			break
		if (cv2.waitKey(1) & 0xFF) == 27:
			break
	else:
		break
# 释放资源
cap.release()
cv2.destroyAllWindows()