import json
import time

from sqlalchemy import and_
import yfinance as yf
import pandas as pd

from privateServer.app import db
from privateServer.app.models import StockPriceDataframe
from datetime import datetime, date


class DataframeCollector:
    def __init__(self):
        df = yf.download("AAPL", start="2000-01-01")
        df.reset_index(inplace=True)
        df = df.drop(['Open', 'High', 'Adj Close', 'Volume', 'Low'], axis=1)
        df['Date'] = pd.to_datetime(df['Date'])
        self.last_date = df['Date'].iloc[-1]

    def get(self, ticker: str, start, end=None):
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
        db_df: StockPriceDataframe = StockPriceDataframe.query.filter(and_(StockPriceDataframe.ticker == ticker,
                                                                           StockPriceDataframe.start <= start.date(),
                                                                           StockPriceDataframe.end >= end.date())).first()
        if db_df is None:
            df = yf.download(ticker, start="2000-01-01")
            time.sleep(1)
            df.reset_index(inplace=True)
            df = df.drop(['Open', 'High', 'Adj Close', 'Volume', 'Low'], axis=1)
            df['Date'] = pd.to_datetime(df['Date'])
            old_dataframes = StockPriceDataframe.query.filter(StockPriceDataframe.ticker == ticker).all()
            for old_dataframe in old_dataframes:
                db.session.delete(old_dataframe)
            stock_price_data_frame = StockPriceDataframe(ticker=ticker,
                                                         start=datetime.strptime("2000-01-01", "%Y-%m-%d"),
                                                         end=df['Date'].iloc[-1], data=df.to_json())
            db.session.add(stock_price_data_frame)
            db.session.commit()

        else:
            df = pd.DataFrame(json.loads(db_df.data))
            df['Date'] = pd.to_datetime(df['Date'], unit='ms')

        df = df[(df['Date'] >= start.strftime("%Y-%m-%d")) & (df['Date'] <= end.strftime("%Y-%m-%d"))]
        df.reset_index(inplace=True, drop=True)
        return df
