#!/bin/env python
import socket
import select

class Proxy(object):
    def __init__(self):
        self.pools = []
        self.sk_map = {}

    def addPair(self,fd1,fd2):
        self.pools.append(fd1)
        self.pools.append(fd2)
        self.sk_map[fd1] = fd2
        self.sk_map[fd2] = fd1

    def loop(self):
		rfds,_,_ = select.select(self.pools,[],[],0)
		if len(rfds) != 0:
			for fd in rfds:
				try:
					buf = fd.recv(1024)
				except:
					buf = False
				send_fd = self.sk_map[fd]
				if not buf:
					fd.close()
					send_fd.close()
					self.pools.remove(fd)
					self.pools.remove(send_fd)
					del self.sk_map[fd]
					del self.sk_map[send_fd]
				else:
					try:
						send_fd.send(buf)
					except:
						fd.close()
						send_fd.close()
						self.pools.remove(fd)
						self.pools.remove(send_fd)
						del self.sk_map[fd]
						del self.sk_map[send_fd]
						

