from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '812ey8ihbkxjoapi-210(&(U2(&(*&*('
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:nguyen498@localhost/hotelapp?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)
