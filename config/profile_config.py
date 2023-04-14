# coding:utf-8


class ProfileConfig(object):
    # 不同环境配置信息

    # 数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLACHEMY_ECHO = False
    # 使用返回的json数据可以用中文显示
    JSON_AS_ASCII = False


class DevelopmentProfileConfig(ProfileConfig):
    """开发模式的配置信息"""
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:gdpujf2021@39.108.228.165:3306/gdpujf-dev"
    DEBUG = True
    PORT = 3307
    # 七牛云配置
    QINIU_ACCESS_KEY = "MfIg6EPzU2Hn9dnjYqpG4a8E5ySoZ1QfHs-30N9L"
    QINIU_SECRET_KEY = "KzhMUTzHXHRLq-HhjzJFfm2_d6qq50MEKL9zAP7k"
    QINIU_BUCKET = "gdpujf2021"
    QINIU_URL = "https://file.gdpujf.com/"
    WX_APP_ID = "wxb19cb690caafbecc"
    WX_APP_SECRET = "5e1f0457090ffbdf05c4cbc0486652b2"
    WX_MP_ID = "wx1245e18904d67a4a"
    WX_MP_SECRET = "d5312e328fc8a6ea35732477d3b13012"


class ProductionProfileConfig(ProfileConfig):
    """生产环境配置信息"""
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:gdpujf2021@39.108.228.165:3306/gdpujf-prod"
    DEBUG = False
    # 七牛云配置
    QINIU_ACCESS_KEY = "MfIg6EPzU2Hn9dnjYqpG4a8E5ySoZ1QfHs-30N9L"
    QINIU_SECRET_KEY = "KzhMUTzHXHRLq-HhjzJFfm2_d6qq50MEKL9zAP7k"
    QINIU_BUCKET = "gdpujf2021"
    QINIU_URL = "https://file.gdpujf.com/"
    WX_APP_ID = "wxb19cb690caafbecc"
    WX_APP_SECRET = "5e1f0457090ffbdf05c4cbc0486652b2"
    WX_MP_ID = "wx1245e18904d67a4a"
    WX_MP_SECRET = "d5312e328fc8a6ea35732477d3b13012"


config_map = {
    "develop": DevelopmentProfileConfig,
    "product": ProductionProfileConfig
}
