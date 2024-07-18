# coding=utf-8
# author=XingLong Pan
# date=2016-12-04

# 豆瓣电影的登录入口页面
DOUBAN_MOVIE_LOGIN_URL = 'https://accounts.douban.com/login'

# 搜索引擎（SEO爬虫）的请求头
USER_AGENT = [
        'DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)',
        'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
        'ia_archiver (+http://www.alexa.com/site/help/webmasters; crawler@alexa.com)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 11; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36'

    ]
AGENT_SIZE = 7

# 延时设置
DELAY_MIN_SECOND = 1 
DELAY_MAX_SECOND = 3

# 豆瓣电影的url前缀
URL_PREFIX = 'https://movie.douban.com/subject/'

"""
这里用到了阿布云代理动态版。使用影梭或者其他代理，甚至不用代理也可以
"""
# 代理服务器
proxyHost = "proxy.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "HT1LX50X8R4P0I8D"
proxyPass = "1133BD889583B72A"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}
