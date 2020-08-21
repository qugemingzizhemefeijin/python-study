"""
提取出带名字的Email地址：

<Tom Paris> tom@voyager.org => Tom Paris
bob@example.com => bob
"""

import re

def name_of_email(addr):
	regex = r'^<([^>]+)>[^@]+@[0-9a-zA-Z]+.[a-z]{3}$'
	regex2 = r'^([^@]+)@[0-9a-zA-Z]+.[a-z]{3}$'

	m = re.match(regex, addr)
	if m:
		return m.group(1)
	else:
		m = re.match(regex2, addr)
		if m:
			m.group(1)
			return m.group(1)
		else:
			return None

# 测试:
assert name_of_email('<Tom Paris> tom@voyager.org') == 'Tom Paris'
assert name_of_email('tom@voyager.org') == 'tom'
print('ok')