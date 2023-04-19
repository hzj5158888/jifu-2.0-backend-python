#!/usr/bin/env python
# coding: utf-8
from datetime import datetime

from application_initializer import db
from common.utils.model_to_dict import model_to_dict


@model_to_dict
class InviteCode(db.Model):
    __tablename__ = 'invite_code'

    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(255), nullable=False, default='00000000')
    campus_id = db.Column(db.ForeignKey('campus_info.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    dept_id = db.Column(db.ForeignKey('campus_dept_info.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    gmt_create = db.Column(db.DateTime, default=datetime.now)
    gmt_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    campus = db.relationship('CampusInfo', primaryjoin='InviteCode.campus_id == CampusInfo.id', backref='invite_code')
    dept = db.relationship('CampusDeptInfo', primaryjoin='InviteCode.dept_id == CampusDeptInfo.id', backref='invite_code')