"""
自定义预训练模型
分词模式下，用户需要加载预训练好的模型。pkuseg提供三种不同数据类型训练得到的模型。

MSRA: 在MSRA（新闻语料）上训练的模型。https://pan.baidu.com/s/1twci0QVBeWXUg06dK47tiA

CTB8: 在CTB8（新闻文本及网络文本的混合型语料）上训练的模型。https://pan.baidu.com/s/1DCjDOxB0HD2NmP9w1jm8MA

WEIBO: 在微博（网络文本语料）上训练的模型。https://pan.baidu.com/s/1QHoK2ahpZnNmX6X7Y9iCgQ

MixedModel: 混合数据集训练的通用模型。随pip包附带的是此模型。https://pan.baidu.com/s/1Ej2TFTOLp84FDIPoQMtsMg
"""

import pkuseg

# 下载后解压出来，并复制文件夹路径
file_path = 'E:\Downloads\ctb8'

# 加载其他预训练模型
seg = pkuseg.pkuseg(model_name=file_path)
text = seg.cut('京东商城信得过，买的放心，用的省心、安心、放心！')

print(text)

