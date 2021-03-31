# -*- coding: utf-8 -*-
"""
# @Time    : 2021/3/31 16:19
# @Author  : ChristineHu
"""

from  xmlrpc.client import ServerProxy
from os.path import join, isfile
from xmlrpc.server import SimpleXMLRPCServer
from urllib.parse import urlparse
import sys

MAX_HISTORY_LENGTH = 6

OK = 1
FAIL = 2
EMPTY = ''

def get_port(url):
	'从URL中提取端口'
	name =urlparse(url)[1]
	parts = name.split(':')
	return int(parts[-1])

class Node:
	"""
	P2P网络中的节点
	"""
	def __init__(self, url, dirname, secret):
		self.url = url
		self.dirname = dirname
		self.secret = secret
		self.known = set()

	def query(self, query, history=[]):
		"""
		查询文件（可能向已知节点寻求帮助），并以字符串的方式返回它
		:param query:
		:param history:
		:return:
		"""
		code, data = self._handle(query)
		if code == OK:
			return code, data
		else:
			history = history + [self.url]
			if len(history) >= MAX_HISTORY_LENGTH:
				return FAIL, EMPTY
			return self._broadcast(query, history)

	def hello(self, other):
		"""
		用于向其他节点介绍自己
		:param other:
		:return:
		"""
		self.known.add(other)
		return OK

	def fetch(self, query, secret):
		"""
		用于让节点查找并下载文件
		:param query:
		:param secret:
		:return:
		"""
		if secret != self.secret:
			return FAIL
		code, data = self.query(query)
		if code == OK:
			f = open(join(self.dirname, query),' w')
			f.write(data)
			f.close()
			return OK
		else:
			return FAIL

	def _start(self):
		"""
		供内部来启动XML_RPC服务器
		:return:
		"""
		s = SimpleXMLRPCServer(("",get_port(self.url)), logRequests=False)
		s.register_instance(self)
		s.serve_forever()

	def _handle(self, query):
		"""
		供内部用来查询的
		:param query:
		:return:
		"""
		dir = self.dirname
		name = join(dir, query)
		if not isfile(name):
			return FAIL, EMPTY
		return OK, open(name).read()

	def _broadcast(self, query, history):
		"""
		供内部用俩向所有已知节点广播查询
		:param query:
		:param history:
		:return:
		"""
		for other in self.known.copy():
			if other in history:
				continue
			try:
				s = ServerProxy(other)
				code, data = s.query(query, history)
				if code == OK:
					return code, data
			except:
				self.known.remove(other)
			return FAIL, EMPTY

def main():
		url, directory, secret = sys.argv[1:]
		n = Node(url, directory, secret)
		n._start()


if __name__ == '__main__':
    main()