import sublime
import sublime_plugin

from .ipaddress.IpAddress import IpAddress


def insert(view, edit, ip):
    if ip is None:
        sublime.error_message("Unable to retrieve IP address")
        return

    for region in view.sel():
        if not region.empty():
            view.replace(edit, region, ip)
        else:
            view.insert(edit, region.begin(), ip)


def set_clipboard(ip):
    if ip is None:
        sublime.error_message("Unable to retrieve IP address")
        return

    sublime.set_clipboard(ip)
    sublime.status_message("IP address {0} was copied to clipboard".format(ip))


class InsertIpAddressCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        insert(self.view, edit, IpAddress.instance().get('ipv4'))


class InsertIpv6AddressCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        insert(self.view, edit, IpAddress.instance().get('ipv6'))


class SetClipboardIpAddressCommand(sublime_plugin.WindowCommand):
    def run(self):
        set_clipboard(IpAddress.instance().get('ipv4'))


class SetClipboardIpv6AddressCommand(sublime_plugin.WindowCommand):
    def run(self):
        set_clipboard(IpAddress.instance().get('ipv6'))


class RefreshIpAddressCommand(sublime_plugin.WindowCommand):
    def run(self):
        ipv4 = IpAddress.instance().get('ipv4', True)
        ipv6 = IpAddress.instance().get('ipv6', True)

        if ipv4 is None and ipv6 is None:
            sublime.error_message("Unable to retrieve IP address")
        else:
            sublime.status_message(
                "IP address was refreshed: {0}".format(ipv4)
            )
