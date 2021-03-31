#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
# @Time    : 2021/3/31 8:50
# @Author  : ChristineHu
"""
print('Content-type: text/html\n')

import cgitb;

cgitb.enable()
import sqlite3

conn = sqlite3.connect('messages.db')
curs = conn.cursor()

print("""
<html>
	<head>
		<title>The FooBar Bulletin Board</title>
	</head>
	<body>
		<h1>The FooBar Bulletin Board</h1>
""")

curs.execute('select * from messages')
names = [d[0] for d in curs.description]
rows = [dict(zip(names, row)) for row in curs.fetchall()]

toplevel = []
children = {}

for row in rows:
	parent_id = row['reply_no']
	if parent_id is None:
		toplevel.append(row)
	else:
		children.setdefault(parent_id, []).append(row)


def formats(row):
	print('<p><a href="view.py?id={id}i">{subject}</a></p>'.format(row))
	try:
		kids = children[row['id']]
	except KeyError:
		pass
	else:
		print('<blockquote>')
		for kid in kids:
			formats(kid)
		print('</blockquote>')
	print('<p>')
	for row in toplevel:
		formats(row)
	print("""
		</p>
		<hr/>
		<p><a href="edit.py">Post message</a></p>>
	</body>
	</html>
	""")
