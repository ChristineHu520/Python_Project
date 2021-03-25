# -*- coding: utf-8 -*-
"""
# @Time    : 2021/3/25 8:37
# @Author  : ChristineHu
"""
from nntplib import NNTP

servername = 'news.gmane.org'
group = 'com.lang.python.announce'
server = NNTP(servername)
howmany = 10
resp, count, first, last, name = server.group(group)
start = last - howmany + 1
resp, overviews = server.over((start, last))
for id, over in overviews:
	subject = over['subject']
	resp, info = server.body(id)
	print(subject)
	print('_'*len(subject))
	for line in info.lines:
		print(line.decode('latin1'))
	print()
server.quit()