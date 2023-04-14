#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/11/1 20:52
@note     
"""
from werkzeug.exceptions import HTTPException
from common.api.common_result import R


class ApiException(HTTPException):

    def __init__(self, message=None):

        if message is not None:
            self.description = message
        else:
            self.description = "系统错误"

    def get_body(self, environ=None):
        return R.failedMsg(self.get_description(environ))

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

    def get_description(self, environ=None):
        return self.description

    def get_response(self, environ=None):
        return R.failedMsg(self.description)
