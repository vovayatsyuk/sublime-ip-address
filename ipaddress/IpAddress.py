import json
import urllib.request
import urllib.error
import re

class IpAddress(object):
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.ip = None
        self.urls = {
            'http://ipecho.net/plain': {
                'format': 'text'
            },
            'http://jsonip.com': {
                'format': 'json',
                'path'  : 'ip'
            }
        }
        self.parseRules = {
            'json': lambda data, settings: json.loads(data)[settings['path']],
            'text': lambda data, settings: data
        }
        self.ipMatcher = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

    def get(self, refresh = False):
        if (self.ip is None or refresh):
            self.ip = self.fetch()
        return self.ip

    def fetch(self):
        for server in self.urls:
            settings = self.urls[server]
            try:
                self.debug("Getting IP using {0}".format(server))
                response = urllib.request.urlopen(server).read().decode('UTF-8')
                ip = self.parseRules[settings['format']](response, settings)
            except urllib.error.URLError: # urlopen exception
                self.debug("Unable to connect to {0}".format(server))
                continue
            except UnicodeDecodeError: # decode exception
                self.debug("Unable to decode response from {0}".format(server))
                continue
            except: # parse response exception
                self.debug("Unable to parse IP from {0}".format(server))
                continue

            if not self.ipMatcher.match(ip):
                self.debug("{0} is not a valid IP address".format(ip))
                continue

            self.debug("{0} received using {1}".format(ip, server))
            return ip
        return None

    def debug(self, text):
        print('[IpAddress] ' + text)
