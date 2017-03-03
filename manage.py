# coding=utf-8
import os
from app import create_app, db
from app.models import User, Role
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User,Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def init_db():
    db.drop_all()
    db.create_all()

@manager.command
def create_db():

    u = User()
    # r = Role()


    u.email = '8112@qq.com'
    u.username = 'yehai2'
    u.password = '123456'
    u.role_id = 2
    # r.name = 'Teacher'
    # u.role = r




    db.session.add(u)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
    # app.run()

