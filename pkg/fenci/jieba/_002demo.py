"""
pip install pandas

Pandas 是 Python 语言的一个扩展程序库，用于数据分析。
Pandas 是一个开放源码、BSD 许可的库，提供高性能、易于使用的数据结构和数据分析工具。
Pandas 名字衍生自术语 "panel data"（面板数据）和 "Python data analysis"（Python 数据分析）。
Pandas 一个强大的分析结构化数据的工具集，基础是 Numpy（提供高性能的矩阵运算）。
Pandas 可以从各种文件格式比如 CSV、JSON、SQL、Microsoft Excel 导入数据。
Pandas 可以对各种数据进行运算操作，比如归并、再成形、选择，还有数据清洗和数据加工特征。
Pandas 广泛应用在学术、金融、统计学等各个数据分析领域。
"""

import pandas as pd
import jieba
from collections import Counter
from pprint import pprint

# 读取数据
data = pd.read_csv('../meidi_jd.csv', encoding='gb18030')

# 查看数据
print(data.head())
print('=============================')

# 生成分词
data['cut'] = data['comment'].apply(lambda x : list(jieba.cut(x)))

print(data.head())
print('=============================')

# 分词去重
data['cut'] = data['comment'].apply(lambda x : list(set(jieba.cut(x))))
print(data.head())
print('=============================')

# 读取停用词数据
stopwords = pd.read_csv('../cn_stopwords.txt', encoding='utf8', names=['stopword'], index_col=False)

# 转化词列表
stop_list = stopwords['stopword'].tolist()

# 去除停用词
data['cut'] = data['comment'].apply(lambda x : [i for i in jieba.cut(x) if i not in stop_list])

print(data.head())
print('=============================')

# 将所有的分词合并
words = []

for content in data['cut']:
    words.extend(content)

# 创建分词数据框
corpus = pd.DataFrame(words, columns=['word'])
corpus['cnt'] = 1

# 分组统计
g = corpus.groupby(['word']).agg({'cnt': 'count'}).sort_values('cnt', ascending=False)

print(g.head(10))
print('=============================')


counter = Counter(words)

# 打印前十高频词
pprint(counter.most_common(10))
print('=============================')

