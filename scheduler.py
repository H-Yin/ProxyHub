#!/home/yinhao/anaconda3/bin/python
#-*- coding=utf-8 -*-

##################################################################
#  File        : scheduler.py
#  Author      : H.Yin
#  Email       : csustyinhao@gmail.com
#  Created     : 2019-06-01 23:23:30(+0800)
#  Modified    : 2019-06-04 18:27:30(+0800)
#  GitHub      : https://github.com/H-Yin/
#  Description : 
#################################################################

import queue as _q
import threading
import signal
import time
from operator import methodcaller

from utils.logger import logger
from parser import Parser, ParserList
from checker import Checker


class Scheduler(object):

    def __init__(self, mincount=10, maxsize=1000):
        self._in = _q.Queue(maxsize=maxsize)   # input queue
        self._out = _q.Queue(maxsize=maxsize * 0.5)  # output queue
        self._drop = _q.Queue()
        self._in_set = set()
        #create parser
        self._parser = Parser()
        #create checker
        self._checker = Checker()
        # thread status
        self._running = False
        self._min = mincount

    def run(self):
        def _parser(self):
            while self._running:
                if self._out.qsize() < self._min:
                    for x in ParserList:
                        items = methodcaller(x)(self._parser)
                        for x in items:
                            if x['ip'] not in self._in_set:
                                self._in_set.add(x['ip'])
                                self._in.put(x, True)
                time.sleep(60)

        def _checker(self, x):
            while self._running:
                try:
                    item = self._in.get(True)
                    res = self._checker.check(item['ip'], item['port'])
                    if res:
                        self._out.put(res)
                        self._in_set.remove(res['ip'])
                    else:
                        self._drop.put(res)
                except _q.Empty:
                    pass
                except KeyboardInterrupt:
                    break
        self._running = True
        # create 2 thread to get and check ip:port
        t_parser = threading.Thread(target=_parser, args=(self,))
        t_parser.start()
        for x in range(0, 5):
            t_checker = threading.Thread(target=_checker,args=(self,x))
            t_checker.start()
        # prepear
        while self._out.qsize() < 3:
            time.sleep(1)

    def stop(self, signum=None, frame=None):
        self._running = False

    def get(self):
        proxy = None
        try:
            proxy = self._out.get(False)
            self._in.put(proxy)
        except _q.Empty:
            pass
        return proxy

if __name__ =='__main__':
    s = Scheduler()
    # signal process
    # signal.signal(signal.SIGINT, s.stop)
    # signal.signal(signal.SIGHUP, s.stop)
    # signal.signal(signal.SIGTERM, s.stop)
    
    s.run()

    i = 1000
    while i > 0:
        print(s._in.qsize(), s._out.qsize())
        #print("2", s.get())
        time.sleep(1)
        i -= 1
