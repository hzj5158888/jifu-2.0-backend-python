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
class CampusMemberMeritsRecord(db.Model):
    __tablename__ = 'campus_member_merits_record'

    id = db.Column(db.BigInteger, primary_key=True)
    member_id = db.Column(db.ForeignKey('campus_member.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    score = db.Column(db.Float(32, True), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    operator_type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    operator = db.Column(db.String(255))
    gmt_create = db.Column(db.DateTime, default=datetime.now)
    gmt_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    member = db.relationship('CampusMember', primaryjoin='CampusMemberMeritsRecord.member_id == CampusMember.id', backref='campus_member_merits_records')
