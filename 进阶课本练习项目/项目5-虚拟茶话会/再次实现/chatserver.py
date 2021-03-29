# -*- coding: utf-8 -*-
"""
# @Time    : 2021/3/29 8:43
# @Author  : ChristineHu
"""
import asyncore
import socket
from asynchat import async_chat
from asyncore import dispatcher

PORT = 5005
NAME = 'TestChat'


class EndSession(Exception): pass


class CommandHandle:
	"""
	类似于标准库中的cmd.Cmd的简单命令处理程序
	"""

	def unknow(self, session, cmd):
		"""
		响应未知命令
		:param session:
		:param cmd:
		:return:
		"""
		session.push('Unknow command: {}s\r\n'.format(cmd))

	def handle(self, session, line):
		"""
		处理从指定会话收到的行
		:param session:
		:param line:
		:return:
		"""
		if not line.strip():
			return
		# 提取命令
		parts = line.split(' ', 1)
		cmd = parts[0]
		try:
			line = parts[1].strip()
		except IndexError:
			line = ''
		# 尝试查找处理程序
		meth = getattr(self, 'do_' + cmd, None)
		try:
			# 假定命令是可调用的
			meth(session, line)
		except TypeError:
			# 如果是不可调用的，就响应未知命令
			self.unknow(session, cmd)


class Room(CommandHandle):
	"""
	可能包含一个或多个用户（会话）的通用环境，它负责基本的命令处理程序和广播
	"""

	def __init__(self, server):
		self.server = server
		self.sessions = []

	def add(self, session):
		"""有会话（用户）进入聊天室"""
		self.sessions.append(session)

	def remove(self, session):
		"""有会话（用户）离开聊天室"""
		self.sessions.remove(session)

	def broadcast(self, line):
		""""将一行内容发送给聊天室内的所有会话"""
		for session in self.sessions:
			session.push(line)

	def do_logout(self, session, line):
		"""响应命令logout"""
		raise EndSession


class LoginRoom(Room):
	"""
	为刚连接的用户准备的聊天室
	"""

	def add(self, session):
		Room.add(self, session)
		# 用户进入聊天室的时候发出问候
		self.broadcast('Welcome to {}\r\n'.format(self.server.name))

	def unknow(self, session, cmd):
		# 除了login和logout之外的命令都会导致系统显示提示消息
		session.push('Please log in\nuse "login <nick>"\r\n')

	def do_login(self, session, line):
		name = line.strip()
		# 确保用户输入了用户名
		if not name:
			session.push('Please enter a name\r\n')
		# 确保用户名未被占用
		elif name in self.server.users:
			session.push('The name "{}" is taken.\r\n'.format(name))
			session.push('Please try again.\r\n')
		else:
			# 用户名没问题，因此将其存储到会话中并将用户移到主聊天室
			session.name = name
			session.enter(self.server.main_room)


class ChatRoom(Room):
	"""
	为多个用户准备的聊天室
	"""

	def add(self, session):
		# 告诉所有用户有新用户进入聊天室
		self.broadcast(session.name + 'has entered the room.\r\n')
		self.server.users[session.name] = session
		super().add(session)

	def remove(self, session):
		Room.remove(self, session)
		# 告诉所有人有用户离开
		self.broadcast(session.name + 'has left the room.\r\n')

	def do_say(self, session, line):
		self.broadcast(session.name + ': ' + line + '\r\n')

	def do_look(self, session, line):
		# 处理命令look，这个命令用于查看聊天室里都有谁
		session.push(other.name + '\r\n')

	def do_who(self, session, line):
		# 这个命令用于查看谁已经登录
		session.push('The following are logged in :\r\n')
		for name in self.server.users:
			session.push(name + '\r\n')


class LogoutRoom(Room):
	"""
	为单个用户准备的聊天室，仅用于将用户名从服务器删除
	"""

	def add(self, session):
		# 将进入LogoutRoom的用户删除
		try:
			del self.server.users[session.name]
		except KeyError:
			pass


class ChatSession(asynchat.async_chat):
	"""
	单个会话，负责与单个用户通信
	"""

	def __init__(self, server, sock):
		super().__init__(sock)
		self.server = server
		self.set_terminator('\r\n')
		self.data = []
		self.name = None
		# 所有会话最初在LoginRoom
		self.enter(LoginRoom(server))

	def enter(self, room):
		# 自己从当前聊天室离开，并进入下一个聊天室
		try:
			cur = self.room
		except AttributeError:
			pass
		else:
			cur.remove(self)
		self.room = room
		room.add(self)

	def collect_incoming_data(self, data):
		self.data.append(data)

	def found_terminator(self):
		line = ''.join(self.data)
		self.data = []
		try:
			self.room.handle(self, line)
		except EndSession:
			self.handle_close()

	def handle_close(self):
		async_chat.handle_close(self)
		self.enter(LogoutRoom(self.server))


class ChatServer(dispatcher):
	"""只有一个聊天室的聊天服务器"""

	def __init__(self, port, name):
		super().__init__()
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(('', port))
		self.listen(5)
		self.name = name
		self.users = {}
		self.main_room = ChatRoom(self)

	def handle_accept(self):
		conn, addr = self.accept()
		ChatSession(self, conn)


if __name__ == '__main__':
	s = ChatServer(PORT, NAME)
	try:
		asyncore.loop()
	except KeyboardInterrupt: print()
