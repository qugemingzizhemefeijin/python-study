"""
机票路线图
"""

import random, os, pymongo, json

from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import GeoType, SymbolType
from pyecharts.faker import Faker

# mogondb数据库
client = pymongo.MongoClient(host='127.0.0.1', port=27017, username="root", password="123456", authSource="test", authMechanism='SCRAM-SHA-1')
# 获取数据库
db = client['test']

# 查询一条符合条件的数据    
data = list(db.elong.find({'date': '2022-03-17'}))
print("data = %s" %(len(data)))

# 关闭数据库
client.close()

# 数据为0则不动
if len(data) == 0:
    exit(0)
    
citys = list(map(lambda x: x['endCity'], data))
print(citys)

map = (
    Geo()
        .add_schema(maptype="china", itemstyle_opts=opts.ItemStyleOpts(color="#9cf", border_color="#111"))
        .add(series_name="价格",
             data_pair=[list(z) for z in zip(citys, [i['price'] for i in data])],
             type_ = GeoType.EFFECT_SCATTER,
             symbol_size = 14,
             color = Faker.visual_color[0],
        )
        .add(series_name="行程",
             data_pair=[('北京', i['endCity']) for i in data],
             type_ = GeoType.LINES,
             effect_opts = opts.EffectOpts(
                 symbol = SymbolType.ARROW, symbol_size=5, color=Faker.visual_color[2],
             ),
             # curve>0,曲线凸；curve<0，曲线凹
             linestyle_opts = opts.LineStyleOpts(curve=0.1),
             # color=Faker.visual_color[2],
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(title_opts=opts.TitleOpts(title="北京飞行价格图"))
)
map.render(path="E:/tmp/ticket_geo_lines.html")

os.system("E:/tmp/ticket_geo_lines.html")
