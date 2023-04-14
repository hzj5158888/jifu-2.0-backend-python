#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/11/27 10:42
@note     
"""
from enum import Enum


class StatusEnum(Enum):
    """
    状态类型枚举
    """

    # 开启
    OPEN = 1
    # 关闭
    CLOSE = 0

    @staticmethod
    def value_list():
        return list(map(lambda c: c.value, StatusEnum))
