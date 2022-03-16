"""
pip install thulac

THULAC（THU Lexical Analyzer for Chinese）由清华大学自然语言处理与社会人文计算实验室研制推出的一套中文词法分析工具包，具有中文分词和词性标注功能。THULAC具有如下几个特点：

能力强。利用我们集成的目前世界上规模最大的人工分词和词性标注中文语料库（约含5800万字）训练而成，模型标注能力强大。

准确率高。该工具包在标准数据集Chinese Treebank（CTB5）上分词的F1值可达97.3％，词性标注的F1值可达到92.9％，与该数据集上最好方法效果相当。

速度较快。同时进行分词和词性标注速度为300KB/s，每秒可处理约15万字。只进行分词速度可达到1.3MB/s。


总体感觉不如 jieba
"""

import thulac

"""
user_dict           设置用户词典，用户词典中的词会被打上uw标签。词典中每一个词一行，UTF8编码
T2S                 默认False, 是否将句子从繁体转化为简体
seg_only            默认False, 时候只进行分词，不进行词性标注
filt                默认False, 是否使用过滤器去除一些没有意义的词语，例如“可以”。
model_path          设置模型文件所在文件夹，默认为models/
text                默认为False, 是否返回文本，不返回文本则返回一个二维数组([[word, tag]..]),seg_only模式下tag为空字符。

"""

# 代码示例1
text = thulac.thulac(seg_only=True, filt=True).cut("我爱北京天安门", text=True)  #进行一句话分词
print(text)

# 代码示例2 input.txt需要GBK编码
thu1 = thulac.thulac(seg_only=True)  #只进行分词，不进行词性标注
thu1.cut_f("input.txt", "E:/output.txt")  #对input.txt文件内容进行分词，输出到output.txt
