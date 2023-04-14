# coding:utf-8

from application_initializer import create_application, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# 创建flask的应用对象
app = create_application("develop")

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


if __name__ == '__main__':
    manager.run()
