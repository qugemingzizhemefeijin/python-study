"""
pip install jieba

Python的中文分词库有很多，常见的有：

jieba（结巴分词）
THULAC（清华大学自然语言处理与社会人文计算实验室）
pkuseg（北京大学语言计算与机器学习研究组）
SnowNLP
pynlpir
CoreNLP
pyltp
通常前三个是比较经常见到的，主要在易用性/准确率/性能都还不错。


“结巴”中文分词：做最好的 Python 中文分词组件

支持三种分词模式：

       精确模式，试图将句子最精确地切开，适合文本分析；
       全模式，把句子中所有的可以成词的词语都扫描出来, 速度非常快，但是不能解决歧义；
       搜索引擎模式，在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词。

支持繁体分词

支持自定义词典
"""

import jieba

str = """
缠绵悱恻间，他猛然闷哼了一声，继而用拇指摸了摸嘴角，只见鲜血殷红，他厉声道“顾青辞，你知不知道你如今是什么身份？你是钰王妃，你还想为他守节到什么时候？”

他的话语中声声指责，让青辞无言以对，不知如何回答，只能低头沉默不语。她是钰王妃，就算祁邺想要她，也是情理之中的事情，她又有什么理由去拒绝呢？

她的沉默更加惹怒了祁钰，祁邺猛然间撕裂她的衣裳，露出了小巧精致的锁骨和圆润白皙的肩头。

他用力一拽，将她扔到床榻之上，声音冰冷邪魅，“本王已经容忍你一年了”
"""

def stopwordslist():
    stopwords = [line.strip() for line in open('../cn_stopwords.txt', 'r', encoding='utf-8').readlines()]
    return stopwords

stopwords = stopwordslist()  # 这里加载停用词的路径

uniq = set(jieba.cut(str))
for s in uniq:
    if s.strip() != '' and s not in stopwords:
        print(s)
