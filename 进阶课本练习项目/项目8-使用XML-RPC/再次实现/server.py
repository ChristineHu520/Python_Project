# -*- coding: utf-8 -*-
"""
# @Time    : 2021/4/1 8:46
# @Author  : ChristineHu
"""
from xmlrpc.client import ServerProxy, Fault
from os.path import join, abspath, isfile
from xmlrpc.server import SimpleXMLRPCServer
from urllib.parse import urlparse
import sys

SimpleXMLRPCServer.allow_reuse_address = 1

MAX_HISTORY_LENGTH = 6

UNHANDLED = 100
ACCESS_DENIED = 200


class UnhandledQuery(Fault):
	"""
	表示未得到处理的异常
	"""

	def __init__(self, message="Couldn't handle the query"):
		super().__init__(UNHANDLED, message)


class AccessDenied(Fault):
	"""
	用户视图方位未获得授权的资源时引发的异常
	"""

	def __init__(self, message="Access denied"):
		super().__init__(ACCESS_DENIED, message)


def inside(dir, name):
	"""
	检查指定的目录是否包含指定的文件
	:param dir:
	:param name:
	:return:
	"""
	dir = abspath(dir)
	name = abspath(name)
	return name.startswith(join(dir, ''))


def get_port(url):
	"""
	从URL中提取端口号
	:param url:
	:return:
	"""
	name = urlparse(url)[1]
	parts = name.split(':')
	return int(parts[-1])


class Node:
	"""
	P2P网络的节点
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
		try:
			return self._handle(query)
		except UnhandledQuery:
			history = history + [self.url]
			if len(history) >= MAX_HISTORY_LENGTH:
				raise
			return self._broadcast(query, history)

	def hello(self, other):
		"""
		用于向其他节点介绍自己
		:param other:
		:return:
		"""
		self.known.add(other)
		return 0

	def fetch(self, query, secret):
		"""
		用于让节点查找并下载文件
		:param query:
		:param secret:
		:return:
		"""
		if secret != self.secret:
			raise ACCESS_DENIED
		result = self.query(query)
		f = open(join(self.dirname, query), 'w')
		f.write(result)
		f.close()
		return 0

	def _start(self):
		"""
		供内部来启动XML_RPC服务器
		:return:
		"""
		s = SimpleXMLRPCServer(("", get_port(self.url)), logRequests=False, allow_none=True)
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
			raise UnhandledQuery
		if not inside(dir, name):
			raise ACCESS_DENIED
		return open(name).read()

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
				return s.query(query, other)
			except Fault as f:
				if f.faultCode == UNHANDLED:
					pass
				else:
					self.known.remove(other)
			except:
				self.known.remove(other)
		raise UnhandledQuery


def main():
	url, directory, secret = sys.argv[1:]
	n = Node(url, directory, secret)
	n._start()


if __name__ == '__main__':
    main()