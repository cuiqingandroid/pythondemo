import hashlib
import json
import os
from urllib import parse

from mitmproxy import http
from mitmproxy.script import concurrent

import mongodb


def getAbsPath(file, relativePath):
    return os.path.join(os.path.dirname(file), relativePath)


def md5(str):
    """md5 """
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    return hl.hexdigest()

@concurrent
def response(flow: http.HTTPFlow) -> None:
    if flow.response and flow.response.content and flow.request.url.startswith('https://app2.api.lianjia.com/Rentplat/v1/rented/list'):
        # print(flow.response.content)
        url = flow.request.url
        params = dict(parse.parse_qsl(parse.urlsplit(url).query))
        print(params)
        data = json.loads(flow.response.text)
        for item in data['data']['list']:
            mongodb.insert_deal_item(item)
        # with open(getAbsPath(__file__, f'E:/python/code/mitmproxy/data/{md5(flow.request.url)}'), mode='w+') as f:
        #     f.write(flow.request.url)
        #     f.write('\n')
        #     f.write(flow.response.text)




