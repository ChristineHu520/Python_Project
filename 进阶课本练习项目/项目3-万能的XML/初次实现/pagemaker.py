# -*- coding: utf-8 -*-
"""
# @Time    : 2021/3/23 15:44
# @Author  : ChristineHu
"""
from xml.sax import parse
from xml.sax.handler import ContentHandler


class PageMaker(ContentHandler):
	passthrough = False

	def startElement(self, name, attrs):
		if name == 'page':
			self.passthrough = True
			self.out = open(attrs['name'] + '.html', 'w')
			self.out.write('<html><head>\n')
			self.out.write('<title>{}</title>\n'.format(attrs['title']))
			self.out.write('</head><body>\n')
		elif self.passthrough:
			self.out.write('<' + name)
			for key, value in attrs.items():
				self.out.write(' {}="{}"'.format(key, value))
			self.out.write('>')

	def endElement(self, name):
		if name == 'page':
			self.passthrough = False
			self.out.write('\n</body></html>\n')
			self.out.close()
		elif self.passthrough:
			self.out.write('</{}>'.format(name))

	def characters(self, content):
		if self.passthrough:
			self.out.write(content)


if __name__ == '__main__':
	parse('website.xml', PageMaker())
