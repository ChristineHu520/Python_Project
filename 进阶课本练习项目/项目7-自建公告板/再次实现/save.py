#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
# @Time    : 2021/3/31 9:33
# @Author  : ChristineHu
"""
print('Content-type: text/html\n')
import cgitb;cgitb.enable()
import sqlite3
conn = sqlite3.connect('messages.db')
curs = conn.cursor()
import cgi
import sys
form = cgi.FieldStorage()
sender = form.getvalue('sender')
subject = form.getvalue('subject')
text = form.getvalue('text')
reply_no = form.getvalue('reply_no')
if not(sender and subject and text):
	print('Please supply sender, subject, and text')

if reply_no is not None:
	query = ("""
		insert into messages(reply_no, sender, subject, text)
		values (%s, '%s', '%s', '%s')""", (int(reply_no), sender, subject, text))
else:
	query = ("""
	insert into messages (sender, subject, text)
	 values ('%s', '%s', '%s')""", (sender, subject, text))

curs.execute(*query)
conn.commit()

print("""
<html>
	<head>
		<title>Message Saved</title>
	</head>
	<body>
		<h1>Message Saved</h1>
		<hr/>
		<a href='main.py'>Back to the main page</a>
	</body>
</html>
""")