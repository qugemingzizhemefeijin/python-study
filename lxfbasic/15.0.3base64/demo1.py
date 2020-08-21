"""
Python内置的base64可以直接进行base64的编解码：
"""

import base64

print(base64.b64encode(b'binary\x00string'))
print(base64.b64decode(b'YmluYXJ5AHN0cmluZw=='))

#由于标准的Base64编码后可能出现字符+和/，在URL中就不能直接作为参数，所以又有一种"url safe"的base64编码，其实就是把字符+和/分别变成-和_

print(base64.b64encode(b'i\xb7\x1d\xfb\xef\xff'))
print(base64.urlsafe_b64encode(b'i\xb7\x1d\xfb\xef\xff'))
print(base64.urlsafe_b64decode('abcd--__'))

#练习
#请写一个能处理去掉=的base64解码函数：

"""
def safe_base64_decode(s):
	# 题目中的 b'YWJjZA==' 是一个bytes类型，于是直接用utf-8转换为string以便后面添加等号
	if type(s) == bytes:
		s = str(s, encoding='utf-8')
	if len(s) % 4 == 0:
		return base64.b64decode(s)
	else:
		return base64.b64decode(s + '=' * (4-len(s) % 4))
"""

def safe_base64_decode(s):
	if isinstance(s, str):
		s = s.encode('ascii')
	s += b'='*(4-len(s)%4)
	return base64.b64decode(s)

# 测试:
assert b'abcd' == safe_base64_decode(b'YWJjZA=='), safe_base64_decode('YWJjZA==')
assert b'abcd' == safe_base64_decode(b'YWJjZA'), safe_base64_decode('YWJjZA')
print('ok')

