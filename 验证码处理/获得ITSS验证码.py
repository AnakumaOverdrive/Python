from urllib import request
import time

def downImage(src):
	newFileName = "Img"+ str(round(time.time() * 1000)) +".jpg"
	request.urlretrieve(src,newFileName)
	time.sleep(0.01);
	
for i in range(20):
	downImage('http://192.168.100.16:9896/Pages/ValidCode.aspx?r=Math.random()')

        





