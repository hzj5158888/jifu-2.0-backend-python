#!/usr/bin/env python
# coding: utf-8
"""
Api异常断言异常 用于抛出程序内部执行发生的业务错误
@author   ChenDehua 2020/11/1 19:48
@note     
"""
from config.exception.api_exception import ApiException


class Assert:

    @staticmethod
    def fail(message=None):
        raise ApiException(message)
