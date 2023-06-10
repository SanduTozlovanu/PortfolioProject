import configparser
import functools
import os
import json
import threading
from urllib.parse import urlencode
import jwt
import requests
from flask import make_response, request, jsonify

from JWTHelper import JWTHandler
from portfolioCreatorServer.ColumnCreator import ColumnCreator
from portfolioCreatorServer.DTOs.CreatedPortfolioDto import CreatedPortfolioDto
from portfolioCreatorServer.DTOs.EqualWeightStockDto import EqualWeightStockDto
from portfolioCreatorServer.DTOs.MomentumStockDto import MomentumStockDto
from portfolioCreatorServer.DTOs.ValueMomentumStockDto import ValueMomentumStockDto
from portfolioCreatorServer.DTOs.ValueStockDto import ValueStockDto
from portfolioCreatorServer.DTOs.WeightedStockDto import WeightedStockDto
from portfolioCreatorServer.PortfolioCreator import PortfolioCreator
from privateServer.app import create_app

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), "config.ini"))
app = create_app()
app.config["SECRET_KEY"] = config.get("keys", "SECRET_KEY")
jwt_helper = JWTHandler(app.config["SECRET_KEY"])

app.config["JWT"] = jwt_helper.create_jwt_token("PortfolioCreatorServer")
BASE_PUBLIC_ENDPOINT = "http://127.0.0.1:6000/api/"
BASE_PRIVATE_ENDPOINT = "http://127.0.0.1:5999/"


def serialize_object(obj):
    if isinstance(obj, (EqualWeightStockDto, MomentumStockDto, ValueMomentumStockDto, ValueStockDto, WeightedStockDto,
                        CreatedPortfolioDto)):
        return obj.__dict__
    raise TypeError(f'Object of type {type(obj).__name__} is not JSON serializable')


def get_jwt_token():
    if not jwt_helper.is_token_valid(app.config["JWT"]):
        app.config["JWT"] = jwt_helper.create_jwt_token("PortfolioCreatorServer")
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


@app.route('/api/portfolio/create/equalWeight/<money>', methods=['GET'])
@jwt_required
def create_equal_weight_portfolio(money):
    try:
        response = make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/basedata")
        df, residual_cash = PortfolioCreator.create_equal_weight_dataframe(response.json(), float(money))
        dto_return: list[EqualWeightStockDto] = []
        for row in df.index:
            dto_return.append(EqualWeightStockDto(id=len(dto_return) + 1, price=df.loc[row, "price"],
                                                  quantity=df.loc[row, "sharesToBuy"], ticker=df.loc[row, "ticker"]))
        columns = ColumnCreator.get_equal_weight_stocks_columns()
        dto = CreatedPortfolioDto(cash=residual_cash, data=dto_return, columns=columns)
        return make_response(json.dumps(dto, default=serialize_object), 200)
    except Exception as exc:
        print(exc)
        return make_response("Internal server error", 500)


@app.route('/api/portfolio/create/weighted/<money>', methods=['GET'])
@jwt_required
def create_weighted_portfolio(money):
    try:
        response = make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/basedata")
        df, residual_cash = PortfolioCreator.create_weighted_dataframe(response.json(), float(money))
        dto_return: list[WeightedStockDto] = []
        for row in df.index:
            dto_return.append(WeightedStockDto(id=len(dto_return) + 1, price=df.loc[row, "price"],
                                               quantity=df.loc[row, "sharesToBuy"], ticker=df.loc[row, "ticker"],
                                               marketCap=df.loc[row, "marketCap"]))
        columns = ColumnCreator.get_weighted_stocks_columns()
        dto = CreatedPortfolioDto(cash=residual_cash, data=dto_return, columns=columns)
        return make_response(json.dumps(dto, default=serialize_object), 200)
    except Exception as exc:
        print(exc)
        return make_response("Internal server error", 500)


@app.route('/api/portfolio/create/momentum/<money>', methods=['GET'])
@jwt_required
def create_quantitative_momentum_portfolio(money):
    try:
        response = make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/priceChanges")
        df, residual_cash = PortfolioCreator.create_filtered_quantitative_momentum_dataframe(response.json(),
                                                                                             float(money))
        dto_return: list[MomentumStockDto] = []
        for row in df.index:
            dto_return.append(MomentumStockDto(id=len(dto_return) + 1, price=df.loc[row, "price"],
                                               quantity=df.loc[row, "sharesToBuy"], ticker=df.loc[row, "ticker"],
                                               yearChange=df.loc[row, "yearChange"]))
        columns = ColumnCreator.get_momentum_stocks_columns()
        dto = CreatedPortfolioDto(cash=residual_cash, data=dto_return, columns=columns)
        return make_response(json.dumps(dto, default=serialize_object), 200)
    except Exception as exc:
        print(exc)
        return make_response("Internal server error", 500)


@app.route('/api/portfolio/create/value/<money>', methods=['GET'])
@jwt_required
def create_quantitative_value_portfolio(money):
    try:
        response = make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/ratios")
        df, residual_cash = PortfolioCreator.create_filtered_quantitative_value_dataframe(response.json(), float(money))
        dto_return: list[ValueStockDto] = []
        for row in df.index:
            dto_return.append(ValueStockDto(id=len(dto_return) + 1, price=df.loc[row, "price"],
                                            quantity=df.loc[row, "sharesToBuy"], ticker=df.loc[row, "ticker"],
                                            ebtPerEbit=df.loc[row, "ebtPerEbit"], evToEbitda=df.loc[row, "evToEbitda"],
                                            freeCashFlowYield=df.loc[row, 'freeCashFlowYield'],
                                            score=df.loc[row, "score"],
                                            operatingMargin=df.loc[row, "operatingMargin"],
                                            peRatio=df.loc[row, "peRatio"],
                                            priceToSales=df.loc[row, "priceToSales"],
                                            priceToBookRatio=df.loc[row, "priceToBookRatio"],
                                            profitMargin=df.loc[row, "profitMargin"]))
        columns = ColumnCreator.get_value_stocks_columns()
        dto = CreatedPortfolioDto(cash=residual_cash, data=dto_return, columns=columns)
        return make_response(json.dumps(dto, default=serialize_object), 200)
    except Exception as exc:
        print(exc)
        return make_response("Internal server error", 500)


@app.route('/api/portfolio/create/valueMomentum/<money>', methods=['GET'])
@jwt_required
def create_quantitative_value_momentum_portfolio(money):
    try:
        value_response = make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/ratios")
        momentum_response = make_request("GET", BASE_PUBLIC_ENDPOINT + "stock/priceChanges")
        df, residual_cash = PortfolioCreator.create_filtered_quantitative_value_momentum_dataframe(
            value_response.json(),
            momentum_response.json(), float(money))
        dto_return: list[ValueMomentumStockDto] = []
        for row in df.index:
            dto_return.append(ValueMomentumStockDto(id=len(dto_return) + 1, price=df.loc[row, "price"],
                                                    quantity=df.loc[row, "sharesToBuy"], ticker=df.loc[row, "ticker"],
                                                    ebtPerEbit=df.loc[row, "ebtPerEbit"],
                                                    evToEbitda=df.loc[row, "evToEbitda"],
                                                    freeCashFlowYield=df.loc[row, 'freeCashFlowYield'],
                                                    score=df.loc[row, "score"],
                                                    operatingMargin=df.loc[row, "operatingMargin"],
                                                    peRatio=df.loc[row, "peRatio"],
                                                    priceToSales=df.loc[row, "priceToSales"],
                                                    priceToBookRatio=df.loc[row, "priceToBookRatio"],
                                                    profitMargin=df.loc[row, "profitMargin"],
                                                    yearChange=df.loc[row, "yearChange"]))
        columns = ColumnCreator.get_value_momentum_stocks_columns()
        dto = CreatedPortfolioDto(cash=residual_cash, data=dto_return, columns=columns)
        return make_response(json.dumps(dto, default=serialize_object), 200)
    except Exception as exc:
        print(exc)
        return make_response("Internal server error", 500)


def app_run():
    app.run(debug=True, port=6001, use_reloader=False)


if __name__ == "__main__":
    thread = threading.Thread(target=app_run, daemon=True)
    thread.start()
    thread.join()
