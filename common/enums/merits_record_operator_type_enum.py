
from enum import Enum


class MeritsOperatorTypeEnum(Enum):
    """
    绩效记录操作者的类型枚举
    """

    # 系统
    SYSTEM = 0
    # 人工
    ARTIFICIAL = 1

    MAP = {
        0: "系统",
        1: "人工"
    }


