from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager
from flask_migrate import Migrate
from flask_mail import Mail
from market.config import Config
import os


db = SQLAlchemy()
# Must be render_as_batch while using sqlite
migrate = Migrate(db, render_as_batch=True)
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login_page'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from market.users.routes import users
    from market.posts.routes import posts
    from market.main.routes import main
    from market.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
