"""
pip3 install numpy==1.16.0
pip install pkuseg

pkuseg具有如下几个特点：

多领域分词。不同于以往的通用中文分词工具，此工具包同时致力于为不同领域的数据提供个性化的预训练模型。根据待分词文本的领域特点，用户可以自由地选择不同的模型。
我们目前支持了新闻领域，网络文本领域和混合领域的分词预训练模型，同时也拟在近期推出更多的细领域预训练模型，比如医药、旅游、专利、小说等等。

更高的分词准确率。相比于其他的分词工具包，当使用相同的训练数据和测试数据，pkuseg可以取得更高的分词准确率。

支持用户自训练模型。支持用户使用全新的标注数据进行训练。

注：pkuseg目前仅支持Python3，目前已经很多主流库开始不支持Python2，建议使用Python3版本，如需使用Python2可创建虚拟环境来搭建。
"""

import pandas as pd
import pkuseg

# 读取数据
data = pd.read_csv('../meidi_jd.csv', encoding='gb18030')

# 查看数据
print(data.head())
print('=============================')

# 读取停用词数据
stopwords = pd.read_csv('../cn_stopwords.txt', encoding='utf8', names=['stopword'], index_col=False)
# 转化词列表
stop_list = stopwords['stopword'].tolist()

# 以默认配置加载模型
seg = pkuseg.pkuseg() 

# 进行分词
data['cut'] = data['comment'].apply(lambda x: [i for i in seg.cut(x) if i not in stop_list])

# 查看数据
print(data.head())
print('=============================')


# 使用默认模型，并使用自定义词典（这样子在dict.txt中的词不会被分解）
seg = pkuseg.pkuseg(user_dict='dict.txt') 

# 进行分词
data['cut'] = data['comment'].apply(lambda x: [i for i in seg.cut(x) if i not in stop_list])

# 查看数据
print(data.head())
print('=============================')
