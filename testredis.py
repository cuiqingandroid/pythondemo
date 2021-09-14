import redis

r = redis.Redis(host='10.0.100.138', port=6379, decode_responses=True)  # host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
keys = r.keys()
print(keys)

r.set("123", "346")
v = r.get("123")
print(v)