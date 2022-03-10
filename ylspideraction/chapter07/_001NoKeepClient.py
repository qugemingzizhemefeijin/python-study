# 短连接
from websocket import create_connection

ws = create_connection("ws://echo.websocket.org/") # 创建连接
print("Sending 'Hello, World'...") # 打印发送内容
ws.send('Hello, World') # 发送信息
print('Sent')           # 已发送
print('Receiving...')   # 正在接收
result = ws.recv()      # 获取返回结果
print("Received '%s'" % result) # 打印返回结果
ws.close()              # 关闭连接
