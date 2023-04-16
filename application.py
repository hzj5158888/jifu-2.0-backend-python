# coding:utf-8
import sys

from application_initializer import create_application, db

# 创建flask的应用对象
app = create_application("develop")

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'createdb':
        with app.app_context():
            db.create_all()
    elif len(sys.argv) == 2 and sys.argv[1] == 'resetdb':
        with app.app_context():
            db.drop_all()
            db.create_all()
    
    app.run()