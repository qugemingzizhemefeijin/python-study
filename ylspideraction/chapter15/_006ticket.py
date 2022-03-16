"""
爬取最低价机票数据
"""

import json
import requests
from multiprocessing.dummy import Pool as ThreadPool
import pymongo

import logging, traceback

# 启用调试于 http.client 级别 (requests->urllib3->http.client)
# 你将能看到 REQUEST，包括 HEADERS 和 DATA，以及包含 HEADERS 但不包含 DATA 的 RESPONSE。
# 唯一缺少的是 response.body，它不会被 log 记录。

"""
try:
    from http.client import HTTPConnection
except ImportError:
    from httplib import HTTPConnection
HTTPConnection.debuglevel = 1

logging.basicConfig() # 初始化 logging，否则不会看到任何 requests 的输出。
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
"""

# mogondb数据库
client = pymongo.MongoClient(host='127.0.0.1', port=27017, username="root", password="123456", authSource="test", authMechanism='SCRAM-SHA-1')
# 获取数据库
db = client['test']

city_code = ['SHA', 'NKG', 'NNG', 'CTU', 'WUH', 'HGH', 'SZX']
city = ['上海', '南京', '南宁', '成都', '武汉', '杭州', '深圳']
cityMap = {}
# 生成索引下标
for i, j in enumerate(city_code):
    print(j)
    cityMap[j] = city[i]
# 将北京的加上
cityMap['PEK'] = '北京'

def start(cityCode):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'Referer': 'https://www.ly.com/flights/itinerary/oneway/PEK-SHA?date=2022-03-17&from=%E5%8C%97%E4%BA%AC&to=%E4%B8%8A%E6%B5%B7&fromairport=&toairport=&p=465&childticket=0,0',
        'content-type': 'application/json;charset=UTF-8'
    }
    url = 'https://www.ly.com/flights/api/getpricecalendar'
    data = {
            "StartPort":"PEK",
            "EndPort":cityCode,
            "QueryBegDate":"2022-03-16",
            "QueryEndDate":"2022-05-17",
            "QueryType":1,
            "travelTypes":[1],
            "flat":"465",
            "plat":"465",
            "isFromKylin":1,
            "refid":""
    }
    
    for i in range(3):
        try:
            res = requests.post(url, headers = headers, data = json.dumps(data))
            print(city)
            v = res.json()
            print('code = %s, msg = %s' % (v['resCode'], v['resDesc']))
            if v['resCode'] == 0 :
                print('start %s %s , end %s %s' % (v['body']['startport'], v['body']['startportname'], v['body']['endport'], v['body']['endportname']))
                for k in v['body']['fzpriceinfos']:
                    item = {
                            'startCityCode': v['body']['startport'],
                            'startCity': cityMap[v['body']['startport']],
                            'startPort': v['body']['startportname'],
                            'endCityCode': v['body']['endport'],
                            'endCity': cityMap[v['body']['endport']],
                            'endPort': v['body']['endportname'],
                            'date': k['flydate'],
                            'price': k['price'],
                            'flightno': k['flightno']
                    }
                    # 存储到数据库
                    print(item)
                    db.elong.insert_one(item)
                break
        except:
            traceback.print_exc()
    
if __name__ == '__main__':
    print('初始化数据库')
    # 清空数据
    db.elong.delete_many({})
    print('数据库初始化完成')
    
    pool = ThreadPool(1)
    pool.map(start, city_code) # 通过map将city元素里的元素逐一映射
    pool.close()
    pool.join()
    print('完成抓取工作')
    # 关闭数据库
    client.close()
