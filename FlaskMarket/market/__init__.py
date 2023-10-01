from flask import Flask
from flask_sqlalchemy import SQLAlchemy # sqlite3
from flask_bcrypt import Bcrypt # for password hashing
from flask_login import LoginManager # for login management

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db" # URI = Uniform Resource Identifier
app.config["SECRET_KEY"] = "29d28d719f0820b682056ba1" # for CSRF protection
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login" # decorator
login_manager.login_message_category = "info" # bootstrap class

app.app_context().push()

from market import routes
