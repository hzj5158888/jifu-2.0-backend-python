#!/usr/bin/env python
# coding: utf-8
"""
千牛图片上传
@author   ChenDehua 2020/11/1 19:27
@note     
"""

from qiniu import Auth, put_data
from common.api.system_assert import Assert


class QiniuComponent:

    @staticmethod
    def uploadFile(file):
        """
        文件上传
        @param file: 文件数据
        @return: 文件链接url
        """
        from application import app
        access_key = app.config['QINIU_ACCESS_KEY']
        secret_key = app.config['QINIU_SECRET_KEY']
        bucket = app.config['QINIU_BUCKET']
        url = app.config['QINIU_URL']

        q = Auth(access_key, secret_key)

        token = q.upload_token(bucket)

        ret, info = put_data(token, None, data=file)

        if info.status_code != 200:
            Assert.fail("文件上传失败")

        return url + ret['hash']
