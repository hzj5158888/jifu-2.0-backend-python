#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/11/25 10:25
@note     
"""
import requests
import json
from common.api.system_assert import Assert


class WxApiUtil:

    @staticmethod
    def is_fail(ret):
        """
        判断微信API是否执行失败
        """
        return 'errcode' in ret and ret['errcode'] != 0

    @staticmethod
    def getWxLoginClaim(code):
        """
        获取微信小程序wxLogin Api返回信息
        @param code: 微信登录code
        @return: openid， session_key
        """
        wx_login_url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code"

        from application import app
        result = requests.get(wx_login_url % (
            app.config['WX_APP_ID'], app.config['WX_APP_SECRET'], code))

        ret = result.json()
        if WxApiUtil.is_fail(ret):
            Assert.fail("微信登录失败")

        return ret['openid'], ret['session_key']

    @staticmethod
    def getOpenId(code):
        """
        获取微信小程序openid
        @param code:  微信登录code
        @return:  openid
        """
        open_id, session_key = WxApiUtil.getWxLoginClaim(code)
        return open_id

    @staticmethod
    def getMpAccessToken():
        """
        获取微信公众号AccessToken
        @return: AccessToken
        """
        wx_token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"

        from application import app
        result = requests.get(wx_token_url % (app.config['WX_MP_ID'], app.config['WX_MP_SECRET']))
        ret = result.json()
        if WxApiUtil.is_fail(ret):
            Assert.fail("微信公众号AccessToken获取失败")

        return ret['access_token']

    @staticmethod
    def getMpMaterialCounts():
        """
        获取微信公众号素材数量
        @return: obj
        """
        access_token = WxApiUtil.getMpAccessToken()

        result = requests.get(
            "https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token=%s" % access_token)
        result.encoding = 'utf-8'
        ret = result.json()

        if WxApiUtil.is_fail(ret):
            Assert.fail("微信公众号素材数量获取失败")

        return ret

    @staticmethod
    def getMpNews(offset=0, page_size=20):
        """
        获取微信公众号图文
        @return: obj
        """
        access_token = WxApiUtil.getMpAccessToken()

        result = requests.post(
            "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s" % access_token,
            data=json.dumps({'type': 'news', 'offset': offset, 'count': page_size}))
        result.encoding = 'utf-8'
        ret = result.json()

        if WxApiUtil.is_fail(ret):
            Assert.fail("微信公众号文章获取失败")

        return ret
