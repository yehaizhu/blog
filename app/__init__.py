from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import config
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
db = SQLAlchemy()
bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    login_manager.init_app(app)
    config[config_name].init_app(app)
    bootstrap.init_app(app)

    # db.init_app(app)

    from auth import auth as auth_blueprint
    # from main import main as main_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # app.register_blueprint(main_blueprint, static_folder='static')

    return app