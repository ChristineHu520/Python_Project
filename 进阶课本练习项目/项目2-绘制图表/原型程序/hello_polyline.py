# -*- coding: utf-8 -*-
"""
# @Time    : 2021/3/18 16:02
# @Author  : ChristineHu
"""

from reportlab.graphics.shapes import Drawing, PolyLine
from reportlab.graphics import renderPDF
from reportlab.lib import colors

data = [
	(2016, 0o3, 30.9, 29.9),
	(2016, 0o4, 30.5, 28.5)
]

pred = [row[2] for row in data]
times = [str(row[0])+'.'+str(int(row[1]/2)) for row in data]
print(times)
drawing = Drawing(100, 100)
drawing.add(PolyLine(list(zip(times, pred)), strokeColor=colors.blue))
renderPDF.drawToFile(drawing, 'hello_polyline.pdf', 'A simple PDF file')