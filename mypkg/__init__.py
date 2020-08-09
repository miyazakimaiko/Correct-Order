import redis
from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# import pickle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'redis'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['USER_APP_NAME'] = "CorrectOrder App"  # Shown in and email templates and page footers
app.config['USER_ENABLE_EMAIL'] = False  # Disable email authentication
app.config['USER_ENABLE_USERNAME'] = True  # Enable username authentication
app.config['USER_REQUIRE_RETYPE_PASSWORD'] = False  # Simplify register form
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'userLogin'
login_manager.logout_view = 'userLogin'
Session(app)

from . import routes