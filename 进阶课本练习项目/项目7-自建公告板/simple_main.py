# ！/usr/bin/python
# -*- coding: utf-8 -*-
"""
# @Time    : 2021/3/30 17:00
# @Author  : ChristineHu
"""

print('Content-type: text/html\n')

import cgitb;cgitb.enable()
import sqlite3
conn = sqlite3.connect('message.db')
curs = conn.cursor()

print("""
<html>
	<head>
		<title>The FooBar Bulletin Board</title>
	</head>
	<body>
		<h1>The FooBar Bulletin Board</h1>
""")

curs.execute('select * from messages;')
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

def format(row):
	print(row['subject'])
	try:
		kids = children[row['id']]
	except KeyError:
		pass
	else:
		print('<blockquote>')
		for kid in kids:
			format(kid)
		print('</blockquote>')
	print('<p>')
	for row in toplevel:
		format(row)
	print("""
		</p>
	</body>
	</html>
	""")

