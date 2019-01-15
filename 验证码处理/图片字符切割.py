# -*- coding: utf-8 -*-  
import cv2
import numpy as np
import datetime,time,os
#import PIL.Image as Image
from PIL import Image,ImageDraw

class ImageCrop(object):
	"""图片字符切割"""
	def __init__(self):
		self.Images = []
		self.ChildImg = [] #切割后的图片
			
				
	def loadimgs(self,path):
		"""加载图片数据集"""
		for dirname, dirnames, filenames in os.walk(path):
			for filename in filenames:
				if os.path.splitext(os.path.join(dirname, filename))[1].lower() != ".db":
					im = Image.open(os.path.join(dirname, filename))
					im = im.convert("L") #数据转换为long类型
					#self.Images.append(np.asarray(im, dtype=np.uint8))
					self.Images.append(im)
	def crop(self):
		"""切图原理
		1.图片的大小 100 * 50
		2.左白 11 上白 8 右白 11 下白 8
		3.数字大小 19  字间距 3
		"""
		for img in self.Images:
			for i in range(4):
				x = 11 + i * (19 + 1)  # 见原理图 调整字间距为1
				y = 8
				child_img = img.crop((x, y, x + 18, y + 30))
				self.ChildImg.append(child_img)
	
	def	Save(self,folder):
		"""保存图片"""
		if os.path.exists(folder) != True:
			os.makedirs(folder)
			
		for image in self.ChildImg:
			newFileName = folder+ "\Proc"+str(time.time())+".jpg"
			image.save(newFileName)
			time.sleep(0.0000001)
			
imgp = ImageCrop()
imgp.loadimgs("Pretreatment")
imgp.crop()
imgp.Save("Processing")








