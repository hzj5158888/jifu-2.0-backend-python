#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/11/3 19:38
@note     
"""
from datetime import datetime

from application_initializer import db
from common.utils.model_to_dict import model_to_dict


@model_to_dict
class PowerUserInfo(db.Model):
    __tablename__ = 'power_user_info'

    id = db.Column(db.BigInteger, primary_key=True)
    account = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255))
    salt = db.Column(db.String(255), nullable=False)
    nick_name = db.Column(db.String(255), nullable=False)
    real_name = db.Column(db.String(255))
    avatar_url = db.Column(db.String(255), nullable=False)
    sex = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    birthday = db.Column(db.DateTime)
    status = db.Column(db.Integer, default=1)
    gmt_create = db.Column(db.DateTime, default=datetime.now)
    gmt_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

