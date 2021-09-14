import hashlib
import urllib.parse
from time import time

import requests

# host = "http://10.0.0.16:8001/"
host = "https://kaoqin.inagora.org/"

def md5(str):
    """md5 """
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    return hl.hexdigest()

def signParams(params):
    sortedParams = ''
    for k in sorted(params.keys()):
        if len(sortedParams) > 0:
            sortedParams += "&"
        sortedParams += k
        sortedParams += "="
        sortedParams += str(params[k])
    sortedParams += "d8b5b4635095cdca84ca66972f4b0e45"
    sortedParams = sortedParams.lower()
    print(sortedParams)
    return md5(sortedParams)

def setUserOnePermission():
    url = host + "app/ajaxSetDoorPermission?"

    getParams = {
        "start_time": int(time()-2600),
        "end_time": int(time())+86400*7,
        "count": 99,
        "user_name": "jinfang",
        "door_id": 8,
        "appid":"house_goods_manager",
        "ts": int(time())
    }
    getParams['sign'] = signParams(getParams)
    querystring = urllib.parse.urlencode(getParams)
    url = url+querystring
    resp = requests.get(url)
    print(url)
    print(resp.json())


def getUserInfo():
    url = host + "app/ajaxGetUserInfo?"

    getParams = {
        "card_sn": '5901634',
        "appid": "house_goods_manager"
    }
    getParams['sign'] = signParams(getParams)
    querystring = urllib.parse.urlencode(getParams)
    url = url+querystring
    resp = requests.get(url)
    print(url)
    print(resp.json())

def getActiveDoors():
    url = host + "app/ajaxGetActiveDoors?"

    getParams = {
        "appid": "house_goods_manager",
        "ts": int(time())
    }
    getParams['sign'] = signParams(getParams)
    querystring = urllib.parse.urlencode(getParams)
    url = url+querystring
    resp = requests.post(url)
    print(url)
    print(resp.json())
# getUserInfo()
setUserOnePermission()
# getActiveDoors()
# print(signParams(data))