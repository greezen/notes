"""
    功能:获取免费ip池
    作者:greezen
    日期:2018-04-17
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
import random
import os


class IpPool:

    __xicidaili_url = 'http://www.xicidaili.com/nn/'

    __cn_proxy_url = 'http://cn-proxy.com/'

    __type_xicidaili = 'xicidaili'

    __type_cn_proxy = 'cn-proxy'

    filename = 'ip_pool.csv'

    __site = ''

    def __init__(self, site='cn-proxy'):
        self.__site = site
        if site == self.__type_cn_proxy:
            self.url = self.__cn_proxy_url
        else:
            self.url = self.__xicidaili_url

    def run(self):
        """
        执行抓取
        :return:
        """
        if self.__site == self.__type_cn_proxy:
            self.spider_cn_proxy()
        elif self.__site == self.__type_xicidaili:
            max_page = self.get_max_page()
            for page in range(1, max_page+1):
                self.spider_xicidaili(page)
                print('第{}页采集完成,共{}页'.format(page, max_page))

    def spider_cn_proxy(self):
        """
        抓取 http://cn-proxy.com/ 的免费代理ip
        :return:
        """

        # 用shadowsocks代理抓取
        proxies = {"http": "socks5://127.0.0.1:1080", "https": "socks5://127.0.0.1:1080"}
        soup = self.get_html(self.url, **{'proxies': proxies})
        tr_list = soup.select('tbody tr')

        ip_pool_list = []
        ip_pool_key = ['ip', 'port', 'address']
        for tr in tr_list:
            td_list = tr.find_all('td')
            ip = td_list[0].text.strip()
            port = td_list[1].text.strip()
            address = td_list[2].string.strip()
            ip_pool_val = [ip, port, address]
            ip_item = dict(zip(ip_pool_key, ip_pool_val))
            ip_pool_list.append(ip_item)

        self.save2json('cn-proxy.json', ip_pool_list)

    def get_request_header(self):
        """
        获取http请求头
        :return:
        """
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'referer': 'https://www.taobao.com/'
        }
        return header

    def spider_xicidaili(self, page=1):
        """
        抓取数据
        :param page:
        :return:
        """
        url = self.url + str(page)
        soup = self.get_html(url, **{'proxies': self.get_proxy()})
        print(soup)
        tr_list = soup.find_all('tr', {'class': 'odd'})

        ip_list = []
        for item in tr_list:
            ip_item_key = ['ip', 'port', 'addr', 'city', 'type', 'speed', 'connect_time', 'active_time', 'check_time']

            td = item.find_all('td')
            ip = td[1].string
            port = td[2].string
            if len(td[3].find_all('a')) > 0:
                addr = td[3].a.string
                city = td[3].a['href'].split('/')[-1]
            else:
                addr = ''
                city = ''

            type = td[5].string
            speed = td[6].div['title'].strip('秒')
            connect_time = td[7].div['title'].strip('秒')
            active_time = td[8].string
            check_time = td[9].string

            # print(time.mktime(time.strptime(check_time, '%y-%m-%d %H:%M')))
            # exit()

            ip_item_val = [ip, port, addr, city, type, speed, connect_time, active_time, check_time]
            ip_item = dict(zip(ip_item_key, ip_item_val))
            ip_list.append(ip_item)

        with open(self.filename, 'a', encoding='utf-8') as f:
            writer = csv.DictWriter(f, ip_item_key)
            if page == 1:
                writer.writeheader()
            writer.writerows(ip_list)

    def get_html(self, request_url, **kwargs):
        """
        获取html
        :param request_url:
        :return:
        """

        if 'proxies' in kwargs.keys():
            proxy = kwargs['proxies']
        else:
            proxy = {}

        response = requests.get(request_url, headers=self.get_request_header(), proxies=proxy)
        soup = BeautifulSoup(response.text, 'html.parser')

        return soup

    def get_proxy(self):
        """
        获取爬虫代理配置
        :return:
        """
        proxy_file = 'cn-proxy.json'
        proxy = {}
        if os.path.exists(proxy_file):
            with open(proxy_file, 'r') as f:
                proxy_list = json.load(f)
                random_proxy = random.choice(proxy_list)

            if len(random_proxy) > 0:
                proxy = {'http': 'http://{}:{}'.format(random_proxy['ip'], random_proxy['port'])}

        return proxy

    def get_max_page(self):
        """
        获取总的页码
        :return:
        """
        url = self.url + '1'
        html = self.get_html(url)
        pagination = html.find_all('div', {'class': 'pagination'})[0]
        max_page = pagination.find_all('a')[-2].text.strip()

        return int(max_page)

    def get_pool(self):
        """
        获取ip池信息
        :return:
        """
        ip_pool = []
        with open(self.filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ip_pool.append(dict(row))
        return ip_pool

    @staticmethod
    def validate():
        """
        验证ip是否可用
        :return:
        """
        ip_pool = IpPool.get_pool()
        ip_pool_ok = []
        for item in ip_pool:
            ip = item['ip']
            port = item['port']
            proxy = {
                'http': 'http://' + ip + ':' + port
            }

            try:
                res = requests.get('http://dtest.7gwifi.cn/portal/l/t', proxies=proxy, timeout=0.5)
                html = BeautifulSoup(res.text, 'html.parser')
                if res.status_code == 200:
                    ip_pool_ok.append(item)
                    print("http://{}:{}".format(ip, port))
            except:
                pass

        with open('ip_pool_ok.json', 'w') as f:
            json.dump(ip_pool_ok, f)

    def save2csv(self, file_name, data, mode='w'):
        """
        以字典的形式保存数据到csv
        :param file_name: 文件名称
        :param data: 数据,包括header和list
        :param mode: 写入方式
        :return:
        """
        with open(file_name, mode) as f:
            writer = csv.DictWriter(f, data['header'])
            writer.writeheader()
            writer.writerows(data['list'])

    def save2json(self, file_name, data, mode='w'):
        """
        次数数据保存为json文件
        :param file_name:
        :param data:
        :param mode:
        :return:
        """
        with open(file_name, mode) as f:
            json.dump(data, f)

    @staticmethod
    def ts():
        print(IpPool.filename)


ippool = IpPool()
# ippool.spider(1)
ippool.run()