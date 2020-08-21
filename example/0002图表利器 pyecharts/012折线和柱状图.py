# encoding:utf-8

from pyecharts.charts import Line
from pyecharts.charts import Bar
from pyecharts.charts import Grid
from pyecharts import options as opts

x = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
data_china = [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
data_russia = [1.6, 5.4, 9.3, 28.4, 22.7, 60.7, 162.6, 199.2, 56.7, 43.8, 3.0, 4.9]

bar = (
    Bar()
    .add_xaxis(x)
    .add_yaxis('china', data_china)
    .add_yaxis("sussia", data_russia)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Grid - 多图合并"),
    )
)

line = (
    Line()
    .add_xaxis(x)
    .add_yaxis("蒸发量", [x + 50 for x in data_china])
)

bar.overlap(line)
grid = Grid()
grid.add(bar, opts.GridOpts(pos_left="5%", pos_right="5%"), is_control_axis_index=True)
grid.render()
