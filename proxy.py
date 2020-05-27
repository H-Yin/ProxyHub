#!/home/yinhao/anaconda3/bin/python
#-*- coding=utf-8 -*-

##################################################################
#  File        : proxy.py
#  Author      : H.Yin
#  Email       : csustyinhao@gmail.com
#  Created     : 2020-05-16 01:49:52(+0800)
#  Modified    : 2020-05-16 17:52:07(+0800)
#  GitHub      : https://github.com/H-Yin/
#  Description : 
#################################################################

import json
from lxml import etree, html
import requests
import urllib3
urllib3.disable_warnings()

from config import PROXY_ZDAYE as conf


PROXY_URL='https://www.zdaye.com/FreeIPList.html'
TEST_URL='http://www.baidu.com/'

HEADER={
    'Host': 'www.zdaye.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.zdaye.com/',
    'Connection': 'close',
    'Upgrade-Insecure-Requests': '1',
}

cert_file ='/etc/ssl/certs/ca-bundle.crt'

def get_proxy_list(proxy=None):
    proxy_list = []
    try:
        top_page = requests.get(conf['baseURL'] + "/dayProxy.html", 
                proxies=proxy, verify=False, timeout=30, headers=HEADER)
        if top_page.ok:
            top_page_dom = etree.HTML(top_page.content)
            sub_page_url = top_page_dom.xpath(conf['xpath']['top'])[0]
            sub_page = requests.get(conf['baseURL'] + sub_page_url, 
                    verify=False, timeout=30, headers=HEADER)
            if sub_page.ok:
                sub_page_dom = etree.HTML(sub_page.content)
                ip_list = sub_page_dom.xpath(conf['xpath']['sub'])
                proxy_list = [ip.split("@")[0].split(":") for ip in ip_list]
                proxy_list = [(ip, int(port)) for ip, port in proxy_list]
            else:
                print(sub_page.statu_code)
        else:
            print(top_page.status_code)
    except Exception as ex:
        print(ex)
    return proxy_list

def make_proxies(ip, port):
    return {
        "http": "http://%s:%s" % (ip, str(port)),
        "https": "http://%s:%s" % (ip, str(port)),
    }

def verify_proxy(ip, port):
    try:
        res = requests.get(conf['testURL'], proxies=make_proxies(ip, port), timeout=30)
        if res.ok:
            res = json.loads(res.content)
            print(res)
            return True
        else:
            return False
    except Exception as ex:
        print(ex)

        return False

if __name__ == '__main__':
    '''
    218.60.8.99:3129
    182.108.45.238:1624
    125.126.111.251:60004
    111.202.247.50:8080
    125.126.109.80:60004
    125.126.98.3:60004
    118.181.226.166:44640
    111.47.154.34:53281
    46.101.215.222:8118
    '''
    #ip, port='46.101.215.222', 8118
    ip, port ='125.126.109.80', 60004
    verify_proxy(ip, port)
    proxy_list = get_proxy_list(proxy=make_proxies(ip, port))
    for ip,port in proxy_list:
        verify_proxy(ip, port)
        break
