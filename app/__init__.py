# app>__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'authentication.do_the_login'
login_manager.session_protection = 'strong'
bcrypt = Bcrypt()


def create_app(config_type):
    app = Flask(__name__)
    # Get the config file name
    # The run.py call this function so os.getcwd() return root folder
    configuration = os.path.join(os.getcwd(), 'config', config_type + '.py')
    app.config.from_pyfile(configuration)
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # YOU HAVE TO REGISTER ALL BLUEPRINTS HERE!!!
    from app.blog import main
    app.register_blueprint(main)

    from app.book import book
    app.register_blueprint(book)

    from app.auth import authentication
    app.register_blueprint(authentication)

    from app.misc import misc
    app.register_blueprint(misc)

    from app.sched import appointment
    app.register_blueprint(appointment)

    return app



