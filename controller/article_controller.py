from flask import Blueprint, request

from common.api.common_page import CommonPage
from common.api.common_result import R
from common.models.article import Article

article_api = Blueprint("article", __name__)


@article_api.route("/count", methods=["GET"])
def get_count():
    '''
    获取文章总数
    '''
    return R.successData(len(Article.query.all()))


@article_api.route("/", methods=['GET'])
def listArticles():
    """
    分页获取文章
    @param: page_size 页大小(default:15)
    @param: page_num 页码(default:1)
    @return: 报障数据列表
    """
    req = request.args

    page_size = int(req['page_size']) if ('page_size' in req and req['page_size']) else 15
    page_num = int(req['page_num']) if ('page_num' in req and req['page_num']) else 1

    report_infos = Article.query.filter_by().order_by(Article.gmt_create.desc()).paginate(page=page_num, per_page=page_size)
    page_result = CommonPage.restPage(report_infos)

    return R.successData(page_result)
