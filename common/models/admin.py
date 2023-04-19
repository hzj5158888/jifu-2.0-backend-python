#!/usr/bin/env python
# coding: utf-8
from datetime import datetime

from application_initializer import db
from common.utils.model_to_dict import model_to_dict


@model_to_dict
class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.BigInteger, primary_key=True)
    invite_code = db.Column(db.String(255), nullable=False)
    campus_id = db.Column(db.ForeignKey('campus_info.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    dept_id = db.Column(db.ForeignKey('campus_dept_info.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    member_id  = db.Column(db.BigInteger, nullable=False)
    invite_count = db.Column(db.Integer, default=3)
    gmt_create = db.Column(db.DateTime, default=datetime.now)
    gmt_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    campus = db.relationship('CampusInfo', primaryjoin='Admin.campus_id == CampusInfo.id', backref='admin')
    dept = db.relationship('CampusDeptInfo', primaryjoin='Admin.dept_id == CampusDeptInfo.id', backref='admin')