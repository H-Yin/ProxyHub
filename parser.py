#!/opt/anaconda3/bin/python
#-*- coding=utf-8 -*-

##################################################################
#  File        : parser.py
#  Author      : H.Yin
#  Email       : csustyinhao@gmail.com
#  Created     : 2019-04-17 22:29:52(+0800)
#  Modified    : 2020-05-17 01:13:08(+0800)
#  GitHub      : https://github.com/H-Yin/ProxyHub
#  Description : A parser that can parser HTML to get IPs
#################################################################

import sys
import time
import requests
from lxml import etree

from logger import logger
from config import PARSER

ParserList=[
    "parse_kuaidaili",
    "parse_shenjidaili",
    "parse_qydaili",
    "parse_superfastip",
    "parse_89ip",
    "parse_data5u",
    "parse_31f"
]

class Parser(object):
    _in_queue = None 
    def __init__(self, q=None):
        if _in_queue is None and q is not None:
            _in_queue = q

        assert _in_queue is not None

    def parse_kuaidaili(self, num=5):
        items = []
        target = ['inha', 'intr']
        for target_id in range(len(target)):
            for page_id in range(1, num+1):
                response = requests.get("https://www.kuaidaili.com/free/%s/%d/" % (target[target_id], page_id))
                if response.status_code != 200:
                    logger.error("download kuaidaili page <%s,%d> failed.(status_code:%d)" % (
                        target[target_id], page_id, response.status_code))
                    break
                html = etree.HTML(response.text)
                trs = html.xpath('//*[@id="list"]/table/tbody/tr')
                for tr in trs:
                    item = {}
                    tds = tr.xpath('td')
                    item['ip'] = tds[0].text.strip()                # IP
                    item['port'] = tds[1].text.strip()              # Port
                    item['http_type'] = tds[3].text.strip()         # HTTP or HTTPS
                    items.append(item)
                time.sleep(1)
        logger.info("get %d IPs from kuaidaili." % len(items))
        return items

    def parse_shenjidaili(self):
        items = []
        response = requests.get("http://www.shenjidaili.com/open/")
        if response.status_code == 200:
            html = etree.HTML(response.text)
            trs_http = html.xpath('//*[@id="pills-stable_http"]/table/tr')[1:]
            trs_https = html.xpath('//*[@id="pills-stable_https"]/table/tr')[1:]
            trs = trs_http + trs_https
            for tr in trs:
                item = {}
                tds = tr.xpath('td')
                item['ip'] = tds[0].text.strip().split(":")[0]  # IP
                item['port'] = tds[1].text.strip()              # Port
                item['http_type'] = tds[3].text.strip()         # HTTP or HTTPS
                items.append(item)
        else:
            logger.error("download shenjidaili page failed.(status_code:%d)" % response.status_code)
        logger.info("get %d IPs from shenjidaili." % len(items))
        return items

    def parse_qydaili(self, num = 10):
        items = []
        for page_id in range(1, num+1):
            response = requests.get("http://www.qydaili.com/free/?action=china&page=%d" % page_id)
            if response.status_code != 200:
                logger.error("download qydaili page <%d> failed.(status_code:%d)" % (page_id, response.status_code))
                break
            html = etree.HTML(response.text)
            trs = html.xpath('//table/tbody/tr')
            for tr in trs:
                item = {}
                tds = tr.xpath('td')
                item['ip'] = tds[0].text.strip()                # IP
                item['port'] = tds[1].text.strip()              # Port
                item['http_type'] = tds[3].text.strip()         # HTTP or HTTPS
                items.append(item)
            time.sleep(1)
        logger.info("get %d IPs from qydaili." % len(items))
        return items

    def parse_superfastip(self, num = 10):
        items = []
        for page_id in range(1, num+1):
            response = requests.get("http://www.superfastip.com/welcome/freeip/%d" % page_id)
            if response.status_code != 200:
                logger.error("download superfastip page <%d> failed.(status_code:%d)" % (page_id,response.status_code))
                break
            html = etree.HTML(response.text)
            trs = html.xpath('//table/tbody/tr')
            for tr in trs:
                item = {}
                tds = tr.xpath('td')
                item['ip'] = tds[0].text.strip()                # IP
                item['port'] = tds[1].text.strip()              # Port
                item['http_type'] = tds[3].text.strip()         # HTTP or HTTPS
                items.append(item)
            time.sleep(1)
        logger.info("get %d IPs from superfastip." % len(items))
        return items

    def parse_89ip(self, num=18):
        items = []
        for page_id in range(1, num+1):
            response = requests.get("http://www.89ip.cn/index_%d.html" % page_id)
            if response.status_code != 200:
                logger.error("download 89ip page <%d> failed.(status_code:%d)" % (page_id,response.status_code))
                break
            html = etree.HTML(response.text)
            trs = html.xpath('//table/tbody/tr')
            for tr in trs:
                item = {}
                tds = tr.xpath('td')
                item['ip'] = tds[0].text.strip()        # IP
                item['port'] = tds[1].text.strip()      # Port
                item['http_type'] = ''                  # HTTP or HTTPS
                items.append(item)
            time.sleep(1)
        logger.info("get %d IPs from 89ip." % len(items))
        return items

    def parse_data5u(self):
        target = ['', '/gngn','/gnpt','/gwgn','/gwpt']
        header = {
            'Host': 'www.data5u.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        base_url = "http://www.data5u.com/free%s/index.shtml"
        items = []
        for page_id in range(len(target)):
            response = requests.get(base_url % target[page_id], headers = header)
            # print(response.text)
            if response.status_code != 200:
                logger.error("download data5u page <%s> failed.(status_code:%d)" % (target[page_id],response.status_code))
                break
            html = etree.HTML(response.text)
            trs = html.xpath('//ul[@class="l2"]')
            for tr in trs:
                item = {}
                tds = tr.xpath('span/li')
                item['ip'] = tds[0].text.strip()                # IP
                item['port'] = tds[1].text.strip()              # Port
                item['http_type'] = tds[3].text.strip()         # HTTP or HTTPS
                items.append(item)
            time.sleep(1)
        logger.info("get %d IPs from data5u." % len(items))
        return items

    ''' 521 问题需要绕过 js 
    def parse_66ip(self, num=5):
        items = []
        for page_id in range(1, num+1):
            response = requests.get("http://www.66ip.cn/%d.html" % page_id)
            if response.status_code != 200:
                logger.error("download 66ip page <%d> failed.(status_code:%d)" % (page_id, response.status_code))
                break
            html = etree.HTML(response.text)
            trs = html.xpath('//table/tr')
            for tr in trs:
                item = {}
                tds = tr.xpath('td')
                item['ip'] = tds[0].text.strip()        # IP
                item['port'] = tds[1].text.strip()      # Port
                item['http_type'] = ''                  # HTTP or HTTPS
                items.append(item)
            time.sleep(1)
        logger.info("get %d IPs from 66ip." % len(items))
        return items
    '''

    def parse_31f(self):
        target = ['http-proxy/', 'https-proxy/']
        base_url = "http://31f.cn/%s"
        items = []
        for page_id in range(len(target)):
            response = requests.get(base_url % target[page_id])
            if response.status_code != 200:
                logger.error("download 66ip page <%s> failed.(status_code:%d)" % (target[page_id], response.status_code))
                break
            html = etree.HTML(response.text)
            trs = html.xpath('//table[1]/tr')
            for tr in trs[1:]:
                item = {}
                tds = tr.xpath('td')
                item['ip'] = tds[1].text.strip()                # IP
                item['port'] = tds[2].text.strip()              # Port
                item['http_type'] = 'http' if page_id == 0 else 'https' # HTTP or HTTPS
                items.append(item)
            time.sleep(1)
        logger.info("get %d IPs from 31f." % len(items))
        return items

    def parse(self):
        items = []
        items.extend(self.parse_kuaidaili())
        items.extend(self.parse_shenjidaili())
        items.extend(self.parse_qydaili())
        items.extend(self.parse_superfastip())
        items.extend(self.parse_89ip())
        items.extend(self.parse_data5u())
        items.extend(self.parse_31f())
        return items
    
if __name__ == '__main__':
    parser = Parser()
    res = parser.parse_kuaidaili()
    print(res)
