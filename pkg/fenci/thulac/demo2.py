import pandas as pd
import thulac

# 读取数据
data = pd.read_csv('../meidi_jd.csv', encoding='gb18030')

# 查看数据
print(data.head())
print('=============================')

thulac1 = thulac.thulac(seg_only=True, filt=True)

# 生成分词
data['cut'] = data['comment'].apply(lambda x : list(map(lambda y : y[0], thulac1.cut(x))))

print(data.head())
print('=============================')


# 代码示例1
text = thulac.thulac(seg_only=True, filt=True).cut("京东商城信得过，买得放心，用得省心、安心、放心", text=True)  #进行一句话分词
print(text)
