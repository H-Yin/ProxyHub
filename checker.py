#!/opt/anaconda3/bin/python
#-*- coding=utf-8 -*-

##################################################################
#  File        : checker.py
#  Author      : H.Yin
#  Email       : csustyinhao@gmail.com
#  Created     : 2019-04-24 16:39:40(+0800)
#  Modified    : 2019-04-24 16:41:57(+0800)
#  GitHub      : https://github.com/H-Yin/ProxyHub.git
#  Description : Build a checher that can check wether the ip:port
#                is valid or not.
#################################################################


import re
import time
import requests
from lxml import etree

from utils.logger import logger

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
    
    def check(self, ip, port, timeout=5):
        http_type = 0
        if self._check_ip(ip) and self._check_port(port):
            try:
                proxies = {"http" : "http://%s:%d" % (ip, port)}
                res = requests.get('http://www.httpbin.org/headers', proxies=proxies, timeout=timeout)
                if res.ok:
                    http_type |= 1
            except:
                logger.error("<http://%s:%d> is not available." % (ip,port))
            try:
                proxies = {"https" : "https://%s:%d" % (ip, port)}
                requests.get('http://www.httpbin.org/headers', proxies=proxies, timeout=timeout)
                if res.ok:
                    http_type |= 2
            except:
                logger.error("<https://%s:%d> is not available." % (ip,port))
        
        if http_type > 0:
            return (ip, port, http_type)
        return None

    def get_address():
        pass
if __name__ == '__main__':
    checker = Checker()
    print(checker.check('118.24.61.165', 8118))