# encoding: utf-8

"""
抓取的配置信息
"""

# 请求json的url
API_URL = "https://www.lagou.com/jobs/positionAjax.json"

# 爬取职位要求的url
INFO_URL = "https://www.lagou.com/jobs/%s.html"

# 请求json文件用的headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B8%88?px=default&city=%E6%B7%B1%E5%9C%B3&district=%E5%8D%97%E5%B1%B1%E5%8C%BA",
    "X-Requested-With": "XMLHttpRequest",
    "Host": "www.lagou.com",
    "Cookie": "JSESSIONID=ABAAAECABGFABFFE75009C8A8CAE3B99CEF3FA123D76560; user_trace_token=20200314215308-93db1fff-082a-404f-92d1-d078ddd19973; WEBTJ-ID=20200314215307-170d951e334205-01497ca22ec41d-b791b36-1327104-170d951e3365ad; _ga=GA1.2.1107527964.1584193988; _gid=GA1.2.565586761.1584193988; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1584193988; LGSID=20200314215309-f6d5420c-46fe-48b7-90a1-00ec078cc4ee; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2FallCity.html; LGUID=20200314215309-ce93fb86-d5cc-47ea-92b2-5c502c8f5694; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22170d958e80253-0c7a2281cc9d5e-b791b36-1327104-170d958e803939%22%2C%22%24device_id%22%3A%22170d958e80253-0c7a2281cc9d5e-b791b36-1327104-170d958e803939%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; LGRID=20200314220114-85b28200-ff1e-4d61-8050-cde3f7ab09cd; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1584194473; X_MIDDLE_TOKEN=fde2950adaef5425444ce5e0d1fe8771; X_HTTP_TOKEN=81847f15dc971fe93554914851e3aca0f6b77b89fe; SEARCH_ID=37cae7811c45427abcefbb7269ff9236",
    "Connection": "keep-alive",
    "Origin": "https://www.lagou.com",
    "Upgrade-Insecure-Requests": "1",
    "X-Anit-Forge-Code": "0",
    "X-Anit-Forge-Token": "None",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8"
}

# 爬取职位要求的header
HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"
}

# 新加停用词
STOPWORD_NEW = {'公司', '团队', '介绍', '使用', '岗位职责', '就是', '不是', '回复', '以上', '设计', '任职', '要求', '职位', '描述', '技能', ' 岗位', '职责', '工作', '资格', '优先', '能力', '工作'}
