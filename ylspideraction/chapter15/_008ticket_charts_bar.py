"""
获取最低票价的树形图

https://www.freesion.com/article/9613563913/

"""

import random, os, pymongo, json

from pyecharts.charts import Bar
from pyecharts import options as opts

# mogondb数据库
client = pymongo.MongoClient(host='127.0.0.1', port=27017, username="root", password="123456", authSource="test", authMechanism='SCRAM-SHA-1')
# 获取数据库
db = client['test']

day = '2022-03-19'
# 查询一条符合条件的数据    
data = list(db.elong.find({'date': day}))
print("data = %s" %(len(data)))

# 关闭数据库
client.close()

# 数据为0则不动
if len(data) == 0:
    exit(0)
    
bar = (Bar()
       .add_xaxis(list(map(lambda x: x['endCity'], data)))
       .add_yaxis(
            '从北京出发',
            list(map(lambda x: x['price'], data)), category_gap="50%",
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="min", name="最小值"),
                    opts.MarkPointItem(type_="max", name="最大值")
                ]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[
                    opts.MarkLineItem(type_="min", name="最小值"),
                    opts.MarkLineItem(type_="max", name="最大值")
                ]
            )
        )
       .set_global_opts(
            title_opts=opts.TitleOpts(title="航班价格"),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}/元"),name="价格")
        )
)

bar.render("E:/tmp/ticket_render.html")

os.system('E:/tmp/ticket_render.html')
