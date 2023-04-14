#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@time:2021/01/25/15:40
@author:WYY
@content:
"""
from common.enums.group_member_type_enum import GroupMemberEnum
from common.models.report_group import ReportGroup
from common.models.campus_member_merits_record import CampusMemberMeritsRecord
from common.models.campus_member import CampusMember
from common.models.report_info import ReportInfo
from common.models.campus_system_info import CampusSystemInfo
from common.enums.report_types_enum  import ReportTypes
from common.enums.merits_record_operator_type_enum import MeritsOperatorTypeEnum
from application_initializer import db
from sqlalchemy import and_


class ReportGroupService:
    @staticmethod
    def isInGroup(report_id, member_id):
        report_group = ReportGroup.query.filter(and_(ReportGroup.report_id==report_id, ReportGroup.member_id==member_id)).first()
        if report_group:
            return True
        else:
            return False


    @staticmethod
    def isReportGroupLeader(report_id, member_id):
        report_group = ReportGroup.query.filter(and_(ReportGroup.report_id==report_id, ReportGroup.member_id==member_id)).first()
        if report_group.role == GroupMemberEnum.GROUP_LEADER.value:
            return True
        else:
            return False


    @staticmethod
    def member_get_report_merits(report_id):
        # 通过报障的类型和校区，得到单次分数
        model_report = ReportInfo.query.filter_by(id=report_id).first()
        _type = model_report.type
        campus_id = model_report.campus_id

        model_campus_system_info = CampusSystemInfo.query.filter_by(id=campus_id).first()
        if _type==ReportTypes.TEACHER.value:
            once_score = model_campus_system_info.teacher_report_basic
        else:
            once_score = model_campus_system_info.student_report_basic


        #找出所有团队成员
        model_group = ReportGroup.query.filter_by(report_id=report_id).all()
        for member in model_group:

            model_merits = CampusMemberMeritsRecord()

            model_merits.member_id = member.member_id
            model_merits.score = round(once_score, 2)
            model_merits.type = "任务"
            model_merits.operator_type = MeritsOperatorTypeEnum.SYSTEM.value
            model_merits.operator = MeritsOperatorTypeEnum.MAP.value[0]

            model_member = CampusMember.query.filter_by(id=member.member_id).first()
            model_member.merits += once_score

            db.session.add(model_merits, model_member)
            db.session.commit()
