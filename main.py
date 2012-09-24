#!/bin/env python
import socket
import os
from proxy import Proxy
from control import *

loghandle = open('log','w')
def log(message):
	#print message
	loghandle.write(message + "\n")
	loghandle.flush()	

if __name__ == '__main__':
	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	server.bind((socket.gethostbyname(socket.gethostname()),80))
	server.listen(5)
	server.setblocking(0)

	p = Proxy()
	c = Control()

	while True:
		try:
			client,(ip,port) = server.accept()
			log('connected from [%s:%d]'%(ip,port))
			
			#get proxy config 
			config = c.getConfig(ip)
			if config == None:
				log('config file not found for this ip[%s]'%(ip))
				client.close()
				raise Exception()
			
			remote_ip = config.remote_ip
			remote_port = config.remote_port
			log('[%s:%d] xforward [%s:%d]'%(ip,port,remote_ip,remote_port))
			sock = socket.create_connection((remote_ip,remote_port))
			log('create connection to [%s:%d] success'%(remote_ip,remote_port))
			p.addPair(client,sock)
		except Exception as e:
			if e.__str__() != '[Errno 11] Resource temporarily unavailable':
				print e
			pass

		p.loop()
