"""
滑动验证码破解，未试验过
"""

import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image
import random

# 这个函数是计算本次需要移动的水平距离
def get_distance(image1, image2):
    threshold = 90                                  # 可以从50开始尝试，这里说明90是因为成功率最高
    left = 57                                       # 左边第一个拼图结束的位置
    for i in range(left, image1.size[0]):           # left为x轴开始的点，image1.size[0]则为图片x轴上的终点，即图片宽度
        for j in range(image1.size[1]):             # image1.size[1]为图片的高度，由低到高进行遍历
            # i, j就是一个不断地以左上角为中心向右下角变化的坐标范围
            rgb1 = image1.load()[i, j]              # 获取图1限定范围的RGB
            rgb2 = image2.load()[i, j]              # 获取图2限定范围RGB
            res1 = abs(rgb1[0] - rgb2[0])           # 对比两图R之间差距，数值越大颜色差距越大
            res2 = abs(rgb1[1] - rgb2[1])           # 对比两图G之间差距，数值越大颜色差距越大
            res3 = abs(rgb1[2] - rgb2[2])           # 对比两图B之间差距，数值越大颜色差距越大
            
            if not (res1 < threshold and res2 < threshold and res3 < threshold):    # 当RGB大于这个标准的时候，代表出现缺口
                print(i)
                print((res1, res2, res3))
                return i - 7  # 经过测试，误差大概为7
    print(i)
    return i - 7 # 经过测试，误差大概为7

# 返回每次移动的滑块的速率，不能太快了，否则会被反作弊监测出来
def get_track(length):
    list = []
    # 间隔通过随机范围函数来获得，每次移动一步或者两步
    x = random.randint(1, 3)
    # 生成轨迹并保存到list内
    while length - x >= 5:
        list.append(x)
        length = length - x
        x = random.randint(1, 3)
    # 最后五步都是一步步移动
    for i in range(length):
        list.append(1)
    return list

# 对网页截图
def get_snap():
    """
        对整个网页截图，保存成图片，然后用PIL.Image拿到图片对象
    :return 图片对象
    """
    driver.save_screenshot('E:/snap.png')
    return Image.open('E:/snap.png')

# 将除验证码外的其他的部分去掉
def get_image():
    """
        从网页的网站截图，截图验证码图片
    :return 验证码图片
    """    
    img = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'bg-img')))
    time.sleep(2)   # 保证图片刷新出来
    localtion = img.location
    size = img.size
    top = localtion['y']
    bottom = top + size['height']
    left = localtion['x']
    right = left + size['width']
    page_snap_obj = get_snap()
    crop_imag_obj = page_snap_obj.crop((left, top, right, bottom))
    # crop_imag_obj.show()
    return crop_imag_obj
    
try:
    driver = webdriver.Chrome()
    driver.get('https://account.geetest.com/login')                 # 打开登录界面
    wait = WebDriverWait(driver, 10)                                # 等待10秒
    # 点击按钮弹出验证码图片
    button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_radar_tip')))   # 等待直到出现指定元素
    button.click()
    # 拿到没有缺口的图片
    image1 = get_image()
    driver.save_screenshot('E:/snap1.png')
    # 点击滑动条滑出有缺口的图片
    button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_slider_button')))
    button.click()
    # 拿到有缺口的图片
    image2 = get_image()
    # 对比两张图的RGB，找到不一样的地方，获得距离
    distance = get_distance(image1, image2)
    # 把需要拖送的总距离分成一段段小的轨迹
    tracks = get_track(distance)
    print(tracks)
    print(image1.size)
    print(distance, sum(tracks))
    
    # 按照轨迹拖动，完成验证
    button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_slider_button')))
    ActionChains(driver).click_and_hold(button).perform()
    for track in tracks:
        ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()
    time.sleep(0.5) # 0.5秒后释放鼠标
    ActionChains(driver).release().perform()
    # 完成登录
    input_email = driver.find_element_by_id('email')
    input_password = driver.find_element_by_id('password')
    button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-btn')))
    input_email.send_keys('你的帐号')
    input_password.send_keys('你的密码')
    # button.send_keys(Keys.ENTER)
    button.click()
finally:
    driver.close()
    
    