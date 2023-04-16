#!/usr/bin/env python
# coding: utf-8
from datetime import datetime

from application_initializer import db
from common.utils.model_to_dict import model_to_dict


@model_to_dict
class InviteCode(db.Model):
    __tablename__ = 'InviteCode'

    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(255), default='00000000')
    gmt_create = db.Column(db.DateTime, default=datetime.now)
    gmt_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)