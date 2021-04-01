# -*- coding: utf-8 -*-
"""
# @Time    : 2021/4/1 9:07
# @Author  : ChristineHu
"""

import sys
from cmd import Cmd
from random import choice
from string import ascii_lowercase
from threading import Thread
from time import sleep
from xmlrpc.client import ServerProxy, Fault

from server import Node, UNHANDLED

HEAD_START = 0.1  # 单位秒
SECRET_LENGTH = 100


def random_string(length):
	"""
	返回一个指定长度的随机字符串
	:param length:
	:return:
	"""
	chars = []
	letters = ascii_lowercase[:26]
	while length > 0:
		length -= 1
		chars.append(choice(letters))
	return ''.join(chars)


class Client(Cmd):
	"""
	一个基于文本的界面
	"""
	prompt = '> '

	def __init__(self, url, dirname, urlfile):
		"""
		设置url，dirname和urlfile，并在一个独立的线程中启动Node服务器
		:param url:
		:param dirname:
		:param urlfile:
		"""
		Cmd.__init__(self)
		self.secret = random_string(SECRET_LENGTH)
		n = Node(url, dirname, self.secret)
		t = Thread(target=n._start)
		t.setDaemon(1)
		t.start()
		# 让服务器先行一步
		sleep(HEAD_START)
		self.server = ServerProxy(url)
		for line in open(urlfile):
			line = line.strip()
			self.server.hello(line)

	def do_fetch(self, arg):
		"""
		调用服务器的方法fetch
		:param arg:
		:return:
		"""
		try:
			self.server.fetch(arg, self.secret)
		except Fault as f:
			if f.faultCode != UNHANDLED:
				raise
			print("Couldn't fine the file", arg)

	def do_exit(self, arg):
		"退出程序"
		print()
		sys.exit()


def main():
	urlfile, directory, url = sys.argv[1:]
	client = Client(url, directory, urlfile)
	client.cmdloop()


if __name__ == '__main__':
	main()
