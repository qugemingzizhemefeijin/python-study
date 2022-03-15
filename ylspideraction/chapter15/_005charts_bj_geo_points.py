"""
分布图
"""

import os
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ThemeType
from pyecharts.faker import Faker
import numpy as np

length = 100
lons = np.random.ranf(length) * (117.30043 - 115.71633) + 115.71633
lats = np.random.ranf(length) * (40.65389 - 39.47002) + 39.47002

map = (Geo(init_opts=opts.InitOpts(width="1000px", height="800px", renderer="svg",
                                  theme=ThemeType.LIGHT, animation_opts=opts.AnimationOpts(animation=True)))
    .add_schema(maptype="北京", layout_size=100))

# 添加自定义点和属性
[map.add_coordinate("点%d" % i, lons[i], lats[i])
     .add(series_name=(lambda x: "类别-0" if x % 2 == 0 else "类别-1")(i),
          data_pair=[("点%d" % i, i * 100)],
          color=(lambda x: Faker.visual_color[0] if x % 2 == 0 else Faker.visual_color[2])(i),
          ) for i in range(length)]

map.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
map.set_global_opts(title_opts=opts.TitleOpts(title="自定义点"))
# 在 html 渲染图表
map.render('E:/tmp/geo_points.html')
# 在 Jupyter Notebook 中渲染图表
# map.render_notebook()

os.system('E:/tmp/geo_points.html')

