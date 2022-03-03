### Python 学习案例

Python3 + Win10

```
// 安装完3.9.10后执行，安装pip

python -m ensurepip
python -m pip install --upgrade pip
```

配置国内镜像
```
// windows home目录下新建pip.ini

[global] 
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = mirrors.aliyun.com
```

常用命令
```
显示版本和路径
pip --version
 
获取帮助
pip --help
 
安装包
pip install package  #install后面跟包名，默认最新版本(后面例子都是此包名)
pip install package==0.1.9.4    #指定版本
pip install 'package>=0.1.9.4'  #最小版本  
 
升级包
pip install --upgrade package
 
卸载包
pip uninstall package
 
搜索包
pip search package
 
显示安装包信息
pip show package
 
查看指定包的详细信息
pip show -f package
 
列出已安装的包
pip list
 
查看可升级的包
pip list -o
 
报错信息记录1：
ERROR: Could not install packages due to an EnvironmentError: [WinError 5] 拒绝访问。: 'c:\\program files\\python37\\lib\\site-packages\\pip-19.2.3.dist-info\\entry_points.txt'
Consider using the `--user` option or check the permissions.
先试试：
python -m pip install -U pip
python -m pip install --upgrade pip
换源update:
python -m pip install --upgrade pip -i https://pypi.douban.com/simple
添加--user选项赋予权限：
python -m pip install --upgrade pip -i https://pypi.douban.com/simple --user
 

```

#### 1.目录介绍

| 名称 | 介绍 |
| --- | --- |
| example | 基础案例 |
| lxfbasic | 廖雪峰基础课程 |
| spider | 爬虫 |
| unicorn | 模拟ARM等引擎执行SO等文件 |
| frida | 安卓Hook技术 |
