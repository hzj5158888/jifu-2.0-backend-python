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
class ReportPicture(db.Model):
    __tablename__ = 'report_picture'

    id = db.Column(db.BigInteger, primary_key=True)
    report_id = db.Column(db.ForeignKey('report_info.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    img_url = db.Column(db.String(255), nullable=False)
    gmt_create = db.Column(db.DateTime, default=datetime.now)
    gmt_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    report = db.relationship('ReportInfo', primaryjoin='ReportPicture.report_id == ReportInfo.id', backref='report_pictures')
