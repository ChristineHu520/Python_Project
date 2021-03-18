# -*- coding: utf-8 -*-
"""
# @Time    : 2021/3/18 9:18
# @Author  : ChristineHu
"""
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics import renderPDF

d = Drawing(100, 100)
s = String(50, 50, 'Hello, World!', textAnchor='middle')
d.add(s)
renderPDF.drawToFile(d, 'hello_reportlab.pdf', 'A simple PDF file')