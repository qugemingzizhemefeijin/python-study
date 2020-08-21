# -*- coding: utf-8 -*-

import config_default

class Dict(dict):
	'''
	配置信息维护类
	'''
	def __init__(self, names=(), values=(), **kw):
		super().__init__(**kw)
		for k, v in zip(names, values):
			self[k] = v

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

	def __setattr__(self, key, value):
		self[key] = value

def merge(defaults, override):
	'''
	将两个字典合并，第二个字典覆盖第一个字典的数据
	'''
	r = {}
	for k, v in defaults.items():
		if k in override:
			if isinstance(v, dict):
				r[k] = merge(v, override[k])
			else:
				r[k] = override[k]
		else:
			r[k] = v
	return r

def toDict(d):
	'''
	此方法是将传入的参数中包含dict的数据全部转化成Dict对象
	'''
	D = Dict()
	for k, v in d.items():
		D[k] = toDict(v) if isinstance(v, dict) else v
	return D

# 默认使用default配置
configs = config_default.configs

try:
	import config_override
	# 如果有config_override.py则合并两个文件的数据
	configs = merge(configs, config_override.configs)
except ImportError:
	pass

# 将数据拍平
configs = toDict(configs)
