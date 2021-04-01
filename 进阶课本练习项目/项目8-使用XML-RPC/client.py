# -*- coding: utf-8 -*-
"""
# @Time    : 2021/4/1 11:22
# @Author  : ChristineHu
"""
from xmlrpc.client import *
mpeer = ServerProxy('http://localhost:4243')
code, data = mpeer.query('test.txt')
print(code)