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
class ReportGroup(db.Model):
    __tablename__ = 'report_group'

    id = db.Column(db.BigInteger, primary_key=True)
    report_id = db.Column(db.ForeignKey('report_info.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    member_id = db.Column(db.ForeignKey('campus_member.id', ondelete=None, onupdate='CASCADE'), nullable=False, index=True)
    role = db.Column(db.Integer, nullable=False)
    gmt_create = db.Column(db.DateTime, default=datetime.now)
    gmt_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    member = db.relationship('CampusMember', primaryjoin='ReportGroup.member_id == CampusMember.id', backref='report_groups')
    report = db.relationship('ReportInfo', primaryjoin='ReportGroup.report_id == ReportInfo.id', backref='report_groups')
