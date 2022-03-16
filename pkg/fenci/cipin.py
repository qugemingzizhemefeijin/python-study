"""
方式一：

# 创建分词数据框
corpus = pd.DataFrame(words, columns=['word'])
corpus['cnt'] = 1

# 分组统计
g = corpus.groupby(['word']).agg({'cnt': 'count'}).sort_values('cnt', ascending=False)

g.head(10)


方式二：

# 导入相关库
from collections import Counter
from pprint import pprint


counter = Counter(words)

# 打印前十高频词
pprint(counter.most_common(10))
"""