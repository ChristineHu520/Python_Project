#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
# @Time    : 2021/3/31 8:56
# @Author  : ChristineHu
"""
print('Content-type: tex/html\n')

import cgitb;cgitb.enable()
import sqlite3
conn = sqlite3.connect('messages.db')
curs = conn.cursor()

import cgi
import sys
form = cgi.FieldStorage()
id = form.getvalue('id')

print("""
<html>
	<head>
		<title>View Message</title>
	</head>
	<body>
		<h1>View Message</h1>
""")

try:
	id = int(id)
except:
	print('Invalid message ID')
	sys.exit()
curs.execute('select * from messages where id = %s', (format(id),))
names = [d[0] for d in curs.description]
rows = [dict(zip(names, row)) for row in curs.fetchall()]

if not rows:
	print('Unknown message ID')
	sys.exit()

row = rows[0]
print("""
		<p><b>Subject:</b>{subject}<br/>
		<b>Sender:</b>{sender}<br/>
		<pre>{text}</pre>
		</p>
		<hr/>
		<a href='main.py'>Back to the main page</a>
		| <a href="edit.py?reply_no={id}">Reply</a>
	</body>
</html>
""".format(row))