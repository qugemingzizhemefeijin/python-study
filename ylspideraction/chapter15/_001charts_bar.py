"""
数据可视化
"""

import os
from pyecharts.charts import Bar
from pyecharts import options as opts

cate = ["衬衫", "羊毛衫", "雪纺纱", "裤子", "高跟鞋", "袜子"]
data1 = [5, 20, 46, 10, 75, 90]
bar = (Bar()
       .add_xaxis(cate)
       .add_yaxis('服装', data1,category_gap="50%")
       .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
)

bar.render("E:/tmp/render.html")

os.system('E:/tmp/render.html')
