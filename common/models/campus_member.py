#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/11/3 19:37
@note     
"""
from datetime import datetime

from application_initializer import db
from common.utils.model_to_dict import model_to_dict
# 确保可以获取到CampusDeptInfo.campus_members
from common.models.campus_dept_info import CampusDeptInfo

@model_to_dict
class CampusMember(db.Model):
    __tablename__ = 'campus_member'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.ForeignKey('power_user_info.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    campus_id = db.Column(db.ForeignKey('campus_info.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    dept_id = db.Column(db.ForeignKey('campus_dept_info.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    class_name = db.Column(db.String(255), nullable=False)
    merits = db.Column(db.Float(32, True), nullable=False)
    position = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    gmt_create = db.Column(db.DateTime, default=datetime.now)
    gmt_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    campus = db.relationship('CampusInfo', primaryjoin='CampusMember.campus_id == CampusInfo.id', backref='campus_members')
    dept = db.relationship('CampusDeptInfo', primaryjoin='CampusMember.dept_id == CampusDeptInfo.id', backref='campus_members')
    user = db.relationship('PowerUserInfo', primaryjoin='CampusMember.user_id == PowerUserInfo.id', backref='campus_members')

