#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/11/3 19:39
@note     
"""
from datetime import datetime

from application_initializer import db

from common.utils.model_to_dict import model_to_dict


@model_to_dict
class SystemFeedback(db.Model):
    __tablename__ = 'system_feedback'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.ForeignKey('power_user_info.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    contact = db.Column(db.String(255))
    gmt_create = db.Column(db.DateTime, default=datetime.now)
    gmt_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    user = db.relationship('PowerUserInfo', primaryjoin='SystemFeedback.user_id == PowerUserInfo.id', backref='system_feedbacks')
