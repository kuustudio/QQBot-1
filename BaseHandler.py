#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年9月2日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: BaseHandler
@description: 
"""
import json
import logging

from tornado.escape import to_basestring
from tornado.gen import coroutine
from tornado.web import RequestHandler

import MsgHandler


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0


class DottedDict(dict):
    # 用于实现通过.方式直接访问字典中的数据

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError("'{}'".format(attr))

    __setattr__ = dict.__setitem__

    __delattr__ = dict.__delitem__


class IndexHandler(RequestHandler):

    @coroutine
    def get(self, *args, **kwargs):  # @UnusedVariable
        self.finish({'msg': 'ok'})


class MahuaHandler(RequestHandler):

    def prepare(self):
        super(MahuaHandler, self).prepare()
        if self.request.body:
            try:
                self._data = json.loads(
                    to_basestring(self.request.body), object_hook=DottedDict)
            except Exception as e:
                logging.exception(e)
        else:
            self._data = DottedDict()

    @coroutine
    def post(self, *args, **kwargs):  # @UnusedVariable
        print(self._data)
        # 把消息放入队列
        yield MsgHandler.MessageInQueue.put(self._data)
        self.finish({'msg': 'ok'})
