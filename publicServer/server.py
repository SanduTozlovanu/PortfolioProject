import functools
import threading
from sqlite3 import Row

import jwt
import requests
import yfinance as yf
from flask import make_response, request, Flask
from plotly import graph_objs as go
from sqlalchemy import or_

from JWTHelper import JWTHandler
from publicServer.DataCollector.Database.Models.Company import Company
from publicServer.DataCollector.Database.Models.CompanyProfile import CompanyProfile
from publicServer.DataCollector.Database.Models.FinancialStatement import FinancialStatement
from publicServer.DataCollector.Database.Models.StockPrice import StockPrice
from publicServer.DataCollector.Database.session import db
from publicServer.DataCollector.collectorCore import runCollector
from publicServer.SimilarityChecker import find_most_similar_strings
from publicServer.config.definitions import SECRET_KEY

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
jwt_helper = JWTHandler(app.config["SECRET_KEY"])
SERVER_NAME = "PublicServer"
app.config["JWT"] = jwt_helper.create_jwt_token(SERVER_NAME)


def get_jwt_token():
    try:
        if jwt_helper.is_token_valid(app.config["JWT"]):
            return app.config["JWT"]
    except jwt.ExpiredSignatureError:
        app.config["JWT"] = jwt_helper.create_jwt_token("PublicServer")
        return app.config["JWT"]


def make_request(method: str, url: str, json=None, request=None):
    headers = {"Authorization": get_jwt_token()}
    if method == "GET":
        if request:
            return requests.get(url, headers=headers, params=request.args)
        else:
            return requests.get(url, headers=headers)
    elif method == "POST":
        if request:
            return requests.post(url, json=json, headers=headers, params=request.args)
        else:
            return requests.post(url, json=json, headers=headers)
    elif method == "PUT":
        if request:
            return requests.put(url, json=json, headers=headers, params=request.args)
        else:
            return requests.put(url, json=json, headers=headers)
    elif method == "DELETE":
        if request:
            return requests.delete(url, headers=headers, params=request.args)
        else:
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
                return func(*args, **kwargs)
            else:
                return make_response("The provided jwt is invalid", 403)

        except jwt.ExpiredSignatureError:
            return make_response("The provided jwt is expired", 403)

    return decorator


@app.route('/api/stock/details/<company_ticker>', methods=['GET'])
@jwt_required
def get_company_details(company_ticker):
    try:
        company_profile = db.query(CompanyProfile).filter(CompanyProfile.ticker == company_ticker).first()
        if company_profile is None:
            return make_response("Company not found", 404)
        return make_response(company_profile.as_dict(), 200)
    except Exception as exc:
        print(exc)
        return make_response("Internal server error", 500)


@app.route('/api/stock/statement/list/<company_ticker>', methods=['GET'])
@jwt_required
def get_financial_statement_list(company_ticker):
    try:
        company_financial_statement_list = db.query(FinancialStatement.title).filter(
            FinancialStatement.ticker == company_ticker).all()
        if company_financial_statement_list is None or len(company_financial_statement_list) == 0:
            return make_response("Company not found", 404)
        list_to_return = []
        for row in company_financial_statement_list:
            row: Row
            list_to_return.append(row["title"])
        return make_response(list_to_return, 200)
    except Exception as exc:
        print(exc)
        return make_response("Internal server error", 500)


@app.route('/api/stock/statement', methods=['GET'])
@jwt_required
def get_financial_statement():
    try:
        company_ticker = request.args.get("ticker")
        title = request.args.get("title")
        company_financial_statement = db.query(FinancialStatement).filter(
            FinancialStatement.ticker == company_ticker).filter(FinancialStatement.title == title).first()
        if company_financial_statement is None:
            return make_response("Company not found", 404)
        return make_response(company_financial_statement.as_dict(), 200)
    except Exception as exc:
        print(exc)
        return make_response("Internal server error", 500)


@app.route('/api/stock/price/<company_list>', methods=['GET'])
@jwt_required
def get_companies_price(company_list):
    try:
        response_dict = {}
        company_list = company_list.split(",")
        for company in company_list:
            price = db.query(StockPrice.price).filter(
                StockPrice.ticker == company).first()
            if price is None:
                return make_response("Company not found", 404)
            response_dict[company] = price["price"]

        return make_response(response_dict, 200)
    except Exception as exc:
        print(exc)
        return make_response("Internal server error", 500)


@app.route('/api/stock/chart/price/<company_ticker>', methods=['GET'])
@jwt_required
def get_company_price_chart(company_ticker):
    try:
        company = db.query(Company).filter(Company.ticker == company_ticker).first()
        if company is None:
            return make_response("Company not found", 404)
        data = yf.download(company_ticker, period="max")
        data.reset_index(inplace=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
        fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
        return make_response(fig.to_json(), 200)
    except:
        return make_response("Internal server error", 500)


@app.route('/api/stock/search/<company>', methods=['GET'])
@jwt_required
def get_search_stocks(company):
    try:
        full_company_list = []
        companies = db.query(Company.ticker, Company.name).all()
        for entry in companies:
            full_company_list.append(entry["name"])
            full_company_list.append(entry["ticker"])

        similar_strings = find_most_similar_strings(company, full_company_list)
        return_dictionary = {}
        for string in similar_strings:
            received_company: Company = db.query(Company).filter(or_(
                Company.ticker == string, Company.name == string)).first()
            if received_company is None:
                continue
            ticker = received_company.ticker
            price = db.query(StockPrice.price).filter(
                StockPrice.ticker == ticker).first()
            return_dictionary[ticker] = price["price"]

        return make_response(return_dictionary, 200)
    except Exception as exc:
        print(exc)
        return make_response("Internal server error", 500)


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
