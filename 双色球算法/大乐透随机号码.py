import time,random,math,os

def loadExcludeNumber():
	excludeNumber = []
	excludeLowNumber = []
	file = open('排除号码.txt')
	lines = file.readlines()
	for line in lines:
		tmp = line.replace('\n','').replace(' ','').split(',')
		if len(tmp) > 0:
			excludeNumber.extend(tmp[:5])
			excludeLowNumber.extend(tmp[5:])
		
	excludeNumber = list(set(excludeNumber))
	excludeLowNumber = list(set(excludeLowNumber))
	return excludeNumber,excludeLowNumber
	
def getRandomNumber(s,e,excludeNumber):
	while True:
		num = random.randint(s,e)
		if num not in excludeNumber:
			return num

def simpleRandomGreatLotto():
	num = [random.randint(1,35) for i in range(5)]
	while len(num) != len(set(num)):
		num = [random.randint(1,35) for i in range(5)]
		
	lownum = [random.randint(1,12) for i in range(2)]
	while len(lownum) != len(set(lownum)):
		lownum = [random.randint(1,12) for i in range(2)]
			
def excludeRandomGreatLotto():
	#获得需要排除的数字
	excludeNumber,excludeLowNumber = loadExcludeNumber();
	
	num = [getRandomNumber(1,35,excludeNumber) for i in range(5)]
	while len(num) != len(set(num)):
		num = [getRandomNumber(1,35,excludeNumber) for i in range(5)]
		
	lownum = [getRandomNumber(1,12,excludeLowNumber) for i in range(2)]
	while len(lownum) != len(set(lownum)):
		lownum = [getRandomNumber(1,12,excludeLowNumber) for i in range(2)]
			
	num.sort()
	lownum.sort()
	num.extend(lownum)
	return num

isExcludeNumber = input("是否启用排除号码功能?(y/n)").lower()

if isExcludeNumber == 'y':
	excludeNumber,excludeLowNumber = loadExcludeNumber();
	print("前5位所要排除的号码是:",excludeNumber)
	print("后2位所要排除的号码是:",excludeLowNumber)
	
count = input("请输入要随机的注数:")

file=open('大乐透随机号码.txt','w') 

for i in range(0,int(count)):
	n1 = excludeRandomGreatLotto() if isExcludeNumber == 'y' else simpleRandomGreatLotto()
	print(n1)
	file.write(str(n1)+'\n'); 

file.close()

os.startfile("大乐透随机号码.txt"); 
