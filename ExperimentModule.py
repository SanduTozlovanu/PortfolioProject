import requests
import yfinance as yf

from privateServer.contants import DATE_TO_START, NEXT_DAY, DATE_BEFORE


class OldDataRetriever:
    @staticmethod
    def modify_stock_price(stocks: list):
        try:
            company_list = ""
            for ticker in stocks:
                company_list += (ticker["ticker"] + ",")
            company_list = company_list[:-1]
            df = yf.download(company_list, start=DATE_TO_START, end=NEXT_DAY)
            df.reset_index(inplace=True)
            df = df.drop(['Open', 'High', 'Adj Close', 'Volume', 'Low'], axis=1)
            for ticker in stocks:
                if ticker["ticker"] == "GEHC" or ticker["ticker"] == "FISV" or ticker["ticker"] == "CEG":
                    continue
                ticker_df = df.loc[:, [('Date', ''), ('Close', ticker["ticker"])]]
                ticker_df.columns = ticker_df.columns.droplevel(1)
                ticker["price"] = round(float(ticker_df.iloc[0]["Close"]), 2)
            index = len(stocks) - 1
            while index >= 0:
                if stocks[index].get("ticker") == "FISV" or stocks[index].get("ticker") == "CEG" or stocks[index].get("ticker") == "GEHC" or stocks[index].get("ticker") == "LNC":
                    del stocks[index]
                index -= 1
        except Exception as exc:
            print(exc)

    @staticmethod
    def modify_year_change(stocks: list):
        try:
            company_list = ""
            for ticker in stocks:
                company_list += (ticker["ticker"] + ",")
            company_list = company_list[:-1]
            df = yf.download(company_list, start=DATE_BEFORE, end=NEXT_DAY)
            df.reset_index(inplace=True)
            df = df.drop(['Open', 'High', 'Adj Close', 'Volume', 'Low'], axis=1)
            for ticker in stocks:
                if ticker["ticker"] == "GEHC" or ticker["ticker"] == "FISV" or ticker["ticker"] == "CEG":
                    continue
                ticker_df = df.loc[:, [('Date', ''), ('Close', ticker["ticker"])]]
                ticker_df.columns = ticker_df.columns.droplevel(1)
                first_close = round(float(ticker_df.iloc[0]["Close"]), 2)
                last_close = round(float(ticker_df.iloc[-1]["Close"]), 2)
                ticker["yearChange"] = round(((last_close / first_close) - 1) * 100, 2)
                row_with_desired_date = ticker_df[ticker_df["Date"] == DATE_TO_START]
                ticker["price"] = round(float(row_with_desired_date["Close"]), 2)
            index = len(stocks) - 1
            while index >= 0:
                if stocks[index].get("ticker") == "FISV" or stocks[index].get("ticker") == "CEG" or stocks[index].get(
                        "ticker") == "GEHC" or stocks[index].get("ticker") == "LNC":
                    del stocks[index]
                index -= 1
        except Exception as exc:
            print(exc)

    @staticmethod
    def get_stock_basedata():
        response: list = requests.get("http://127.0.0.1:6000/api/stock/basedata").json()
        OldDataRetriever.modify_stock_price(response)
        return response

    @staticmethod
    def get_stock_price_change_basedata():
        response: list = requests.get("http://127.0.0.1:6000/api/stock/priceChanges").json()
        OldDataRetriever.modify_year_change(response)
        return response

    @staticmethod
    def get_stock_value_basedata():
        response = requests.get("http://127.0.0.1:6000/api/stock/ratios").json()
        OldDataRetriever.modify_stock_price(response)
        return response
