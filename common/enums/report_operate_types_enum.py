from enum import Enum


class ReportRecordLogTypes(Enum):
    """
    报账单操作记录类型
    """

    # 添加备注
    CHANGE_NOTE = 0

    # 修改状态
    CHANGE_STATUS = 1

    # 更改无法处理原因
    CHANGE_UNABLE_REASON = 2

    # 团队更变
    CHANGE_GROUP = 3
