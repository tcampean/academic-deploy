from flask import Flask, render_template, request, redirect
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

database = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.secret_key = 'thisisasecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MAI.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    login_manager.init_app(app)
    database.init_app(app)
    migrate.init_app(app)
    bcrypt.init_app(app)

    return app