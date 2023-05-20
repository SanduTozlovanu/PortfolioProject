import functools
import json
import threading
from sqlite3 import Row

import jwt
import requests
import yfinance as yf
from flask import make_response, request, Flask, jsonify
from plotly import graph_objs as go
from sqlalchemy import or_
from urllib.parse import urlencode

from JWTHelper import JWTHandler
from publicServer.DTOs.RevenueChartBarDto import RevenueChartBarDto
from publicServer.DTOs.SearchStockDto import SearchStockDto
from publicServer.DTOs.StockFinancesDto import StockFinancesDto
from publicServer.DataCollector.Database.Models.Balance import Balance
from publicServer.DataCollector.Database.Models.Company import Company
from publicServer.DataCollector.Database.Models.CompanyProfile import CompanyProfile
from publicServer.DataCollector.Database.Models.FinancialStatement import FinancialStatement
from publicServer.DataCollector.Database.Models.KeyMetrics import KeyMetrics
from publicServer.DataCollector.Database.Models.PricePrediction import PricePrediction
from publicServer.DataCollector.Database.Models.Ratios import Ratios
from publicServer.DataCollector.Database.Models.Score import Score
from publicServer.DataCollector.Database.Models.StockPrice import StockPrice
from publicServer.DataCollector.Database.session import db
from publicServer.DataCollector.collectorCore import runCollector
from publicServer.SimilarityChecker import find_most_similar_strings
from publicServer.config.constants import API_ENDPOINT
from publicServer.config.definitions import SECRET_KEY, KEY_URL

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
jwt_helper = JWTHandler(app.config["SECRET_KEY"])
SERVER_NAME = "PublicServer"
app.config["JWT"] = jwt_helper.create_jwt_token(SERVER_NAME)


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


@app.route('/api/stock/statement/last/<company_name>', methods=['GET'])
@jwt_required
def get_financial_statement(company_name):
    try:
        company_financial_statement = db.query(FinancialStatement).filter(
            FinancialStatement.ticker == company_name).order_by(FinancialStatement.date.desc()).first()
        if company_financial_statement is None:
            return make_response("Company not found", 404)
        return make_response(company_financial_statement.as_dict(), 200)
    except Exception as exc:
        print(exc)
        return make_response("Internal server error", 500)


@app.route('/api/stock/finances/<company_ticker>', methods=['GET'])
@jwt_required
def get_company_finances(company_ticker):
    try:
        company_financial_statement = db.query(FinancialStatement).filter(
            FinancialStatement.ticker == company_ticker).order_by(FinancialStatement.date.desc()).first()
        if company_financial_statement is None:
            return make_response("Company statement not found", 404)

        company_balance: Balance = db.query(Balance).filter(
            Balance.ticker == company_ticker).first()
        if company_balance is None:
            return make_response("Company balance not found", 404)

        company_ratios: Ratios = db.query(Ratios).filter(
            Ratios.ticker == company_ticker).first()
        if company_ratios is None:
            return make_response("Company ratios not found", 404)

        company_key_metrics: KeyMetrics = db.query(KeyMetrics).filter(
            KeyMetrics.ticker == company_ticker).first()
        if company_key_metrics is None:
            return make_response("Company key metrics not found", 404)

        company_score: Score = db.query(Score).filter(
            Score.ticker == company_ticker).first()
        if company_score is None:
            return make_response("Company score not found", 404)

        company_statement: FinancialStatement = db.query(FinancialStatement).filter(
            FinancialStatement.ticker == company_ticker).order_by(FinancialStatement.date.desc()).first()
        if company_statement is None:
            return make_response("Company financial statement", 404)
        stock_finances_dto = StockFinancesDto(balance=company_balance, ratios=company_ratios, score=company_score,
                                              key_metrics=company_key_metrics, statement=company_statement)
        return make_response(jsonify(stock_finances_dto.__dict__), 200)
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
        fig.layout.update(xaxis_rangeslider_visible=True, showlegend=False)
        return make_response(fig.to_json(), 200)
    except:
        return make_response("Internal server error", 500)


@app.route('/api/stock/chart/prediction/<company_ticker>', methods=['GET'])
@jwt_required
def get_company_price_prediction(company_ticker):
    try:
        prediction: PricePrediction = db.query(PricePrediction).filter(PricePrediction.ticker == company_ticker).first()
        if prediction is None:
            return make_response("Prediction not found", 404)
        return make_response(json.loads(prediction.jsonData), 200)
    except Exception as exc:
        print(exc)
        return make_response("Internal server error", 500)


@app.route('/api/stock/chart/revenue/<company_ticker>', methods=['GET'])
@jwt_required
def get_company_revenue_chart(company_ticker):
    try:
        returned_dtos = []
        statements_list: list[FinancialStatement] = db.query(FinancialStatement).filter(
            FinancialStatement.ticker == company_ticker).order_by(FinancialStatement.date.asc()).all()
        if len(statements_list) == 0:
            return make_response("No financial statement found for this company_ticker", 404)
        for statement in statements_list:
            returned_dtos.append(RevenueChartBarDto(statement.date, statement.revenue))
        return make_response(jsonify([revenue_dto.__dict__ for revenue_dto in returned_dtos]), 200)
    except:
        return make_response("Internal server error", 500)


@app.route('/api/stock/search/<company>', methods=['GET'])
@jwt_required
def get_search_stocks(company):
    try:
        full_company_list = []
        companies = db.query(CompanyProfile.ticker, CompanyProfile.companyName).all()
        for entry in companies:
            full_company_list.append(entry["companyName"])
            full_company_list.append(entry["ticker"])

        similar_strings = find_most_similar_strings(company, full_company_list)
        returned_companies = []
        for string in similar_strings:
            received_company: CompanyProfile = db.query(CompanyProfile.companyName, CompanyProfile.mktCap,
                                                        CompanyProfile.ticker,
                                                        CompanyProfile.sector, CompanyProfile.beta).filter(or_(
                CompanyProfile.ticker == string, CompanyProfile.companyName == string)).first()
            if received_company is None:
                continue

            price = db.query(StockPrice.price).filter(
                StockPrice.ticker == received_company["ticker"]).first()
            returned_companies.append(SearchStockDto(len(returned_companies) + 1, received_company["companyName"],
                                                     received_company["ticker"], received_company["mktCap"],
                                                     received_company["beta"], price["price"],
                                                     received_company["sector"]))

        return make_response(jsonify([company_dto.__dict__ for company_dto in returned_companies]), 200)
    except Exception as exc:
        print(exc)
        return make_response("Internal server error", 500)


@app.route('/api/stock/search', methods=['GET'])
@jwt_required
def search_query():
    try:
        query_string = urlencode(request.args)
        response = requests.get(API_ENDPOINT + "v3/stock-screener?" + query_string + "&" + KEY_URL).json()
        company_profiles = db.query(CompanyProfile.ticker).all()
        companies_to_return = []

        for company1 in company_profiles:
            company1: CompanyProfile
            for company2 in response:
                if company2["symbol"] == company1.ticker:
                    if "marketCap" not in company2:
                        market_cap = "Unknown"
                    else:
                        market_cap = company2["marketCap"]
                    companies_to_return.append(SearchStockDto(len(companies_to_return) + 1, company2["companyName"],
                                                              company2["symbol"], market_cap, company2["beta"],
                                                              company2["price"], company2["sector"]))
                    break

        return make_response(jsonify([company_dto.__dict__ for company_dto in companies_to_return]), 200)
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
