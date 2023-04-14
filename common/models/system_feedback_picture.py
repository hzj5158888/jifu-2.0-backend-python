#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@time:2021/02/01/14:52
@author:WYY
@content:
"""
from datetime import datetime
from application_initializer import db
from common.utils.model_to_dict import model_to_dict


@model_to_dict
class SystemFeedbackPicture(db.Model):
    __tablename__ = 'system_feedback_picture'

    id = db.Column(db.BigInteger, primary_key=True)
    system_feedback_id = db.Column(db.ForeignKey('system_feedback.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    img_url = db.Column(db.String(255), nullable=False)
    gmt_create = db.Column(db.DateTime, default=datetime.now)
    gmt_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    SystemFeedback = db.relationship('SystemFeedback', primaryjoin='SystemFeedbackPicture.system_feedback_id == SystemFeedback.id', backref='system_feedback_pictures')

