"""
Pipe只能在两个进程之间进行通信的场景。但是它没说一定要早子进程之间进行通信。只要管道通常，可以在子进程之间也可以在主进程与子进程之间进行通信。
"""

from multiprocessing import Process, Pipe
import os, time, random

def productor(pipe):
    pipe.send('我来自生产者productor')
    
def consumer(pipe):
    reply = pipe.recv()
    print('消费者获取信息：', reply)
    pipe.send('我来自消费者 consumer')
    
if __name__ == '__main__':
    # con1, con2可以理解为一个通道的两个出入口
    (con1, con2) = Pipe()
    # 创建子进程send
    sender = Process(target = productor, args = (con1, ))
    sender.start()
    # 创建子进程 reciver
    reciver = Process(target = consumer, args = (con2, ))
    reciver.start()
    
    sender.join()
    reciver.join()
    
    print('主进程获取信息：', con1.recv())
