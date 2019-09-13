import json
import urllib.request
import urllib.error


class IpAddress(object):
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.ip = {
            'ipv4': None,
            'ipv6': None
        }
        self.urls = {
            'ipv4': {
                'https://ipecho.net/plain': {
                    'format': 'text'
                },
                'https://ipv4.jsonip.com/': {
                    'format': 'json',
                    'path': 'ip'
                }
            },
            'ipv6': {
                'https://ipv6.jsonip.com/': {
                    'format': 'json',
                    'path': 'ip'
                }
            }
        }
        self.parseRules = {
            'json': lambda data, settings: json.loads(data)[settings['path']],
            'text': lambda data, settings: data
        }

    def get(self, version='ipv4', refresh=False):
        if version not in self.urls:
            return None

        if (self.ip[version] is None or refresh):
            self.ip[version] = self.fetch(version)
        return self.ip[version]

    def fetch(self, version='ipv4'):
        for server in self.urls[version]:
            settings = self.urls[version][server]
            try:
                self.debug("Getting IP using {0}".format(server))
                response = (
                    urllib.request.urlopen(server).read().decode('UTF-8')
                )
                ip = self.parseRules[settings['format']](response, settings)
            except urllib.error.URLError:
                self.debug("Unable to connect to {0}".format(server))
                continue
            except UnicodeDecodeError:
                self.debug("Unable to decode response from {0}".format(server))
                continue
            except Exception:
                self.debug("Unable to parse IP from {0}".format(server))
                continue

            self.debug("{0} received using {1}".format(ip, server))
            return ip
        return None

    def debug(self, text):
        print('[IpAddress] ' + text)
