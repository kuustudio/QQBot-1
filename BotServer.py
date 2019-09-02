#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年9月2日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: BotServer
@description: 
"""
import logging

from tornado.gen import coroutine, sleep
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define
from tornado.options import options
from tornado.web import Application

from BaseHandler import MahuaHandler, IndexHandler
import MsgHandler


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0

define('shost', default='127.0.0.1', help='PY机器人地址')
define('sport', default=65321, help='PY机器人端口')
define('ahost', default='127.0.0.1', help='接口地址')
define('aport', default=36524, help='接口端口')


class BotApplication(Application):

    def __init__(self, *args, **kwargs):  # @UnusedVariable
        handlers = [
            (r'/api/ReceiveMahuaOutput', MahuaHandler),
            (r'/.*', IndexHandler)
        ]
        settings = {'debug': False}
        super(BotApplication, self).__init__(handlers, **settings)


@coroutine
def recvMessage():
    """队列处理消息
    """
    while 1:
        nxt = sleep(0.01)
        message = yield MsgHandler.MessageInQueue.get()
        try:
            yield MsgHandler._recv_message(message)
        except Exception as e:
            logging.exception(e)
        yield nxt


@coroutine
def sendMessage():
    """队列发送消息
    """
    while 1:
        nxt = sleep(0.01)
        message, kwargs = yield MsgHandler.MessageOutQueue.get()
        try:
            yield MsgHandler._send_message(message, **kwargs)
        except Exception as e:
            logging.warn(str(e))
        yield nxt


def main():
    # 解析命令行参数
    options.parse_command_line()

    logging.info('shost: {}'.format(options.shost))
    logging.info('sport: {}'.format(options.sport))
    logging.info('ahost: {}'.format(options.ahost))
    logging.info('aport: {}'.format(options.aport))

    # 创建本地web服务
    server = HTTPServer(BotApplication())
    server.listen(options.sport, options.shost)
    loop = IOLoop.current()
    # 队列处理消息
    loop.spawn_callback(recvMessage)
    # 队列发送消息
    loop.spawn_callback(sendMessage)
    loop.start()


if __name__ == '__main__':
    main()
