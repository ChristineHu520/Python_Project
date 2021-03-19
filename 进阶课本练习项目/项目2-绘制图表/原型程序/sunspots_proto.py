# -*- coding: utf-8 -*-
"""
# @Time    : 2021/3/18 19:37
# @Author  : ChristineHu
"""
# 太阳黑子的数据
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing, PolyLine, String
from reportlab.lib import colors

data = [
	# year   month  Predicted    High    Low
	(2020, 9, 10, 11, 9),
	(2020, 10, 10.5, 12.5, 8.5),
	(2020, 11, 11.2, 14.2, 8.2),
	(2020, 12, 12, 17, 7, 75.1),
	(2021, 1, 12.7, 17.7, 7.7),
	(2021, 2, 13.5, 19.5, 7.5),
	(2021, 3, 14.8, 21.8, 7.8),
	(2021, 4, 15.9, 22.9, 8.9),
	(2021, 5, 15.7, 23.7, 7.7),
	(2021, 6, 15.5, 24.5, 6.5),
	(2021, 7, 16.5, 25.5, 7.5),
	(2021, 8, 18.3, 28.3, 8.3),
	(2021, 9, 20.3, 30.3, 10.3),
	(2021, 10, 22.5, 32.5, 12.5),
	(2021, 11, 24.7, 34.7, 14.7),
	(2021, 12, 27.1, 37.1, 17.1),
	(2022, 1, 29.6, 39.6, 19.6),
	(2022, 2, 32.1, 42.1, 22.1),
]

drawing = Drawing(200, 150)
pred = [row[2] - 40 for row in data]
high = [row[3] - 40 for row in data]
low = [row[4] - 40 for row in data]
times = [200 * (row[0] + row[1] / 12.0 - 2007) - 100 for row in data]

drawing.add(PolyLine(list(zip(times, pred)), strokeColor=colors.blue))
drawing.add(PolyLine(list(zip(times, high)), strokeColor=colors.red))
drawing.add(PolyLine(list(zip(times, low)), strokeColor=colors.green))

s = String(65, 115, 'Sunspots', fontsize=18, strokeColor=colors.pink)
drawing.add(s)
renderPDF.drawToFile(drawing, 'Sunspots.pdf', 'Sunspots')
