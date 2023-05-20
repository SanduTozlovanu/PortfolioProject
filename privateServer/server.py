import configparser
import datetime
import functools
import os
import threading
from random import randint
from urllib.parse import urlencode

from pymongo import MongoClient

import jwt
import requests
from flask import make_response, request
from flask_cors import cross_origin
from requests import Response
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

from JWTHelper import JWTHandler
from privateServer import mailSender
from privateServer.app import db, create_app
from privateServer.app.models import User, Stock, Transaction, Portfolio

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), "config.ini"))
client = MongoClient(config.get("connection_strings", "MONGO_URL"))
mongodb = client['portfolio']
confirmations = mongodb['confirmations']
app = create_app()
app.config["SECRET_KEY"] = config.get("keys", "SECRET_KEY")
jwt_helper = JWTHandler(app.config["SECRET_KEY"])
app.config["JWT"] = jwt_helper.create_jwt_token("PrivateServer")
BASE_PUBLIC_ENDPOINT = "http://127.0.0.1:6000/api/"
BASE_PREDICTION_ENDPOINT = "http://127.0.0.1:6001/api/"


def get_jwt_token():
    if not jwt_helper.is_token_valid(app.config["JWT"]):
        app.config["JWT"] = jwt_helper.create_jwt_token("PrivateServer")
    return app.config["JWT"]


def make_request(method: str, url: str, json=None, request=None):
    headers = {"Authorization": get_jwt_token()}
    if request:
        query_string = "?" + urlencode(request.args)
        url += query_string
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


def return_response(response: Response):
    return make_response(response.text, response.status_code)


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


@app.route('/user/login', methods=['POST'])
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
            return make_response({"token": jwt_helper.create_jwt_token(user_email),
                                  "name": user.name}, 200)
        else:
            return make_response("The account hasn't been confirmed yet", 403)

    except:
        return make_response("Internal server error", 500)


@app.route('/user/register', methods=['POST'])
@cross_origin()
def register():
    try:
        user_email = request.json["email"]
        user_password = request.json['password']
        user_name = request.json['name']
        new_user = User(email=user_email, password=user_password, name=user_name, type="user", status=False)
        random_number = randint(10000, 99999)
        confirmations.insert_one({'code': random_number, "email": user_email})
        mailSender.send_mail(user_email, random_number)
    except:
        return make_response("Wrong data", 400)
    try:
        db.session.add(new_user)
        db.session.commit()
        return make_response(new_user.as_dict(), 201)
    except SQLAlchemyError:
        return make_response("<h1>This user already exists</h1>", 409)
    except Exception as exc:
        print(exc)
        return make_response("<h1>Internal Server error</h1>", 500)


@app.route('/user/confirm/resend', methods=['POST'])
@cross_origin()
def confirm_resend():
    try:
        user_email = request.json["email"]
        random_number = randint(10000, 99999)
        confirmations.insert_one({'code': random_number, "email": user_email})
        mailSender.send_mail(user_email, random_number)
    except:
        return make_response("Wrong data", 400)
    try:
        return make_response("Succesfully sent", 200)
    except Exception as exc:
        print(exc)
        return make_response("<h1>Internal Server error</h1>", 500)


@app.route('/user/confirm', methods=['POST'])
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
                    if user.status:
                        return make_response("User email is already confirmed!", 400)
                    user.status = True
                    new_portfolio = Portfolio(user_id=user.id, money=10000)
                    db.session.add(new_portfolio)
                    db.session.commit()
                    return make_response("Succesfully confirmed", 200)
        if not found_email:
            return make_response("Email not found!", 404)
        if not found_code:
            return make_response("Invalid Code!", 400)
    except:
        return make_response("Server error", 500)


@app.route('/portfolio/stock/buy', methods=['POST'])
@cross_origin()
@jwt_required
def buy_stock():
    try:
        ticker = request.json["ticker"]
        price = request.json["price"]
        quantity = request.json["quantity"]
        email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
        portfolio = Portfolio.get_portfolio(email)
        if quantity * price > portfolio.money:
            return make_response("Not enough funds to buy stock", 400)
        stock: Stock = Stock.query.filter(and_(Stock.ticker == ticker, Stock.portfolio_id == portfolio.id)).first()
        if stock is None:
            new_stock = Stock(ticker=ticker, portfolio_id=portfolio.id, medium_buy_price=price,
                              buy_date=datetime.datetime.now(), quantity=quantity)
            db.session.add(new_stock)
        else:
            stock.medium_buy_price = (stock.medium_buy_price * stock.quantity + price * quantity) / (
                    quantity + stock.quantity)
            stock.quantity += quantity
        new_transaction = Transaction(portfolio_id=portfolio.id, ticker=ticker, piece_price=price,
                                      date=datetime.datetime.now(),
                                      quantity=quantity, is_buy=True)
        portfolio.money -= new_transaction.total_price
        db.session.add(new_transaction)
        db.session.commit()
        return make_response("Succesfully bought", 200)
    except Exception as exc:
        print(exc)
        return make_response("Server Error", 500)


@app.route('/portfolio/stock/sell', methods=['POST'])
@cross_origin()
@jwt_required
def sell_stock():
    try:
        ticker = request.json["ticker"]
        price = request.json["price"]
        quantity = request.json["quantity"]
        email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
        portfolio = Portfolio.get_portfolio(email)
        stock: Stock = Stock.query.filter(and_(Stock.ticker == ticker, Stock.portfolio_id == portfolio.id)).first()
        if stock is None:
            return make_response("You dont have this stock!", 404)
        else:
            if stock.quantity < quantity:
                return make_response("You dont have enough of this stock!", 400)
            stock.quantity -= quantity
            if stock.quantity == 0:
                db.session.delete(stock)
        new_transaction = Transaction(portfolio_id=portfolio.id, ticker=ticker, piece_price=price,
                                      date=datetime.datetime.now(),
                                      quantity=quantity, is_buy=False)
        portfolio.money += new_transaction.total_price
        db.session.add(new_transaction)
        db.session.commit()
        return make_response("Succesfully sold", 200)
    except Exception as exc:
        print(exc)
        return make_response("Server Error", 500)


@app.route('/stock/details/<company_ticker>', methods=['GET'])
@cross_origin()
def get_company_details(company_ticker):
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/details/" + company_ticker))


@app.route('/stock/chart/price/<company_ticker>', methods=['GET'])
@cross_origin()
def get_company_price_chart(company_ticker):
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/chart/price/" + company_ticker))


@app.route('/stock/chart/prediction/<company_ticker>', methods=['GET'])
@cross_origin()
def get_company_price_prediction(company_ticker):
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/chart/prediction/" + company_ticker))


@app.route('/stock/chart/revenue/<company_ticker>', methods=['GET'])
@cross_origin()
def get_company_revenue_data(company_ticker):
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/chart/revenue/" + company_ticker))


@app.route('/stock/finances/<company_ticker>', methods=['GET'])
@cross_origin()
def get_company_finances(company_ticker):
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/finances/" + company_ticker))


@app.route('/stock/statement/last/<company_ticker>', methods=['GET'])
@cross_origin()
def get_company_financial_statement(company_ticker):
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/statement/last/" + company_ticker))


@app.route('/stock/price/<company_list>', methods=['GET'])
@cross_origin()
def get_companies_price(company_list):
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/price/" + company_list))


@app.route('/stock/search/<company>', methods=['GET'])
@cross_origin()
def search_companies(company):
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/search/" + company))


@app.route('/stock/search', methods=['GET'])
@cross_origin()
def search_query():
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/search", request=request))


def app_run():
    app.run(debug=True, port=5999, use_reloader=False)


if __name__ == "__main__":
    thread = threading.Thread(target=app_run, daemon=True)
    thread.start()
    thread.join()
