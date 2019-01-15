# -*- coding: utf-8 -*-  
import cv2,os
import numpy as np
import datetime

def HBImgs(path): 
	"""改变图片大小"""
	for dirname, dirnames, filenames in os.walk(path):
		#print(dirname, dirnames, filenames)
		for filename in filenames:
			#print(os.path.join(dirname, filename))
			#排除非图片类型的文件
			if os.path.splitext(os.path.join(dirname, filename))[1].lower() != ".db":
				img = cv2.imread(os.path.join(dirname, filename),cv2.IMREAD_GRAYSCALE)
				cv2.imwrite("esint\\test\\HB."+filename, img) # 保存图片
HBImgs("esint\\test")
