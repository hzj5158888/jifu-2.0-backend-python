#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/11/1 19:51
@note     
"""
from common.api.common_result import R
from config.exception.api_exception import ApiException



def register_error(app):

    @app.errorhandler(Exception)
    def internal_server_error(e):
        if isinstance(e, ApiException):
            return R.failedMsg(e.description)
        print(repr(e))
        return R.failedMsg(repr(e))

    @app.errorhandler(404)
    def internal_server_error(e):
        return R.validateFailed()

    @app.teardown_request
    def exceptionDbRollback(exception):
        from application_initializer import db
        if exception:
            db.session.rollback()
        db.session.remove()
