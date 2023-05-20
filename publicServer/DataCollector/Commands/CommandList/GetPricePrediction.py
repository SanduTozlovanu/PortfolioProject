from abc import ABC

import yfinance as yf
from matplotlib import pyplot as plt
from prophet import Prophet
from prophet.plot import plot_plotly

from publicServer.DataCollector.Commands.Command import Command
from publicServer.DataCollector.Database.Models.Company import Company
from publicServer.DataCollector.Database.Models.PricePrediction import PricePrediction
from publicServer.DataCollector.Database.session import db
from publicServer.config.constants import ONE_MINUTE


class GetPricePrediction(Command, ABC):
    def __init__(self):
        super().__init__(ONE_MINUTE, 5, 1)

    def execute(self):
        collect_list = []
        for ticker in db.query(Company.ticker).all():
            ticker = ticker.ticker
            prediction = db.query(PricePrediction).filter(PricePrediction.ticker == ticker).first()
            if not prediction:
                collect_list.append(ticker)
                if len(collect_list) >= 10:
                    break
        for ticker in collect_list:
            try:
                data = yf.download(ticker, period="max")
                self.collectData(data, ticker)
            except:
                print(f"[GetPricePrediction] failed to get a price prediction ")

    @staticmethod
    def collectData(data, ticker: str):
        period = 5 * 365
        data.reset_index(inplace=True)
        df_train = data[['Date', 'Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

        m = Prophet()
        m.fit(df_train)
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)
        fig1 = plot_plotly(m, forecast)
        prediction_to_insert = PricePrediction(ticker=ticker, jsonData=fig1.to_json())
        db.add(prediction_to_insert)
        db.commit()
