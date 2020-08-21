# encoding: utf-8

'''
此功能是抓取公众号页面信息并生成PDF
'''

import requests
import json
import re
import random
import time
import pdfkit

# 打开 cookie.txt
with open('cookie.txt', 'r') as file:
    cookie = file.read()
cookies = json.loads(cookie)

url = "https://mp.weixin.qq.com"
# 请求公众号平台
response = requests.get(url, cookies=cookies)

# 从url中后去token
token = re.findall(r'token=(\d+)', str(response.url))[0]
# 设置请求访问头信息
headers = {
    "Referer": "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=" + token + "&lang=zh_CN",
    "Host": "mp.weixin.qq.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
}

fakeid = "MzU1NDk2MzQyNg=="

# 循环遍历前10页的文章
for j in range(1, 10, 1):
    begin = (j-1)*5
    # 请求当前页获取文章列表
    requestUrl = "https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin="+str(begin)+"&count=5&fakeid=" + fakeid + "&type=9&query=&token=" + token + "&lang=zh_CN&f=json&ajax=1"
    search_response = requests.get(requestUrl, cookies=cookies, headers=headers)
    # 获取到返回列表 Json 信息
    re_text = search_response.json()
    list = re_text.get("app_msg_list")
    # 遍历当前页的文章列表
    for i in list:
        print("title=%s,link=%s" % (i["title"], i["link"]))
        # 将文章链接转换 pdf 下载到当前目录
        pdfkit.from_url(i["link"], i["title"] + ".pdf")
    # 过快请求可能会被微信问候，这里进行10秒等待
    time.sleep(10)
