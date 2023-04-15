#!/usr/bin/env python
# coding: utf-8
from datetime import datetime

from application_initializer import db
from common.utils.model_to_dict import model_to_dict


@model_to_dict
class InviteCode(db.Model):
    __tablename__ = 'InviteCode'

    code = db.Column(db.String(255), default='00000000', primary_key=True)