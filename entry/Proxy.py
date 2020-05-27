import re
import requests

class Proxy(self):
    regexp = re.compile('^((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)$'
    def __init__(self, ip, port, max_retry_num=5):
        assert ip is not None and type(ip) == str
        assert port is not None and type(port) == int
        #
        if regexp.match(ip) and 0< port < 65535:
            self._ip = ip
            self._port = int(str(port))
            self._retry_num = 0
            self._ha = False

    def isHighlyAnonymous(self):
        self._ha = False
        return self._ha

    def __str__(self):
        return "$s:%d" % (self._ip, self._port)
