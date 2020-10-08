import redis
import os
from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_oauthlib.provider import OAuth2Provider
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# import pickle

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'redis'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['USER_APP_NAME'] = "CorrectOrder App"  # Shown in and email templates and page footers
app.config['USER_ENABLE_EMAIL'] = False  # Disable email authentication
app.config['USER_ENABLE_USERNAME'] = True  # Enable username authentication
app.config['USER_REQUIRE_RETYPE_PASSWORD'] = False  # Simplify register form
app.config['USER_LOGIN_URL'] = '/user-login'
app.config['USER_LOGOUT_URL'] = '/user-logout'
app.config['USER_REGISTER_URL'] = '/user-register'
oauth = OAuth2Provider(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'userLogin'
login_manager.logout_view = 'userLogin'
Session(app)


from . import routes
# from . import talech_oauth

