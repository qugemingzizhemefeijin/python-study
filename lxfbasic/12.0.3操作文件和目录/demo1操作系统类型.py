"""
如果要在Python程序中执行这些目录和文件的操作怎么办？其实操作系统提供的命令只是简单地调用了操作系统提供的接口函数，Python内置的os模块也可以直接调用操作系统提供的接口函数。

打开Python交互式命令行，我们来看看如何使用os模块的基本功能：
"""

import os

#如果是posix，说明系统是Linux、Unix或Mac OS X，如果是nt，就是Windows系统。
print(os.name)

#获取详细的系统信息，可以调用uname()函数：
#注意uname()函数在Windows上不提供，也就是说，os模块的某些函数是跟操作系统相关的。
#print(os.uname)