from application_initializer import db
from common.models.campus_info import CampusInfo
from common.models.campus_dept_info import CampusDeptInfo
from common.models.campus_carousel import CampusCarousel
from common.models.invite_code import InviteCode
from common.models.campus_system_info import CampusSystemInfo
from common.models.admin import Admin

zs_campus_id = 2

def init_campus_info_zs():
    # 中山校区
    campus_info = CampusInfo()
    campus_info.id = zs_campus_id
    campus_info.name = '中山校区'
    campus_info.img_url = 'https://www.gdpu.edu.cn/__local/F/4A/DF/C2E56E8050380EC82AFB0FDCC77_3E61551C_1813D.jpg'
    campus_info.introduction = '广东药科大学中山校区'
    campus_info.address = '广东省中山市五桂山镇长命水大道9-13号'
    campus_info.phone = '020-39352060'
    campus_info.email = 'yuanban@gdpu.edu.cn'
    campus_info.status = 1
    db.session.add(campus_info)
    db.session.commit()


def init_campus_dept_info_zs():
    # 中山
    
    name_list = [
        '技术部',
        '网络部',
        '策划部',
    ]
    
    for name in name_list:
        campus_dept_info = CampusDeptInfo()
        campus_dept_info.campus_id = zs_campus_id # 中山
        campus_dept_info.name = name
        campus_dept_info.full_name = "计服" + name
        campus_dept_info.remark = 'null'
        db.session.add(campus_dept_info)
    
    db.session.commit()
    
    
def init_campus_carousel_zs():
    url_list = [
        'https://www.gdpu.edu.cn/__local/2/30/13/356E373A898E121770EC13C5388_B8ADC4A1_18DD8.jpg',
        'https://www.gdpu.edu.cn/__local/3/E6/9E/320ADEF4EE88763138582E3A325_A91C2C9F_1DA15.jpg',
        'https://www.gdpu.edu.cn/__local/1/7F/63/83F9E43DC4D11801D8C8BEC93A3_3CA98586_150DE.jpg',
        'https://www.gdpu.edu.cn/__local/5/9C/F8/DE890BAEE3180A36BCB618C1EAE_FA620821_C4A7F.jpg'
    ]
    
    for url in url_list:
        campus_carousel = CampusCarousel()
        campus_carousel.campus_id = zs_campus_id # 中山
        campus_carousel.url = url
        db.session.add(campus_carousel)
    
    db.session.commit()
    

def init_campus_system_info_zs():
    # 中山
    
    campus_system_info = CampusSystemInfo()
    campus_system_info.campus_id = zs_campus_id
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
    

def init_invite_code_zs():
    dept_list = CampusDeptInfo.query.filter_by(campus_id = zs_campus_id).all()
    
    for dept in dept_list:
        invite_code = InviteCode()
        invite_code.code = '123456789'
        invite_code.campus_id = zs_campus_id
        invite_code.dept_id = dept.id
        db.session.add(invite_code)

    db.session.commit()
    
    
def init_administrator_zs():
    dept_list = CampusDeptInfo.query.filter_by(campus_id = zs_campus_id).all()
    
    for dept in dept_list:
        admin = Admin()
        admin.invite_code = 'admin'
        admin.campus_id = zs_campus_id
        admin.dept_id = dept.id
        admin.invite_count = 1
        admin.member_id = 0
        db.session.add(admin)

    db.session.commit()
    
    
def init_db_zs():
    init_campus_info_zs()
    init_campus_dept_info_zs()
    init_campus_carousel_zs()
    init_campus_system_info_zs()
    init_invite_code_zs()
    init_administrator_zs()