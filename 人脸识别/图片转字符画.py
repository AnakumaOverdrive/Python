# -*- coding: utf-8 -*-  
from PIL import Image
import argparse
import os

IMG = "wz.jpg"
WIDTH = 50
HEIGHT = 50
OUTPUT = "zifu.txt"

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!;:,\"^`'.")
#ascii_char = list("$@B%8&WM#.")

def get_char(r,b,g,alpha = 256):
	if alpha == 0:
		return ' '
	length = len(ascii_char)
	gray = int(0.2126*r+0.7152*g+0.0722*b)

	unit = (256.0+1)/length
	return ascii_char[int(gray/unit)]
	
im = Image.open(IMG)
im = im.resize((WIDTH,HEIGHT),Image.NEAREST)
txt = ""
for i in range(HEIGHT):
	for j in range(WIDTH):
		txt += get_char(*im.getpixel((j,i)))
	txt += '\n'

print(txt)
	
with open(OUTPUT,'w') as f:
	f.write(txt)