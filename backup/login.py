import requests
import ddddocr
import time
from bs4 import BeautifulSoup
import lxml

cookies = {

}


def visit_login_page():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
    }

    try:
        response = requests.get('https://aaaa.bbbb.com/login', cookies=cookies, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')

            it = soup.find('input', {'name': 'lt'})['value']
            execution = soup.find('input', {'name': 'execution'})['value']
            rand_id = soup.find('input', {'name': 'randId'})['value']

            cookie_dic = response.cookies.get_dict()
            cookies['SESSION'] = cookie_dic.get('SESSION')
            print('SESSION = ' + cookies['SESSION'])

            return {'it': it, 'execution': execution, 'rand_id': rand_id}
        else:
            print(response.status_code)
            return None
    except Exception as e:
        print("获取界面元素发生异常：%s" % e)
    return None


# 获取验证码
def get_valid_code():
    timestamp = time.time()
    params = {
        'a': timestamp,
    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
    }

    try:
        response = requests.get('https://aaaa.bbbb.com/image', params=params, cookies=cookies, headers=headers)

        if response.status_code == 200:
            # 使用 BytesIO 将响应内容转换为字节流
            ocr = ddddocr.DdddOcr()
            var_code = ocr.classification(response.content)
            print("验证码图片：", var_code)
            return var_code
    except Exception as e:
        print("获取验证码异常".format(e))
    return None


# 登录
def submit_login(valid_code, p):
    if p is None:
        print('获取界面元素失败')
        return None

    data = {
        "lt": p['it'],
        "execution": p['execution'],
        "randId": p['rand_id'],
        "browse": "Win64;+x64;+rv:126.0)+Gecko/20100101+Firefox/126.0",
        "username": "abc",
        "password": "efg",
        "validCode": valid_code,
    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
    }

    url = "https://aaaa.bbbb.com/login"

    resp = requests.post(url=url, data=data, headers=headers, cookies=cookies)
    if resp.status_code == 200:
        cookie_dic = resp.cookies.get_dict()
        return cookie_dic.get('ABC')
    else:
        print(resp.status_code)
        return None


def login():
    # 获取session
    p = visit_login_page()
    # 破解验证码
    code = get_valid_code()
    if code is None:
        print('验证码获取错误')
        return False

    print(p)

    abc = submit_login(code, p)
    if abc is None:
        print('获取ABC错误')
        return False
    cookies['ABC'] = abc

    session_id = get_from_session_id()
    if session_id is None:
        print('获取sessionId错误')
        return False

    cookies['sessionId'] = session_id

    return True


def get_session_id(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
    }

    resp = requests.get(url, cookies=cookies, headers=headers, allow_redirects=False)
    if resp.status_code == 302:
        return resp.cookies.get_dict().get('sessionId')
    return None


def get_from_session_id():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
    }

    try:
        resp = requests.get('https://aaaa.bbbb.com/login?service=redirectURL',
                            cookies=cookies, headers=headers, allow_redirects=False)
        if resp.status_code == 200:
            return True
        elif resp.status_code == 302:
            url = resp.headers['Location']
            print(url)

            session_id = get_session_id(url)
            print("sessionId == " + session_id)
            return session_id
        else:
            print(resp.status_code)
            return None
    except Exception as e:
        print("尝试请求京东失败".format(e))
    return None


def get_shop_list():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
    }

    data = {
        "pageNo": "1",
        "pageSize": "20",
    }

    # 请求接口，需要带上cookies
    resp = requests.post("http://aaaa.bbbb.com:8888/xxxx/search", data=data, headers=headers, cookies=cookies)
    print(resp.text)


if __name__ == '__main__':
    login()
