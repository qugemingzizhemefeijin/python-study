"""
案例 ws://121.40.165.18:8800
"""

import websocket
import threading
import time
import pprint

def on_message(ws, message):
    print(1)
    pprint.pprint(message)
    
def on_error(ws, error):
    print(2)
    print(error)
    
def on_close(ws):
    print("### closed ###")
    
def on_open(ws):
    def run(*args):
        ws.send('我的测试者')
        print('yoyoyo')
        time.sleep(5)
        ws.close()
        print("thread terminating...")
    threading._start_new_thread(run, ()) # 启动多线程

headers = {
        'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'Accept-Encoding: gzip, deflate',
        'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control: no-cache',
        'Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits'
}

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp('ws://121.40.165.18:8800',
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close,
                                header = headers)    # 配置参数
    ws.on_open = on_open        # 运行
    ws.run_forever()            # 保持长连接
    
