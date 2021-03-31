#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
# @Time    : 2021/3/31 9:16
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
reply_no = form.getvalue('reply_no')

print("""
<html>
	<head>
		<title>Compose Message</title>
	</head>
	<body>
		<h1>Compose Message</h1>
		<form action='save.py' method='POST'>
""")
subject = ''
if reply_no is not None:
	print('<input type="hidden" name="reply_no" value="{}"/>'.format(reply_no))
	curs.execute('select subject from messages where id = %s', (format(reply_no),))
	subject = curs.fetchone()[0]
	if not subject.startwith('Re: '):
		subject = 'Re: ' + subject
print("""
	<b>Subject:</b><br/>
	<input type='text' size='40' name='subject' value='{}' /><br/>
	<b>Sender:</b><br/>
	<input type='text' size='40' name='sender' /><br/>
	<b>Message:</b><br/>
	<textarea type='text' cols='40' rows='20'</textarea><br/>
	<input type='submit' value='Save' /><br/>
	</form>
	<hr/>
	<a href='main.py'>Back to the main page</a>
</body>
</html>
""".format(subject))