# coding=utf-8
import os
from app import create_app, db
from app.models import User, Role
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell


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
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade
    from app.models import Role, User

    # migrate database to latest revision
    upgrade()


if __name__ == '__main__':
    manager.run()
    # app.run()

