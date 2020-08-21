import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 绑定端口
s.bind(('127.0.0.1', 9999))

print('Bind UPD on 9999....')
while True:
	# 接收数据
	data, addr = s.recvfrom(1024)
	print('Received from %s:%s.' % addr)
	s.sendto(b'Hello, %s!' % data, addr)

#recvfrom()方法返回数据和客户端的地址与端口，这样，服务器收到数据后，直接调用sendto()就可以把数据用UDP发给客户端。
#注意这里省掉了多线程，因为这个例子很简单。

