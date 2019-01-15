# -*- coding: utf-8 -*-  
import cv2
import numpy as np
import datetime,time,os
#import PIL.Image as Image
from PIL import Image,ImageDraw

class ImagePretreatment(object):
	"""图片预处理"""
	def __init__(self):
		self.Images = []
		self.threshold = 140 #阈值
		self.table = []
		self.TwoValueImages = [] #二值化图片
		self.ClearNoiseImages =[] #降噪图片
			
	def sum_9_region(self,img, x, y):
		"""
		9邻域框,以当前点为中心的田字框,黑点个数
		:param x:
		:param y:
		:return:
		"""
		# todo 判断图片的长宽度下限
		cur_pixel = img.getpixel((x, y))  # 当前像素点的值
		width = img.width
		height = img.height

		if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
			return 0

		if y == 0:  # 第一行
			if x == 0:  # 左上顶点,4邻域
				# 中心点旁边3个点
				sum = cur_pixel \
					  + img.getpixel((x, y + 1)) \
					  + img.getpixel((x + 1, y)) \
					  + img.getpixel((x + 1, y + 1))
				return 4 - sum
			elif x == width - 1:  # 右上顶点
				sum = cur_pixel \
					  + img.getpixel((x, y + 1)) \
					  + img.getpixel((x - 1, y)) \
					  + img.getpixel((x - 1, y + 1))

				return 4 - sum
			else:  # 最上非顶点,6邻域
				sum = img.getpixel((x - 1, y)) \
					  + img.getpixel((x - 1, y + 1)) \
					  + cur_pixel \
					  + img.getpixel((x, y + 1)) \
					  + img.getpixel((x + 1, y)) \
					  + img.getpixel((x + 1, y + 1))
				return 6 - sum
		elif y == height - 1:  # 最下面一行
			if x == 0:  # 左下顶点
				# 中心点旁边3个点
				sum = cur_pixel \
					  + img.getpixel((x + 1, y)) \
					  + img.getpixel((x + 1, y - 1)) \
					  + img.getpixel((x, y - 1))
				return 4 - sum
			elif x == width - 1:  # 右下顶点
				sum = cur_pixel \
					  + img.getpixel((x, y - 1)) \
					  + img.getpixel((x - 1, y)) \
					  + img.getpixel((x - 1, y - 1))

				return 4 - sum
			else:  # 最下非顶点,6邻域
				sum = cur_pixel \
					  + img.getpixel((x - 1, y)) \
					  + img.getpixel((x + 1, y)) \
					  + img.getpixel((x, y - 1)) \
					  + img.getpixel((x - 1, y - 1)) \
					  + img.getpixel((x + 1, y - 1))
				return 6 - sum
		else:  # y不在边界
			if x == 0:  # 左边非顶点
				sum = img.getpixel((x, y - 1)) \
					  + cur_pixel \
					  + img.getpixel((x, y + 1)) \
					  + img.getpixel((x + 1, y - 1)) \
					  + img.getpixel((x + 1, y)) \
					  + img.getpixel((x + 1, y + 1))

				return 6 - sum
			elif x == width - 1:  # 右边非顶点
				# print('%s,%s' % (x, y))
				sum = img.getpixel((x, y - 1)) \
					  + cur_pixel \
					  + img.getpixel((x, y + 1)) \
					  + img.getpixel((x - 1, y - 1)) \
					  + img.getpixel((x - 1, y)) \
					  + img.getpixel((x - 1, y + 1))

				return 6 - sum
			else:  # 具备9领域条件的
				sum = img.getpixel((x - 1, y - 1)) \
					  + img.getpixel((x - 1, y)) \
					  + img.getpixel((x - 1, y + 1)) \
					  + img.getpixel((x, y - 1)) \
					  + cur_pixel \
					  + img.getpixel((x, y + 1)) \
					  + img.getpixel((x + 1, y - 1)) \
					  + img.getpixel((x + 1, y)) \
					  + img.getpixel((x + 1, y + 1))
				return 9 - sum
		
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
				
	def loadimgs(self,path):
		"""加载图片数据集"""
		for dirname, dirnames, filenames in os.walk(path):
			for filename in filenames:
				if os.path.splitext(os.path.join(dirname, filename))[1].lower() != ".db":
					im = Image.open(os.path.join(dirname, filename))
					im = im.convert("L") #数据转换为long类型
					#self.Images.append(np.asarray(im, dtype=np.uint8))
					self.Images.append(im)
				
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
			self.ClearNoiseImages.append(draw)	  
			image.show()
imgp = ImagePretreatment()
imgp.loadimgs("one")
imgp.ClearNoise()








