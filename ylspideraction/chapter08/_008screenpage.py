"""
截图测试
"""

import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image
import random

# 对网页截图
def get_snap():
    """
        对整个网页截图，保存成图片，然后用PIL.Image拿到图片对象
    :return 图片对象
    """
    driver.save_screenshot('E:/snap.png')
    return Image.open('E:/snap.png')

try:
    driver = webdriver.Chrome()
    driver.get('https://www.bilibili.com/')                 # 打开登录界面
    wait = WebDriverWait(driver, 10)                                          # 等待10秒
    # 截取图片
    get_snap()
finally:
    time.sleep(10)
    driver.close()
    