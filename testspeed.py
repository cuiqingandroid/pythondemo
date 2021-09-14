import time

import requests

start = time.time()*1000
requests.get("https://oss.wandougongzhu.cn/d297fd146a60759d74f499d4c12a50c0.jpg?x-oss-process=image/resize,w_500,h_4000/format,webp")
print(time.time()*1000 -start)