"""
用Python来编写脚本简化日常的运维工作是Python的一个重要用途。在Linux下，有许多系统命令可以让我们时刻监控系统运行的状态，如ps，top，free等等。要获取这些系统信息，Python可以通过subprocess模块调用并获取结果。
但这样做显得很麻烦，尤其是要写很多解析代码。

在Python中获取系统信息的另一个好办法是使用psutil这个第三方模块。顾名思义，psutil = process and system utilities，它不仅可以通过一两行代码实现系统监控，还可以跨平台使用，
支持Linux／UNIX／OSX／Windows等，是系统管理员和运维小伙伴不可或缺的必备模块。

pip install psutil
"""

import psutil

###获取CPU信息

print(psutil.cpu_count())	#cpu逻辑数量
print(psutil.cpu_count(logical=False))	#CPU物理核心

###统计CPU的用户／系统／空闲时间：
print(psutil.cpu_times())

###再实现类似top命令的CPU使用率，每秒刷新一次，累计10次：

#for x in range(10):
#	psutil.cpu_percent(interval=1, percpu=True)

###获取内存信息

#使用psutil获取物理内存和交换内存信息，分别使用：
print(psutil.virtual_memory())

#返回的是字节为单位的整数，可以看到，总内存大小是8589934592 = 8 GB，已用7201386496 = 6.7 GB，使用了66.6%。
#而交换区大小是1073741824 = 1 GB。

###获取磁盘信息

#可以通过psutil获取磁盘分区、磁盘使用率和磁盘IO信息：
print(psutil.disk_partitions())	# 磁盘分区信息
print(psutil.disk_usage('C:/'))	# 磁盘使用情况
print(psutil.disk_io_counters())	# 磁盘IO

###获取网络信息
print(psutil.net_io_counters())	# 获取网络读写字节／包的个数
print(psutil.net_if_addrs())	# 获取网络接口信息
print(psutil.net_if_stats())	# 获取网络接口状态

#要获取当前网络连接信息，使用net_connections()：
print(psutil.net_connections())

#你可能会得到一个AccessDenied错误，原因是psutil获取信息也是要走系统接口，而获取网络连接信息需要root权限，这种情况下，可以退出Python交互环境，用sudo重新启动：

###获取进程信息
print(psutil.pids())	# 获取所有进程ID

## 获取指定进程ID=3776，其实就是当前Python交互环境
p = psutil.Process(8880)
print(p.name())	#进程名称
print(p.exe())	#进程路径
print(p.cwd())	#进程工作目录
print(p.cmdline())	#进程启动的命令行
print(p.ppid())	#父进程ID
print(p.parent())	#父进程
print(p.children())	#子进程列表
print(p.status())	#进程状态
print(p.username())	#进程用户名
print(p.create_time())	#进程创建时间
#print(p.terminal())	#Linux 才能调用 进程终端
print(p.cpu_times())	#进程使用的CPU时间
print(p.memory_info())	#进程使用的内存
print(p.open_files())	#进程打开的文件
print(p.connections())	#进程相关网络连接
print(p.num_threads())	#进程的线程数量
print(p.threads())	#所有线程信息
print(p.environ())	#进程环境变量
#p.terminate()	#结束进程

#psutil还提供了一个test()函数，可以模拟出ps命令的效果：

psutil.test()