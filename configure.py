import sys
import tools.init_database as InitDataBase

from application_initializer import create_application, db

if __name__ == '__main__':
    if 'develop' in sys.argv:
        app = create_application("develop")
    elif 'product' in sys.argv:
        app = create_application('product')
    else:
        print("请指定配置模式：开发环境/生成环境(develop/product)")
        sys.exit()
    
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