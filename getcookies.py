# coding:utf-8

# anthor： NingAnMe
# email：ninganme0317@gmail.com

"""
使用selenium模拟登录获取cookies，
手动填验证码，
增加不同的网站，只需要继承WeiboCookies,
然后重写login方法就可以了，
基本适用于所有网站。
"""

from selenium import webdriver

import time

try:
    import cPickle
except:
    import pickle as cPickle


class WeiboCookies(object):
    def __init__(self, url, driver, username, password):
        # 如果使用phantomJS浏览器，将下面几行的注释去掉
        # dcap = dict(DesiredCapabilities.PHANTOMJS)
        # dcap["phantomjs.page.settingsc.userAgent"] = (
        # "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36\
        # (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
        # )
        """
        :param url:网站的登录地址
        :param driver:一个初始化的selenium实例
        :param username:用户名
        :param password:密码
        """
        self.url = url
        self.driver = driver
        self.username = username
        self.password = password

    def _open_url(self):
        """打开登录页面并且判断是否正常打开
        """
        self.driver.get(self.url)

    def _is_open(self, element):
        """判断是否存在某个元素，代表页面正常打开
        :param element:网页中的一个元素，Xpath写法
        """
        if element is not None:
            return
        else:
            print '页面还没有打开，请等待2秒'
            time.sleep(2)

    def login(self):
        """登录网站，不同的网站需要重写这个方法
        """
        time.sleep(2)
        username = self.driver.find_element_by_xpath(
            '//input[@id="loginName"]')
        password = self.driver.find_element_by_xpath(
            '//input[@id="loginPassword"]')
        login = self.driver.find_element_by_xpath(
            '//a[@id="loginAction"]')

        self._is_open(login)

        username.clear()
        username.send_keys(self.username)

        password.clear()
        password.send_keys(self.password)

        time.sleep(1)
        login.click()
        time.sleep(12)

    def store_cookies(self):
        """将获取到的cookies储存到本地
        """
        self._open_url()

        self.login()

        cookies = self.driver.get_cookies()

        with open('cookie.txt', 'wb') as f:
            cPickle.dump(cookies, f)
            print '成功储存cookies'

        self.driver.close()


class DoubanCookies(WeiboCookies):
    def login(self):
        """登录网站，不同的网站需要重写这个方法
        """
        time.sleep(1)
        username = self.driver.find_element_by_xpath(
            '//input[@id="form_email"]')
        password = self.driver.find_element_by_xpath(
            '//input[@id="form_password"]')
        remember = self.driver.find_element_by_xpath(
            '//input[@id="form_remember"]')

        username.clear()
        username.send_keys(self.username)

        password.clear()
        password.send_keys(self.password)

        remember.click()

        time.sleep(5)
        self.driver.find_element_by_xpath(
            '//input[@class="bn-submit"]').click()

        time.sleep(5)


def choose_site(*args, **keys):
    """网站分发，初始化对应的实例
    """
    sites = {'weibo': WeiboCookies, 'douban': DoubanCookies, }
    cls = sites[site](*args)
    return cls

def main():
    if len(site) > 0 and len(url) > 0 and len(username) > 0 and password > 0:
        # 默认使用Chrome驱动
        driver = webdriver.Chrome()
        
        gc = choose_site(url, driver, username, password, site=site)
        gc.store_cookies()

    else:
        print '请检查输入项是否填写正确！'

if __name__ == '__main__':
    # 获取哪个网站的cookies，豆瓣
    site = 'douban'  # 'weibo', 'douban'

    # 登录页面
    url = 'https://www.douban.com/'
    #url = 'https://passport.weibo.cn/signin/login?entry=mweibo'

    # 账号
    username = ''
    # 密码
    password = ''

    main()
