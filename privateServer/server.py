import configparser
from datetime import datetime, timedelta
import functools
import os
import threading
from random import randint
from urllib.parse import urlencode
from plotly import graph_objs as go
import traceback

from pymongo import MongoClient

import jwt
import requests
from flask import make_response, request, jsonify
from flask_cors import cross_origin
from requests import Response
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

from JWTHelper import JWTHandler
from privateServer import mailSender
from privateServer.DTOs.PieChartDto import PieChartDto
from privateServer.DTOs.PortfolioSelectDataDto import PortfolioSelectDataDto
from privateServer.DTOs.PortfolioStatsDto import PortfolioStatsDto
from privateServer.DTOs.TickerPriceDto import TickerPriceDto
from privateServer.DTOs.TransactionDto import TransactionDto
from privateServer.PortfolioAnalyser import PortfolioAnalyser
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
portfolio_analyser = PortfolioAnalyser()

app.config["JWT"] = jwt_helper.create_jwt_token("PrivateServer")
BASE_PUBLIC_ENDPOINT = "http://127.0.0.1:6000/api/"
BASE_PORTFOLIO_CREATOR_ENDPOINT = "http://127.0.0.1:6001/api/"


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
        money = request.json['money']
        created_on = datetime.now()
        if created_on.weekday() >= 5:
            created_on -= timedelta(days=2)
        else:
            created_on -= timedelta(days=1)
        new_user = User(email=user_email, password=user_password, name=user_name, type="user", status=False,
                        created_on=created_on)
        random_number = randint(10000, 99999)
        confirmations.insert_one({'code': random_number, "email": user_email})
        mailSender.send_mail(user_email, random_number)
    except:
        return make_response("Wrong data", 400)
    try:
        db.session.add(new_user)
        db.session.commit()
        inserted_user = User.query.filter(User.email == new_user.email).first()
        new_portfolio = Portfolio(user_id=inserted_user.id, money=money)
        db.session.add(new_portfolio)
        db.session.commit()
        return make_response(new_user.as_dict(), 201)
    except SQLAlchemyError as exc:
        return make_response("This user already exists", 409)
    except Exception as exc:
        print(exc)
        return make_response("Internal Server error", 500)


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
        return make_response("Internal Server error", 500)


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
                    db.session.commit()
                    return make_response("Succesfully confirmed", 200)
        if not found_email:
            return make_response("Email not found!", 404)
        if not found_code:
            return make_response("Invalid Code!", 400)
    except:
        return make_response("Server error", 500)


@app.route('/portfolio/select', methods=['GET'])
@cross_origin()
@jwt_required
def get_portfolio_select_data():
    try:
        email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
        portfolio = Portfolio.get_portfolio(email)
        tickers_to_return = []
        portfolio_select_data_list: list[Stock] = Stock.query.filter(
            Stock.portfolio_id == portfolio.id).all()
        company_list = ""
        for stock in portfolio_select_data_list:
            company_list += (stock.ticker + ",")
        company_list = company_list[:-1]
        response_json = make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/price/" + company_list).json()

        for stock in portfolio_select_data_list:
            tickers_to_return.append(
                PortfolioSelectDataDto(stock.ticker, stock.ticker, response_json[stock.ticker], stock.quantity))
        return make_response(jsonify([tickerSelectDto.__dict__ for tickerSelectDto in tickers_to_return]), 200)
    except Exception as exc:
        print(exc)
        return make_response("Internal server error", 500)


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
                              buy_date=datetime.now(), quantity=quantity)
            db.session.add(new_stock)
        else:
            stock.medium_buy_price = (stock.medium_buy_price * stock.quantity + price * quantity) / (
                    quantity + stock.quantity)
            stock.quantity += quantity
        portfolio.money -= (quantity * price)
        new_transaction = Transaction(portfolio_id=portfolio.id, ticker=ticker, piece_price=price,
                                      date=datetime.now(),
                                      quantity=quantity, is_buy=True, cash_after_transaction=portfolio.money)
        db.session.add(new_transaction)
        db.session.commit()
        return make_response("Succesfully bought", 200)
    except Exception as exc:
        print(exc)
        return make_response("Server Error", 500)


@app.route('/portfolio/stock/buy/batch', methods=['POST'])
@cross_origin()
@jwt_required
def buy_stock_batch():
    try:
        email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
        portfolio = Portfolio.get_portfolio(email)
        stock_list = request.json["stocks"]
        for stock in stock_list:
            quantity = stock["quantity"]
            price = stock["price"]
            ticker = stock["ticker"]
            if quantity * price > portfolio.money:
                return make_response("Not enough funds to buy stock", 400)
            stock: Stock = Stock.query.filter(and_(Stock.ticker == ticker, Stock.portfolio_id == portfolio.id)).first()
            if stock is None:
                new_stock = Stock(ticker=ticker, portfolio_id=portfolio.id, medium_buy_price=price,
                                  buy_date=datetime.now(), quantity=quantity)
                db.session.add(new_stock)
            else:
                stock.medium_buy_price = (stock.medium_buy_price * stock.quantity + price * quantity) / (
                        quantity + stock.quantity)
            stock.quantity += quantity
            portfolio.money -= (quantity * price)
            new_transaction = Transaction(portfolio_id=portfolio.id, ticker=ticker, piece_price=price,
                                          date=datetime.now(),
                                          quantity=quantity, is_buy=True, cash_after_transaction=portfolio.money)
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
        portfolio.money += (quantity * price)
        new_transaction = Transaction(portfolio_id=portfolio.id, ticker=ticker, piece_price=price,
                                      date=datetime.now(),
                                      quantity=quantity, is_buy=False, cash_after_transaction=portfolio.money)
        db.session.add(new_transaction)
        db.session.commit()
        return make_response("Succesfully sold", 200)
    except Exception as exc:
        print(exc)
        return make_response("Server Error", 500)


@app.route('/stock/personalised', methods=['GET'])
@cross_origin()
@jwt_required
def get_personalised_stocks():
    try:
        email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
        portfolio: Portfolio = Portfolio.get_portfolio(email)
        ticker_list = ""
        stock_list: list[Stock] = Stock.query.filter(Stock.portfolio_id == portfolio.id).all()
        if len(stock_list) > 0:
            for stock in stock_list:
                ticker_list += (stock.ticker + ",")
            ticker_list = ticker_list[:-1]
            return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/similar/" + ticker_list))
        return make_response([], 200)
    except Exception as exc:
        print(exc)
        return make_response("Server Error", 500)


@app.route('/portfolio/stock/performance', methods=['GET'])
@cross_origin()
@jwt_required
def get_portfolio_holdings():
    try:
        email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
        portfolio: Portfolio = Portfolio.get_portfolio(email)
        ticker_list = ""
        stock_list: list[Stock] = Stock.query.filter(Stock.portfolio_id == portfolio.id).all()
        list_to_return = []
        if len(stock_list) > 0:
            for stock in stock_list:
                ticker_list += (stock.ticker + ",")
            ticker_list = ticker_list[:-1]
            response_json = make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/price/" + ticker_list).json()
            for ticker in response_json:
                for stock in stock_list:
                    if stock.ticker == ticker:
                        list_to_return.append(TickerPriceDto(ticker, round(
                            (1 - stock.medium_buy_price / response_json[ticker]) * 100, 2)))
        return make_response(jsonify([tickerDto.__dict__ for tickerDto in list_to_return]), 200)
    except Exception as exc:
        print(exc)
        return make_response("Server Error", 500)


@app.route('/portfolio/chart/performance', methods=['GET'])
@cross_origin()
@jwt_required
def get_portfolio_performance_chart():
    try:
        email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
        portfolio = Portfolio.get_portfolio(email)
        transactions: list[Transaction] = Transaction.query.filter(Transaction.portfolio_id == portfolio.id).order_by(
            Transaction.date.asc()).all()
        user: User = User.query.filter(User.email == email).first()
        df = portfolio_analyser.create_chart_data(transactions, user.created_on, portfolio.money)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Value'], name="Stock Value"))
        fig.layout.update(xaxis_rangeslider_visible=True, showlegend=False)
        return make_response(fig.to_json(), 200)
    except Exception as exc:
        print(exc)
        return make_response("Server Error", 500)


@app.route('/portfolio/chart/holdings', methods=['GET'])
@cross_origin()
@jwt_required
def get_portfolio_pieChart():
    try:
        email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
        portfolio = Portfolio.get_portfolio(email)
        stocks: list[Stock] = Stock.query.filter(Stock.portfolio_id == portfolio.id).all()
        chart_data = [PieChartDto("CASH", portfolio.money)]
        for stock in stocks:
            chart_data.append(PieChartDto(stock.ticker, stock.quantity * stock.medium_buy_price))
        return make_response(jsonify([pie_dto.__dict__ for pie_dto in chart_data]), 200)
    except Exception as exc:
        print(exc)
        return make_response("Server Error", 500)


@app.route('/portfolio/stats', methods=['GET'])
@cross_origin()
@jwt_required
def get_portfolio_stats():
    try:
        email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
        portfolio = Portfolio.get_portfolio(email)
        transactions: list[Transaction] = Transaction.query.filter(Transaction.portfolio_id == portfolio.id).order_by(
            Transaction.date.asc()).all()
        user: User = User.query.filter(User.email == email).first()
        stocks: Stock = Stock.query.filter(Stock.portfolio_id == portfolio.id).all()
        stats: PortfolioStatsDto = portfolio_analyser.get_portfolio_stats(len(stocks), transactions, user.created_on,
                                                                          portfolio.money)
        return make_response(jsonify(stats.__dict__), 200)
    except Exception as exc:
        print(exc)
        return make_response("Server Error", 500)


@app.route('/news', methods=['GET'])
@cross_origin()
def get_latest_news():
    try:
        if "Authorization" in request.headers:
            email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
            portfolio = Portfolio.get_portfolio(email)
            stock_list: list[Stock] = Stock.query.filter(Stock.portfolio_id == portfolio.id).all()
            ticker_list = ""
            if len(stock_list) > 0:
                for stock in stock_list:
                    ticker_list += (stock.ticker + ",")
                ticker_list = ticker_list[:-1]
                return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "news/" + ticker_list))

        return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "news/all"))
    except Exception as exc:
        print(exc)
        return make_response("Server Error", 500)


@app.route('/transactions', methods=['GET'])
@cross_origin()
@jwt_required
def get_transaction_history():
    try:
        transaction_dto_list: list[TransactionDto] = []
        email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
        portfolio = Portfolio.get_portfolio(email)
        transactions: list[Transaction] = Transaction.query.filter(Transaction.portfolio_id == portfolio.id).order_by(
            Transaction.date.desc()).all()
        for transaction in transactions:
            transaction_dto_list.append(TransactionDto(id=len(transaction_dto_list) + 1, date=transaction.date,
                                                       is_buy=transaction.is_buy, piece_price=transaction.piece_price,
                                                       quantity=transaction.quantity, ticker=transaction.ticker))
        return make_response(jsonify([transaction_dto.__dict__ for transaction_dto in transaction_dto_list]), 200)
    except Exception as exc:
        print(exc)
        return make_response("Server Error", 500)


@app.route('/stock/select', methods=['GET'])
@cross_origin()
def get_companies_select_data():
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/select"))


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


@app.route('/stock/gainers', methods=['GET'])
@cross_origin()
def get_top_gainers():
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/gainers"))


@app.route('/stock/losers', methods=['GET'])
@cross_origin()
def get_top_losers():
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/losers"))


@app.route('/portfolio/create/equal_weight', methods=['GET'])
@jwt_required
@cross_origin()
def create_equal_weight_portfolio():
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    portfolio = Portfolio.get_portfolio(email)
    return return_response(
        make_request("GET", BASE_PORTFOLIO_CREATOR_ENDPOINT + "portfolio/create/equal_weight/" + str(portfolio.money)))


@app.route('/portfolio/create/weighted', methods=['GET'])
@jwt_required
@cross_origin()
def create_weighted_portfolio():
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    portfolio = Portfolio.get_portfolio(email)
    return return_response(
        make_request("GET", BASE_PORTFOLIO_CREATOR_ENDPOINT + "portfolio/create/weighted/" + str(portfolio.money)))


@app.route('/portfolio/create/momentum', methods=['GET'])
@jwt_required
@cross_origin()
def create_quantitative_momentum_portfolio():
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    portfolio = Portfolio.get_portfolio(email)
    return return_response(
        make_request("GET", BASE_PORTFOLIO_CREATOR_ENDPOINT + "portfolio/create/momentum/" + str(portfolio.money)))


@app.route('/portfolio/create/value', methods=['GET'])
@jwt_required
@cross_origin()
def create_quantitative_value_portfolio():
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    portfolio = Portfolio.get_portfolio(email)
    return return_response(
        make_request("GET", BASE_PORTFOLIO_CREATOR_ENDPOINT + "portfolio/create/value/" + str(portfolio.money)))


@app.route('/portfolio/create/value_momentum', methods=['GET'])
@jwt_required
@cross_origin()
def create_quantitative_value_momentum_portfolio():
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    portfolio = Portfolio.get_portfolio(email)
    return return_response(
        make_request("GET",
                     BASE_PORTFOLIO_CREATOR_ENDPOINT + "portfolio/create/value_momentum/" + str(portfolio.money)))


def app_run():
    app.run(debug=True, port=5999, use_reloader=False)


if __name__ == "__main__":
    thread = threading.Thread(target=app_run, daemon=True)
    thread.start()
    thread.join()
