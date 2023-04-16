import hashlib
import hmac
import math
import time
import uuid
import datetime

import requests
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import json
from application_initializer import db
from common.api.common_result import R
from common.models.campus_member import CampusMember
from common.models.power_user_info import PowerUserInfo
from common.models.power_user_oauth import PowerUserOauth
from common.utils.jwt_util import JwtUtil
from common.utils.wxapi_util import WxApiUtil
from service.user_service import UserService
auth_api = Blueprint("auth", __name__)


@auth_api.route("/login/password/<string:username>/<string:token>/<string:challenge>/<string:timestamp>", methods=['POST'])
def web_login(username, token, challenge, timestamp):
    info = PowerUserInfo.query.filter_by(account=username).first()

    if not info:
        return R.validateFailedMsg('用户名或者密码错误')

    pwd = hashlib.sha256((token + "." + username + "." + info.salt).encode()).hexdigest()

    if pwd != info.password:
        return R.validateFailedMsg('用户名或者密码错误')

    print(str(timestamp),(token + "." + timestamp))
    print(hmac.new(str(timestamp).encode(), (token + "." + timestamp).encode(), 'sha256').hexdigest())
    if hmac.new(str(timestamp).encode(), (token + "." + timestamp).encode(), 'sha256').hexdigest() != challenge:
        return R.validateFailedMsg('用户名或者密码错误')

    if math.fabs(int(time.time()) - int(timestamp)) >= 300:
        return R.validateFailedMsg('用户名或者密码错误')

    return JwtUtil.generate_token(info.id)

@auth_api.route("/login/wx", methods=['POST'], strict_slashes=False)
def wx_login():
    """
    微信小程序登录
    @param code: 小程序登陆api获取的code
    @param userInfo: 小程序获取的用户信息e.detail.rawData
    @return: access_token:登陆令牌 refresh_token:刷新令牌
    """
    req = request.get_json()
    code_wx = req.get("code")
    info_wx = json.loads(req.get("userInfo"))
    if not code_wx or not info_wx:
        return R.validateFailedMsg("登录失败")

    openid, session_key = WxApiUtil.getWxLoginClaim(code_wx)
    user_oauth = PowerUserOauth.query.filter_by(openid=openid).first()

    if not user_oauth:
        # 创建新用户

        nickname = info_wx['nickName'] if 'nickName' in info_wx else ''
        sex = info_wx['gender'] if 'gender' in info_wx else ''
        avatar = info_wx['avatarUrl'] if 'avatarUrl' in info_wx else ''

        user_info = PowerUserInfo()
        user_info.account = f"wx_{openid}"
        user_info.nick_name = nickname
        user_info.salt = str(uuid.uuid4()).replace('-','')
        user_info.avatar_url = avatar
        user_info.sex = sex
        db.session.add(user_info)
        db.session.commit()
        # 添加绑定关系
        user_oauth = PowerUserOauth()
        user_oauth.user_id = user_info.id
        user_oauth.openid = openid
        user_oauth.access_token = session_key
        user_oauth.type = "wechat"
        db.session.add(user_oauth)
        db.session.commit()

    user_id = user_oauth.user.id

    return JwtUtil.generate_token(user_id)


@auth_api.route("/refresh", methods=['GET'], strict_slashes=False)
#@jwt_refresh_token_required
def refresh():
    """
    刷新token
    @return: 新的access_token:登陆令牌 + 新的refresh_token:刷新令牌
    """
    user_id = get_jwt_identity()
    return JwtUtil.generate_token(user_id)


@auth_api.route("/info", methods=['GET'])
@jwt_required()
def getUserBasicInfo():
    """
    获取用户基本信息
    @return:
    """
    user_id = get_jwt_identity()

    user_info = PowerUserInfo.query.filter_by(id=user_id).first()
    result_user_info = {
        "account": user_info.account,
        "nick_name": user_info.nick_name,
        "real_name": user_info.real_name,
        "avatar_url": user_info.avatar_url,
        "sex": user_info.sex,
        "phone": user_info.phone,
        "birthday": user_info.birthday
    }

    return R.successData(result_user_info)

@auth_api.route("/info/<int:user_id>", methods=['PUT'])
@jwt_required()
def updateUserInfo(user_id):
    """
    修改用户基本信息
    @param (Query)userId 用户id
    @param (Body){
        "nick_name": user_info.nick_name,
        "real_name": user_info.real_name,
        "avatar_url": user_info.avatar_url,
        "sex": user_info.sex,
        "phone": user_info.phone,
        "birthday": user_info.birthday ex:2020-02-18 00:00:00
    }
    @return:
    """
    req = request.get_json()
    nick_name = req.get("nick_name")
    real_name = req.get("real_name")
    avatar_url = req.get("avatar_url")
    sex = req.get("sex")
    phone = req.get("phone")
    birthday = req.get("birthday")
    if (nick_name is None) or (avatar_url is None):
        return R.validateFailed()

    user_info = PowerUserInfo.query.filter_by(id=user_id).first()
    if not user_info:
        return R.failedMsg("找不到用户")

    user_info.nick_name = nick_name
    user_info.real_name = real_name
    user_info.avatar_url = avatar_url
    user_info.sex = sex
    user_info.phone = phone
    user_info.birthday = birthday
    db.session.add(user_info)
    db.session.commit()

    return R.success()
