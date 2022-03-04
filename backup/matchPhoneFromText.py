# !/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import os
import traceback
import ConfigParser
import logging
import logging.handlers

cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_path + '/lib')

import mysql.connector

#reload(sys)
#sys.setdefaultencoding('utf8')

mobile_regex = re.compile('1[0-9- ]{10,}')
wx_regex = re.compile('[a-zA-Z]{1}[-_a-zA-Z0-9]{5,}')

wx_feature = unicode('vV❤信微薇星⭐威','utf-8')
xw_startwith = [ 'vx' , 'V' ]

def hasWeixinCharacter(line):
	for s in line:
		for v in wx_feature:
			if s == v:
				return True
	return False

def weixinStartWithLength(s):
	s = s.lower()
	if s.startswith('vx'):
		return 2
	if s.startswith('v') or s.startswith('x'):
		return 1
	return 0

signature = '''
定个小目标，一直走下去   只要努力，不成功也值了   Vx：Li1483959159
'''

mobiles = set()
wxs = set()

#匹配手机
results = mobile_regex.findall(signature,re.S)
#print("%s " %(results))
for result in results:
	result=result.replace("-","")
	result=result.replace(" ","")
	if len(result) == 11:
		mobiles.add(result)

#匹配微信
lines = signature.split('\n')
for line in lines:
	#判断是否有微信特征的字符
	if hasWeixinCharacter(unicode(line,'utf-8')) :
		results = wx_regex.findall(line , re.S)
		for result in results:
			s = weixinStartWithLength(result)
			if s > 0:
				result = result[s:]
			wxs.add(result)

#打印手机
print "===============打印手机========="
for mobile in mobiles:
	print mobile

#打印微信
print "===============打印微信========="
for wx in wxs:
	print wx