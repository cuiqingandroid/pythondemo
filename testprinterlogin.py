import requests

import testPrintApi

host = "10.0.100.136"

headers = {
    "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
    "Cookie": "AWMS2LOGIN_AUTO=True; ASP.NET_SessionId=rs1gkmikhhdpbsi0txhv440n",
    "X-Requested-With": "XMLHttpRequest",
    "__AWMS2RequestVerificationToken": "undefined",
    "Accept-Language":"zh-CN,zh;q=0.9"
}


def login():
    modules = "E329CFCCF2DC28B6944F30EFC627B647B74A7E5B875369B71EC5E660789CB689795592B499AB526CA6114A2FC479FAB0054FBA494A38D653A321F6630C99AD51C6825CFF11EF7C4DAC55E44BC1786E9BA6D0B10A2BA7ADF8512921D6D18AFFCAF4A1901A54FF1FBF309CFF7A4BDC6269E93DB947FC17617478A4418ED7FD7FB8407A790A371D7B9CD822FC488A8A7AEC160C61EF45C586CD1826F49A90719735FF7045C0411568B990F88B3EBCBDD9BA4AB6FCAD07FEDC73AFA9D92AE0311483F7C1C71141B654F576EB7FD46DD80CCE799A50D99D2BE362CE3F78D1471C017418B5A59E51EDFA82E2B0CFE01B18222F4C64A24E9A1FAEB68BAAB3EA66CCEEF9"
    exponent = "010001"
    _challenge = "07e77106-c123-429b-a07e-a14c6024c894"
    data = {
        "returnUrl": "",
        "EncryptedPassword": """025120c80debbbcc8c96ac9cccfae343049d5a1a7588a5d3a0b0fde7f3a0e1b60a70ae90192fff1a373ae72d4e368af2bdcbaa980be3ab390d0486ad
603309fa81d99f705be231cd72ffe2a3b8f36dabe4f1d1d18450623e51fff80d42a3c6926640778c4cb128c78d013be333fac35e3ad8ba6ae5085cb8
a884124b6922602005da046b162aae090cd4d4489eb52bc1060f1b8bcbbccf68efc2dc30bcfb197f1f99d418801add91b4dda7b2f882f40de1dad522
d98ed96e8222d30d6cd803eb56a79669b3b4848f9c53b48c36888bee5a56e001d4dd5240fe7142c4eec9e9c808af8e7703e52d46d58e0a5354110875
f81c186eca2bdbbfbd8aa01d55bd119d""",
        "RSAKeyInfo.Modulus": modules,
        "RSAKeyInfo.Exponent": exponent,
        "RSAKeyInfo.Challenge": _challenge,
        "Username": "kaoqin_manager"
    }
    url = f"http://{host}/Login/"
    resp = requests.post(url, headers=headers, data=data, proxies={"http":"http://127.0.0.1:8282"})
    print(resp.text)
    if resp.status_code == 200 and resp.json()['Success']:
        return resp.json()['ReturnUrl'], resp.cookies
    return None


loginRet = login()
cookies = requests.utils.dict_from_cookiejar(loginRet[1])
print(cookies)
if loginRet is not None:
    resp = requests.post(f"http://{host}/Admin", headers=headers, cookies=cookies, proxies={"http":"http://127.0.0.1:8282"})
    print(resp.text)

    # do call back
    import bs4
    soup = bs4.BeautifulSoup(resp.text, 'html.parser')
    inp = soup.find("input", {"name":"wresult"})
    callbackData = {
        "wa": "wsignin1.0",
        "wresult": inp["value"],
        "wctx" : soup.find("input", {"name":"wctx"})['value'],
    }
    callbackCookie = requests.utils.dict_from_cookiejar(resp.cookies)
    resp = requests.post(f"http://{host}/Admin/LoginPostBack", data=callbackData, allow_redirects=False, proxies={"http":"http://127.0.0.1:8282"})
    # resp = requests.post(f"http://{host}/Admin/LoginPostBack", data=callbackData, cookies=callbackCookie,proxies={"http":"http://127.0.0.1:8282"})
    # newCookies = requests.utils.dict_from_cookiejar(resp.cookies)
    # newCookies = resp.headers['Set-Cookie']
    # newCookies = resp.request.headers['Cookie']
    newCookies = ''
    for k,v in requests.utils.dict_from_cookiejar(resp.cookies).items():
        if len(newCookies) > 0:
            newCookies += ";"
        newCookies += f"{k}={v}"
    print(testPrintApi.getUserInfo(newCookies, "nimid:11:0001-00000002c3", "wangjunwu"))
    print(testPrintApi.searchUser(newCookies, "cuiqing"))