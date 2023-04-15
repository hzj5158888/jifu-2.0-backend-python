#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@time:2021/02/01/14:47
@author:WYY
@content:反馈模块
"""
from flask import Blueprint, request
from common.api.common_result import R
from flask_jwt_extended import jwt_required
from common.models.system_feedback import SystemFeedback
from common.models.system_feedback_picture import SystemFeedbackPicture
from application_initializer import db

feedback_api = Blueprint("feedback", __name__)


@feedback_api.route("/", methods=['POST'], strict_slashes=False)
@jwt_required()
def postFeedback():
    """
    提交反馈意见
    @param user_id 用户id
    @param content 问题描述
    @param contact 联系方式
    @param pic_list 反馈意见的图片url列表(可为空)
    @return: 操作结果
    """
    req = request.get_json()

    user_id = req.get("user_id")
    content = req.get("content")
    contact = req.get("contact")
    pic_list = req.get("pic_list")

    if content is None or len(str(content)) < 5:
        return R.validateFailedMsg('请输入符合规范的反馈描述并不少于5个字符')

    model_feedback = SystemFeedback()

    model_feedback.user_id = user_id
    model_feedback.content = content
    model_feedback.contact = contact

    db.session.add(model_feedback)
    db.session.commit()

    # 保存反馈图片
    if pic_list:
        for url in pic_list:
            model_system_feedback_pic = SystemFeedbackPicture()
            model_system_feedback_pic.system_feedback_id = model_feedback.id
            model_system_feedback_pic.img_url = url
            db.session.add(model_system_feedback_pic)
            db.session.commit()

    return R.success()
