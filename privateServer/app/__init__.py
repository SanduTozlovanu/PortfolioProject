from os import path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
DB_NAME = "users.db"


def create_app():
    global app
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    global db
    db.init_app(app)
    create_database(app)
    return app


def create_database(app):
    global db
    if not path.exists('app/' + DB_NAME) or path.getsize('app/' + DB_NAME) < 10000:
        db.create_all(app=app)
        print('Created database!')
