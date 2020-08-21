#在操作系统中定义的环境变量，全部保存在os.environ这个变量中，可以直接查看：

import os

print(os.environ)

#要获取某个环境变量的值，可以调用os.environ.get('key')
print(os.environ.get('PATH'))

print(os.environ.get('x', 'default'))