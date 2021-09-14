# coding=utf-8
# AES AES/CBC/PKCS5|Zero
import ast
import base64
import hashlib
import json
import time

import requests
from Crypto.Cipher import AES

# pip install pycryptodome

'''
采用AES对称加密算法
'''
# str不是16的倍数那就补足为16的倍数. ZeroPadding

'''
    在PKCS5Padding中，明确定义Block的大小是8位
    而在PKCS7Padding定义中，对于块的大小是不确定的，可以在1-255之间
    PKCS #7 填充字符串由一个字节序列组成，每个字节填充该字节序列的长度。
    假定块长度为 8，数据长度为 9，
    数据： FF FF FF FF FF FF FF FF FF
    PKCS7 填充： FF FF FF FF FF FF FF FF FF 01 01 01 01 01 01 01   ?应该是填充01

    python3:填充bytes(这个说法不对,AES的参数是字符串,不是byte)
    length = 16 - (len(data) % 16)
    data += bytes([length])*length

    python2:填充字符串
    length = 16 - (len(data) % 16)
    data += chr(length)*length

    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    unpad = lambda s : s[0:-ord(s[-1])]
'''


class AES_CBC:
    def __init__(self, key="d4d0Y7Zb1lh576E7kHLdm8D4f7o0O74N", iv="d4d0Y7Zb1lh576E7"):
        self.key = key
        self.iv = iv

    # 加密方法
    def encrypt_oracle(self, text):
        # 偏移量 16个0
        # 初始化加密器
        aes = AES.new(str.encode(self.key), AES.MODE_CBC, str.encode(self.iv))
        bs = AES.block_size
        pad2 = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)  # PKS7

        encrypt_aes = aes.encrypt(str.encode(pad2(text)))

        # 用base64转成字符串形式
        # 执行加密并转码返回bytes
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')
        # 和js的 结果相同 http://tool.chacuo.net/cryptaes
        return encrypted_text

    # 解密方法
    def decrypt_oralce(self, text):
        # 初始化加密器
        # 偏移量 16个0
        aes = AES.new(str.encode(self.key), AES.MODE_CBC, str.encode(self.iv))
        # 优先逆向解密base64成bytes
        base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
        #
        decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8')  # 执行解密密并转码返回str
        unpad = lambda s: s[0:-ord(s[-1])]
        return unpad(decrypted_text)


def batchBrandList(page):
    url = "https://app.zhenwoapp.com/blade-product/app/batch/brand/list"
    timestamp = str(int(time.time() * 1000))
    nonce = "2cXjGCtZ4nTIxNYOdJCMQY9FZ5GHDZic"
    headers = {
        "timestamp": timestamp,
        "nonce": nonce,
        "token": 'PJlSUPtAX+sq+apzZ1sYQ64ZEgBglrp29a662yeIOi43/TMbiqin41s6bvcmfihPUC+I5gFX0CL8hQyVeKNY+g==',
        'signature': hashlib.sha1(str.encode(f'{timestamp}{nonce}')).hexdigest(),
        "Content-Type": "application/json"
    }
    data = {
        "name": '',
        "size": 20,
        'page': page
    }
    key = "d4d0Y7Zb1lh576E7kHLdm8D4f7o0O74N"
    iv = "d4d0Y7Zb1lh576E7"
    aes = AES_CBC(key, iv)
    resp = requests.post(url, headers=headers, data=aes.encrypt_oracle(str(data)))

    if resp.status_code == 200:
        try:
            ret = resp.json()
            if ret['success']:
                return Exception(ret['msg'])
        except Exception as e:
            ret = json.loads(aes.decrypt_oralce(resp.text))
            if ret['success']:
                return ret['data']
    return Exception(f"{resp.status_code} {resp.text}")


def batchQuery(batch, branchId):
    url = "https://app.zhenwoapp.com/blade-product/app/batch/search"
    timestamp = str(int(time.time() * 1000))
    nonce = "2cXjGCtZ4nTIxNYOdJCMQY9FZ5GHDZic"
    headers = {
        "timestamp": timestamp,
        "nonce": nonce,
        "token": "vc2iUip3S99VAwGmi6of9nABVPbYy5UlXEgBqHm4MLc0fX3m5PlDQgv2PWqHOy1sOGMY+orMACd/fNoRKqNKwQ==",
        'signature': hashlib.sha1(str.encode(f'{timestamp}{nonce}')).hexdigest(),
        "Content-Type": "application/json"
    }
    data = {
        "batch": batch,
        "id": branchId
    }

    aes = AES_CBC()
    resp = requests.post(url, headers=headers, data=aes.encrypt_oracle(str(data)))
    print(resp.text)
    print(aes.decrypt_oralce(resp.text))


if __name__ == '__main__':
    aes = AES_CBC()

    # 解密
    dec_text = aes.decrypt_oralce('hTEKk/vcmUbSHdi58y3+foRtoKCTxy//TkJT2TjuJLHzKojZ0/rDrWiRk63NjRy74SJ4z21hREN5i/e4G95SddJ5Qrq1XbtqTLVEIWqF1pwh7C202xffkLbljuG7HIXk8Wckmf/Xc8U7isbvE7iancfpR30BMkeQrSaeBIIu9kK7cZMflhrU3xB9318LhDHRyddo0Da4Oh/EQD+YE1hR9VbViq4QkZPrAw8hYHZTVv5vQ1KEs8sk9URfnqM5QnyKDw/S5nKqANQDShOA1rvLHMYoNL+/3B9TVVyA0cklUSrhBMelURKr3EDJZ21IGUEFoT8k4YGcn1u4dRHe/NMMJa9AlJzHYD/a5aaj+oCZ2IpAMhC3+odJN0TRcsPBIzgbpZofvxinHnoaMIjm0WBlCvHu25aGpj9SV+l/Tv/Gycy7CVCddUuKQG2yV4l4Vak8kSiTms7DOTijGhXaJfOAgmqeJGGCPRhZv+PzAK/DXk3sfFKgH1gzpiLfMRamQtOmElrRQYrj/niq9sb6Rqz//ELdMGYe3CLKYBMH4gI7q+T18ZfkS+RDHtK4sSC9gG11dfGeBZdAhsO2o5yjSiS4rA==')
    print(dec_text)
    data = {
        "batch": "B0003140",
        "id": "7b4ebe495fdf3556e743cbe28350691d"
    }
    print(str(data))

    # brandData = batchBrandList(1)
    # print(brandData)
    # with open('zhenwo_brands', mode='w', encoding='utf-8') as f:
    #     for item in brandData['records']:
    #         f.write(str(item))
    #         f.write('\n')
    count = 0
    with open('zhenwo_brands', mode='r', encoding='utf-8') as f:
        for line in f.readlines():
            item = ast.literal_eval(line)
            print(item)
            if item['isSearch'] == 1:
                count += 1
    print(count)
    exit()

    brandList = []
    page = 1
    while True:
        brandData = batchBrandList(page)
        records = brandData['records']
        if len(records) <= 0:
            break
        brandList.extend(records)
        print(page, brandData)
        page += 1
        time.sleep(0.1)

    with open('zhenwo_brands', mode='w+', encoding='utf-8') as f:
        for item in brandList:
            f.write(str(item))
            f.write('\n')

    # print(getBrands()['brands'])
    # db = DBClient()
    # for brand in getBrands()['brands']:
    #     name = brand['name']
    #     oid = brand['oid']
    #     if db.queryaal(oid) is None:
    #         db.insertBrand(name, oid)

    # batchQuery('B0003140', '7b4ebe495fdf3556e743cbe28350691d')

    # batchBrandList()

    # print(hashlib.md5(sha1))
