# encoding: utf-8

'''
此代码为unicorn 的Hello World示例，主要是做了一个减法操作寄存器
'''

from unicorn import *
from unicorn.arm_const import *

# mov r0, #0x37; 
# sub r1, r2, r3
ARM_CODE = b"\x37\x00\xa0\xe3\x03\x10\x42\xe0"


# mov r0, #0x37;
# sub r1, r2, r3
# Test ARM
 
# callback for tracing instructions
def hook_code(uc, address, size, user_data):
	print(">>> Tracing instruction at 0x%x, instruction size = 0x%x" % (address, size))
 
 
def test_arm():
	print("Emulate ARM code")
	try:
		# 创建一个UC对象并设置异常处理
		# Initialize emulator in ARM mode
		# Uc 是unicorn的主类，Uc对象则代表了一个独立的虚拟机实例，它有独立的寄存器和内存等资源，不同Uc对象之间的数据是独立的。
		# Uc的构造函数有两个参数 arch 和 mode，用来指定模拟执行的指令集和对应的位数或模式。
		# arch常量参数一般以 UC_ARCH_ 开头，MODE常量以UC_MODE_ 开头。

		# 同一种指令集可以有多种模式，比如x86可以同时运行32位和16位的汇编，arm也有arm模式和Thumb模式，它们是向下兼容的，并可以通过特殊指令来切换CPU运行模式。
		# 调用构造函数时的模式（mode）以第一条执行指令的模式为准。
		mu = Uc(UC_ARCH_ARM, UC_MODE_THUMB) #创建UC对象

		# map 2MB memory for this emulation 创建2MB的内存空间
		ADDRESS = 0x10000
		# mem_map函数特别娇气，要求 address 和 size 参数都与0x1000对齐,否则会报UC_ERR_ARG异常
		mu.mem_map(ADDRESS, 2 * 0x10000)
		# 我们要执行代码，就需要将欲执行代码的字节数据写入到虚拟机内存中。
		# mem_write的第二个参数也很娇气，只支持python的byte数组，不能是String或者bytearray。
		mu.mem_write(ADDRESS, ARM_CODE) #将前面定义的ARM_CODE传入内存空间内，只支持byte

		# 给寄存器赋值
		# 未开机前寄存器赋值
		mu.reg_write(UC_ARM_REG_R0, 0x1234)
		mu.reg_write(UC_ARM_REG_R2, 0x6789)
		mu.reg_write(UC_ARM_REG_R3, 0x3333)
		
		#添加指令集Hook
		mu.hook_add(UC_HOOK_CODE, hook_code, begin=ADDRESS, end=ADDRESS)

		# emulate machine code in infinite time，开机
		# 可以通过timeout参数设置最长执行时长，防止线程死在虚拟机里面。
		# emu_start 执行完成后，可以通过读取内存或寄存器的方式来获取执行结果。
		mu.emu_start(ADDRESS, ADDRESS + len(ARM_CODE))
		print("已开机")
		#获取计算器结果
		r0 = mu.reg_read(UC_ARM_REG_R0)
		r1 = mu.reg_read(UC_ARM_REG_R1)
		print(">>> R0 = 0x%x" % r0)
		print(">>> R1 = 0x%x" % r1)
	except UcError as e:
		print("ERROR: %s" % e)

test_arm()
