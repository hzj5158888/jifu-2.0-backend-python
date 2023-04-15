#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/10/29 20:39
@note     jwt配置 文档地址: https://flask-jwt-extended.readthedocs.io/en/latest
"""

from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token

from common.api.common_result import R
import datetime


def init_jwt(application):
    for key, value in jwt_config_map.items():
        application.config[key] = value

    jwt = JWTManager(application)
    jwt.invalid_token_loader(invalid_token_handler)
    jwt.unauthorized_loader(invalid_token_handler)
    jwt.expired_token_loader(invalid_token_handler)


def invalid_token_handler(invalidMsg):
    return R.unauthorized()


jwt_config_map = {
    # jwt加解密密钥
    "JWT_SECRET_KEY": "4xp5AU9lOvurRPAAkDerbt8VO2KkLW2Jmylz5k6C",
    # 是否开启黑名单
    "JWT_BLACKLIST_ENABLED": False,
    # 设置过期时间
    "JWT_ACCESS_TOKEN_EXPIRES": datetime.timedelta(days=30),
    # jwt头部位置
    "JWT_TOKEN_LOCATION": ['headers']
}
