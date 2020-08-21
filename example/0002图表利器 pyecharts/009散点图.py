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

x = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
data_china = [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]

scatter = (
    EffectScatter()
    .add_xaxis(x)
    .add_yaxis("", data_china)
    .set_global_opts(title_opts=opts.TitleOpts(title="EffectScatter - 基本示例"))
)
scatter.render()
