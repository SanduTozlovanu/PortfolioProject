import configparser
import functools
import os
import threading
from random import randint
from pymongo import MongoClient

import jwt
import requests
from flask import make_response, request
from flask_cors import cross_origin
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

from JWTHelper import JWTHandler
from privateServer import mailSender
from privateServer.app import db, create_app
from privateServer.app.models import User

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), "config.ini"))
client = MongoClient(config.get("connection_strings", "MONGO_URL"))
mongodb = client['portfolio']
confirmations = mongodb['confirmations']
app = create_app()
app.config["SECRET_KEY"] = config.get("keys", "SECRET_KEY")
jwt_helper = JWTHandler(app.config["SECRET_KEY"])
app.config["JWT"] = jwt_helper.create_jwt_token("PrivateServer")
BASE_PUBLIC_ENDPOINT = "http://127.0.0.1:5000/"
BASE_PREDICTION_ENDPOINT = "http://127.0.0.1:5001/"

def get_jwt_token():
    try:
        jwt_helper.is_token_valid(app.config["JWT"])
    except jwt.ExpiredSignatureError:
        app.config["JWT"] = jwt_helper.create_jwt_token("PrivateServer")
        return app.config["JWT"]


def make_request(method: str, url: str, json=None):
    headers = {"Authorization": get_jwt_token()}
    if method == "GET":
        return requests.get(url, headers=headers)
    elif method == "POST":
        return requests.post(url, json=json, headers=headers)
    elif method == "PUT":
        return requests.put(url, json=json, headers=headers)
    elif method == "DELETE":
        return requests.delete(url, headers=headers)
    else:
        return None


def jwt_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if request.headers:
            request_jwt = request.headers.get("Authorization")
        else:
            return make_response("Please provide the Authorization header", 403)
        # Check if jwt is correct and valid
        try:
            if jwt_helper.is_token_valid(request_jwt):
                user = User.query.filter(User.email == jwt_helper.get_mail_from_jwt(request_jwt)).first()
                if user is None:
                    return make_response("Invalid Credentials", 401)
                return func(*args, **kwargs)
            else:
                return make_response("The provided jwt is invalid", 403)

        except jwt.ExpiredSignatureError:
            return make_response("The provided jwt is expired", 403)

    return decorator


@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    try:
        user_email = request.json["email"]
        user_password = request.json['password']
        user = User.query.filter(and_(User.email == user_email, User.password == user_password)).first()
        if user is None:
            return make_response("Invalid Credentials", 401)
        user: User
        if user.status:
            return make_response({"token": jwt_helper.create_jwt_token(user_email)}, 200)
        else:
            return make_response("The account hasn't been confirmed yet", 403)

    except:
        return make_response("Internal server error", 500)


@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    try:
        user_email = request.json["email"]
        user_password = request.json['password']
        new_user = User(email=user_email, password=user_password, type="user", status=False)
        random_number = randint(10000, 99999)
        confirmations.insert_one({'code': random_number, "email": user_email})
        mailSender.send_mail(user_email, random_number)
    except:
        return make_response("Wrong data", 400)
    try:
        db.session.add(new_user)
        db.session.commit()
        return make_response(new_user.as_dict(), 201)
    except SQLAlchemyError as exception:
        return make_response("<h1>This user already exists</h1>", 409)
    except Exception as exc:
        print(exc)
        return make_response("<h1>Internal Server error</h1>", 500)


@app.route('/confirm', methods=['POST'])
@cross_origin()
def confirm():
    try:
        user_email = request.json["email"]
        user_code = int(request.json['code'])
        found_code = False
        found_email = False
        for confirmation in confirmations.find({'email': user_email}):
            found_email = True
            if confirmation['email'] == user_email:
                if confirmation['code'] == user_code:
                    user = User.query.filter(User.email == user_email).first()
                    if user is None:
                        return make_response("Invalid email", 401)
                    user: User
                    user.status = True
                    db.session.commit()
                    return make_response("Succesfully confirmed", 200)
        if not found_email:
            return make_response("Email not found!", 404)
        if not found_code:
            return make_response("Invalid Code!", 400)
    except:
        return make_response("Server error", 500)


def app_run():
    app.run(debug=True, port=4999, use_reloader=False)


if __name__ == "__main__":
    thread = threading.Thread(target=app_run, daemon=True)
    thread.start()
    thread.join()
