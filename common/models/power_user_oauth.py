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
class PowerUserOauth(db.Model):
    __tablename__ = 'power_user_oauth'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.ForeignKey('power_user_info.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    openid = db.Column(db.String(255), nullable=False)
    access_token = db.Column(db.String(255))
    refresh_token = db.Column(db.String(255))
    type = db.Column(db.String(255), nullable=False)
    gmt_create = db.Column(db.DateTime, default=datetime.now)
    gmt_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    user = db.relationship('PowerUserInfo', primaryjoin='PowerUserOauth.user_id == PowerUserInfo.id', backref='power_user_oauths')
