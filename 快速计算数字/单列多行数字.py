#! /usr/bin/python

import uuid
import os

sum = 0.0
f = open("JoinStr.txt",encoding='utf-8',errors='ignore');
LINES = f.readlines();
f.close();

for line in LINES:
	sum += float(line.replace("\n",""))

print(sum)