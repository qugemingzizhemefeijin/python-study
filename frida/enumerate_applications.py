import frida

# 获取模拟器或者手机上已连接的设备
device = frida.get_remote_device()
print(device)

# 获取device上的所有app
applications = device.enumerate_applications()

for application in applications:
	print(application)