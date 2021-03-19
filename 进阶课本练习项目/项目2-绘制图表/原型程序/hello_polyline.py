# -*- coding: utf-8 -*-
"""
# @Time    : 2021/3/18 16:02
# @Author  : ChristineHu
"""

from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing, PolyLine

data = [
	(2016, 3, 30.9, 29.9),
	(2016, 4, 30.5, 28.5)
]
point = [(1, 2), (3, 4)]
pred = [row[1] for row in data]
times = [row[0] + row[1] / 2 for row in data]
drawing = Drawing(500, 500)
print(list(zip(times, pred)))
drawing.add(PolyLine(point))
renderPDF.drawToFile(drawing, r'hello_polyline.pdf', 'A simple PDF file')
