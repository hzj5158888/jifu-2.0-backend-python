#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/11/3 19:37
@note     
"""
from datetime import datetime

from application_initializer import db
from common.utils.model_to_dict import model_to_dict


@model_to_dict
class CampusInfo(db.Model):
    __tablename__ = 'campus_info'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    img_url = db.Column(db.String(255), nullable=False)
    introduction = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    gmt_create = db.Column(db.DateTime, default=datetime.now)
    gmt_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

