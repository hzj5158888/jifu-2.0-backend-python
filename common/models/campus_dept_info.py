#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/11/3 19:37
@note     
"""
from datetime import datetime
from common.utils.model_to_dict import model_to_dict
from application_initializer import db


@model_to_dict
class CampusDeptInfo(db.Model):
    __tablename__ = 'campus_dept_info'

    id = db.Column(db.BigInteger, primary_key=True)
    campus_id = db.Column(db.ForeignKey('campus_info.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False,
                          index=True)
    name = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    remark = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    gmt_create = db.Column(db.DateTime, default=datetime.now)
    gmt_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    campus = db.relationship('CampusInfo', primaryjoin='CampusDeptInfo.campus_id == CampusInfo.id',
                             backref='campus_dept_infos')
