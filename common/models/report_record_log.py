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
class ReportRecordLog(db.Model):
    __tablename__ = 'report_record_log'

    id = db.Column(db.BigInteger, primary_key=True)
    report_id = db.Column(db.ForeignKey('report_info.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    operator = db.Column(db.ForeignKey('campus_member.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    gmt_create = db.Column(db.DateTime, default=datetime.now)
    gmt_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    campus_member = db.relationship('CampusMember', primaryjoin='ReportRecordLog.operator == CampusMember.id', backref='report_record_logs')
    report = db.relationship('ReportInfo', primaryjoin='ReportRecordLog.report_id == ReportInfo.id', backref='report_record_logs')
