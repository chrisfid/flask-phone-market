from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'c1b2ab50c74d1c749c1943f4'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

from market import routes