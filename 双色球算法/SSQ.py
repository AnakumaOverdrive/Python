import time,random,math
from pylab import *
import numpy as np

def loadData(f):
	rows = []
	for line in open(f):
		rows.append(line.split())
	return rows
	
datas = loadData("03001-17148.txt")
# print(datas)
# for data in datas:
	# print(data[2:9])
	
# x = [[1,2,8,13,17,24,13],[14,15,18,25,26,30,1]]
y = [1,2,3,4,5,6,7]
dataX = np.array(datas)

plot(dataX[:,1],dataX[:,2],'o')

show()
