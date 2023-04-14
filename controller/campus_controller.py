from flask import Blueprint, request
from common.api.common_result import R
from common.models.campus_carousel import CampusCarousel


campus_api = Blueprint("campus", __name__)


@campus_api.route("/<int:campus_id>/carousels", methods=['GET'], strict_slashes=False)
def listAllCarousel(campus_id):
    """
    获取校区轮播图
    @param campus_id: 校区id
    @return: 轮播图列表
    """
    campus_c_infos = CampusCarousel.query.filter_by(campus_id=campus_id).all()
    return R.successData([campus_c_info.to_dict() for campus_c_info in campus_c_infos])

