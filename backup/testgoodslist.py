import requests
import sys
from login import login, cookies

is_login = False
for i in range(3):
    if login():
        is_login = True
        break

print(is_login)

if not is_login:
    print('登录失败')
    sys.exit()

print('登陆成功')

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
}

data = {
    'abc': '123',
    'pageNo': '1',
    'pageSize': '20',
}
try:
    response = requests.post(
        'http://aaa.bbb.com:8080/list',
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False,
    )
    print(response.text)
except Exception as e:
    print("查询异常".format(e))
