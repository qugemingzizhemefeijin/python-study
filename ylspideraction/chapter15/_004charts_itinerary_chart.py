"""
行程图
"""

import random, os

from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import GeoType, SymbolType
from pyecharts.faker import Faker

Faker.provinces = ["北京", "上海", "江苏", "浙江", "江西", "广东", "湖南", "和布克赛尔蒙古自治县"]
map = (
    Geo()
        .add_schema(maptype="china",
                    itemstyle_opts=opts.ItemStyleOpts(color="#9cf", border_color="#111"))
        .add(series_name="顺序",
             data_pair=[list(z) for z in
                        zip(Faker.provinces,
                            [i + 1 for i in range(len(Faker.provinces))])],
             type_=GeoType.EFFECT_SCATTER,
             color=Faker.visual_color[0],
             )
        .add(series_name="行程",
             data_pair=[(Faker.provinces[i], Faker.provinces[(i + 1) % len(Faker.provinces)]) for i in
                        range(len(Faker.provinces))],
             type_=GeoType.LINES,
             effect_opts=opts.EffectOpts(
                 symbol=SymbolType.ARROW, symbol_size=5, color=Faker.visual_color[2],
             ),
             # curve>0,曲线凸；curve<0，曲线凹
             linestyle_opts=opts.LineStyleOpts(curve=0.1),
             # color=Faker.visual_color[2],
             )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="行程图"))
)
map.render(path="E:/tmp/geo_lines.html")

os.system("E:/tmp/geo_lines.html")
