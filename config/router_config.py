#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/10/29 20:39
@note     全局路由配置
"""


def create_router(application):

    from controller.file_upload_controller import file_upload_api
    from controller.campus_controller import campus_api
    from controller.report_controller import report_api
    from controller.auth_controller import auth_api
    from controller.article_controller import article_api
    from controller.member_controller import member_api
    from controller.feedback_controller import feedback_api

    """
    统一创建路由文件
    @param application: flask应用
    """
    application.register_blueprint(file_upload_api, url_prefix="/file")
    application.register_blueprint(campus_api, url_prefix="/campus")
    application.register_blueprint(report_api, url_prefix="/report")
    application.register_blueprint(auth_api, url_prefix="/auth")
    application.register_blueprint(article_api, url_prefix="/article")
    application.register_blueprint(member_api, url_prefix="/member")
    application.register_blueprint(feedback_api, url_prefix="/feedback")

