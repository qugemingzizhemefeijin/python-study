# encoding:utf-8

from pyecharts.charts import Bar
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
data_russia = [1.6, 5.4, 9.3, 28.4, 22.7, 60.7, 162.6, 199.2, 56.7, 43.8, 3.0, 4.9]

bar = Bar()
bar.add_xaxis(x)
bar.add_yaxis("降水量", data_china)
bar.set_global_opts(title_opts=opts.TitleOpts(title="Bar - 基本示例"))
# render 会生成本地 HTML 文件
bar.render()
# bar.render_notebook()
