from . import db
from .JsonAble import JsonAble


class StockPriceDataframe(db.Model, JsonAble):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String, nullable=False)
    start = db.Column(db.Date, nullable=False)
    end = db.Column(db.Date, nullable=False)
    data = db.Column(db.String, nullable=False)
