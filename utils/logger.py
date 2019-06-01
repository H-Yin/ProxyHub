#!/opt/anaconda3/bin/python
#-*- coding=utf-8 -*-

##################################################################
#  File        : logger.py
#  Author      : H.Yin
#  Email       : csustyinhao@gmail.com
#  Created     : 2019-04-17 17:16:16(+0800)
#  Modified    : 2019-04-17 17:19:45(+0800)
#  GitHub      : https://github.com/H-Yin/ProxyHub
#  Description : setup a logger that can output to stream and file
#################################################################

import logging
import sys

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FORMAT = "%(asctime)s %(levelname)s %(filename)s:%(funcName)s:%(lineno)d %(message)s"
FORMAT = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    # StreamHandler
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(level=logging.DEBUG)
    logger.addHandler(stream_handler)
    # FileHandler
    file_handler = logging.FileHandler('proxyhub.log')
    file_handler.setLevel(level=logging.INFO)
    file_handler.setFormatter(FORMAT)
    logger.addHandler(file_handler)

if __name__ == "__main__":
    logger.debug("This is the 1st test!")
    logger.info("This is the 2nd test!")
    logger.error("This is the 3rd test!")
