# -*- coding: utf-8 -*-
"""
# @Time    : 2021/3/23 16:17
# @Author  : ChristineHu
"""


class Dispatcher:
	def startElement(self, name, attrs):
		self.dispatch('start', name, attrs)

	def endElement(self, name, attrs):
		self.dispatch('end', name, attrs)

	def dispatch(self, prefix, name, attrs=None):
		mname = prefix + name.capitalize()
		dname = 'default' + prefix.capitalize()
		method = getattr(self, mname, None)
		if callable(method):
			args = ()
		else:
			method = getattr(self, dname, None)
			args = name
		if prefix == 'start':
			args += attrs
		if callable(method):
			method(*args)