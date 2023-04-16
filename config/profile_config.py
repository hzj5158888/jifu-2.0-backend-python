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
    # 数据库 FIXME!
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:gdpujf2021@39.108.228.165:3306/gdpujf-dev"
    DEBUG = True
    PORT = 3307
    # 七牛云配置 FIXME!
    QINIU_ACCESS_KEY = "MfIg6EPzU2Hn9dnjYqpG4a8E5ySoZ1QfHs-30N9L"
    QINIU_SECRET_KEY = "KzhMUTzHXHRLq-HhjzJFfm2_d6qq50MEKL9zAP7k"
    QINIU_BUCKET = "gdpujf2021"
    QINIU_URL = "https://file.gdpujf.com/"
    # 微信
    WX_APP_ID = "wxb19cb690caafbecc"
    WX_APP_SECRET = "5e1f0457090ffbdf05c4cbc0486652b2"
    WX_MP_ID = "wx1245e18904d67a4a"
    WX_MP_SECRET = "d5312e328fc8a6ea35732477d3b13012"
    WX_QY_CORP_ID = "wwfa9562749e6077e6"
    WX_QY_CORP_SECRET = "dfwom_hGAas99K6dYdYg2B5rn6X5ZziAP1hoR7VevHc"
    WX_QY_AGENT_ID = 1000002
    WX_QY_PARTY_GZ = "4"
    WX_QY_PARTY_ZS = "6"
    WX_QY_PARTY_YF = ""
    WX_QY_PARTY_TEST = "10"
    WX_QY_TOKEN = "Vd6tkcB8FfU7MnRXFo"
    WX_QY_AES_KEY = "8Xm2nOfr4wKWvtaEKdO2HCiPftlrWa5bb5Lt21MfBak"


class ProductionProfileConfig(ProfileConfig):
    """生产环境配置信息"""
    # 数据库 FIXME!
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:gdpujf2021@39.108.228.165:3306/gdpujf-prod"
    DEBUG = False
    # 七牛云配置 FIXME!
    QINIU_ACCESS_KEY = "MfIg6EPzU2Hn9dnjYqpG4a8E5ySoZ1QfHs-30N9L"
    QINIU_SECRET_KEY = "KzhMUTzHXHRLq-HhjzJFfm2_d6qq50MEKL9zAP7k"
    QINIU_BUCKET = "gdpujf2021"
    QINIU_URL = "https://file.gdpujf.com/"
    # 微信
    WX_APP_ID = "wxb19cb690caafbecc"
    WX_APP_SECRET = "5e1f0457090ffbdf05c4cbc0486652b2"
    WX_MP_ID = "wx1245e18904d67a4a"
    WX_MP_SECRET = "d5312e328fc8a6ea35732477d3b13012"
    WX_QY_CORP_ID = "wwfa9562749e6077e6"
    WX_QY_CORP_SECRET = "dfwom_hGAas99K6dYdYg2B5rn6X5ZziAP1hoR7VevHc"
    WX_QY_AGENT_ID = 1000002
    WX_QY_PARTY_GZ = "4"
    WX_QY_PARTY_ZS = "6"
    WX_QY_PARTY_YF = ""
    WX_QY_PARTY_TEST = "10"
    WX_QY_TOKEN = "Vd6tkcB8FfU7MnRXFo"
    WX_QY_AES_KEY = "8Xm2nOfr4wKWvtaEKdO2HCiPftlrWa5bb5Lt21MfBak"


config_map = {
    "develop": DevelopmentProfileConfig,
    "product": ProductionProfileConfig
}
