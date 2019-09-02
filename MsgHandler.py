#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年9月2日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: MsgHandler
@description: 
"""
from tornado.gen import coroutine
from tornado.queues import Queue


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0

# 待处理消息队列
MessageInQueue = Queue()
# 待发送消息队列
MessageOutQueue = Queue()


@coroutine
def _send_message(message, **kwargs):
    pass


@coroutine
def _recv_message(message, **kwargs):
    pass
