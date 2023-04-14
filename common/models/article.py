#!/usr/bin/env python
# coding: utf-8
"""
@author   liziyi0914 2021/02/25 17:36
@note
"""
from datetime import datetime

from application_initializer import db
from common.utils.model_to_dict import model_to_dict
from sqlalchemy.dialects.mysql import LONGTEXT


@model_to_dict
class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(512), nullable=False)
    author = db.Column(db.String(512))
    avatar = db.Column(db.String(512))
    description = db.Column(db.String(512))
    content = db.Column(LONGTEXT, nullable=False)
    gmt_create = db.Column(db.DateTime, default=datetime.now)
    gmt_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
