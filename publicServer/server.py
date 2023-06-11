import functools
import json
import threading
import traceback
from urllib.parse import urlencode

import jwt
import requests
from flask import make_response, request, Flask, jsonify
from flask_caching import Cache

from JWTHelper import JWTHandler

from exceptions import NotFoundException, BadRequestException, UnauthorizedException, ForbiddenException, \
    ConflictException
from publicServer.DataCollector.collectorCore import runCollector
from publicServer.config.definitions import SECRET_KEY
from publicServer.controllers.ChartController import ChartController
from publicServer.controllers.NewsController import NewsController
from publicServer.controllers.SearchController import SearchController
from publicServer.controllers.StockFinancialsController import StockFinancialsController
from publicServer.controllers.StockPriceController import StockPriceController
from publicServer.controllers.StockProfileController import StockProfileController

app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET_KEY
app.config['CACHE_TYPE'] = 'simple'
jwt_helper = JWTHandler(app.config["SECRET_KEY"])
SERVER_NAME = "PublicServer"
app.config["JWT"] = jwt_helper.create_jwt_token(SERVER_NAME)
cache = Cache(app)

def get_jwt_token():
    if not jwt_helper.is_token_valid(app.config["JWT"]):
        app.config["JWT"] = jwt_helper.create_jwt_token("PublicServer")
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


def jwt_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        request_jwt = request.headers.get("Authorization")
        if not request_jwt:
            return make_response("Please provide the Authorization header", 403)
        # Check if jwt is correct and valid
        try:
            if jwt_helper.is_token_valid(request_jwt):
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
        except Exception as exc:
            traceback.print_exc()
            return make_response("Internal server error", 500)

    return wrapper


def base_decorators(func):
    @jwt_required
    @exception_catcher
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@app.route('/api/stock/details/<company_ticker>', methods=['GET'])
@base_decorators
def get_company_details(company_ticker):
    company_profile = StockProfileController.receive_company_details(company_ticker)
    return make_response(company_profile.as_dict(), 200)


@app.route('/api/stock/losers', methods=['GET'])
@base_decorators
@cache.cached(timeout=60)
def get_top_losers():
    loosers = StockPriceController.receive_top_loosers()
    return make_response(jsonify([loserDto.__dict__ for loserDto in loosers]), 200)


@app.route('/api/stock/gainers', methods=['GET'])
@base_decorators
@cache.cached(timeout=60)
def get_top_gainers():
    gainers = StockPriceController.receive_top_gainers()
    return make_response(jsonify([gainerDto.__dict__ for gainerDto in gainers]), 200)


@app.route('/api/stock/similar/<ticker_list>', methods=['GET'])
@base_decorators
@cache.cached(timeout=1800)
def get_similar_stocks(ticker_list):
    similars_to_return = SearchController.receive_similar_stocks(ticker_list)
    return make_response(jsonify([similarDto.__dict__ for similarDto in similars_to_return]), 200)


@app.route('/api/stock/select', methods=['GET'])
@base_decorators
@cache.cached(timeout=1800)
def get_companies_select_data():
    tickers_to_return = StockProfileController.receive_companies_select_data()
    return make_response(jsonify([tickerSelectDto.__dict__ for tickerSelectDto in tickers_to_return]), 200)


@app.route('/api/stock/statement/last/<company_name>', methods=['GET'])
@base_decorators
@cache.cached(timeout=1800)
def get_financial_statement(company_name):
    company_financial_statement = StockFinancialsController.receive_financial_statement(company_name)
    return make_response(company_financial_statement.as_dict(), 200)


@app.route('/api/stock/finances/<company_ticker>', methods=['GET'])
@base_decorators
@cache.cached(timeout=1800)
def get_company_finances(company_ticker):
    stock_finances_dto = StockFinancialsController.receive_company_finances(company_ticker)
    return make_response(jsonify(stock_finances_dto.__dict__), 200)


@app.route('/api/stock/price/<company_list>', methods=['GET'])
@base_decorators
@cache.cached(timeout=20)
def get_companies_price(company_list):
    response_dict = StockPriceController.receive_companies_price(company_list)
    return make_response(response_dict, 200)


@app.route('/api/stock/priceChange/<company_tickers>', methods=['GET'])
@base_decorators
@cache.cached(timeout=20)
def get_tickers_price_change(company_tickers):
    response_list = StockPriceController.receive_tickers_price_change(company_tickers)
    return make_response(jsonify([priceDto.__dict__ for priceDto in response_list]), 200)


@app.route('/api/stock/chart/price/<company_ticker>', methods=['GET'])
@base_decorators
@cache.cached(timeout=1800)
def get_company_price_chart(company_ticker):
    fig = ChartController.receive_company_price_chart(company_ticker)
    return make_response(fig.to_json(), 200)


@app.route('/api/stock/chart/prediction/<company_ticker>', methods=['GET'])
@base_decorators
@cache.cached(timeout=1800)
def get_company_price_prediction(company_ticker):
    prediction = ChartController.receive_company_price_prediction(company_ticker)
    return make_response(json.loads(prediction.jsonData), 200)


@app.route('/api/stock/chart/revenue/<company_ticker>', methods=['GET'])
@base_decorators
@cache.cached(timeout=1800)
def get_company_revenue_chart(company_ticker):
    returned_dtos = ChartController.receive_company_revenue_chart(company_ticker)
    return make_response(jsonify([revenue_dto.__dict__ for revenue_dto in returned_dtos]), 200)


@app.route('/api/stock/search/<company>', methods=['GET'])
@base_decorators
@cache.cached(timeout=60)
def get_search_stocks(company):
    returned_companies = SearchController.receive_search_stocks(company)
    return make_response(jsonify([company_dto.__dict__ for company_dto in returned_companies]), 200)


@app.route('/api/stock/search', methods=['GET'])
@base_decorators
@cache.cached(timeout=60)
def search_query():
    companies_to_return = SearchController.search_query(urlencode(request.args))
    return make_response(jsonify([company_dto.__dict__ for company_dto in companies_to_return]), 200)


@app.route('/api/new/latest', methods=['GET'])
@base_decorators
@cache.cached(timeout=60)
def get_latest_new():
    new = NewsController.receive_latest_new()
    return make_response(jsonify(new.__dict__))


@app.route('/api/news/<ticker_list>', methods=['GET'])
@base_decorators
@cache.cached(timeout=60)
def get_latest_news(ticker_list):
    news = NewsController.receive_latest_news(ticker_list)
    return make_response(jsonify([new_dto.__dict__ for new_dto in news]), 200)


@app.route('/api/stock/ratios', methods=['GET'])
@base_decorators
@cache.cached(timeout=60)
def get_companies_ratios():
    stock_ratios_dtos = StockFinancialsController.receive_companies_ratios()
    return make_response(jsonify([stock_ratio_dto.__dict__ for stock_ratio_dto in stock_ratios_dtos]), 200)


@app.route('/api/stock/priceChanges', methods=['GET'])
@base_decorators
@cache.cached(timeout=5)
def get_all_tickers_price_change():
    response_list = StockPriceController.receive_all_tickers_price_change()
    return make_response(jsonify([priceDto.__dict__ for priceDto in response_list]), 200)


@app.route('/api/stock/basedata', methods=['GET'])
@base_decorators
@cache.cached(timeout=50)
def get_stocks_basedata():
    returned_companies = StockProfileController.receive_stocks_basedata()
    return make_response(jsonify([company_dto.__dict__ for company_dto in returned_companies]), 200)


@app.route('/api/stock/ticker_list', methods=['GET'])
@exception_catcher
@cache.cached(timeout=1800)
def get_ticker_list():
    ticker_list = StockProfileController.receive_ticker_list()
    return make_response(ticker_list, 200)


def app_run():
    app.run(debug=True, port=6000, use_reloader=False)


if __name__ == "__main__":
    try:
        threadMain = threading.Thread(target=app_run)
        threadCollector = threading.Thread(target=runCollector)
        threadMain.start()
        threadCollector.start()
        threadMain.join()
        threadCollector.join()
    except Exception as exc:
        print(exc)
