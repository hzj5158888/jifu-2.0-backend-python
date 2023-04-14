#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/11/25 11:11
@note     
"""
import time

from sqlalchemy import and_

from common.enums.report_status_enum import ReportStatus
from common.enums.status_enum import StatusEnum
from common.models.report_picture import ReportPicture
from common.utils.Helper import getCurrentDate

from common.models.campus_system_info import CampusSystemInfo

from common.models.report_info import ReportInfo

from common.enums.report_types_enum import ReportTypes


class ReportService:

    @staticmethod
    def isExistInCompleteReport(phone):
        """
        判断此手机号是否存在未完结的报障
        @param phone: 手机号
        @return: 是否存在未完结的报障
        """
        check_repeat_report = ReportInfo.query.filter(and_(ReportInfo.status.in_(
            [ReportStatus.UNCONFIRMED.value, ReportStatus.CONFIRMED.value, ReportStatus.HANDLED.value]),
            ReportInfo.phone == phone)).count()

        return check_repeat_report > 0

    @staticmethod
    def isEnableSubmitReport(campus_id, report_type):
        """
        判断是否可以提交报障
        @param campus_id: 校区id
        @param report_type:报障类型 详见 utils.report_types_enum.py
        @return [True/False," "]:是否可以提交报障，不能提交则写明理由
        """
        present_time = getCurrentDate()
        origin_day_time = getCurrentDate("%Y-%m-%d") + " 00:00:00"

        report_today_count = ReportInfo.query.filter(and_(origin_day_time < ReportInfo.gmt_create,
                                                             ReportInfo.gmt_create < present_time,
                                                            ReportInfo.campus_id==campus_id,
                                                            ReportInfo.type==report_type)).count()

        system_config = CampusSystemInfo.query.filter_by(campus_id=campus_id).first()
        if system_config is None:
            return [False,"找不到此校园系统信息。"]

        if system_config.report_status == StatusEnum.CLOSE.value:
            return [False,system_config.report_content]

        if report_type == ReportTypes.TEACHER.value:
            if report_today_count >= system_config.report_teacher_size:
                return [False,"今天我们接收到的报障太多啦，请明天再来吧~"]
        else:
            if report_today_count >= system_config.report_student_size:
                return [False,"今天我们接收到的报障太多啦，请明天再来吧~"]
        return [True," "]



    @staticmethod
    def findAllPictureUrls(report_id):
        picture_models = ReportPicture.query.filter_by(report_id=report_id).all()
        return [picture_model.img_url for picture_model in picture_models]
