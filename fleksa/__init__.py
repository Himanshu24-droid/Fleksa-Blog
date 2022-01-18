import os
from flask import Flask
from flask_migrate import Migrate
from .extensions import db,login_manager
from .models import User, Post


def create_app(config_file='settings.py'):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_pyfile(config_file)
    
    migrate = Migrate(app,db)

    from .extensions import db
    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    from .db import create_tables
    app.cli.add_command(create_tables)

    return app
