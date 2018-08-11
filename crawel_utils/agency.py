# coding=utf-8
# IP地址取自国内髙匿代理IP网站：http://www.xicidaili.com/nn/
# 仅仅爬取首页IP地址就足够一般使用

from bs4 import BeautifulSoup
import requests
import random

URL = 'http://www.xicidaili.com/nn/'
HEADERS = {
    'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}


def get_ip_list(url=URL, headers=HEADERS):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list


def get_random_ip():
    ip_list = get_ip_list()
    # 一行语句完成遍历赋值
    proxy_list = ['http://' + ip for ip in ip_list]
    # 随机选取ip
    proxy_ip = random.choice(proxy_list)
    proxy_dict = {'http': proxy_ip}
    return proxy_dict



if __name__ == '__main__':
    proxy_dict = get_random_ip()
    print(proxy_dict)

    # ip, port = ("http://110.73.2.182", "8123")
    # proxy_url = "{0}:{1}".format(ip, port)
    # print(proxy_url)
