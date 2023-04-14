#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/10/29 19:55
@note     http状态码枚举
"""

from enum import Enum


class ResultCodeEnum(Enum):

    SUCCESS_CODE = 200
    SUCCESS_MESSAGE = "操作成功"

    FAILED_CODE = 500
    FAILED_MESSAGE = "操作失败"

    VALIDATE_FAILED_CODE = 404
    VALIDATE_FAILED_MESSAGE = "参数检验失败"

    UNAUTHORIZED_CODE = 401
    UNAUTHORIZED_MESSAGE = "暂未登录或token已经过期"

    FORBIDDEN_CODE = 403
    FORBIDDEN_MESSAGE = "没有相关权限"



