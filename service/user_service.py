#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/11/28 10:49
@note     
"""
from flask_jwt_extended import get_jwt_claims


class UserService:

    @staticmethod
    def isMember():
        """
        通过jwt判断当前用户是否为职员
        @return:
        """
        return get_jwt_claims()["is_member"]
