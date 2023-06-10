import configparser
import functools
import os
from urllib.parse import urlencode

import jwt
import requests
from flask import make_response, request, jsonify
from flask_cors import cross_origin
from pymongo import MongoClient
from requests import Response

from JWTHelper import JWTHandler
from exceptions import NotFoundException, ForbiddenException, UnauthorizedException, BadRequestException, \
    ConflictException
from privateServer.DTOs.PortfolioSelectDataDto import PortfolioSelectDataDto
from privateServer.DTOs.TickerPriceDto import TickerPriceDto
from privateServer.DTOs.TransactionDto import TransactionDto
from privateServer.PortfolioAnalyser import PortfolioAnalyser
from privateServer.app import create_app
from privateServer.app.models import User, Portfolio
from privateServer.controllers.ChartController import ChartController
from privateServer.controllers.PortfolioManagementController import PortfolioManagementController
from privateServer.controllers.PortfolioStatsController import PortfolioStatsController
from privateServer.controllers.UserController import UserController

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
        request_jwt = request.headers.get("Authorization")
        if not request_jwt:
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


def exception_catcher(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFoundException as exc:
            return make_response(exc.msg, 404)
        except BadRequestException as exc:
            return make_response(exc.msg, 400)
        except UnauthorizedException as exc:
            return make_response(exc.msg, 401)
        except ForbiddenException as exc:
            return make_response(exc.msg, 403)
        except ConflictException as exc:
            return make_response(exc.msg, 409)
        except Exception:
            return make_response("Internal server error", 500)

    return wrapper


def base_decorators(func):
    @cross_origin()
    @exception_catcher
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@app.route('/user/login', methods=['POST'])
@base_decorators
def login():
    user_email = request.json["email"]
    user_password = request.json['password']
    return UserController.login(user_email, user_password, jwt_helper)


@app.route('/user/register', methods=['POST'])
@base_decorators
def register():
    user_email = request.json["email"]
    user_password = request.json['password']
    user_name = request.json['name']
    money = request.json['money']
    response = UserController.register(user_email, user_password, user_name, money, confirmations)
    return make_response(response.as_dict(), 201)


@app.route('/user/reset', methods=['DELETE'])
@base_decorators
@jwt_required
def reset():
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    UserController.reset(email)
    return make_response("Successfully reseted", 200)


@app.route('/user/confirm/resend', methods=['POST'])
@base_decorators
def confirm_resend():
    UserController.confirm_resend(request.json["email"], confirmations)
    return make_response("Successfully sent", 200)


@app.route('/user/confirm', methods=['POST'])
@base_decorators
def confirm():
    user_email = request.json["email"]
    user_code = int(request.json['code'])
    UserController.confirm(user_email, user_code, confirmations)
    return make_response("Succesfully confirmed", 200)


@app.route('/portfolio/select', methods=['GET'])
@base_decorators
@jwt_required
def get_portfolio_select_data():
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    portfolio = Portfolio.get_portfolio(email)
    tickers_to_return = []
    portfolio_select_data_list = PortfolioStatsController.get_portfolio_stock_list(portfolio)
    if len(portfolio_select_data_list) == 0:
        return make_response([], 200)
    company_list = ""
    for stock in portfolio_select_data_list:
        company_list += (stock.ticker + ",")
    company_list = company_list[:-1]
    response_json = make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/price/" + company_list).json()

    for stock in portfolio_select_data_list:
        tickers_to_return.append(
            PortfolioSelectDataDto(stock.ticker, stock.ticker, response_json[stock.ticker], stock.quantity))
    return make_response(jsonify([tickerSelectDto.__dict__ for tickerSelectDto in tickers_to_return]), 200)


@app.route('/portfolio/stock/buy', methods=['POST'])
@base_decorators
@jwt_required
def buy_stock():
    ticker = request.json["ticker"]
    price = request.json["price"]
    quantity = request.json["quantity"]
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    portfolio = Portfolio.get_portfolio(email)
    PortfolioManagementController.buy_stock(ticker, price, quantity, portfolio)
    return make_response("Succesfully bought", 200)


@app.route('/portfolio/stock/buy/batch', methods=['POST'])
@base_decorators
@jwt_required
def buy_stock_batch():
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    portfolio = Portfolio.get_portfolio(email)
    stock_list = request.json["portfolioData"]
    PortfolioManagementController.buy_stock_batch(portfolio, stock_list)
    return make_response("Succesfully bought", 200)


@app.route('/portfolio/stock/sell', methods=['POST'])
@base_decorators
@jwt_required
def sell_stock():
    ticker = request.json["ticker"]
    price = request.json["price"]
    quantity = request.json["quantity"]
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    portfolio = Portfolio.get_portfolio(email)
    PortfolioManagementController.sell_stock(ticker, price, quantity, portfolio)
    return make_response("Succesfully sold", 200)


@app.route('/stock/personalised', methods=['GET'])
@base_decorators
@jwt_required
def get_personalised_stocks():
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    portfolio: Portfolio = Portfolio.get_portfolio(email)
    ticker_list = ""
    stock_list = PortfolioStatsController.get_portfolio_stock_list(portfolio)
    if len(stock_list) > 0:
        for stock in stock_list:
            ticker_list += (stock.ticker + ",")
        ticker_list = ticker_list[:-1]
        return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/similar/" + ticker_list))
    return make_response([], 200)


@app.route('/portfolio/stock/performance', methods=['GET'])
@base_decorators
@jwt_required
def get_portfolio_holdings():
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    portfolio: Portfolio = Portfolio.get_portfolio(email)
    ticker_list = ""
    stock_list = PortfolioStatsController.get_portfolio_stock_list(portfolio)
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


@app.route('/portfolio/chart/performance', methods=['GET'])
@base_decorators
@jwt_required
def get_portfolio_performance_chart():
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    fig = ChartController.get_portfolio_performance_chart(email, portfolio_analyser)
    return make_response(fig.to_json(), 200)


@app.route('/portfolio/chart/holdings', methods=['GET'])
@base_decorators
@jwt_required
def get_portfolio_pieChart():
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    portfolio = Portfolio.get_portfolio(email)
    chart_data = ChartController.get_portfolio_pieChart(portfolio)
    return make_response(jsonify([pie_dto.__dict__ for pie_dto in chart_data]), 200)


@app.route('/portfolio/stats', methods=['GET'])
@base_decorators
@jwt_required
def get_portfolio_stats():
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    stats = PortfolioStatsController.get_portfolio_stats(email, portfolio_analyser)
    return make_response(jsonify(stats.__dict__), 200)


@app.route('/news', methods=['GET'])
@base_decorators
def get_latest_news():
    if "Authorization" in request.headers:
        email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
        portfolio = Portfolio.get_portfolio(email)
        stock_list = PortfolioStatsController.get_portfolio_stock_list(portfolio)
        ticker_list = ""
        if len(stock_list) > 0:
            for stock in stock_list:
                ticker_list += (stock.ticker + ",")
            ticker_list = ticker_list[:-1]
            return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "news/" + ticker_list))

    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "news/all"))


@app.route('/transactions', methods=['GET'])
@base_decorators
@jwt_required
def get_transaction_history():
    transaction_dto_list: list[TransactionDto] = []
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    portfolio = Portfolio.get_portfolio(email)
    transactions = PortfolioStatsController.get_transaction_list(portfolio)
    for transaction in transactions:
        transaction_dto_list.append(TransactionDto(id=len(transaction_dto_list) + 1, date=transaction.date,
                                                   is_buy=transaction.is_buy, piece_price=transaction.piece_price,
                                                   quantity=transaction.quantity, ticker=transaction.ticker))
    return make_response(jsonify([transaction_dto.__dict__ for transaction_dto in transaction_dto_list]), 200)


@app.route('/stock/select', methods=['GET'])
@base_decorators
def get_companies_select_data():
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/select"))


@app.route('/stock/details/<company_ticker>', methods=['GET'])
@base_decorators
def get_company_details(company_ticker):
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/details/" + company_ticker))


@app.route('/stock/chart/price/<company_ticker>', methods=['GET'])
@base_decorators
def get_company_price_chart(company_ticker):
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/chart/price/" + company_ticker))


@app.route('/stock/chart/prediction/<company_ticker>', methods=['GET'])
@base_decorators
def get_company_price_prediction(company_ticker):
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/chart/prediction/" + company_ticker))


@app.route('/stock/chart/revenue/<company_ticker>', methods=['GET'])
@base_decorators
def get_company_revenue_data(company_ticker):
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/chart/revenue/" + company_ticker))


@app.route('/stock/finances/<company_ticker>', methods=['GET'])
@base_decorators
def get_company_finances(company_ticker):
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/finances/" + company_ticker))


@app.route('/stock/statement/last/<company_ticker>', methods=['GET'])
@base_decorators
def get_company_financial_statement(company_ticker):
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/statement/last/" + company_ticker))


@app.route('/stock/price/<company_list>', methods=['GET'])
@base_decorators
def get_companies_price(company_list):
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/price/" + company_list))


@app.route('/stock/search/<company>', methods=['GET'])
@base_decorators
def search_companies(company):
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/search/" + company))


@app.route('/stock/search', methods=['GET'])
@base_decorators
def search_query():
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/search", request=request))


@app.route('/stock/gainers', methods=['GET'])
@base_decorators
def get_top_gainers():
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/gainers"))


@app.route('/stock/losers', methods=['GET'])
@base_decorators
def get_top_losers():
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/losers"))


@app.route('/new/latest', methods=['GET'])
@base_decorators
def get_latest_new():
    return return_response(make_request("GET", BASE_PUBLIC_ENDPOINT + "new/latest"))


@app.route('/portfolio/create/equalWeight', methods=['GET'])
@base_decorators
@jwt_required
def create_equal_weight_portfolio():
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    portfolio = Portfolio.get_portfolio(email)
    return return_response(
        make_request("GET", BASE_PORTFOLIO_CREATOR_ENDPOINT + "portfolio/create/equalWeight/" + str(portfolio.money)))


@app.route('/portfolio/create/weighted', methods=['GET'])
@base_decorators
@jwt_required
def create_weighted_portfolio():
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    portfolio = Portfolio.get_portfolio(email)
    return return_response(
        make_request("GET", BASE_PORTFOLIO_CREATOR_ENDPOINT + "portfolio/create/weighted/" + str(portfolio.money)))


@app.route('/portfolio/create/momentum', methods=['GET'])
@base_decorators
@jwt_required
def create_quantitative_momentum_portfolio():
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    portfolio = Portfolio.get_portfolio(email)
    return return_response(
        make_request("GET", BASE_PORTFOLIO_CREATOR_ENDPOINT + "portfolio/create/momentum/" + str(portfolio.money)))


@app.route('/portfolio/create/value', methods=['GET'])
@base_decorators
@jwt_required
def create_quantitative_value_portfolio():
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    portfolio = Portfolio.get_portfolio(email)
    return return_response(
        make_request("GET", BASE_PORTFOLIO_CREATOR_ENDPOINT + "portfolio/create/value/" + str(portfolio.money)))


@app.route('/portfolio/create/valueMomentum', methods=['GET'])
@base_decorators
@jwt_required
def create_quantitative_value_momentum_portfolio():
    email = jwt_helper.get_mail_from_jwt(request.headers["Authorization"])
    portfolio = Portfolio.get_portfolio(email)
    return return_response(
        make_request("GET",
                     BASE_PORTFOLIO_CREATOR_ENDPOINT + "portfolio/create/valueMomentum/" + str(portfolio.money)))


def app_run():
    app.run(debug=True, port=5999, use_reloader=False)


if __name__ == "__main__":
    app_run()
