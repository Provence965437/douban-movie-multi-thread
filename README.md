# 豆瓣电影爬虫

　　fork自https://github.com/panxl6/douban-movie

基于以上项目添加了一些修改：
- 支持多线程抓取
- 接入站大爷代理
- 优化爬虫信息打印
- 容错处理保证成功率
- 添加了电影封面链接的获取

本文在关注以上问题的基础上重新设计豆瓣爬虫程序。

## 原理
基本的抓取原理和fork项目并无二致，只是添加了多线程实现。
线程数量在配置文件中设置。
维护一个代理ip数组，每个线程只访问自己的数组，避免多线程冲突。
## 注意的问题
1.代理ip会过期，过期调用接口自动重新获取
2.ip会被豆瓣封禁，封禁之后也自动获取
3.获取的页面也可能不能正常识别，原因和header有关，会尝试更换header
# TODO:
- [ ] 目前在显示上依然有优化空间，显示的清楚是为了方便发现爬虫中遇到的bug
- [ ] 不开代理会有bug，目前未处理

# 使用说明
默认设置
- 测试用的账号密码
- 默认为csv方式存储，存储路径为程序当前路径
- 默认遍历方式为id遍历
- 安装依赖：`pip3 install -r requirements.txt`

![演示](./doc/running.png)

# 数据库设计
很明显，项目中的数据库设计是不符合数据库范式的。为了上手容易，一切从简。

# 法律义务
该爬虫仅为个人研究。如有商业用途请与豆瓣联系或参考相关法律约束。
