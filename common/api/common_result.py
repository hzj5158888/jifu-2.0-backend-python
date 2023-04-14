#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/10/29 19:41
@note     api通用返回结果
"""

from flask import jsonify
from common.api.result_code_enum import ResultCodeEnum


class R(object):

    resp = {'code': 200, 'msg': "操作成功", 'data': {}}

    def __init__(self, code, message, data):
        self.resp['code'] = code
        self.resp['msg'] = message
        self.resp['data'] = data

    @staticmethod
    def success(message=None):
        """
        返回成功结果
        @return: json结果
        """
        if message is None:
            return jsonify(R(ResultCodeEnum.SUCCESS_CODE.value, ResultCodeEnum.SUCCESS_MESSAGE.value, None).get())
        else:
            return jsonify(R(ResultCodeEnum.SUCCESS_CODE.value, ResultCodeEnum.SUCCESS_MESSAGE.value, message).get())

    @staticmethod
    def successData(data=None, **meta_data):
        """
        返回成功结果
        @param data: 承载数据(meta_data:name="xxx",pwd=56486....../data:接收其他类型的数据)
        @return:  json结果
        """
        if data and meta_data:
            resp = data.update(meta_data)
        else:
            if data:
                resp = data
            else:
                resp = meta_data

        return jsonify(R(ResultCodeEnum.SUCCESS_CODE.value, ResultCodeEnum.SUCCESS_MESSAGE.value, resp).get())

    @staticmethod
    def failed():
        """
        返回失败结果
        @return:json结果
        """
        return jsonify(R(ResultCodeEnum.FAILED_CODE.value, ResultCodeEnum.FAILED_MESSAGE.value, None).get())

    @staticmethod
    def failedMsg(failed_message):
        """
        返回失败结果
        @param failed_message: 承载信息
        @return:json结果
        """
        return jsonify(R(ResultCodeEnum.FAILED_CODE.value, failed_message, None).get())

    @staticmethod
    def validateFailed():
        """
        参数验证失败返回结果
        @return:json结果
        """
        return jsonify(
            R(ResultCodeEnum.VALIDATE_FAILED_CODE.value, ResultCodeEnum.VALIDATE_FAILED_MESSAGE.value, None).get())

    @staticmethod
    def validateFailedMsg(failed_message):
        """
        参数验证失败返回结果
        @param failed_message: 承载信息
        @return:json结果
        """
        return jsonify(R(ResultCodeEnum.VALIDATE_FAILED_CODE.value, failed_message, None).get())

    @staticmethod
    def unauthorized():
        """
        未登录返回结果
        @return:json结果
        """
        return jsonify(
            R(ResultCodeEnum.UNAUTHORIZED_CODE.value, ResultCodeEnum.UNAUTHORIZED_MESSAGE.value, None).get())

    @staticmethod
    def forbidden():
        """
        未授权返回结果
        @return:json结果
        """
        return jsonify(R(ResultCodeEnum.FORBIDDEN_CODE.value, ResultCodeEnum.FORBIDDEN_MESSAGE.value, None).get())

    def get(self):
        return self.resp
