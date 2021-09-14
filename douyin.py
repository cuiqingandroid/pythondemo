import requests

# LUOPAN_DT 风险检测
cookie = 'LUOPAN_DT=session_6999834920998781218'
url = 'https://compass.jinritemai.com/business_api/shop/product_summary/download?query_condition=&date_type=2&begin_date=1629676800&end_date=1629676800'
headers = {
    'cookie': cookie,
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}
resp = requests.get(url=url, headers=headers)
if resp.status_code == 200:
    try:
        resp.json()
        print(resp.json())
    except Exception as e:
        with open("douyin.xlsx", mode='wb+') as f:
            f.write(resp.content)
else:
    print(resp.status_code, resp.text)
