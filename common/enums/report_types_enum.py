from enum import Enum


class ReportTypes(Enum):
    """
    报账单类型
    """

    # 教师报障
    TEACHER = 0
    # 学生报障
    STUDENT = 1

    @staticmethod
    def value_list():
        return list(map(lambda c: c.value, ReportTypes))
    
    def get_type_name(idx):
        return "学生" if idx == ReportTypes.STUDENT.value else "老师"
    
