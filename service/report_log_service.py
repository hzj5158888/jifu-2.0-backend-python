"""
记录对报账单的操作
"""
from application_initializer import db
from common.models.report_info import ReportInfo
from common.models.report_record_log import ReportRecordLog
from common.api.system_assert import Assert
from common.enums.report_status_enum import ReportStatus
from common.enums.report_operate_types_enum import ReportRecordLogTypes
from service.member_service import MemberService
from service.report_push_service import ReportPushService


class ReportLogService:

    def __init__(self, record_type, report_id, member_id, content):
        """

        @param record_type: 操作类型 见common.enums.report_operate_types_enum.py
        @param report_id: 报障单id
        @param member_id: 职员id
        @param content: 记录内容
        """
        self.record_type = record_type
        self.report_id = report_id
        self.member_id = member_id
        self.content = content

    def insertReportRecordLog(self):
        """
        插入报障操作记录
        """
        model_info_change = ReportRecordLog()
        model_info_change.operator = self.member_id
        model_info_change.report_id = self.report_id
        model_info_change.content = self.content
        model_info_change.type = self.record_type
        db.session.add(model_info_change)
        db.session.commit()

    @staticmethod
    def insertChangeStatusRecordLog(report_id, member_id, new_status):
        """
        往保障操作记录表插入状态更改记录
        @param report_id: 报障单id
        @param member_id: 职员id
        @param new_status: 修改的状态

        """
        status_change_term = "将报障单状态从{origin_status}修改为{new_status}"
        report_info = ReportInfo.query.filter_by(id=report_id).first()
        if not report_info:
            Assert.fail("报障单不存在")

        status_change_term = status_change_term \
            .format(origin_status=ReportStatus.MAP.value[report_info.status],
                    new_status=ReportStatus.MAP.value[new_status])

        change_log_service = ReportLogService(ReportRecordLogTypes.CHANGE_STATUS.value, report_id, member_id,
                                              status_change_term)
        change_log_service.insertReportRecordLog()
        
    @staticmethod
    def insertChangeNoteRecordLog(report_id, member_id, note):
        """
        往保障操作记录表插入新增备注更改记录
        @param report_id: 报障单id
        @param member_id: 职员id
        @param note: 备注内容

        """
        status_note_term = "新增备注：{note}"
        report_info = ReportInfo.query.filter_by(id=report_id).first()
        if not report_info:
            Assert.fail("报障单不存在")

        status_note_term = status_note_term.format(note=note)

        change_log_service = ReportLogService(ReportRecordLogTypes.CHANGE_NOTE.value, report_id, member_id,
                                              status_note_term)
        change_log_service.insertReportRecordLog()

    @staticmethod
    def insertUnableHandlerRecordLog(report_id, member_id, unable_reason):
        """
        往保障操作记录表插入新增无法处理原因更改记录
        @param report_id: 报障单id
        @param member_id: 职员id
        @param unable_reason: 无法处理原因

        """
        unable_handle_term = "更改无法处理原因：{unable_reason}"
        report_info = ReportInfo.query.filter_by(id=report_id).first()
        if not report_info:
            Assert.fail("报障单不存在")

        unable_handle_term = unable_handle_term.format(unable_reason=unable_reason)

        change_log_service = ReportLogService(ReportRecordLogTypes.CHANGE_UNABLE_REASON.value, report_id, member_id,
                                              unable_handle_term)
        change_log_service.insertReportRecordLog()

    @staticmethod
    def insertChangeGroupRecordLog(report_id, member_id, new_group_member_id):
        """
        往保障操作记录表插入团队更改记录
        @param report_id: 报障单id
        @param member_id: 职员id
        @param new_group_member_id: 新加入的团队队员id

        """
        group_change_term = "团队更变：邀请了{member_nickname}进入报障处理团队"
        report_info = ReportInfo.query.filter_by(id=report_id).first()
        if not report_info:
            Assert.fail("报障单不存在")

        # 获取新加入的团队队员俗称
        member_nickname = MemberService.getMemberNickName(new_group_member_id)

        group_change_term = group_change_term.format(member_nickname=member_nickname)

        change_log_service = ReportLogService(ReportRecordLogTypes.CHANGE_GROUP.value, report_id, member_id,
                                              group_change_term)
        change_log_service.insertReportRecordLog()
