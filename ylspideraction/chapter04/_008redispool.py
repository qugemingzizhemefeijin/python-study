import redis
import time

ip = '127.0.0.1'
port = 6379

"""
redis-py 使用 connection pool 来管理对一个 redis server 的所有连接，避免每次建立、释放连接的开销。
默认，每个Redis实例都会维护一个自己的连接池。可以直接建立一个连接池，然后作为参数 Redis，这样就可以实现多个 Redis 实例共享一个连接池。

decode_responses=True 改成字符串
"""

pool = redis.ConnectionPool(host=ip, port=port, decode_responses=True)
r = redis.Redis(connection_pool=pool)
r.set('food', 'mutton', ex=3)    # key是"food" value是"mutton" 将键值对存入redis缓存
print(r.get('food'))  # mutton 取出键food对应的值

r.setex("fruit2", 5, "orange")
time.sleep(1)
print(r.get('fruit2'))  # 5秒后，取值就从orange变成None

r.set("foo", 123)
print(r.mget("foo", "foo1", "foo2", "k1", "k2"))
r.incr("foo", amount=1)
print(r.mget("foo", "foo1", "foo2", "k1", "k2"))
