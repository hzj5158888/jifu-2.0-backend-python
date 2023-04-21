# 广药计服-ijf小程序与网站2.0

#### 环境配置

**1.创建虚拟环境**

python -m venv venv_demo

在当前目录下生成了一个名为venv_demo的虚拟环境文件夹

**2.激活虚拟环境**

windows：

进入到虚拟环境的scripts目录下

 venv_demo\scripts\activate或者activate.bat

Linux:

$ source venv_demo/bin/activate

**3.安装所需要的包**

pip install -r requirements.txt

#### 配置修改

config.py

### 数据库配置
0.  注意当前的模式是开发模式还是生成环境，两者要配置的位置不一样
1.  数据库的地址定义在./config/profile_config.py中的SQLALCHEMY_DATABASE_URI,格式是：协议+用户名:密码@主机IP/数据库名称
2.  设置好数据库服务器的地址、用户名(默认root、建议默认)、密码(默认为空)。
    * 修改密码请参考：https://blog.csdn.net/qq_40757240/article/details/118068317
3.  配置数据库。连接到数据库服务器，输入命令：'create database gdpujf_dev/gdpujf-prod(也可以换成你想要的名称)'创建数据库，然后在profile_config.py中配置好数据库名
4.  cd 当前目录下，执行'./configure.py develop resetdb initdb' (开发环境)，或'./configure.py product resetdb initdb'(生产环境)

#### 输出依赖文件
`pip3 install pipreqs`
`pipreqs ./ --encoding=utf-8`

#### 使用说明

1.  启动
    * python manage.py runserver(本地)

### API文档
[加入Postman团队](https://app.getpostman.com/join-team?invite_code=2c51a20b4f3884f4f196b3c4db22bba2&ws=9250807b-06bd-4673-bf00-979d2dafb360)

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/483c660ff1e9f19bd269#?env%5Bdev%5D=W3sia2V5IjoidXJsIiwidmFsdWUiOiJodHRwOi8vMTI3LjAuMC4xOjUwMDAiLCJlbmFibGVkIjp0cnVlfV0=)


### 加密算法
HMAC和Hash均以SHA-256为基础

time = unix时间戳(秒)

token = Hash({account}.{pwd})

challenge = HMAC({token}.{time},{time})

passwd = Hash({token}.{account}.{salt})

测试用户
|account|pwd|token|salt|passwd|
|-|-|-|-|-|
|test|123456|e32a2a744fea5e1ee3d02c1fd21316f6b24d331a423ba406c01fe77d2bd54327|haha|17913fd168c2122e1d754cbe49f786c25d760d8040f5169fd43d8b35b19162ff|

GET /demo/testLogin 获取测试登录url
