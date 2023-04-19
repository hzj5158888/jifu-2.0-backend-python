from application_initializer import db
from common.models.campus_info import CampusInfo
from common.models.campus_dept_info import CampusDeptInfo
from common.models.campus_carousel import CampusCarousel
from common.models.invite_code import InviteCode
from common.models.campus_system_info import CampusSystemInfo
from common.models.admin import Admin

def init_campus_info_gz():
    # 大学城
    campus_info = CampusInfo()
    campus_info.id = 1
    campus_info.name = '大学城校区'
    campus_info.img_url = 'https://www.gdpu.edu.cn/__local/0/E5/14/6DC0A17590A81A3F84E7F05D36E_E625EFC6_1504B.jpg'
    campus_info.introduction = '广东药科大学广州校区大学城校园'
    campus_info.address = '广东省广州市大学城外环东路280号'
    campus_info.phone = '020-39352060'
    campus_info.email = 'yuanban@gdpu.edu.cn'
    campus_info.status = 1
    db.session.add(campus_info)
    db.session.commit()


def init_campus_dept_info_gz():
    # 大学城
    
    name_list = [
        '技术部',
        '网络部',
        '策划部',
    ]
    
    for name in name_list:
        campus_dept_info = CampusDeptInfo()
        campus_dept_info.campus_id = 1 # 大学城
        campus_dept_info.name = name
        campus_dept_info.full_name = "计服" + name
        campus_dept_info.remark = 'null'
        db.session.add(campus_dept_info)
    
    db.session.commit()
    
    
def init_campus_carousel_gz():
    url_list = [
        'https://www.gdpu.edu.cn/__local/3/91/16/FE18C8117961C0681466A899FED_F116EFF1_13CFF.jpg',
        'https://www.gdpu.edu.cn/__local/E/EB/FF/3D3637396EB3AD5B8815443C248_8B726FA6_11041.jpg',
        'https://www.gdpu.edu.cn/__local/0/64/84/750503D77058E3E13C2923FFF6F_6EB4BE6C_27639.jpg',
        'https://www.gdpu.edu.cn/__local/3/76/B6/F56F5A70E7C1BF03124C1285070_0A795EE9_12FA6.jpg'
    ]
    
    for url in url_list:
        campus_carousel = CampusCarousel()
        campus_carousel.campus_id = 1 # 大学城
        campus_carousel.url = url
        db.session.add(campus_carousel)
    
    db.session.commit()
    

def init_campus_system_info_gz():
    # 大学城
    
    campus_system_info = CampusSystemInfo()
    campus_system_info.campus_id = 1
    campus_system_info.report_status = 1
    campus_system_info.report_content = '服务已下线'
    campus_system_info.apply_status = 1
    campus_system_info.apply_content = '服务已下线'
    campus_system_info.report_student_size = 100
    campus_system_info.report_teacher_size = 100
    campus_system_info.student_report_basic = 10
    campus_system_info.teacher_report_basic = 10
    db.session.add(campus_system_info)
    db.session.commit()
    

def init_invite_code_gz():
    dept_list = CampusDeptInfo.query.filter_by(campus_id = 1).all()
    
    for dept in dept_list:
        invite_code = InviteCode()
        invite_code.code = '123456789'
        invite_code.campus_id = 1
        invite_code.dept_id = dept.id
        db.session.add(invite_code)

    db.session.commit()
    
    
def init_administrator_gz():
    dept_list = CampusDeptInfo.query.filter_by(campus_id = 1).all()
    
    for dept in dept_list:
        admin = Admin()
        admin.invite_code = 'admin'
        admin.campus_id = 1
        admin.dept_id = dept.id
        admin.member_id = 0
        db.session.add(admin)

    db.session.commit()
    
    
def init_db_gz():
    init_campus_info_gz()
    init_campus_dept_info_gz()
    init_campus_carousel_gz()
    init_campus_system_info_gz()
    init_invite_code_gz()
    init_administrator_gz()