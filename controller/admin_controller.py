import hashlib
import datetime
import json
import random

from flask import Blueprint, request
from application_initializer import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from common.utils.jwt_util import JwtUtil
import common.utils.Helper as Helper 

from common.api.common_result import R
from common.models.admin import Admin
from common.models.campus_member import CampusMember
from common.models.invite_code import InviteCode
from common.models.campus_dept_info import CampusDeptInfo
from common.api.common_page import CommonPage

from service.member_service import MemberService

admin_api = Blueprint("admin", __name__)

@admin_api.route("/signup", methods=['PUT'])
@jwt_required()
def adminSignup():
    """
    管理员注册
    @return
    """
    
    req = request.get_json()
    
    member_id = req.get('member_id')
    invite_code = req.get('invite_code')
    
    member_dept = CampusMember.query.filter_by(id = member_id).first().dept_id
    admin_info = Admin.query.filter_by(invite_code = invite_code, dept_id = member_dept).first()
    if not admin_info:
        return R.failedMsg("邀请码不存在或已失效")
    
    if (admin_info.invite_count > 0):
        admin_info.invite_count = admin_info.invite_count - 1
    else:
        admin_info.invite_code = ''
        db.session.add(admin_info)
        db.session.commit()
        return R.failedMsg("邀请码已失效")

    db.session.add(admin_info)
    
    new_admin = Admin()
    new_admin.campus_id = CampusMember.query.filter_by(id = member_id).first().campus_id
    new_admin.member_id = member_id
    new_admin.dept_id = member_dept
    while True:
        new_admin.invite_code = Helper.randomStr(9)
        if not Admin.query.filter_by(invite_code = new_admin.invite_code).first():
            break
    db.session.add(new_admin)
    
    db.session.commit()
    
    return R.success()

@admin_api.route("/<int:admin_member_id>/admin_invitecode", methods=['GET'])
@jwt_required()
def getAdminCode(admin_member_id):
    """
    获取管理员邀请码
    @return
    """
    
    admin_info = Admin.query.filter_by(member_id = admin_member_id).first()
    if not admin_info:
        return R.failedMsg("该成员不是管理员")
    if admin_info.invite_count == 0:
        return R.failedMsg("管理员邀请机会已用完")
    
    admin_info.invite_code = Helper.randomStr(9)
    db.session.add(admin_info)
    db.session.commit()
    
    return R.successData(invite_code = admin_info.invite_code)

@admin_api.route("/<int:admin_member_id>/member/info/get", methods=['GET'], strict_slashes=False)
@jwt_required()
def getAllMemberInfo(admin_member_id):
    """
    校区部门全部成员获取
    @param admin_member_id: 管理员的成员id
    :param page_size: 页大小(default:15)
    :param page_num: 页码(default:1)
    @return: 管理员可管理的职员
    """
    req = request.args
    
    admin_info = Admin.query.filter_by(member_id = admin_member_id).first()
    if not admin_info:
        return R.failedMsg("该成员不是管理员")
    
    admin_dept_id = CampusMember.query.filter_by(id = admin_info.member_id).first().dept_id
    
    page_size = int(req['page_size']) if ('page_size' in req and req['page_size']) else 15
    page_num = int(req['page_num']) if ('page_num' in req and req['page_num']) else 1

    query = CampusMember.query.filter(CampusMember.campus_id == admin_info.campus_id, CampusMember.dept_id == admin_dept_id, CampusMember.end_time > datetime.datetime.now())

    member_infos = query.order_by(CampusMember.status.asc()).paginate(page=page_num, per_page=page_size)
    page_result = CommonPage.restPage(member_infos)

    return R.successData(page_result)

@admin_api.route("/member/info/get/<int:member_id>", methods=['GET'], strict_slashes=False)
@jwt_required()
def getMemberDetail(member_id):
    """
    校区部门全部成员资料获取
    @param admin_member_id: 管理员的成员id
    @return: 成员资料数组
    """
    
    return R.successData(MemberService.member_to_detail(member_id))

@admin_api.route("/member/info/modify/<int:member_id>", methods=['POST'])
@jwt_required()
def modifyinfo(member_id):
    """
    成员资料修改函数
    @param admin_member_id: 管理员的成员id
    @param member_id: 被修改成员的id
    """
    req = request.get_json()
    
    status = req.get('status')
    
    member_info = CampusMember.query.filter_by(id = member_id).first()
    if not member_info:
        return R.failedMsg("找不到用户")
    
    member_info.status = status
    db.session.add(member_info)
    db.session.commit()
    
    return R.success()

@admin_api.route("/<int:admin_member_id>/invitecode/get", methods=['GET'])
@jwt_required()
def getInviteCode(admin_member_id):
    """
    邀请码获取
    @param admin_member_id: 管理员的成员id
    """
    
    admin_info = Admin.query.filter_by(member_id = admin_member_id).first()
    if not admin_info:
        return R.failedMsg("该成员不是管理员")
    
    admin_dept_id = admin_info.dept_id
    admin_campus_id = admin_info.campus_id
    invite_code = InviteCode.query.filter_by(campus_id = admin_campus_id, dept_id = admin_dept_id).first()
    if not invite_code:
        return R.failedMsg("邀请码不存在")
    
    return R.successData(invite_code = invite_code.code)

@admin_api.route("/<int:admin_member_id>/invitecode/refresh", methods=['GET'])
@jwt_required()
def refreshInviteCode(admin_member_id):
    """
    邀请码刷新
    @param admin_member_id: 管理员的成员id
    """
    
    admin_info = Admin.query.filter_by(member_id = admin_member_id).first()
    if not admin_info:
        return R.failedMsg("该成员不是管理员")
    
    admin_dept_id = admin_info.dept_id
    admin_campus_id = admin_info.campus_id
    invite_code_info = InviteCode.query.filter_by(campus_id = admin_campus_id, dept_id = admin_dept_id).first()
    if not invite_code_info:
        invite_code_info = InviteCode()
        invite_code_info.campus_id = admin_campus_id
        invite_code_info.dept_id = admin_dept_id
    
    while True:
        invite_code = Helper.randomStr(9)
        if not InviteCode.query.filter_by(code = invite_code).first():
            invite_code_info.code = invite_code
            break
    db.session.add(invite_code_info)
    db.session.commit()
    
    return R.successData(invite_code = invite_code_info.code)