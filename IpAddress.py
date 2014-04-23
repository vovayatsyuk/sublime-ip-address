import sublime
import sublime_plugin
import json
import urllib.request
import urllib.error
import re

class InsertIpAddressCommand(sublime_plugin.TextCommand):
    ip = None
    urls = {
        'http://ipecho.net/plain': {
            'format': 'text'
        },
        'http://jsonip.com': {
            'format': 'json',
            'path'  : 'ip'
        }
    }
    parseRules = {
        'json': lambda data, settings: json.loads(data)[settings['path']],
        'text': lambda data, settings: data
    }
    ipMatcher = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

    def run(self, edit):
        if self.ip is None:
            for server in self.urls:
                settings = self.urls[server]
                try:
                    sublime.status_message("Getting IP using {0}".format(server))
                    response = urllib.request.urlopen(server).read().decode('UTF-8')
                    ip = self.parseRules[settings['format']](response, settings)
                except urllib.error.URLError: # urlopen exception
                    sublime.status_message(
                        "Unable to connect to {0}".format(server)
                    )
                    continue
                except UnicodeDecodeError: # decode exception
                    sublime.status_message(
                        "Unable to decode response from {0}".format(server)
                    )
                    continue
                except: # parse response exception
                    sublime.status_message(
                        "Unable to parse IP from {0}".format(server)
                    )
                    continue

                if not self.ipMatcher.match(ip):
                    sublime.status_message(
                        "{0} is not a valid IP address".format(ip)
                    )
                    continue

                InsertIpAddressCommand.ip = ip
                break;

            if self.ip is None:
                sublime.error_message("Unable to retrieve IP address")
                return

        for region in self.view.sel():
            if not region.empty():
                self.view.replace(edit, region, self.ip)
            else:
                self.view.insert(edit, region.begin(), self.ip)
