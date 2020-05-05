#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari

import time
import win32api
import win32gui
import win32con
import win32clipboard


def qq_windows(title):
    handle = win32gui.FindWindow(None, title)
    win32gui.SetForegroundWindow(handle)
    time.sleep(0.5)


def set_clipboard(string):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, string)
    win32clipboard.CloseClipboard()


def send_msg(title, string):
    qq_windows(title)
    set_clipboard(string)
    time.sleep(0.5)

    # 粘贴 Ctrl + V
    win32api.keybd_event(17, 0, 0, 0)
    win32api.keybd_event(86, 0, 0, 0)
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)

    # 发送 Ctrl + Enter
    win32api.keybd_event(17, 0, 0, 0)
    win32api.keybd_event(13, 0, 0, 0)
    win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)


if __name__ == '__main__':
    title = 'xx聊天群'
    msg = 'test'
    send_msg(title, msg)
