# -*- coding: utf-8 -*-
"""
# @Time    : 2021/3/23 9:29
# @Author  : ChristineHu
"""
from xml.sax.handler import ContentHandler
from xml.sax import parse


class TestHandler(ContentHandler):
	def startElement(self, name, attrs):
		print(name, attrs.keys())


parse('website.xml', TestHandler())
