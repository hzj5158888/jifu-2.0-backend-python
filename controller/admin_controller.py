import hashlib
import datetime
import json

from flask import Blueprint, request
from application_initializer import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from common.utils.jwt_util import JwtUtil

from common.api.common_result import R
from common.models.admin import Admin
from common.models.campus_member import CampusMember
from common.models.invite_code import InviteCode

from service.member_service import MemberService

admin_api = Blueprint("admin", __name__)

@admin_api.route("/<int:campus_id>/member/info/get", methods=['GET'], strict_slashes=False)
@jwt_required()
def getAllMemberInfo(campus_id):
    """
    校区全部成员资料获取
    @param campus_id: 校区id
    @return: 成员资料数组
    """
    AllMember_Id = CampusMember.query.filter_by(campus_id = campus_id).with_entities(CampusMember.id).all()
    
    AllMember_Info = []
    for member_id in AllMember_Id:
        member_info_dict = MemberService.member_to_detail(member_id)
        member_info_json = json.dumps(member_info_dict)
        AllMember_Info.append(member_info_json)
    
    return R.success(AllMember_Info)

@admin_api.route("/<int:campus_id>/member/info/modify/<int:member_id>", methods=['PUT'])
@jwt_required()
def modifyinfo(campus_id, member_id):
    """
    成员资料修改函数
    @param campus_id: 校区id
    @param member_id: 成员id
    """
    req = request.get_json()
    
    status = req.get('status')
    
    member_info = CampusMember.query.filter_by(id = member_id, campus_id = campus_id).first()
    if not member_info:
        return R.failedMsg("找不到用户")
    
    member_info.status = status
    db.session.add(member_info)
    db.session.commit()
    
    return R.success()

@admin_api.route("/<int:campus_id>/invitecode/get", methods=['GET'])
@jwt_required()
def getInviteCode(campus_id):
    """
    邀请码获取
    @param campus_id: 校区id
    """
    invite_code = InviteCode.query.filter_by(campus_id = campus_id).first()
    if not invite_code:
        return R.failedMsg("邀请码不存在")
    
    return R.success(invite_code.code)

@admin_api.route("/<int:campus_id>/invitecode/modify", methods=['PUT'])
@jwt_required()
def modifyInviteCode(campus_id):
    """
    邀请码修改
    @param campus_id: 校区id
    """
    req = request.get_json()
    
    new_invite_code = req.get('invitecode')
    
    invite_code = InviteCode.query.filter_by(campus_id = campus_id).first()
    if not invite_code:
        invite_code = InviteCode()
        invite_code.campus_id = campus_id
    
    invite_code.code = new_invite_code
    db.session.add(invite_code)
    db.commit()
    
    return R.success()