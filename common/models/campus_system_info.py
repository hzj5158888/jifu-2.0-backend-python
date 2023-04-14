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
class CampusSystemInfo(db.Model):
    __tablename__ = 'campus_system_info'

    id = db.Column(db.BigInteger, primary_key=True)
    campus_id = db.Column(db.ForeignKey('campus_info.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    report_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    report_content = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    apply_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    apply_content = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    report_student_size = db.Column(db.Integer, nullable=False)
    report_teacher_size = db.Column(db.Integer, nullable=False)
    student_report_basic = db.Column(db.Float(32, True), nullable=False, server_default=db.FetchedValue())
    teacher_report_basic = db.Column(db.Float(32, True), nullable=False, server_default=db.FetchedValue())
    gmt_create = db.Column(db.DateTime, default=datetime.now)
    gmt_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    campus = db.relationship('CampusInfo', primaryjoin='CampusSystemInfo.campus_id == CampusInfo.id', backref='campus_system_infos')
