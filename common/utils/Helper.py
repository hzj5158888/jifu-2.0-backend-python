#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/11/24 19:39
@note     工具类
"""


import random
from common.models.campus_system_info import CampusSystemInfo
import datetime
from common.models.report_info import ReportInfo
from common.models.campus_member import CampusMember
from common.enums.report_types_enum import ReportTypes


def getCurrentDate(formatted="%Y-%m-%d %H:%M:%S"):
    """
    返回格式化时间
    @param formatted: 时间格式化表达式
    @return 格式化的当前时间
    """
    return datetime.datetime.now().strftime(formatted)

def randomStr(len):
    digits = '0123456789'
    ascii_letters = 'abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    str_list = [random.choice(digits + ascii_letters) for i in range(len)]
    res = ''.join(str_list)
    
    return res
