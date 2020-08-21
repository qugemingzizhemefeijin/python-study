# encoding: utf-8

'''
快速入门 Capstone
Capstone 很强大，也可以很简单， 下面一段代码就是Capstone的入门例子。
'''

from capstone import *
from capstone.arm import *

CODE = b"\xf1\x02\x03\x0e\x00\x00\xa0\xe3\x02\x30\xc1\xe7\x00\x00\x53\xe3"

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
for i in md.disasm(CODE, 0x1000):
	print('%x:\t%s\t%s' % (i.address, i.mnemonic, i.op_str))

'''
1000:	mcreq	p2, #0, r0, c3, c1, #7
1004:	mov		r0, #0
1008:	strb	r3, [r1, r2]
100c:	cmp	r3, #0
'''