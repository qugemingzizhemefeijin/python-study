from selenium import webdriver
import time

def main():
    chrome_driver = 'D:\Program Files (x86)\chrome\chromedriver.exe'  #chromedriver的文件位置
    b = webdriver.Chrome(executable_path = chrome_driver)
    b.get('https://www.baidu.com')
    time.sleep(5)
    b.quit()

if __name__ == '__main__':
    main()