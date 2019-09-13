import sublime
import sublime_plugin

from .ipaddress.IpAddress import IpAddress


class InsertIpAddressCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        ip = IpAddress.instance().get()

        if ip is None:
            sublime.error_message("Unable to retrieve IP address")
            return

        for region in self.view.sel():
            if not region.empty():
                self.view.replace(edit, region, ip)
            else:
                self.view.insert(edit, region.begin(), ip)


class RefreshIpAddressCommand(sublime_plugin.WindowCommand):
    def run(self):
        ip = IpAddress.instance().get(True)

        if ip is None:
            sublime.error_message("Unable to retrieve IP address")
        else:
            sublime.status_message("IP address was refreshed: {0}".format(ip))


class SetClipboardIpAddressCommand(sublime_plugin.WindowCommand):
    def run(self):
        ip = IpAddress.instance().get()

        if ip is None:
            sublime.error_message("Unable to retrieve IP address")
        else:
            sublime.set_clipboard(ip)
            sublime.status_message(
                "IP address {0} was copied to clipboard".format(ip)
            )
