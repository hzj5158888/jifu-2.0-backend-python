from flask import Blueprint, request
from common.api.common_result import R
from common.enums.report_operate_types_enum import ReportRecordLogTypes
from common.models.report_group import ReportGroup
from common.models.report_info import ReportInfo
from application_initializer import db
from common.models.power_user_info import PowerUserInfo
from common.models.report_picture import ReportPicture
# 让 'ReportInfo'对象拥有属性'report_record_logs'
from common.models.report_record_log import ReportRecordLog
from common.models.campus_info import CampusInfo
from service.report_service import ReportService
from service.member_service import MemberService
from service.user_service import UserService

from common.enums.report_status_enum import ReportStatus
from common.enums.report_types_enum import ReportTypes
from common.api.common_page import CommonPage
from flask_jwt_extended import jwt_required
import re


report_api = Blueprint("report", __name__)


@report_api.route("/", methods=['POST'], strict_slashes=False)
@jwt_required()
def insertReport():
    """
    提交报障单
    @param campus_id 校区id
    @param user_id 用户id
    @param name 姓名
    @param student_num 学号(教师报障为空)
    @param class_name 班级(教师报障为空)
    @param phone 手机号
    @param address 地址
    @param description 问题描述
    @param pic_list 报障图片的url列表["xxx","xxx"](可为空)
    @param type 报障类型0：教师报障，1：学生报障

    @return: 返回报障id
    """
    req = request.get_json()

    campus_id = req.get("campus_id")
    user_id = req.get("user_id")
    name = req.get("name")
    student_num = req.get("student_num")
    class_name = req.get("class_name")
    phone = req.get("phone")
    address = req.get("address")
    description = req.get("description")
    pic_list = req.get("pic_list")
    _type = req.get("type")

    checkIsEnableSubmitReport=ReportService.isEnableSubmitReport(campus_id, _type)
    if not checkIsEnableSubmitReport[0]:
        return R.failedMsg(checkIsEnableSubmitReport[1])

    if campus_id is None:
        return R.validateFailedMsg("校区id不能为空 ")
    if _type is None:
        return R.validateFailedMsg('请选择报障类型')
    if name is None or re.match('^\\w{1,15}$', name) is None:
        return R.validateFailedMsg('请输入符合规范的姓名')
    if phone is None or re.match('^\\d{11}$', str(phone)) is None:
        return R.validateFailedMsg('请输入符合规范的11位手机号')
    if address is None or len(address) < 3:
        return R.validateFailedMsg('请输入符合规范的地址')
    if description is None or len(str(description)) < 5:
        return R.validateFailedMsg('请输入符合规范的描述并不少于5个字符')

    if ReportService.isExistInCompleteReport(phone):
        return R.failedMsg('同一手机号存在未完成报障，在处理完成前暂不可重复提交')

    model_report = ReportInfo()

    if _type == ReportTypes.STUDENT.value:
        if student_num is None or re.match('^\\d{10}$', str(student_num)) is None:
            return R.validateFailedMsg('请输入符合规范的10位学号')
        if class_name is None or len(class_name) < 1:
            return R.validateFailedMsg('请输入符合规范的班级')

        model_report.student_num = student_num
        model_report.class_name = class_name

    model_report.campus_id = campus_id
    model_report.name = name
    model_report.phone = phone
    model_report.address = address
    model_report.description = description
    model_report.user_id = user_id
    # 未评价
    model_report.evaluate = -1
    model_report.type = _type
    model_report.status = ReportStatus.UNCONFIRMED.value

    db.session.add(model_report)
    db.session.commit()

    # 保存报障图片
    if pic_list:
        for url in pic_list:
            model_report_pic = ReportPicture()
            model_report_pic.report_id = model_report.id
            model_report_pic.img_url = url
            db.session.add(model_report_pic)
            db.session.commit()

    return R.successData(report_id=model_report.id)


@report_api.route("/<int:user_id>/infos", methods=['GET'])
@jwt_required()
def listUserAllReport(user_id):
    """
    分页获取用户保障数据
    @param: user_id 用户id
    @param: page_size 页大小(default:15)
    @param: page_num 页码(default:1)
    @return: 报障数据列表
    """
    req = request.args

    user_info = PowerUserInfo.query.filter_by(id=user_id).first()
    if not user_info or user_info.status == 0:
        return R.validateFailedMsg("用户不存在")

    page_size = int(req['page_size']) if ('page_size' in req and req['page_size']) else 15
    page_num = int(req['page_num']) if ('page_num' in req and req['page_num']) else 1

    query = ReportInfo.query.filter_by(user_id=user_id)
    if 'status' in req and int(req['status']) in ReportStatus.value_list():
        query = query.filter(ReportInfo.status == int(req['status']))

    if 'type' in req and int(req['type']) in ReportTypes.value_list():
        query = query.filter(ReportInfo.type == int(req['type']))

    report_infos = query.order_by(ReportInfo.gmt_create.desc()).paginate(page=page_num, per_page=page_size)
    page_result = CommonPage.restPage(report_infos)

    for report_dict in page_result["list"]:
        report_dict["picture_list"] = ReportService.findAllPictureUrls(report_dict["id"])
    return R.successData(page_result)


@report_api.route("/<int:report_id>", methods=['GET'])
@jwt_required()
def getReportDetail(report_id):
    """
    获取保障详情
    @param report_id: 保障id
    @return: 保障信息 + 保障操作记录 + 保障图片
    """
    report_base_info = ReportInfo.query.filter_by(id=report_id).first()
    if not report_base_info:
        return R.failedMsg("报障单不存在")

    report_info = report_base_info.to_dict()

    campus_info = CampusInfo.query.filter_by(id=report_base_info.campus_id).first()
    report_info["campus_info"] = {"campus_name": campus_info.name, "img_url": campus_info.img_url}
    # 保障操作记录(用户只可以见到修改状态和备注的记录)
    report_info["report_record_logs"] = [{"content": j.content,
                                          "operator": MemberService.operator_to_detail(j.operator),
                                          "time": j.gmt_create.timestamp()
                                          } for j in report_base_info.report_record_logs if j.type == ReportRecordLogTypes.CHANGE_STATUS.value or j.type == ReportRecordLogTypes.CHANGE_NOTE.value ]
    # 保障图片
    report_pics = ReportPicture.query.filter_by(report_id=report_id).all()
    report_info["picture_list"] = [report_pic.to_dict() for report_pic in report_pics]
    # 找出所有团队成员
    model_groups = ReportGroup.query.filter_by(report_id=report_id).all()
    report_info["report_group_members"] = [MemberService.operator_detail_with_avter(member_group.member_id) for member_group in model_groups]
    return R.successData(report_info)


@report_api.route("/<int:report_id>/evaluation", methods=['PUT'])
@jwt_required()
def userEvaluateReport(report_id):
    """
    提交报障评价
    @param report_id: 报障id
    @param grade:评价等级 范围1-5
    @param user_id:用户id
    @return:  是否成功
    """
    req = request.get_json()

    evaluation = req.get("grade")
    user_id = req.get("user_id")

    user_info = PowerUserInfo.query.filter_by(id=user_id).first()
    if not user_info or user_info.status == 0:
        return R.validateFailedMsg("用户不存在")

    if evaluation not in [1, 2, 3, 4, 5]:
        return R.validateFailedMsg("无效的评价操作")

    report_info = ReportInfo.query.filter_by(id=report_id).first()
    if not report_info:
        return R.failedMsg("找不到报障单")

    if report_info.evaluate != -1:
        return R.failedMsg("你已经评价过啦")

    if report_info.user_id is not user_id:
        return R.failedMsg("不能评价此报障单")

    report_info.evaluate = evaluation
    db.session.add(report_info)
    db.session.commit()

    return R.success()


@report_api.route("/<int:report_id>/cancel", methods=['PUT'])
@jwt_required()
def cancelReport(report_id):
    """
    用户撤销报障
    :param report_id:报障id
    :param user_id:用户id
    :return: 操作结果
    """
    req = request.get_json()
    user_id = req.get("user_id")

    user_info = PowerUserInfo.query.filter_by(id=user_id).first()
    if not user_info or user_info.status == 0:
        return R.validateFailedMsg("无效用户")

    report_info = ReportInfo.query.filter_by(id=report_id).first()
    if not report_info:
        return R.failedMsg("找不到报障单")

    if report_info.status != ReportStatus.UNCONFIRMED.value:
        return R.failedMsg("不能撤销此报障，工作人员正在处理问题的路上啦，请耐心等待哟")

    report_info.status = ReportStatus.CANCELED.value
    db.session.add(report_info)
    db.session.commit()

    return R.success()
