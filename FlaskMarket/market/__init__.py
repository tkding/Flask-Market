from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy # sqlite3

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db" # URI = Uniform Resource Identifier
app.config["SECRET_KEY"] = "29d28d719f0820b682056ba1" # for CSRF protection
db = SQLAlchemy(app)

app.app_context().push()

from market import routes
