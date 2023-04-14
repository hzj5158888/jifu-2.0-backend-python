#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/11/1 21:45
@note     
"""
from flask import Blueprint, request
from common.api.common_result import R
from common.component.qiniu_component import QiniuComponent
from flask_jwt_extended import jwt_required

file_upload_api = Blueprint("file", __name__)


@file_upload_api.route("/upload", methods=['POST'])
def file_upload():
    """
    图片上传
    @return: 图片地址
    """
    pic = request.files.get("picture")
    if pic is None:
        return R.validateFailed()
    try:
        pic_data = pic.read()
    except Exception:
        return R.failedMsg("上传图片出错")

    return R.success(QiniuComponent.uploadFile(pic_data))
