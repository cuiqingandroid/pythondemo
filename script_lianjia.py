import uiautomator2 as u2
import time
import random

d = u2.connect()  # connect to device
print(d.info)

while True:
    d.swipe(0.5, 0.8, 0.6, 0.5, 0.01)
    time.sleep(3 + random.randint(1, 3))

