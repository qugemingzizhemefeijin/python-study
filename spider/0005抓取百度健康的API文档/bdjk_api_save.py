import os, requests, json, sys, re, traceback
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse

basePath = 'D:/pictures/bdjk/' + datetime.now().strftime('%Y-%m-%d')

template = """
<head>
<meta charset="utf-8">
<meta http-equiv="x-ua-compatible" content="ie=edge">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<link href="https://bce.bdstatic.com/p3m/health/online/health_mall_openapi/health/health_mall_openapi/styles.c57e4da8a2770bb89f1a.css" rel="stylesheet" type="text/css">
<meta name="generator" content="Gatsby 2.18.5">
<title>开放平台 - %s</title>
<meta data-react-helmet="true" name="description" content="">
<meta data-react-helmet="true" name="keywords" content=""><style type="text/css">
    .anchor {
      float: left;
      padding-right: 4px;
      margin-left: -20px;
    }
    h1 .anchor svg,
    h2 .anchor svg,
    h3 .anchor svg,
    h4 .anchor svg,
    h5 .anchor svg,
    h6 .anchor svg {
      visibility: hidden;
    }
    h1:hover .anchor svg,
    h2:hover .anchor svg,
    h3:hover .anchor svg,
    h4:hover .anchor svg,
    h5:hover .anchor svg,
    h6:hover .anchor svg,
    h1 .anchor:focus svg,
    h2 .anchor:focus svg,
    h3 .anchor:focus svg,
    h4 .anchor:focus svg,
    h5 .anchor:focus svg,
    h6 .anchor:focus svg {
      visibility: visible;
    }
  </style>
</head>
<body>

<div class="body" style="margin-top:80px">
    <div class="main">
        <div class="post-wrapper">
            <div class="post">
                <h1 class="post__title">%s</h1>
                <div class="post__description"><div class="post__date">更新时间：%s</div></div>
                <div class="post__body">%s</div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

def init():
    print(basePath)
    # 文件夹不存在，创建
    if not os.path.exists(basePath):
        os.makedirs(basePath)
        
def getAllDocLink():
    url = 'https://bce-cdn.bj.bcebos.com/p3m/health/online/health_mall_openapi/health/health_mall_openapi/平台简介/index.html'
    res = requests.get(url)  # 获取英雄列表json文件
    if res.status_code != 200:
        print("获取API列表失败，status_code = %s" % res.status_code)
        exit(0)
    soup = BeautifulSoup(res.text, 'lxml')
    # 存放列表页url
    data_list = []
    for i in soup.find_all('li', class_='menu-item'):
        try:
            filePath = i.find("a")['data-filepath'].strip().replace('.md', '')
            #url = i.find("a").get('href').strip()
            print(filePath)
            
            pathArr = filePath.split('/')
            
            # 此处中转一下URL中的值
            data_list.append({'name': pathArr[len(pathArr)-1], 'dir': '/'.join(pathArr[0:-1]), 'url': parseUrl(pathArr)})
        except Exception as e:
            traceback.print_exc()
    return data_list

def parseUrl(pathArr):
    for idx in range(len(pathArr)):
        pathArr[idx] = urllib.parse.quote(pathArr[idx])
    return 'https://bce.bdstatic.com/p3m/health/online/health_mall_openapi/health/health_mall_openapi/page-data/'+('/'.join(pathArr))+'/page-data.json'

def downloadDocument():
    data_list = getAllDocLink()
    for item in data_list:
        print(item)
        saveAPI(item)

def saveAPI(item):
    print("download API : %s , dir : %s , url : %s" % (item['name'], item['dir'], item['url']))
    res = requests.get(item['url'])  # 获取英雄列表json文件
    if res.status_code != 200:
        print("获取API失败，status_code = %s" % res.status_code)
        return
    try:
        dir = basePath + '/' + item['dir']
        if not os.path.exists(dir):
            os.makedirs(dir)
        result = res.json()
        with open(dir + '/' + item['name'] + '.txt', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(result, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
        with open(dir + '/' + item['name'] + '.html', 'w', encoding='UTF-8') as f:
            f.write(template % (item['name'], item['name'], result['result']['data']['markdownRemark']['fields']['date'], result['result']['data']['markdownRemark']['html']))
        print('%s 文件保存成功' % item['name'])
    except:
        traceback.print_exc()
        
if __name__ == '__main__':
    init()
    downloadDocument()
    # saveAPI({'name': '订单详情', 'dir': 'API文档/订单类API', 'url': 'https://bce.bdstatic.com/p3m/health/online/health_mall_openapi/health/health_mall_openapi/page-data/API%E6%96%87%E6%A1%A3/%E8%AE%A2%E5%8D%95%E7%B1%BBAPI/%E8%AE%A2%E5%8D%95%E8%AF%A6%E6%83%85/page-data.json'})
    