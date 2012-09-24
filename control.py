#!/bin/env python
import os
import time

CONFIG_DIR='data/'

class Config(object):
	def __init__(self,source_ip,remote_ip,remote_port,time_length = 0):
		self.source_ip = source_ip
		self.remote_ip = remote_ip
		self.remote_port = int(remote_port)
		self.time_length = int(time_length)
		self.create_time = int(time.time())

	def checkAvailable(self):
		if self.time_length == 0:
			return True
		time_now = int(time.time())
		time_used = time_now - self.create_time
		if time_used > self.time_length:
			return False
		return True

class Control(object):
	def __init__(self):
		self.configs = {}

	def getConfig(self,source_ip):
		#check whether config is updated
		new_config = self.__getNewConfigFromFile(source_ip)
		if new_config != None:
			"""if new config available
				1.add/update configs
				2.mv file
			"""
			if True == new_config.checkAvailable():
				self.addConfig(new_config)
				self.__renameConfigFile(source_ip)
				return new_config
			else:
				self.__unlinkConfigFile(source_ip)
				#check old config
				if self.configs.has_key(source_ip):
					del self.configs[source_ip]
				return None
		else:
			if self.configs.has_key(source_ip):
				config = self.configs[source_ip]
				if True == config.checkAvailable():
					return config
				else:
					del self.configs[source_ip]
					self.__unlinkConfigFile(source_ip,False)
					return None
			else:
				return None


	def addConfig(self,config):
		self.configs[config.source_ip] = config

	"""	@desc:get config from file
		@param	source_ip	string
		@return	Config
	"""
	def __getNewConfigFromFile(self,source_ip):
		filepath = CONFIG_DIR + "@" + source_ip
		if not os.path.exists(filepath):
			return None
		try:
			content = open(filepath,'r').read()
			remote_ip,remote_port,time_length = content.strip().split("\t")
			config = Config(source_ip,remote_ip,remote_port,time_length)
			return config
		except:
			return None

	def __renameConfigFile(self,source_ip):
		filepath = CONFIG_DIR + "@" + source_ip
		new_filepath = CONFIG_DIR + source_ip
		os.rename(filepath,new_filepath)

	def __unlinkConfigFile(self,source_ip,new = True):
		if True == new:
			filepath = CONFIG_DIR + "@" + source_ip
		else:
			filepath = CONFIG_DIR + source_ip
