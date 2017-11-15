# getcookies

使用selenium模拟登录，获取网站的cookies，手动过验证，大部分网站通用

完成m.weibo.cn和www.douban.com的登录

如果增加更多的网站登录，继承WeiboCookie类，重写login方法，
然后在分发函数的字典内填写对应的信息就可以了。

# 开发环境

Ubuntu 16.04

Python2

selenium  3.7.0

Chrome：60.0.3112.90（正式版本） （64 位）

