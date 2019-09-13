# Sublime Ip Address

Get your external IPv4 and IPv6 addresses directly inside SublimeText editor.

## Installation

 1. Click _Tools > Command Pallette_
 2. Call "Package Control: Install Package" command
 3. Find and Install `IpAddress` plugin

## Usage

 1. Click _Tools > Command Pallette_ (<kbd>Cmd+Shift+P</kbd> / <kbd>Ctrl+Shift+P</kbd>)
 2. Type "Ip Address" and use one of available commands:

    -  Insert IPv4
    -  Insert IPv6
    -  Copy IPv4 to clipboard
    -  Copy IPv6 to clipboard
    -  Refresh IP

## Keyboard Shortcuts

 1. Click _Preferences > Key Bindings_
 2. Add the following line into your keymap file:

    ```
    { "keys": ["ctrl+alt+i", "ctrl+alt+p"], "command": "insert_ip_address" }
    ```

    Available command names:

    ```
    insert_ip_address
    insert_ipv6_address
    set_clipboard_ip_address
    set_clipboard_ipv6_address
    refresh_ip_address
    ```
