import os, requests, json, sys, re
from bs4 import BeautifulSoup

# 输出缓冲
# sys.stdout.flush()

rpText = re.compile('&[0-9]+')

url = 'https://pvp.qq.com/web201605/js/herolist.json'
herolist = requests.get(url)  # 获取英雄列表json文件
if herolist.status_code != 200:
    print("获取英雄列表失败，status_code = %s" % herolist.status_code)
    exit(0)

herolist_json = herolist.json()  # 转化为json格式

basePath = 'D:\\pictures\\wzry'
# 文件夹不存在，创建
if not os.path.exists(basePath):
    os.makedirs(basePath)
    
def downloadPic(heroName, heroNumber, skinName, skinIndex):
    print('check hero = %s, skin = %s' % (heroName, skinName))
    # 判断皮肤图片是否存在
    picName = str(heroNumber)+'-'+heroName+'-'+skinName + '.jpg'
    if not os.path.exists(basePath+'\\'+picName):
        url = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/' + str(heroNumber) + '/' + str(heroNumber) + '-bigskin-' + str(skinIndex) + '.jpg'
        print('download url = %s' % url)
        im = requests.get(url)  # 请求url
        if im.status_code == 200:
            open(basePath+'\\'+picName, 'wb').write(im.content)  # 写入文件
    else:
        print('hero = %s, skin = %s is exists' % (heroName, skinName))
        
    
print('开始比对图片信息：')

i = 0
for hero in herolist_json:
    heroDetailUrl = 'https://pvp.qq.com/web201605/herodetail/m/'+str(hero['ename'])+'.html'
    res = requests.get(heroDetailUrl)
    res.encoding='gbk'
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')
        skinNames = soup.find('a', class_='hero-skin').get('data-imgname').strip()
        skinNames = rpText.sub('', skinNames)
        print(skinNames)
        
        skinArray = skinNames.split('|')
        for idx, skinName in enumerate(skinArray):
            downloadPic(hero['cname'], hero['ename'], skinName, idx + 1)
            i += 1
    else:
        print(hero['cname']+' get skin error')
    # 刷新输出缓冲
    sys.stdout.flush()
    
    #if True:
    #    break
    """
    if ('skin_name' in hero):
        skinArray = hero['skin_name'].split('|')
        for idx, skinName in enumerate(skinArray):
            downloadPic(hero['cname'], hero['ename'], skinName, idx + 1)
            i += 1
    else:
        downloadPic(hero['cname'], hero['ename'], hero['title'], 1)
        i += 1
    """

print('总计皮肤数量：%i' % i)
