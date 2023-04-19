#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/11/25 10:03
@note     职员模块服务层
"""
from datetime import datetime

from common.models.admin import Admin
from common.models.campus_member import CampusMember
from common.models.campus_member_merits_record import CampusMemberMeritsRecord
from common.enums.merits_record_operator_type_enum import MeritsOperatorTypeEnum

class MemberService:

    @staticmethod
    def getMemberNickName(member_id):
        """
        获取职员俗称(职位+姓名)
        @param member_id: 职员id

        @return: 职员俗称
        """
        member_info = CampusMember.query.filter_by(id=member_id).first()
        if member_info:
            return member_info.position + member_info.name
        else:
            return ""

    @staticmethod
    def operator_to_detail(operator_id):
        """
        获取职员具体的信息
        @param operator_id: 职员id
        """
        member_info = CampusMember.query.filter_by(id=operator_id).first()
        info_dict = {
            "name": member_info.name,
            "dept": member_info.dept.name,
            "position": member_info.position
        }
        return info_dict

    @staticmethod
    def operator_detail_with_avter(member_id):
        """
        获取职员具体的信息
        @param member_id: 职员id
        """
        member_info = CampusMember.query.filter_by(id=member_id).first()
        info_dict = {
            "name": member_info.name,
            "dept": member_info.dept.name,
            "avter_url":member_info.user.avatar_url
        }
        return info_dict


    @staticmethod
    def member_to_detail(member_id):
        """
        获取职员具体的信息
        @param operator: 职员id
        """
        member_info = CampusMember.query.filter_by(id=member_id).first()
        if datetime.now() > member_info.end_time:
            is_tenure = False
        else:
            is_tenure = True

        admin_info = Admin.query.filter_by(member_id = member_id).first()
        is_admin = 0 if not admin_info else 1
        info_dict = {
            "name": member_info.name,
            "campus": member_info.campus.name,
            "is_tenure": is_tenure,
            "dept": member_info.dept.name,
            "position": member_info.position,
            "merits": float(member_info.merits),
            "status": member_info.status,
            "is_admin": is_admin,
            "start_time": member_info.start_time.timestamp(),
            "end_time": member_info.end_time.timestamp()
        }
        return info_dict

    @staticmethod
    def getMemberMerits(member_id,merits_info):
        """
        获取职员单个绩效记录的具体信息
        :param member_id: 单个绩效记录中操作人员的id
        :param merits_info: 单个绩效记录
        :return:
        """
        if merits_info.operator_type == MeritsOperatorTypeEnum.SYSTEM.value:
            operator = "系统"
        else:
            member = CampusMember.query.filter_by(id=member_id).first()
            operator = member.name
        info_dict = {
            "operator": operator,
            "type": merits_info.type,
            "operator_type": MeritsOperatorTypeEnum.MAP.value[merits_info.operator_type],
            "score": float(merits_info.score),
            "create_time": merits_info.gmt_create.timestamp()
        }
        return info_dict
