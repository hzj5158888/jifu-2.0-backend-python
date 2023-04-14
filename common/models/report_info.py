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
class ReportInfo(db.Model):
    __tablename__ = 'report_info'

    id = db.Column(db.BigInteger, primary_key=True)
    campus_id = db.Column(db.ForeignKey('campus_info.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.ForeignKey('power_user_info.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    student_num = db.Column(db.String(255), nullable=False)
    class_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    unable_reason = db.Column(db.Text)
    evaluate = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    gmt_create = db.Column(db.DateTime, default=datetime.now)
    gmt_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    campus = db.relationship('CampusInfo', primaryjoin='ReportInfo.campus_id == CampusInfo.id', backref='report_infos')
    user = db.relationship('PowerUserInfo', primaryjoin='ReportInfo.user_id == PowerUserInfo.id', backref='report_infos')

