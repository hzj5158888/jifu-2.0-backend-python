#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/11/3 19:37
@note     
"""
from datetime import datetime

from application_initializer import db
from common.models.campus_info import CampusInfo
from common.utils.model_to_dict import model_to_dict


@model_to_dict
class CampusCarousel(db.Model):
    __tablename__ = 'campus_carousel'

    id = db.Column(db.BigInteger, primary_key=True)
    campus_id = db.Column(db.ForeignKey('campus_info.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    url = db.Column(db.String(512), nullable=False)
    gmt_create = db.Column(db.DateTime, default=datetime.now)
    gmt_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    campus = db.relationship('CampusInfo', primaryjoin='CampusCarousel.campus_id == CampusInfo.id', backref='campus_carousels')

