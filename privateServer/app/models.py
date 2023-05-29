from sqlalchemy import ForeignKey

from . import db
from .JsonAble import JsonAble


class JsonAbleUser(JsonAble):
    def as_dict(self):
        dict_to_return = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        dict_to_return.pop("password")
        dict_to_return.pop("created_on")
        return dict_to_return


class User(db.Model, JsonAbleUser):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    created_on = db.Column(db.Date, nullable=False)


class Portfolio(db.Model, JsonAble):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), unique=True)
    money = db.Column(db.Float, nullable=False)

    @staticmethod
    def get_portfolio(email):
        user = User.query.filter(User.email == email).first()
        return Portfolio.query.filter(Portfolio.user_id == user.id).first()


class Stock(db.Model, JsonAble):
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.String, ForeignKey("portfolio.id"), nullable=False)
    ticker = db.Column(db.String, nullable=False)
    medium_buy_price = db.Column(db.Float, nullable=False)
    buy_date = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    @property
    def total_price(self):
        return self.quantity * self.medium_buy_price


class Transaction(db.Model, JsonAble):
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, nullable=False)
    ticker = db.Column(db.String, nullable=False)
    piece_price = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cash_after_transaction = db.Column(db.Float, nullable=False)
    is_buy = db.Column(db.Boolean, nullable=False)

    @property
    def total_price(self):
        return self.quantity * self.piece_price


class StockPriceDataframe(db.Model, JsonAble):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String, nullable=False)
    start = db.Column(db.Date, nullable=False)
    end = db.Column(db.Date, nullable=False)
    data = db.Column(db.String, nullable=False)
