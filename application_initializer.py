# coding:utf-8

from flask import Flask
from config.profile_config import config_map
from config.jwt_config import init_jwt
from config.error_register_config import register_error
from flask_sqlalchemy import SQLAlchemy
from config.router_config import create_router

# 数据库初始化
db = SQLAlchemy()


# 初始化app
def create_application(config_name):
    """
    创建flask的应用对象
    :param config_name: str  配置模式的模式的名字 （"develop",  "product"）
    :return:
    """
    app = Flask(__name__)

    # 获取环境配置
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    # 使用app初始化db
    db.init_app(app)

    # 注册路由
    create_router(app)

    # 初始化jwt
    init_jwt(app)

    # 注册异常处理
    register_error(app)

    return app
