#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/11/26 10:38
@note     
"""
from flask_jwt_extended import create_access_token, create_refresh_token
from common.api.common_result import R
from common.models.power_user_info import PowerUserInfo
from common.models.campus_member import CampusMember
from common.enums.status_enum import StatusEnum
from common.models.admin import Admin


class JwtUtil:

    @staticmethod
    def generate_token(user_id):
        """
        生成token token负载里面包含user_id和is_member(是否是职员)
        @param user_id: 用户id
        @return: http json返回结果包含token与刷新令牌
        """

        info_claim = {
            "user_id": user_id
        }

        member_info = CampusMember.query.filter_by(user_id=user_id, status=StatusEnum.OPEN.value).first()

        info_claim["is_member"] = StatusEnum.OPEN.value if member_info else StatusEnum.CLOSE.value
        member_id = member_info.id if member_info else None
        member_status = member_info.status if member_info else StatusEnum.CLOSE.value
        
        admin_info = Admin.query.filter_by(member_id = member_id).first()
        is_admin = StatusEnum.OPEN.value if admin_info else StatusEnum.CLOSE.value

        access_token = create_access_token(identity=user_id, additional_claims=info_claim)
        
        refresh_token = create_refresh_token(identity=user_id)

        return R.successData(access_token=access_token,
                             refresh_token=refresh_token,
                             user_id=user_id,
                             member_id=member_id,
                             is_member=info_claim["is_member"],
                             member_status=member_status,
                             is_admin = is_admin)

