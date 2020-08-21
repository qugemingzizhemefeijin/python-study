# encoding: utf-8

'''
此代码使用capstone 来对操作的代码进行反汇编
'''

from capstone import *
from capstone.arm import *
 
CODE = b"\x37\x00\xa0\xe3\x03\x10\x42\xe0"
 
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
# 对CODE进行反编译，然后循环展示里面的指令
for i in md.disasm(CODE, 0x1000):
    print("%x:\t%s\t%s" % (i.address, i.mnemonic, i.op_str))

'''
结果:
1000:   mov r0, #0x37
1004:   sub r1, r2, r3
'''