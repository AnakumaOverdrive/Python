# -*- coding: utf-8 -*-  
import cv2,os
import numpy as np
import datetime

def resizeImgs(path,w,h): 
	"""改变图片大小"""
	for dirname, dirnames, filenames in os.walk(path):
		print(dirname, dirnames, filenames)
		for filename in filenames:
			#print(os.path.join(dirname, filename))
			#排除非图片类型的文件
			if os.path.splitext(os.path.join(dirname, filename))[1].lower() != ".db":
				img = cv2.imread(os.path.join(dirname, filename),cv2.IMREAD_GRAYSCALE)
				res=cv2.resize(img,(w,h),interpolation=cv2.INTER_CUBIC)
				cv2.imwrite("RES."+filename, res) # 保存图片
resizeImgs("yalefaces\\s1",100,100)
