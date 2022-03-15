### Python3爬虫实战：数据清洗、数据分析与可视化 - 案例

#### 安装模块
```
pip install beautifulsoup4
pip install xlwt
pip install xlrd
pip install python-docx
pip install requests
pip install lxml
pip install parsel
pip install w3lib
pip install twisted
pip install cryptography
pip install pyOpenSSL
pip install Scrapy
pip install scrapy-redis
pip install selenium
pip install pymongo
pip install Pillow
pip install pymysql
pip install redis
// celery 安装的包
pip install celery
pip install msgpack
pip install eventlet
// websocket
pip install websocket-client
// 验证码 tesseract-ocr
pip install pytesseract
pip install tesseract
pip install pytesser3
// 多线程
pip install threadpool
// action
pip install qqbot
pip install pyecharts
pip install echarts-countries-pypkg
pip install echarts-china-provinces-pypkg
pip install echarts-china-cities-pypkg
pip install echarts-china-counties-pypkg
pip install echarts-china-misc-pypkg
pip install numpy

// 或者加入到requirement.txt
pip install -r requirement.txt
```

#### scrapy使用
```
// 新建一个scrapy爬虫项目
scrapy startproject tutoria (tutoria为爬虫名称)

// 开启爬虫
scrapy crawl dahe (dahe为爬虫名称)
```

#### 安装selenium支持的chromedriver
```
// 下载地址有两个
http://chromedriver.storage.googleapis.com/index.html
https://npm.taobao.org/mirrors/chromedriver/
// 首先需要查看你的Chrome版本，在浏览器中输入
chrome://version/
// 获取版本后找到对应的目录
// 我的下载地址是
https://registry.npmmirror.com/-/binary/chromedriver/96.0.4664.45/chromedriver_win32.zip
// 解压压缩包，找到chromedriver.exe复制到chrome的安装目录（其实也可以随便放一个文件夹）。复制chromedriver.exe文件的路径并加入到电脑的环境变量中去。
```

未配置环境也可以，例如：
```
from selenium import webdriver
import time

def main():
    chrome_driver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'  #chromedriver的文件位置
    b = webdriver.Chrome(executable_path = chrome_driver)
    b.get('https://www.google.com')
    time.sleep(5)
    b.quit()

if __name__ == '__main__':
    main()
```

已配置环境变量时，例如：
```
from selenium import webdriver
import time

def main():
    b = webdriver.Chrome()
    b.get('https://www.baidu.com')
    time.sleep(5)
    b.quit()

if __name__ == '__main__':
    main()
```

tesseract-ocr安装：
```
http://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-setup-3.05.00dev.exe


(python2)安装完毕后打开目录 site-packages\pytesseract 下的文件 pytesseract.py
找到 tesseract_cmd = 'tesseract' 修改成你安装地址

tesseract_cmd = r'D:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

(python3)
pip install pytesser3
找到pytesser3下的 __init__.py 修改
tesseract_exe_name = 'D:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe' 

设置环境变量
path = D:\Program Files (x86)\Tesseract-OCR
TESSDATA_PREFIX = D:\Program Files (x86)\Tesseract-OCR\tessdata

 如果碰到GBK编码无法识别的问题，解决该问题的方法是util.py中的retrieve_text函数中的open函数添加一个encoding参数。


def retrieve_text(scratch_text_name_root):
    inf = open(scratch_text_name_root + '.txt', encoding='utf-8')
    text = inf.read()
    inf.close()
    return text
```

#### pyecharts
```
pip install pyecharts
pip install echarts-countries-pypkg
pip install echarts-china-provinces-pypkg
pip install echarts-china-cities-pypkg
pip install echarts-china-counties-pypkg
pip install echarts-china-misc-pypkg
```

[pyecharts官网地址](https://pyecharts.org/#/zh-cn/intro)  - [pyecharts示例地址](https://github.com/pyecharts/pyecharts-gallery)


[当当购买地址](http://product.dangdang.com/27931341.html)

第一篇  基础知识

第1章　Python环境搭建
- 1.1  Python的安装 2
- 1.1.1  Windows下Python的安装 2
- 1.1.2  Mac OS X下Python的安装 3
- 1.1.3  Linux下Python的安装 3
- 1.1.4  安装pip工具 4
- 1.2  虚拟环境Virtualenv 5
- 1.2.1  Virtualenv的安装 5
- 1.2.2  创建虚拟环境 5
- 1.2.3  激活虚拟环境 5
- 1.2.4  创建指定Python版本的虚拟环境 5
- 1.3  选择合适的编辑器 6
- 1.3.1  Vim 6
- 1.3.2  Atom 6
- 1.3.3  Sublime Text 6
- 1.3.4  Notepad 6
- 1.3.5  Pycharm 6

第2章　常用爬虫库Requests

- 2.1  安装Requests 7
- 2.1.1  用pip安装 7
- 2.1.2  用github源码安装 7
- 2.1.3  用curl安装 7
- 2.2  了解 Requests的功能 8
- 2.2.1  使用GET和POST发送请求 8
- 2.2.2  通过URL传递参数 9
- 2.2.3  设置超时 9
- 2.2.4  查看返回内容 9
- 2.2.5  设置请求头 10
- 2.2.6  更多复杂的Post请求 10
- 2.2.7  返回对象状态码 12
- 2.2.8  设置代理IP 13
- 2.3  BeautifulSoup的安装和使用 14
- 2.3.1  使用pip安装BeautifulSoup 14
- 2.3.2  使用BeautifulSoup定位元素 14
- 2.4  初识自动化测试工具Selenium 15
- 2.4.1  Selenium安装 15
- 2.4.2  使用Selnium爬取网站 15
- 2.5  Selenium定位元素 16
- 2.5.1  通过属性定位 17
- 2.5.2  通过xpath定位 17
- 2.6  Selenium反爬设置 18
- 2.6.1  设置请求头 18
- 2.6.2  设置代理IP 19

第3章　常用爬虫框架Scrapy

- 3.1  认识Scrapy 21
- 3.1.1  Scrapy爬取quotes简单示例 21
- 3.1.2  安装所需依赖包 23
- 3.1.3  使用虚拟环境 23
- 3.2  Scrapy shell的使用 24
- 3.2.1  运行shell 24
- 3.2.2  使用Scrapy shell爬取Scrapy.org 24
- 3.2.3  爬虫调用shell 26
- 3.3  使用Scrapy爬取quotes 26
- 3.3.1  创建Scrapy项目并新建爬虫 27
- 3.3.2  爬取和提取数据 27
- 3.3.3  通过脚本运行Scrapy爬虫 29
- 3.3.4  在同一进程下运行多个爬虫 29
- 3.3.5  简易的分布式爬虫思路 30
- 3.3.6  防止爬虫被ban 31
- 3.4  setting基本配置 31
- 3.5  Pipeline模块 32
- 3.5.1  爬取文字板块 32
- 3.5.2  编写Pipeline模块 35
- 3.5.3  通过Pipeline将数据写入MongoDB数据库 36
- 3.5.4  ImagesPipeline处理图片 37
- 3.5.5  FilePipeline下载文件 40
- 3.6  Middleware中间件 41
- 3.6.1  Downloader Middleware 41
- 3.6.2  随机请求头中间件 42
- 3.6.3  更换代理IP中间件 45
- 3.6.4  通过Downloader Middleware使用Selenium 46
- 3.6.5  Spider Middleware 47
- 3.7  新功能拓展 48
- 3.7.1 信号signals 48
- 3.7.2  自定义拓展 51

第4章　数据存储——数据库的选择

- 4.1  MySQL数据库 53
- 4.1.1  MySQL的安装 53
- 4.1.2  几款可视化工具 54
- 4.1.3  数据库连接 55
- 4.1.4  数据库插入操作 55
- 4.1.5  数据库查询 56
- 4.1.6  数据库更新操作 56
- 4.1.7  爬取写入数据库 57
- 4.2  MongoDB数据库 58
- 4.2.1  MongoDB安装 58
- 4.2.2  连接数据库 59
- 4.2.3  查询数据库 59
- 4.2.4  插入和更新数据库 59
- 4.2.5  爬取数据并插入到MongoDB数据库中 60
- 4.3  Redis数据库 60
- 4.3.1  Redis安装 60
- 4.3.2  连接Redis数据库 61
- 4.3.3  Python操作Redis数据库 61
- 4.3.4  爬取并写入Redis做缓存 62

第5章　效率为王——分布式爬虫

- 5.1  什么是分布式爬虫 64
- 5.1.1  分布式爬虫的效率 64
- 5.1.2  实现分布式的方法 64
- 5.2  Celery 65
- 5.2.1  Celery入门 65
- 5.2.2  Celery分布式爬虫 66
- 5.3 使用Scrapy-redis的分布式爬虫 67
- 5.3.1  Scrapy-redis安装与入门 67
- 5.3.2  创建Scrapy-redis爬虫项目 68

第6章　抓包的使用与分析

- 6.1  利用抓包分析目标网站 72
- 6.1.1  如何抓包 72
- 6.1.2  网页抓包分析 72
- 6.2  手机APP抓包 74
- 6.2.1  使用fiddler抓包 75
- 6.2.2  HTTPS证书安装 75
- 6.2.3  booking手机端抓包 76

第7章　Websocket通信网站爬取

- 7.1  什么是Websocket 79
- 7.1.1  Websocket-clinet 79
- 7.1.2  Websocket-clinet简单入门 79
- 7.2  使用Websocket爬取财经网站 81

第8章　验证码破解

- 8.1  关于验证码 84
- 8.1.1  一般的验证码 84
- 8.1.2  极验验证 84
- 8.2  极验滑动验证破解 85
- 8.2.1  准备工具 85
- 8.2.2  分析滑动验证码 85
- 8.2.3  开始破解极限滑动验证码 87
- 8.3  图片验证码破解 89
- 8.3.1  准备工具 89
- 8.3.2  文字图像识别 89
- 8.3.3  识别验证码 90

第9章　多线程与多进程并发爬取

- 9.1  多线程 92
- 9.1.1  堵塞与非堵塞 92
- 9.1.2  继承threading.Thread创建类 96
- 9.1.3  多线程的锁 98
- 9.1.4  queue队列 100
- 9.1.5  线程池 101
- 9.2  多线程爬虫 103
- 9.2.1  爬虫框架 103
- 9.2.2  编写爬虫 104
- 9.2.3  以多线程方式启动 105
- 9.3  多进程 107
- 9.3.1  multiprocessing模块 107
- 9.3.2  通过Pool进程池创建进程 108
- 9.3.3  multiprocessing.Queue队列 109
- 9.3.4  multiprocessing.Pipe管道 112
- 9.3.5  multiprocessing.Lock锁 113
- 9.4  多进程爬虫 114
- 9.4.1  多进程爬取音频 114
- 9.4.2  多进程加多线程进行爬取 116

第10章　爬虫接口优化

- 10.1  Gunicorn的安装与使用 119
- 10.2  Gunicorn配置 121
- 10.2.1  配置参数 121
- 10.2.2  通过config文件启动 123

第11章　使用Docker部署爬虫

- 11.1  Docker 125
- 11.1.1  Docker的安装 125
- 11.1.2  Docker的镜像 125
- 11.1.3  构建自己的Docker镜像 127
- 11.1.4  容器使用 127
- 11.1.5  Dockerfile 129
- 11.2  爬虫部署 130
- 11.2.1  爬虫接口 130
- 11.2.2  部署爬虫接口 131

第二篇  实战案例

第12章　实战1：建立代理IP池

- 12.1  爬取免费代理IP 136
- 12.1.1  爬取代理IP 136
- 12.1.2  检验代理IP 138
- 12.2  建立代理IP池 138
- 12.2.1  检验代理IP 138
- 12.2.2  Redis消息队列 140
- 12.2.3  master爬虫 142

第13章　实战2：磁力链接搜索器

- 13.1  爬取磁力搜索平台 145
- 13.1.1  磁力平台 145
- 13.1.2  slave爬虫 146
- 13.2  实现磁力搜索器 148
- 13.2.1  展示与交互 148
- 13.2.2  数据查询 150

第14章　实战3：爬虫管家

- 14.1  QQ机器人 152
- 14.1.1  qqbot 152
- 14.1.2  基本操作 152
- 14.1.3  实现自己的机器人 153
- 14.2  爬虫监控机器人 153

第15章　实战4：数据可视化

- 15.1  可视化包Pyecharts 156
- 15.1.1  Pyecharts的安装 156
- 15.1.2  地图展示数据 157
- 15.2  爬取价机票数据 158
- 15.2.1  破解旅游网站价格日历接口 159
- 15.2.2  爬取旅游网站 160
- 15.2.3  将数据可视化 161

第16章　实战5：爬取贴吧中的邮箱

- 16.1  爬取网站 164
- 16.1.1  爬取高校名单 164
- 16.1.2  利用正则表达式匹配号码 165
- 16.2  分析贴吧搜索页面并提取号码 165
- 16.3  使用Scrapy开始编码 167
- 16.3.1  创建贴吧Scrapy项目 167
- 16.3.2  新建爬虫并编写爬虫逻辑 168
- 16.3.3  数据处理 170

第17章　实战6：批量爬取企业信息

- 17.1  从第三方平台获取企业名 172
- 17.2  如何爬取企业详细信息 174

第18章　实战7：爬取公众号历史文章

- 18.1  分析公众号接口 177
- 18.1.1  开始抓包 177
