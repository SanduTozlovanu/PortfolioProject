from os import path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
db = SQLAlchemy()
DB_NAME = "users.db"


cred = credentials.Certificate('firebase_secret.json')
firebase_admin.initialize_app(cred)
firestore_db = firestore.client()
firestore_setter = firestore_db.collection('userConfirmation').document('userConfirmationdoc')
firestore_getter = firestore_db.collection('userConfirmation')


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
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Created database!')
