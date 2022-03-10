# 长连接

import websocket
import threading
import time

"""
on_message 函数会在收到服务器返回信息的时候被调用；
on_error 函数会在连接过程出现错误时候调用，返回错误信息；
on_close 函数则是连接中断调用；
on_open 是连接服务器成功时调用的方法；
on_data 当从服务器接收到消息时被调用，有四个参数，分别是：该类本身，接收到的字符串（utf-8），数据类型，连续标志；
ws.run_forever() 让连接保持不中断；
ws.close() 在收到服务器返回信息后中断连接。
on_cont_message：这个对象在接收到连续帧数据时被调用，有三个参数，分别是：类本身，从服务器接受的字符串（utf-8），连续标志。
keep_running：一个二进制的标志位，如果为True，这个app的主循环将持续运行，默认值为True。
get_mask_key：用于产生一个掩码。
subprotocols：一组可用的子协议，默认为空。

长连接关键方法：ws.run_forever(ping_interval=60,ping_timeout=5)
"""

def on_message(ws, message):    # 打印接收到的信息
    print(message)
    
def on_error(ws, error):    # 打印错误
    print(error)
    
def on_close(ws):
    print("### closed ###")
    
def on_open(ws):        # 打开连接
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        print('thread terminating...')
    threading._start_new_thread(run, ())     # 启动多线程
    
if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp('ws://echo.websocket.org/',
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()            # 进行长连接
