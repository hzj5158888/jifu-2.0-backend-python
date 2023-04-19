import sys
import tools.init_database as InitDataBase

from application_initializer import create_application, db

# 创建flask的应用对象
app = create_application("develop")

if __name__ == '__main__':
    if 'createdb' in sys.argv and 'resetdb' not in sys.argv:
        with app.app_context():
            db.create_all()
    elif 'resetdb' in sys.argv:
        with app.app_context():
            db.drop_all()
            db.create_all()
    
    if 'initdb' in sys.argv:
        with app.app_context():
            InitDataBase.init_db()