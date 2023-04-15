# coding:utf-8

from application_initializer import create_application, db

# 创建flask的应用对象
app = create_application("develop")

if __name__ == '__main__':
    app.run()