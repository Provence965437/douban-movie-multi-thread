# coding=utf-8
# author=XingLong Pan
# date=2016-11-07

import random
import requests
import configparser
import constants
from login import CookiesHelper
from page_parser import MovieParser
from utils import Utils
from storage import DbHelper
import time
import threading

proxy_pool=[]
cookies = None
start_id=None
end_id = None
user=None
password=None
open_proxy=None
proxy_id=None
proxy_pass=None
thread_num=None
def init():
    config = configparser.ConfigParser()
    config.read('config.ini')
    user = config['douban']['user'],
    password = config['douban']['password']

    cookie_helper = CookiesHelper.CookiesHelper(
        user,
        password
    )
    cookies = cookie_helper.get_cookies()
    print(cookies)

    # 读取抓取配置
    start_id = int(config['common']['start_id'])
    end_id = int(config['common']['end_id'])
    # 是否多线程抓取
    thread_num = int(config['common']['thread_num'])
    open_proxy = bool(config['proxy']['open_proxy']) 
    proxy_id = config['proxy']['id'] 
    proxy_pass = config['proxy']['pass'] 
    # 读取配置文件信息
    user = config['douban']['user'],
    password = config['douban']['password']

    return cookies, start_id, end_id, user, password, thread_num, open_proxy, proxy_id, proxy_pass
#获取ip池，程序开始时统一填充ip池，未做多线程互斥，不要二次调用
def get_proxy_pool(id, psw, proxy_num):
    proxy_pool.clear();
    api_url = "http://www.zdopen.com/ShortProxy/GetIP/?api=" + id + "&akey=" + psw + "&count=" + str(proxy_num) + "&fitter=2&timespan=2&tunnel=1&type=3"
    try:
      proxy_ip = requests.get(api_url).json()['data']['proxy_list']
      print(proxy_ip)
      print(api_url)
      for i in range(proxy_num):
        proxy_pool.append(proxy_ip[i]['ip'] + ":" + str(proxy_ip[i]['port'])) 
      print(proxy_pool)
    except Exception as e:
      print(f"pool错误：{e},等待一段时间重试")
      time.sleep(5)

#获取单个ip，某线程单独使用
def get_proxy_single(id, psw, thread_index):
    try:
      api_url = "http://www.zdopen.com/ShortProxy/GetIP/?api=" + id + "&akey=" + psw + "&count=1&fitter=2&timespan=6&tunnel=1&type=3"
      res = requests.get(api_url, timeout=5)
      proxy_ip = res.json()['data']['proxy_list']
      proxy_pool[thread_index]= proxy_ip[0]['ip'] + ":" + str(proxy_ip[0]['port'])
      print(f"线程{thread_index}使用新地址：{proxy_pool[thread_index]}")
    except Exception as e:
      print(f"single错误：{res.json()},等待一段时间重试")
      time.sleep(5)

def run1(thread_index):
    proxyMeta=''
    # 获取模拟登录后的cookies
    cookie_helper = CookiesHelper.CookiesHelper(
        user,
        password
    )
    cookies = cookie_helper.get_cookies()
    print(cookies)

    # 实例化爬虫类和数据库连接工具类
    movie_parser = MovieParser.MovieParser()
    db_helper = DbHelper.DbHelper()

    previous_time = time.time()
    start_id_thread = (int)(start_id + thread_index*(end_id - start_id) / thread_num)
    end_id_thread = (int)(start_id_thread + (end_id - start_id) / thread_num)
    
    header_index = 0; 
    # 通过ID进行遍历
    i = start_id_thread
    total = end_id_thread - start_id_thread
    while i < end_id_thread:
        current_time = time.time()
        interval_time = current_time - previous_time

        #headers = {'User-Agent': constants.USER_AGENT[thread_index%len(constants.USER_AGENT)]}
        headers = {'User-Agent': constants.USER_AGENT[header_index]}
        if open_proxy:
             proxyMeta = proxy_pool[thread_index] 
             proxies = {
               "http": proxyMeta,
               "https": proxyMeta,
             }
        print(f"线程:{thread_index}|运行时间: {interval_time:.4f} 秒|当前douban_id:{i}|代理ip：{proxyMeta}|进度{((i - start_id_thread) / total):.2f}%")
        # 获取豆瓣页面(API)数据
        try:
            r = requests.get(
               constants.URL_PREFIX + str(i),
               headers=headers,
               cookies=cookies,
               proxies=proxies,
               timeout = 6)
        except Exception as e:
           print(f"get错误：可能是由于地址过期了。{thread_index}尝试获取新代理")
           get_proxy_single(proxy_id, proxy_pass, thread_index)
           continue
        r.encoding = 'utf-8'

        # 提取豆瓣数据
        movie_parser.set_html_doc(r.text)
        movie = movie_parser.extract_movie_info()

        # 如果获取的数据为空，延时以减轻对目标服务器的压力,并跳过。
        if not movie:
            Utils.Utils.delay(1, 2)
            i+=1
            continue
        # ip失效，需要刷新地址池
        if not movie['title']:
           if movie_parser.is_ip_forbid():
               print(f"ip寄了，线程{thread_index}获取新代理")
               get_proxy_single(proxy_id, proxy_pass, thread_index)
           else: 
               print(f"ip应该还没寄，更换一下header")
               header_index = (header_index + 1) % len(constants.USER_AGENT)
               i+=1
           continue

        # 豆瓣数据有效，写入数据库
        movie['douban_id'] = str(i)
        if movie:
            db_helper.insert_movie(movie)
        i += 1
        Utils.Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)
        
    # 释放资源
    db_helper.close_db()

threads = []
if __name__ == '__main__':
    print("开始抓取\n")
    cookies, start_id, end_id, user, password, thread_num, open_proxy, proxy_id, proxy_pass = init()
    if(open_proxy): 
    	get_proxy_pool(proxy_id, proxy_pass, thread_num)
    #init()
    for i in range(thread_num):
        print(f"thread:{i}開始運行")
        thread = threading.Thread(target=run1, args=(i,))
        threads.append(thread)
    # 启动线程
    for thread in threads:
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()
        print(f"{thread.name} has exited")
