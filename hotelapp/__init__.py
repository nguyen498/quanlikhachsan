import sys

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '812ey8ihbkxjoapi-210(&(U2(&(*&*('
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456789@localhost/hotelapp?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 8

db = SQLAlchemy(app=app)

login_manager = LoginManager(app)

if not '-m' in sys.argv:
    from hotelapp import index
