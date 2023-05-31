import json
import time
import requests
from sqlalchemy import and_
import yfinance as yf
import pandas as pd

from privateServer.app import db
from privateServer.app.models import StockPriceDataframe
from datetime import datetime, date

START_DATE = "2023-01-01"


class DataframeCollector:
    def __init__(self):
        df = yf.download("AAPL", start=START_DATE)
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])
        self.last_date = df['Date'].iloc[-1]
        self.database_valid = False

    def validate_database(self):
        stock_dataframe = StockPriceDataframe.query.filter(and_(StockPriceDataframe.ticker == "AAPL",
                                                                StockPriceDataframe.end >= self.last_date)).first()
        if not stock_dataframe:
            self.populate_database()
        self.database_valid = True

    @staticmethod
    def populate_database():
        db.session.query(StockPriceDataframe).delete()
        ticker_list = requests.get("http://127.0.0.1:6000/api/ticker_list").json()
        ticker_list.append("^GSPC")
        company_list = ""
        for ticker in ticker_list:
            company_list += (ticker + ",")
        company_list = company_list[:-1]
        df = yf.download(company_list, start=START_DATE)
        df.reset_index(inplace=True)
        df = df.drop(['Open', 'High', 'Adj Close', 'Volume', 'Low'], axis=1)
        df['Date'] = pd.to_datetime(df['Date'])
        print(df.columns)
        for ticker in ticker_list:
            ticker_df = df.loc[:, [('Date', ''), ('Close', ticker)]]
            ticker_df.columns = ticker_df.columns.droplevel(1)
            if pd.isna(ticker_df['Close'].iloc[-1]):
                ticker_df['Close'].iloc[-1] = ticker_df['Close'].iloc[-2]
            new_stock_price_dataframe = StockPriceDataframe(ticker=ticker, start=datetime.strptime("2000-01-01", "%Y-%m-%d"),
                                                            end=ticker_df['Date'].iloc[-1], data=ticker_df.to_json())
            db.session.add(new_stock_price_dataframe)
        db.session.commit()

    def get(self, ticker: str, start, end=None):
        if not self.database_valid:
            self.validate_database()
        if end is None:
            end = self.last_date
        if isinstance(start, str):
            start = datetime.strptime(start, "%Y-%m-%d")
        elif isinstance(start, date):
            start = datetime.combine(start, datetime.min.time())
        if isinstance(end, str):
            end = datetime.strptime(end, "%Y-%m-%d")
        elif isinstance(end, date):
            end = datetime.combine(end, datetime.min.time())
        if end > self.last_date:
            end = self.last_date
        if start > end:
            start = end
        db_df: StockPriceDataframe = StockPriceDataframe.query.filter(and_(StockPriceDataframe.ticker == ticker,
                                                                           StockPriceDataframe.start <= start.date(),
                                                                           StockPriceDataframe.end >= end.date())).first()

        df = pd.DataFrame(json.loads(db_df.data))
        df['Date'] = pd.to_datetime(df['Date'], unit='ms')

        df = df[(df['Date'] >= start.strftime("%Y-%m-%d")) & (df['Date'] <= end.strftime("%Y-%m-%d"))]
        df.reset_index(inplace=True, drop=True)
        return df
