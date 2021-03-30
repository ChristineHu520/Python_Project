# -*- coding: utf-8 -*-
"""
# @Time    : 2021/3/30 16:39
# @Author  : ChristineHu
"""
import sqlite3

conn = sqlite3.connect('message.db')
curs = conn.cursor()

curs.execute('''
create table messages(
id integer primary key autoincrement ,
subject text not null ,
sender text not null ,
reply_no int,
text text not null 
)''')

conn.commit()
conn.close()