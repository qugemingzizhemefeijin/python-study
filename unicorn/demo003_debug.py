# encoding: utf-8

'''
前一篇文章中，我们学习了如何使用Unicorn 来模拟执行一段二进制代码。然而目前Unicorn 对于我们来说，几乎就等同于黑盒子。
我们只知输入输出，对于代码中间执行过程的失败与否全然不知，如果出现BUG将难以调试。
为了解决这种难以调试的状况，我决定写一个Unicorn 调试器，用来调试Unicorn 模拟执行的二进制代码。

硬件断点
读/写 寄存器信息
反汇编
dump 内存
单步调试（步入/步过）
快速接入各种不同的Unicorn项目

如何实现
Unicorn 提供了强大的指令级Hook（UC_HOOK_CODE）， 使得每一条指令执行前，我们都有机会处理。

UC_HOOK_CODE 的callback原型定义如下
typedef void (*uc_cb_hookcode_t)(uc_engine *uc, uint64_t address, uint32_t size, void *user_data);

address: 当前执行的指令地址
size: 当前指令的长度，如果长度未知，则为0
user_data: hook_add 设置的user_data参数

调用hook_add 函数可以为指定的代码范围添加hook的callback。
python包中的hook_add函数原型如下：
def hook_add(self, htype, callback, user_data=None, begin=1, end=0, arg1=0):
    pass
UC_HOOK_CODE 的功能是每条指令执行前调用callback。

callback中，我们可以通过参数得知指令执行地址、指令执行长度、虚拟机指针。
有了虚拟机指针，我们可以很方便的访问各种寄存器、内存等资源。在UC_HOOK_CODE的callback中，也可以直接修改PC寄存器来改变流程。
'''

from unicorn import *
from unicorn import arm_const
from unicorn.arm_const import *
import sys
import hexdump

# Capstone是一款支持多种处理器和开发语言的反汇编框架。Capstone http://www.capstone-engine.org/ 我将使用Capstone 作为调试模块的反汇编器。
import capstone as cp

BPT_EXECUTE = 1
BPT_MEMREAD = 2
UDBG_MODE_ALL = 1
UDBG_MODE_FAST = 2

# Unicorn中的寄存器都是以常量来管理的，所以我们要把寄存器常量和文本映射起来
# ARM 寄存器表
REG_ARM = {arm_const.UC_ARM_REG_R0: "R0",
           arm_const.UC_ARM_REG_R1: "R1",
           arm_const.UC_ARM_REG_R2: "R2",
           arm_const.UC_ARM_REG_R3: "R3",
           arm_const.UC_ARM_REG_R4: "R4",
           arm_const.UC_ARM_REG_R5: "R5",
           arm_const.UC_ARM_REG_R6: "R6",
           arm_const.UC_ARM_REG_R7: "R7",
           arm_const.UC_ARM_REG_R8: "R8",
           arm_const.UC_ARM_REG_R9: "R9",
           arm_const.UC_ARM_REG_R10: "R10",
           arm_const.UC_ARM_REG_R11: "R11",
           arm_const.UC_ARM_REG_R12: "R12",
           arm_const.UC_ARM_REG_R13: "R13",
           arm_const.UC_ARM_REG_R14: "R14",
           arm_const.UC_ARM_REG_R15: "R15",
           arm_const.UC_ARM_REG_PC: "PC",
           arm_const.UC_ARM_REG_SP: "SP",
           arm_const.UC_ARM_REG_LR: "LR"
           }

# 平台映射的寄存器表
REG_TABLE = {UC_ARCH_ARM: REG_ARM}

def str2int(s):
    '''
    将字符串转换成数字，包含0x开头的字符串
    '''
    if s.startswith('0x') or s.startswith("0X"):
        return int(s[2:], 16)
    return int(s)

def advance_dump(data, base):
    '''
    魔改的hexdump
    '''
    PY3K = sys.version_info >= (3, 0)
    generator = hexdump.genchunks(data, 16)
    retstr = ''
    # enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。
    for addr, d in enumerate(generator):
        # 00000000:
        line = '%08X: ' % (base + addr * 16)
        # 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
        dumpstr = hexdump.dump(d)
        line += dumpstr[:8 * 3]
        if len(d) > 8:  # insert separator if needed
            line += ' ' + dumpstr[8 * 3:]
        # ................
        # 计算缩进，对于最后一行可能有所不同
        pad = 2
        if len(d) < 16:
            pad += 3 * (16 - len(d))
        if len(d) <= 8:
            pad += 1
        line += ' ' * pad
 
        for byte in d:
            # printable ASCII range 0x20 to 0x7E
            if not PY3K:
                byte = ord(byte)
            if 0x20 <= byte <= 0x7E:
                line += chr(byte)
            else:
                line += '.'
        retstr += line + '\n'
    return retstr

def _dbg_trace(mu, address, size, self):
    '''
    callback 中判断断点。
    _tmp_bpt 是临时断点， 用于支持步过。
    _is_step 步入标记，每条指令都停下来。

    这个方法会被添加到 UC_HOOK_CODE 的callback
    每次执行每个指令的时候，都会调用到此方法中

    self其实就是UnicornDebugger对象
    '''
    self._tracks.append(address) # 将指令地址存储到堆栈列表中
    # 如果不是单步并且没有设置下一个断点地址
    if not self._is_step and self._tmp_bpt == 0:
        # 如果地址不是在断点集合中，则直接返回了
        if address not in self._list_bpt:
            return
    # 当前地址不是指定的下一个断点地址，则直接返回
    if self._tmp_bpt != address and self._tmp_bpt != 0:
        return
 
    return _dbg_trace_internal(mu, address, size, self)
 
 
def _dbg_memory(mu, access, address, length, value, self):
    pc = mu.reg_read(arm_const.UC_ARM_REG_PC)
    print("memory error: pc: %x access: %x address: %x length: %x value: %x" %
          (pc, access, address, length, value))
    _dbg_trace_internal(mu, pc, 4, self)
    mu.emu_stop()
    return True
 
 
def _dbg_trace_internal(mu, address, size, self):
    self._is_step = False
    print("======================= Registers =======================")
    self.dump_reg()
    print("======================= Disassembly =====================")
    self.dump_asm(address, size * self.dis_count)
 
    while True:
        raw_command = input(">")
        if raw_command == '':
            raw_command = self._last_command
        self._last_command = raw_command
        command = []
        for c in raw_command.split(" "):
            if c != "":
                command.append(c)
        try:
            if command[0] == 'set':
                if command[1] == 'reg':  # set reg regname value
                    self.write_reg(command[2], str2int(command[3]))
                elif command[1] == 'bpt':
                    self.add_bpt(str2int(command[2]))
                else:
                    print("[Debugger Error]command error see help.")
 
            elif command[0] == 's' or command[0] == 'step': # 单步执行
                # self._tmp_bpt = address + size
                self._tmp_bpt = 0 # 清除步过标记
                self._is_step = True # 设置步入标记
                break
            elif command[0] == 'n' or command[0] == 'next': # 跳转到下一个断点
                self._tmp_bpt = address + size # 设置下一条指令地址断点
                self._is_step = False # 清除步入标记
                break
 
            elif command[0] == 'r' or command[0] == 'run': # 运行，相当于清空所有的断点信息，直接跑完程序
                self._tmp_bpt = 0
                self._is_step = False
                break
            elif command[0] == 'dump': # 导出内存信息
                if len(command) >= 3:
                    nsize = str2int(command[2])
                else:
                    nsize = 4 * 16
                self.dump_mem(str2int(command[1]), nsize)
            elif command[0] == 'list':
                if command[1] == 'bpt':
                    self.list_bpt()
            elif command[0] == 'del':
                if command[1] == 'bpt':
                    self.del_bpt(str2int(command[2]))
            elif command[0] == 'stop':
                exit(0)
            elif command[0] == 't':
                self._castone = self._capstone_thumb
                print("======================= Disassembly =====================")
                self.dump_asm(address, size * self.dis_count)
            elif command[0] == 'a':
                self._castone = self._capstone_arm
                print("======================= Disassembly =====================")
                self.dump_asm(address, size * self.dis_count)
            elif command[0] == 'f':
                print(" == recent ==")
                for i in self._tracks[-10:-1]:
                    print(self.sym_handler(i))
            else:
                print("Command Not Found!")
 
        except:
            print("[Debugger Error]command error see help.")
 
class UnicornDebugger:

    '''
    调试器的各种功能均在该类中实现， 调用该类的构造函数即可附加到一个Uc虚拟机对象上
    '''

    def __init__(self, mu, mode=UDBG_MODE_ALL):
        self._tracks = [] # 堆栈记录
        self._mu = mu
        self._arch = mu._arch
        self._mode = mu._mode
        self._list_bpt = [] # 断点记录列表
        self._tmp_bpt = 0
        self._error = ''
        self._last_command = ''
        self.dis_count = 5
        self._is_step = False
        self.sym_handler = self._default_sym_handler
        self._capstone_arm = None
        self._capstone_thumb = None

        if self._arch != UC_ARCH_ARM:
            mu.emu_stop()
            raise RuntimeError("arch:%d is not supported! " % self._arch)

        if self._arch == UC_ARCH_ARM:
            capstone_arch = cp.CS_ARCH_ARM
        elif self._arch == UC_ARCH_ARM64:
            capstone_arch = cp.CS_ARCH_ARM64
        elif self._arch == UC_ARCH_X86:
            capstone_arch = cp.CS_ARCH_X86
        else:
            mu.emu_stop()
            raise RuntimeError("arch:%d is not supported! " % self._arch)

        if self._mode == UC_MODE_THUMB:
            capstone_mode = cp.CS_MODE_THUMB
        elif self._mode == UC_MODE_ARM:
            capstone_mode = cp.CS_MODE_ARM
        elif self._mode == UC_MODE_32:
            capstone_mode = cp.CS_MODE_32
        elif self._mode == UC_MODE_64:
            capstone_mode = cp.CS_MODE_64
        else:
            mu.emu_stop()
            raise RuntimeError("mode:%d is not supported! " % self._mode)

        self._capstone_thumb = cp.Cs(cp.CS_ARCH_ARM, cp.CS_MODE_THUMB)
        self._capstone_arm = cp.Cs(cp.CS_ARCH_ARM, cp.CS_MODE_ARM)

        self._capstone = self._capstone_thumb

        if mode == UDBG_MODE_ALL:
            mu.hook_add(UC_HOOK_CODE, _dbg_trace, self)

        mu.hook_add(UC_HOOK_MEM_UNMAPPED, _dbg_memory, self)
        mu.hook_add(UC_HOOK_MEM_FETCH_PROT, _dbg_memory, self)

        self._regs = REG_TABLE[self._arch] # 根据平台切换寄存器映射表，目前只有ARM

    def dump_mem(self, addr, size):
        '''
        dump内存

        Python的hexdump模块的偏移量不支持修改，所以我魔改了hexdump的代码实现了这个功能
        '''
        data = self._mu.mem_read(addr, size)
        print(advance_dump(data, addr))

    def dump_asm(self, addr, size):
        '''
        实现反汇编
        '''
        md = self._capstone #构造函数中初始化的Capstone对象 Cs(CS_ARCH_ARM, CS_MODE_ARM)
        code = self._mu.mem_read(addr, size)
        count = 0
        for ins in md.disasm(code, addr):
            if count >= self.dis_count:
                break
            print("%s:\t%s\t%s" % (self.sym_handler(ins.address), ins.mnemonic, ins.op_str))

    def dump_reg(self):
        result_format = ''
        count = 0
        for rid in self._regs:
            rname = self._regs[rid]
            value = self._mu.reg_read(rid)
            if count < 4:
                result_format = result_format + rname + '=' + hex(value) + '  '
                count += 1
            else:
                count = 0
                result_format += '\n' + rname + '=' + hex(value) + '  '
        print(result_format)

    def write_reg(self, reg_name, value):
        '''
        修改寄存器的值
        '''
        for rid in self._regs:
            rname = self._regs[rid]
            if rname == reg_name:
                self._mu.reg_write(rid, value)
                return
        print("[Debugger Error] Reg not found:%s " % reg_name)

    def show_help(self):
        '''
        调试器要支持的调试指令如下
        '''
        help_info = """
        # commands
        # set reg <regname> <value>
        # set bpt <addr>
        # n[ext]
        # s[etp]
        # r[un]
        # dump <addr> <size>
        # list bpt
        # del bpt <addr>
        # stop
        # a/t change arm/thumb
        # f show ins flow
        """
        print(help_info)

    '''
    使用list来记录所有断点的地址，当UC_HOOK_CODE的callback被调用的时候检查address是否在断点列表中，如果当前指令的执行地址没有断点，
    则直接返回，如果存在断点，则打印寄存器信息、最近的汇编代码、等待用户指令等操作。

    单步分为两种：步入、步过。
    步入：如果遇到call、bl指令会跟随进入（跟随每一条指令）
    步过：遇到call、bl等指令不不进入（跟随每一条地址相邻的指令）
    我这个思路可能有点牵强，因为按照地址相邻，会误判跳转指令，但是为了简单起见，我只好这么做。
    '''
    def list_bpt(self):
        '''
        打印出所有的断点信息
        '''
        for idx in range(len(self._list_bpt)):
            print("[%d] %s" % (idx, self.sym_handler(self._list_bpt[idx])))

    def add_bpt(self, addr):
        '''
        添加一个断点
        '''
        self._list_bpt.append(addr)

    def del_bpt(self, addr):
        '''
        移除一个断点
        '''
        self._list_bpt.remove(addr)

    def get_tracks(self):
        '''
        打印出堆栈信息，只显示最后的100行指令
        '''
        for i in self._tracks[-100:-1]:
            # print (self.sym_handler(i))
            pass
        return self._tracks

    def _default_sym_handler(self, address):
        return hex(address)

    def set_symbol_name_handler(self, handler):
        self.sym_handler = handler

def test_arm():
    print("Emulate Thumb code")
    THUMB = b"\x37\x00\xa0\xe3\x03\x10\x42\xe0"
    # sub    sp, #0xc
    # sub    sp, #0xc
    # sub    sp, #0xc
    try:
        # Initialize emulator in ARM mrode
        mu = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
        print(dir(mu))

        # map 2MB memory for this emulation
        ADDRESS = 0x10000
        mu.mem_map(ADDRESS, 2 * 0x10000)
        mu.mem_write(ADDRESS, THUMB)

        mu.reg_write(UC_ARM_REG_SP, 0x1234)
        mu.reg_write(UC_ARM_REG_R2, 0x6789)

        print('arch=====%s' % mu._arch)

        # debugger attach
        udbg = UnicornDebugger(mu)
        # 在ADDRESS添加了一个断点，程序执行的时候会停下来，陷入调试器的处理，等待调试者的指令。
        udbg.add_bpt(ADDRESS)

        # emulate machine code in infinite time
        mu.emu_start(ADDRESS, ADDRESS + len(THUMB))
        r0 = mu.reg_read(UC_ARM_REG_SP)
        r1 = mu.reg_read(UC_ARM_REG_R1)
        print(">>> SP = 0x%x" % r0)
        print(">>> R1 = 0x%x" % r1)
    except UcError as e:
        print("ERROR: %s" % e)

test_arm()
