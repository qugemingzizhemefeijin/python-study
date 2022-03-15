"""
热力图
"""

from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import GeoType, ThemeType
from pyecharts.faker import Faker
import random, os

map = (
    Geo(init_opts=opts.InitOpts(width="1000px", height="800px", renderer="canvas",
                                theme=ThemeType.LIGHT, animation_opts=opts.AnimationOpts(animation=True)))
        .add_schema(maptype="china")
        .add(series_name="中国热力图",
             data_pair=[list(z) for z in
                        zip(Faker.provinces,
                            [random.randint(0, (i + 1) * 200 + 100) for i in range(len(Faker.provinces))])],
             type_=GeoType.EFFECT_SCATTER, symbol_size=20,
             color=Faker.visual_color[random.randint(0, len(Faker.visual_color)-1)])
        .add(series_name="广东热力图",
             data_pair=[list(z) for z in
                        zip(Faker.guangdong_city,
                            [random.randint(0, (i + 1) * 100) for i in range(len(Faker.provinces))])],
             type_=GeoType.EFFECT_SCATTER, symbol_size=10,
             color=Faker.visual_color[1])
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(visualmap_opts=opts.VisualMapOpts(max_=400, pos_top=20),
                         title_opts=opts.TitleOpts(title=""),
                         )
)
map.render(path="E:/tmp/geo_heatmap.html")


os.system('E:/tmp/geo_heatmap.html')
