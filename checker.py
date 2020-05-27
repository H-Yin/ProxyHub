#!/opt/anaconda3/bin/python
#-*- coding=utf-8 -*-

##################################################################
#  File        : checker.py
#  Author      : H.Yin
#  Email       : csustyinhao@gmail.com
#  Created     : 2019-04-24 16:39:40(+0800)
#  Modified    : 2020-05-17 01:16:43(+0800)
#  GitHub      : https://github.com/H-Yin/ProxyHub.git
#  Description : Build a checker that can check wether the ip:port
#                is valid or not.
#################################################################


import re
import time
import requests
from lxml import etree

from logger import logger
from config import CHECKER 

HTTP_TYPE = {
    'HTTP':1,
    'HTTPS':2,
    'HTTP,HTTPS':3
}

class Checker(object):
    def __init__(self):
        pass
    
    def _check_ip(self, ip):
        ip_regex='^((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)$'
        return re.match(ip_regex, ip) is not None
        
    def _check_port(self, port):
        flag = True
        try:
            temp = int(port)
            if temp < 0 or temp > 65535:
                flag = False
        except ValueError:
            logger.error("%s is not a valid port." % srt(port) )
            flag = False
        return flag
    
    def check(self, ip, port, retry=1, timeout=3):
        retry_count = 0
        while retry_count < retry:
            http_type = 0
            if self._check_ip(ip) and self._check_port(port):
                # check http
                try:
                    proxies = {"http" : "http://%s:%s" % (ip, port)}
                    res = requests.get('http://www.httpbin.org/headers', proxies=proxies, timeout=timeout)
                    if res.ok:
                        http_type |= 1
                except:
                    logger.error("<http://%s:%s> is not available." % (ip, str(port)))
                # check https
                try:
                    proxies = {"https" : "https://%s:%s" % (ip, port)}
                    requests.get('http://www.httpbin.org/headers', proxies=proxies, timeout=timeout)
                    if res.ok:
                        http_type |= 2
                except:
                    logger.error("<https://%s:%s> is not available." % (ip,str(port)))
            else:
                logger.error("%s:%s is error." % (ip, port))
            if http_type > 0:
                return {'ip':ip, 'port':port, 'http_type': http_type}
            retry_count += 1
        return None

    def get_address():
        pass

if __name__ == '__main__':
    checker = Checker()
    print(checker.check('112.87.70.208', 9999))
