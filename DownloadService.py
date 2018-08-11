import urllib.request
import builtwith
import simplejson as json
import time
import random
import requests
from Db import mongoutil
import agency


USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
]

def request_method(url, user_agent=None, num_retries=2, proxies=None):
    # request方法
    ip, port = ("'http://110.73.2.182", "8123")
    proxy_url = "{0}:{1}".format(ip, port)

    print(proxy_url)

    proxy_dict = {
        "http": proxy_url
    }

    try:
        print('Downloading', url)
        response = requests.get(url, proxies=proxy_dict)
        html = str(response.content, 'gbk')

    except requests.HTTPError as e:
        print('Download error', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return request_method(url, num_retries - 1)

    return html

def urllib_method(url, user_agent, num_retries=2, proxies=None):
    # 默认从user_agent池中随机获取
    if user_agent is None:
        user_agent = random.choice(USER_AGENT_LIST)

    headers = {'User-agent': user_agent}

    # 生成一个request，用于加header和各种query
    request = urllib.request.Request(url, headers=headers)

    proxy = urllib.request.ProxyHandler({'http': 'http://115.219.104.191:8010'})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)

    try:
        print('Downloading', url)
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")

    except urllib.request.URLError as e:
        print('Download error', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return urllib_method(request, num_retries - 1)
    return html


def get_built(url):
    return builtwith.parse(url)


def parse_ono_page(html):
    data = json.loads(html)['cmts']  # 评论以json形式存储,故以json形式截取
    for item in data:
        # 该方法返回一个字典
        yield {
            'date': item['time'].split(' ')[0],
            'nickname': item['nickName'],
            'city': item['cityName'],
            'rate': item['score'],
            'comment': item['content'],
        }


# 保存数据到文本文档
def save_to_txt():
    for i in range(1, 1001):
        url = 'http://m.maoyan.com/mmdb/comments/movie/1175253.json?_v_=yes&offset=' + str(i)
        html = urllib_method(url)
        print('正在保存第%d页.' % i)
        for item in parse_ono_page(html):
            with open('影评数据.txt', 'a', encoding='utf-8') as f:
                f.write(
                    item['date'] + ',' + item['nickname'] + ',' + item['city'] + ',' + str(item['rate']) + ',' +
                    item['comment'] + '\n')
        # 反爬
        time.sleep(5 + float(random.randint(1, 100)) / 20)


# 保存数据到Mongodb
def save_to_mongo():
    for i in range(1, 1001):
        url = 'http://m.maoyan.com/mmdb/comments/movie/1175253.json?_v_=yes&offset=' + str(i)
        html = urllib_method(url)
        print('正在保存第%d页.' % i)
        m = mongoutil.MongoUtil()
        c = m.get_collection()

        diction = parse_ono_page(html)
        c.insert(diction)
        # 反爬
        time.sleep(5 + float(random.randint(1, 100)) / 20)


if __name__ == '__main__':

    proxies = agency.get_random_ip(agency.get_ip_list())

    print(proxies)
    url = 'http://www.baidu.com'

    # request_method(url)


    # save_to_txt()
    # save_to_mongo()

