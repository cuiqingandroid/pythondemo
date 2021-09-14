import base64

import requests
from Crypto.Cipher import AES

from db import DBClient


class EncryptDate:
    def __init__(self, key):
        self.key = key  # 初始化密钥
        self.length = AES.block_size  # 初始化数据块大小
        self.aes = AES.new(bytes(self.key, "utf-8"), AES.MODE_ECB)  # 初始化AES,ECB模式的实例
        # 截断函数，去除填充的字符
        self.unpad = lambda date: date[0:-ord(date[-1])]

    def pad(self, text):
        """
        #填充函数，使被加密数据的字节码长度是block_size的整数倍
        """
        count = len(text.encode('utf-8'))
        add = self.length - (count % self.length)
        entext = text + (chr(add) * add)
        return entext

    def encrypt(self, encrData):  # 加密函数
        res = self.aes.encrypt(self.pad(encrData).encode("utf8"))
        msg = str(base64.b64encode(res), encoding="utf8")
        return msg

    def decrypt(self, decrData):  # 解密函数
        res = base64.decodebytes(decrData.encode("utf8"))
        msg = self.aes.decrypt(res).decode("utf8")
        return self.unpad(msg)


key = "4Vt5jmY@aoaola.com**************"


def aoaolaBatchCode(brandOid, code):
    url = f"https://tool.aoaola.com/api/v1/batch_code?oid={brandOid}&code={code}"
    headers = {
        "authorization":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvaWQiOiI0VnQ1am1ZIiwiZXhwIjoxNjM0MTQ4NTc2fQ.LPi7gE_2fg0DIr5qknXZlGWf5RbHphvkGhLDuWYwkdY"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        if data['meta']['status'] == "ok":
            start = data['data']['lot']
            end = data['data']['exp']
            eg = EncryptDate(key)  # 这里密钥的长度必须是16的倍数
            print('生产日期:', eg.decrypt(start))
            print('过期日期:', eg.decrypt(end))


def getBrands():
    url = "https://tool.aoaola.com/api/v1/batch_brands"
    headers = {
        "authorization":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvaWQiOiI1R0dJNFlFIiwiZXhwIjoxNjMxNDE0Mzc0fQ.jS5pDL0SFEaWzQ6DnrKlJUfS4chr0SxLIfl_TtTQqVY"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        if data['meta']['status'] == "ok":
            return data['data']



if __name__ == "__main__":
    code = "B0003140"
    kroid = "IFGR"
    # jmj = "WVKW"
    aoaolaBatchCode(kroid, code)
    exit()
    # aoaolaBatchCode(kroid, "54BSLB")

    print(getBrands()['brands'])
    db = DBClient()
    for brand in getBrands()['brands']:
        name = brand['name']
        oid = brand['oid']
        if db.queryaal(oid) is None:
            db.insertBrand(name, oid)