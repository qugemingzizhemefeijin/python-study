# encoding:utf-8

from pyecharts.charts import Bar
from pyecharts.charts import Pie
from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.charts import EffectScatter
from pyecharts.globals import SymbolType
from pyecharts.charts import Grid
from pyecharts.charts import WordCloud
from pyecharts.charts import Map
import random

provinces = ['广东', '北京', '上海', '湖南', '重庆', '新疆', '河南', '黑龙江', '浙江', '台湾']
values = [random.randint(1, 1024) for x in range(len(provinces))]

map = (
    Map()
    .add("", [list(z) for z in zip(provinces, values)], "china")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="map - 基本示例"),
        visualmap_opts=opts.VisualMapOpts(max_=1024, is_piecewise=True),
    )

)
map.render()
