import redis

ip = '127.0.0.1'
port = 6379

"""
redis 提供两个类 Redis 和 StrictRedis, StrictRedis 用于实现大部分官方的命令，Redis 是 StrictRedis 的子类，用于向后兼用旧版本。
redis 取出的结果默认是字节，我们可以设定 decode_responses=True 改成字符串。
"""

r = redis.Redis(host=ip, port=port, decode_responses=True)  
r.set('name', 'runoob')  # 设置 name 对应的值
print(r['name'])
print(r.get('name'))  # 取出键 name 对应的值
print(type(r.get('name')))  # 查看类型

