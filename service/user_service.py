#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/11/28 10:49
@note     
"""

from flask_jwt_extended import get_jwt, jwt_required

class UserService:

    @staticmethod
    @jwt_required()
    def isMember():
        """
        通过jwt判断当前用户是否为职员
        @return:
        """
        return get_jwt()["is_member"]
