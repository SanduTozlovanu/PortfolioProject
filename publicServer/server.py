import functools
import threading

import jwt
import requests
import yfinance as yf
from flask import make_response, request, Flask, jsonify
from plotly import graph_objs as go

from JWTHelper import JWTHandler
from publicServer.DataCollector.Database.Models.Company import Company
from publicServer.DataCollector.Database.Models.CompanyProfile import CompanyProfile
from publicServer.DataCollector.collectorCore import runCollector
from publicServer.config.definitions import SECRET_KEY

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
jwt_helper = JWTHandler(app.config["SECRET_KEY"])
SERVER_NAME = "PublicServer"
app.config["JWT"] = jwt_helper.create_jwt_token(SERVER_NAME)


def get_jwt_token():
    try:
        jwt_helper.is_token_valid(app.config["JWT"])
    except jwt.ExpiredSignatureError:
        app.config["JWT"] = jwt_helper.create_jwt_token(SERVER_NAME)
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
        company_profile = CompanyProfile.query.filter(CompanyProfile.ticker == company_ticker).first()
        if company_profile is None:
            return make_response("Company not found", 404)
        return make_response(jsonify(company_profile), 200)
    except:
        return make_response("Internal server error", 500)


@app.route("/here", methods=['GET'])
def good():
    make_response("salut", 200)


@app.route('/api/stock/chart/price/<company_ticker>', methods=['GET'])
@jwt_required
def get_company_price_chart(company_ticker):
    try:
        company = Company.query.filter(Company.ticker == company_ticker).first()
        if company is None:
            return make_response("Company not found", 404)
        data = yf.download(company_ticker, period="max")
        data.reset_index(inplace=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
        fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
        fig.to_json()
        return make_response(fig.to_json(), 200)
    except:
        return make_response("Internal server error", 500)


def app_run():
    app.run(debug=True, port=6000, use_reloader=False)


if __name__ == "__main__":
    try:
        threadMain = threading.Thread(target=app_run)
        threadCollector = threading.Thread(target=runCollector)
        threadMain.start()
        #threadCollector.start()
        threadMain.join()
        threadCollector.join()
    except Exception as exc:
        print(exc)
