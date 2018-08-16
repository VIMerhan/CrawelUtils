import urllib.request
import builtwith
import simplejson as json
import time
import random
import requests
import threadpool
from threadpool import ThreadPool, makeRequests

from db_utils import mongoutil
import crawel_utils.agency as agency
import threading


class Maoyan(object):
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
    url = ''
    db_name = '猫眼数据分析'
    set_name = ''
    movie_id = 0
    page_size = 1000
    thread_max = 20
    sleep_time = 1
    proxies = ()

    def __init__(self, movie_id, page_size, thread_max, proxy=None, is_sleep=None):
        self.url = self.url
        self.db_name = self.db_name
        self.set_name = str(movie_id)
        self.movie_id = str(movie_id)
        self.page_size = page_size
        self.thread_max = thread_max
        self.sleep_time = self.sleep_time
        self.proxies = proxy

    def request_method(self, url, user_agent=random.choice(USER_AGENT_LIST), num_retries=2, proxies=None):
        headers = {'User-agent': user_agent}
        try:
            print('Downloading', url)
            response = requests.get(url, headers=headers, proxies=proxies)
            html = str(response.content, 'utf-8')

        except requests.exceptions.ConnectionError as e:
            print('Download error:', e.errno)
            html = None
            if num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    return self.request_method(url, num_retries - 1)

        return html

    def urllib_method(self, url, user_agent=None, num_retries=2, proxies=None):
        # 默认从user_agent池中随机获取
        if user_agent is None:
            user_agent = random.choice(Maoyan.USER_AGENT_LIST)

        headers = {'User-agent': user_agent}

        # 生成一个request，用于加header和各种query
        request = urllib.request.Request(url, headers=headers)

        proxy = urllib.request.ProxyHandler(proxies)
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
                    return self.urllib_method(request, num_retries - 1)
        return html

    def get_built(self, url):
        return builtwith.parse(url)

    def parse_ono_page(self, html):
        data = json.loads(html)['cmts']
        for item in data:
            # 迭代返回一个字典
            yield {
                'date': item['time'].split(' ')[0],
                'nickname': item['nickName'],
                'city': item['cityName'],
                'rate': item['score'],
                'comment': item['content'],
            }

    # 保存数据到文本文档
    def save_to_txt(self):
        for i in range(1, 1001):
            url = 'http://m.maoyan.com/mmdb/comments/movie/' + self.movie_id + '.json?_v_=yes&offset=' + str(i)
            html = self.request_method(url, proxies=self.proxies)
            print('正在保存第%d页.' % i)
            for item in self.parse_ono_page(html):
                with open('影评数据.txt', 'a', encoding='utf-8') as f:
                    f.write(
                        item['date'] + ',' + item['nickname'] + ',' + item['city'] + ',' + str(item['rate']) + ',' +
                        item['comment'] + '\n')
            # 反爬
            # time.sleep(5 + float(random.randint(1, 100)) / 20)

    # 保存数据到Mongodb
    def save_to_mongo(self, start=0, end=0):
        for i in range(start, end):
            url = 'http://m.maoyan.com/mmdb/comments/movie/' + self.movie_id + '.json?_v_=yes&offset=' + str(i)
            html = self.urllib_method(url, proxies=self.proxies)
            print('正在保存第%d页.' % i)
            set = mongoutil.get_collection(self.db_name, self.set_name)

            doc = self.parse_ono_page(html)
            set.insert(doc)
            # 休眠反爬
            # time.sleep(5 + float(random.randint(1, 100)) / 20)

    def get_args_list(self):
        # 生成器，生成thread_max个参数列表
        def generate_arg():
            ratio = self.page_size // self.thread_max
            for i in range(0, self.thread_max):
                yield [i * ratio + 1, (i + 1) * ratio]

        x = []
        for i in generate_arg():
            # x的元素是元组
            x.append((i, None))
        return x

    def serial_thread_download(self, func, *args, **kwargs):
        start_time = time.time()
        func()
        print('%d second' % (time.time() - start_time))

    def multi_thread_download(self, func, *args, **kwargs):
        list_args = self.get_args_list()

        start_time = time.time()
        pool = threadpool.ThreadPool(num_workers=self.thread_max)

        requests = threadpool.makeRequests(func, list_args)
        [pool.putRequest(req) for req in requests]
        pool.wait()
        print('%d second' % (time.time() - start_time))


def test_yield():
    print('ok')
    data = [1,2,3,4,5]
    print(data)
    for item in data:
        print(item)
        x = 10
        yield {
            'date': item
        }

if __name__ == '__main__':
    maoyan = Maoyan(movie_id=1175253, page_size=40, thread_max=1, proxy=None)

    # maoyan.multi_thread_download(func=maoyan.save_to_mongo)
    x=[]
    for i in range(0,5):
        x.append(test_yield())
        print(x)

