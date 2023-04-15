#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@time:2021/01/22/15:53
@author:WYY
@content:职员模块
"""
import time
from datetime import datetime

from flask import Blueprint, request
from common.api.common_result import R
from common.api.common_page import CommonPage
from common.enums.campus_dept_type_enum import CampusDeptEnum
from common.enums.status_enum import StatusEnum
from common.models.report_info import ReportInfo
from common.models.campus_dept_info import CampusDeptInfo
from common.models.campus_member import CampusMember
from common.models.report_group import ReportGroup
from common.models.invite_code import InviteCode
from common.models.power_user_info import PowerUserInfo
from common.models.campus_member_merits_record import CampusMemberMeritsRecord
from application_initializer import db
from common.enums.report_status_enum import ReportStatus
from common.enums.group_member_type_enum import GroupMemberEnum
from common.enums.merits_record_operator_type_enum import MeritsOperatorTypeEnum
from common.models.report_picture import ReportPicture
from service.report_log_service import ReportLogService
from service.member_service import MemberService
from service.report_group_service import ReportGroupService
from sqlalchemy import and_
from flask_jwt_extended import jwt_required

from service.report_service import ReportService

member_api = Blueprint("member", __name__)

@member_api.route("/<int:user_id>/signup", methods=['PUT'])
@jwt_required()
def addMemberInfo(user_id):
    """
    成员注册
    @param (Query)userId 用户id
    @param (Body){
        "real_name": member_info.real_name,
        "avatar_url": member_info.avatar_url,
        "phone": member_info.phone,
        "campus_id" : cmember_info.ampus_id
        "dept_id" : member_info.dept_id
        "class_name" : member_info.class_name
        "invite_code" : member_info.invite_code
    }
    @return:
    """
    req = request.get_json()
    real_name = req.get("real_name")
    avatar_url = req.get("avatar_url")
    phone = req.get("phone")
    campus_id = req.get("campus_id")
    dept_id = req.get("dept_id")
    class_name = req.get("class_name")
    invite_code = req.get("invite_code")
    if avatar_url is None:
        return R.validateFailed()
    
    if invite_code is None:
        return R.failedMsg("邀请码为空")
    elif invite_code not in InviteCode.query.all():
        return R.failedMsg("邀请码错误")

    user_info = PowerUserInfo.query.filter_by(id=user_id).first()
    if not user_info:
        return R.failedMsg("找不到用户")
    
    if CampusMember.query.filter_by(user_id = user_id).first() is not None:
        return R.failedMsg("成员账户已存在")
    
    member_info = CampusMember()
    member_info.user_id = user_id
    member_info.campus_id = campus_id
    member_info.dept_id = dept_id
    member_info.name = real_name
    member_info.phone = phone
    member_info.class_name = class_name
    member_info.merits = 0
    member_info.position = "小干"
    member_info.status = 0
    member_info.start_time = datetime.datetime.now
    member_info.end_time = member_info.start_time + datetime.timedelta(days = 365 * 2)
    
    db.session.add(member_info)
    db.session.commit()

    return R.success("注册成功，等待审核")

@member_api.route("/<int:member_id>/modifyinfo", methods=['PUT'])
@jwt_required()
def updateMemberInfo(member_id):
    """
    成员资料修改
    @param (Query)userId 用户id
    @param (Body){
        "real_name": member_info.real_name,
        "avatar_url": member_info.avatar_url,
        "phone": member_info.phone,
        "campus_id" : cmember_info.ampus_id
        "dept_id" : member_info.dept_id
        "class_name" : member_info.class_name
        "start_time" : member_info.start_time
        "end_time" : member_info.end_time
    }
    @return:
    """
    req = request.get_json()
    real_name = req.get("real_name")
    phone = req.get("phone")
    campus_id = req.get("campus_id")
    dept_id = req.get("dept_id")
    class_name = req.get("class_name")
    
    member_info = CampusMember.query.filter_by(id = member_id).first()
    if not member_info:
        return R.failedMsg("该用户不是成员")
    
    member_info.campus_id = campus_id
    member_info.dept_id = dept_id
    member_info.name = real_name
    member_info.phone = phone
    member_info.class_name = class_name
    member_info.status = 0
    
    db.session.add(member_info)
    db.session.commit()

    return R.success("修改成功，等待审核")


@member_api.route("/<int:member_id>/del", methods=['PUT'])
@jwt_required()
def delMember(member_id):
    """
    成员注销
    @param (Query)userId 用户id
    @return:
    """
    
    member_info = CampusMember.query.filter_by(id = member_id).first()
    if not member_info:
        return R.failedMsg("该用户不是成员")
    
    db.session.delete(member_info)
    db.session.commit()
    

@member_api.route("/<int:member_id>/info", methods=['GET'])
@jwt_required()
def memberGetInfo(member_id):
    """
    职员获取个人信息
    :param member_id: 职员id
    :return: 职员的个人信息
    """
    return MemberService.member_to_detail(member_id)


@member_api.route("/<int:member_id>/merits_logs", methods=['GET'])
@jwt_required()
def memberGerMeritsLogs(member_id):
    """
    职员查看个人绩效记录
    :param member_id: 职员id
    :param page_size: 页大小(default:15)
    :param page_num: 页码(default:1)
    :return: 职员的绩效记录
    """
    req = request.args
    page_size = int(req['page_size']) if ('page_size' in req and req['page_size']) else 15
    page_num = int(req['page_num']) if ('page_num' in req and req['page_num']) else 1

    query = CampusMemberMeritsRecord.query.filter_by(member_id=member_id)
    merits_infos = query.order_by(CampusMemberMeritsRecord.gmt_create.desc()).paginate(page=page_num, per_page=page_size)

    page_result = CommonPage.restPage(merits_infos)
    page_result["list"]=[MemberService.getMemberMerits(merits_info.operator, merits_info) for merits_info in merits_infos.items]

    return R.successData(page_result)


@member_api.route("/<int:report_id>/status", methods=['POST'])
@jwt_required()
def memberOpsOneReport(report_id):
    """
    职员对单个报障进行操作
    :param report_id: 报障id
    :param status: 修改后的报障状态
    :param operator: 操作者的id
    :return: 操作结果
    """
    req = request.get_json()
    operator = req.get("operator")
    status = req.get("status")

    model_member = CampusMember.query.filter_by(id=operator).first()
    if not model_member or model_member.status == StatusEnum.CLOSE.value:
        return R.validateFailedMsg("无效职员")

    report_info = ReportInfo.query.filter_by(id=report_id).first()
    if not report_info:
        return R.failedMsg("找不到报障单")

    if (status not in ReportStatus.value_list()) or status == report_info.status:
        return R.validateFailedMsg("无效的修改操作")

    if report_info.status in [ReportStatus.CANCELED.value, ReportStatus.FINISHED.value, ReportStatus.REJECTED.value]:
        return R.failedMsg("当前此报障状态无法再次修改")

    if status==ReportStatus.FINISHED.value:
        if ReportGroupService.isReportGroupLeader(report_id, operator) == False:
            return R.failedMsg("不是此报障的队长，无法将报障状态修改为已完成")
        ReportGroupService.member_get_report_merits(report_id)

    ReportLogService.insertChangeStatusRecordLog(report_id, operator, status)

    report_info.status = status
    db.session.add(report_info)
    db.session.commit()

    if status==ReportStatus.CONFIRMED.value:
        model_group = ReportGroup()

        model_group.report_id = report_id
        model_group.member_id = operator
        model_group.role = GroupMemberEnum.GROUP_LEADER.value

        db.session.add(model_group)
        db.session.commit()

    return R.success()


@member_api.route("/<int:report_id>/note", methods=['POST'])
@jwt_required()
def memberSetReportNote(report_id):
    """
    对单个报障填写备注
    :param report_id: 报障id
    :param note: 备注的文本内容
    :param operator: 操作者id
    :return: 操作结果
    """
    req = request.get_json()

    note = req.get("note")
    operator = req.get("operator")

    model_member = CampusMember.query.filter_by(id=operator).first()
    if not model_member or model_member.status == 0:
        return R.validateFailedMsg("无效职员")

    ReportLogService.insertChangeNoteRecordLog(report_id, operator, note)

    return R.success()


@member_api.route("/<int:report_id>/unableReason", methods=['POST'])
@jwt_required()
def memberSetReportUnableReason(report_id):
    """
    对单个报障填写无法处理的原因
    :param report_id: 报障id
    :param unable_reason: 无法处理的原因的文本内容
    :param operator: 操作者id
    :return: 操作结果
    """
    req = request.get_json()

    unable_reason = req.get("unable_reason")
    operator = req.get("operator")

    model_member = CampusMember.query.filter_by(id=operator).first()
    if not model_member or model_member.status == 0:
        return R.validateFailedMsg("无效职员")

    if unable_reason is None or len(str(unable_reason)) < 5:
        return R.validateFailedMsg('请输入符合规范的无法处理原因并不少于5个字符')

    report_info = ReportInfo.query.filter_by(id=report_id).first()
    if not report_info:
        return R.failedMsg("找不到报障单")

    if report_info.status != ReportStatus.REJECTED.value:
        return R.failedMsg("无法填写不能处理的原因")

    report_info.unable_reason = unable_reason
    db.session.add(report_info)
    db.session.commit()

    ReportLogService.insertUnableHandlerRecordLog(report_id, operator, unable_reason)

    return R.success()


@member_api.route("/<int:member_id>/reports", methods=['GET'])
@jwt_required()
def campusUserCheckReceivedReport(member_id):
    """
    职员查看已接受的任务
    :param member_id:职员id
    :param page_size: 页大小(default:15)
    :param page_num: 页码(default:1)
    :return: 某个职员已接受的任务
    """
    req = request.args

    page_size = int(req['page_size']) if ('page_size' in req and req['page_size']) else 15
    page_num = int(req['page_num']) if ('page_num' in req and req['page_num']) else 1

    groups = ReportGroup.query.filter_by(member_id=member_id).all()
    all_report_ids = [group.report_id for group in groups]

    query = ReportInfo.query.filter(ReportInfo.id.in_(all_report_ids))
    report_infos = query.order_by(ReportInfo.gmt_create.desc()).paginate(page=page_num, per_page=page_size)
    page_result = CommonPage.restPage(report_infos)

    for report_dict in page_result["list"]:
        report_dict["picture_list"] = ReportService.findAllPictureUrls(report_dict["id"])
    return R.successData(page_result)



@member_api.route("/<int:campus_id>/getreports", methods=['GET'])
@jwt_required()
def memberReceiveReport(campus_id):
    """
    职员查看可领取/全部的任务
    :param page_size: 页大小(default:15)
    :param page_num: 页码(default:1)
    :return: 某个职员可领取/全部的任务
    """
    req = request.args

    page_size = int(req['page_size']) if ('page_size' in req and req['page_size']) else 15
    page_num = int(req['page_num']) if ('page_num' in req and req['page_num']) else 1

    query = ReportInfo.query.filter(ReportInfo.campus_id==campus_id)
    if ('status' in req) and (int(req['status']) in ReportStatus.value_list() ):
        query = query.filter(ReportInfo.status == int(req['status']))

    report_infos = query.order_by(ReportInfo.gmt_create.desc()).paginate(page=page_num, per_page=page_size)
    page_result = CommonPage.restPage(report_infos)

    for report_dict in page_result["list"]:
        report_dict["picture_list"] = ReportService.findAllPictureUrls(report_dict["id"])
    return R.successData(page_result)


@member_api.route("/<int:report_id>/invitation", methods=['POST'])
@jwt_required()
def inviteOtherMember(report_id):
    """
    报障团队队长邀请队员
    :param report_id: 报障id
    :param operator: 操作者id
    :param new_group_member_ids: 被邀请的队员id列表
    :return:操作结果
    """
    req = request.get_json()
    operator = req.get("operator")
    new_group_member_ids = req.get("new_group_member_ids")

    member_info = CampusMember.query.filter_by(id=operator).first()
    if not member_info or member_info.status == 0:
        return R.validateFailedMsg("无效职员")

    report_info = ReportInfo.query.filter_by(id=report_id).first()
    if report_info.status in [ReportStatus.CANCELED.value, ReportStatus.FINISHED.value, ReportStatus.REJECTED.value]:
        return R.failedMsg("当前报障已无法再邀请队员")

    if ReportGroupService.isInGroup(report_id, operator) == False:
        return R.validateFailedMsg("您还不在此报障队伍中")

    for new_group_member_id in new_group_member_ids:
        member_info = CampusMember.query.filter_by(id=new_group_member_id).first()
        if not member_info or member_info.status == 0:
            return R.validateFailedMsg("存在无效的被邀请职员")

        if ReportGroupService.isInGroup(report_id, new_group_member_id) == True:
            return R.validateFailedMsg("被邀请职员已经在队伍中")

    for new_group_member_id in new_group_member_ids:
        model_group = ReportGroup()
        model_group.report_id = report_id
        model_group.member_id = new_group_member_id
        model_group.role = GroupMemberEnum.GROUP_MEMBER.value

        db.session.add(model_group)
        db.session.commit()

        ReportLogService.insertChangeGroupRecordLog(report_id, operator, new_group_member_id)

    return R.success()


@member_api.route("/<int:campus_id>/members", methods=['GET'])
@jwt_required()
def listAllMember(campus_id):
    """
    查看某个校区在职的职员信息
    :param campus_id:校区id
    :param page_size: 页大小(default:15)
    :param page_num: 页码(default:1)
    :return: 职员id + 职员name
    """
    req = request.args

    page_size = int(req['page_size']) if ('page_size' in req and req['page_size']) else 15
    page_num = int(req['page_num']) if ('page_num' in req and req['page_num']) else 1

    dept_info = CampusDeptInfo.query.filter(and_(CampusDeptInfo.campus_id==campus_id, CampusDeptInfo.name==CampusDeptEnum.TECH_DEPT.value)).first()

    query = CampusMember.query.filter(and_(datetime.now() < CampusMember.end_time,
            CampusMember.dept_id==dept_info.id, CampusMember.status==StatusEnum.OPEN.value))

    member_infos = query.paginate(page=page_num, per_page=page_size)

    page_result = CommonPage.restPage(member_infos)
    page_result["list"] = [{"id":member_info.id, "name":member_info.name} for member_info in
                           member_infos.items]

    return R.successData(page_result)
