from enum import Enum


class ReportStatus(Enum):



    """
    报账单状态 0：待确认1：待处理2：已处理3：已完成4：已拒绝 5：用户已取消
    """

    UNCONFIRMED = 0
    CONFIRMED = 1
    HANDLED = 2
    FINISHED = 3
    REJECTED = 4
    CANCELED = 5

    MAP = {
        0: "待确认",
        1: "待处理",
        2: "已处理",
        3: "已完成",
        4: "已拒绝",
        5: "用户已取消"
    }

    @staticmethod
    def value_list():
        value_list = list(map(lambda c: c.value, ReportStatus))
        value_list.pop()
        return value_list

    @staticmethod
    def name_list():
        name_list = list(map(lambda c: c.name, ReportStatus))
        name_list.pop()
        return name_list
