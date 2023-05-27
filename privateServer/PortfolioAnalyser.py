import traceback
from datetime import datetime
import numpy as np
import pandas as pd

from privateServer.DTOs.PortfolioStatsDto import PortfolioStatsDto
from privateServer.DataframeCollector import DataframeCollector
from privateServer.app.models import Transaction
from privateServer.contants import INITIAL_MONEY


class HoldPeriod:
    def __init__(self, ticker, quantity: int, start_date: datetime, end_date: [datetime, None]):
        self.ticker = ticker
        self.quantity = quantity
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return f"ticker:{self.ticker}, quantity:{self.quantity}, start_date:{self.start_date}, end_date:{self.end_date}"


class PortfolioAnalyser:
    def __init__(self):
        self.dataframe_collector = DataframeCollector()

    def create_chart_data(self, transaction_list: list[Transaction], creation_time: datetime):
        hold_periods = PortfolioAnalyser.__generateHoldPeriods(transaction_list)
        df = self.dataframe_collector.get("AAPL", start=creation_time.strftime("%Y-%m-%d"))
        df["Close"] = np.nan
        df = df.rename(columns={'Close': 'Value'})
        PortfolioAnalyser.__initDataframeCash(df, transaction_list)
        print(df)

        for hold_period in hold_periods:
            try:
                if hold_period.end_date is None:
                    df2 = self.dataframe_collector.get(hold_period.ticker, start=hold_period.start_date)
                else:
                    df2 = self.dataframe_collector.get(hold_period.ticker, start=hold_period.start_date,
                                                       end=hold_period.end_date)
            except AttributeError:
                if hold_period.end_date is None:
                    df2 = self.dataframe_collector.get(hold_period.ticker, start=hold_period.start_date)
                else:
                    df2 = self.dataframe_collector.get(hold_period.ticker, start=hold_period.start_date,
                                                       end=hold_period.end_date)
            if df2.shape[0] < 2 and df2['Date'][0].strftime("%Y-%m-%d") != hold_period.start_date.strftime(
                    "%Y-%m-%d"):
                print(hold_period.start_date.strftime("%Y-%m-%d"))
                print(df2['Date'][0])
                continue
            if df2['Date'].iloc[-1] != df['Date'].iloc[-1]:
                last_row = df2.iloc[-1]
                df2.loc[df.index.max() + 1] = last_row
                df2.reset_index(drop=True, inplace=True)
                df2['Date'].iloc[-1] = df['Date'].iloc[-1]

            df = pd.merge(df, df2, on='Date', how='left')
            df['Value_multiplied'] = df['Close'].fillna(0) * hold_period.quantity
            df['Value'] = df['Value'] + df['Value_multiplied']
            df = df[['Date', 'Value']]

        df['Value'] = df['Value'].round(3)
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        return df

    def get_portfolio_stats(self, holdings_count: int, transaction_list: list[Transaction],
                            creation_time: datetime) -> PortfolioStatsDto:
        df = self.create_chart_data(transaction_list, creation_time)
        current_value = df['Value'].iloc[-1]
        portfolio_return = (current_value - INITIAL_MONEY) / INITIAL_MONEY * 100
        snp_data = self.__get_snp_data(df['Date'].iloc[0])
        snp_change = PortfolioAnalyser.__get_snp_percentage_change(snp_data)
        portfolio_beta = PortfolioAnalyser.__get_portfolio_beta(df, snp_data)
        highest_value = df['Value'].max()
        lowest_value = df['Value'].min()

        return PortfolioStatsDto(initialValue=INITIAL_MONEY, currentValue=current_value, holdings=holdings_count,
                                 beta=portfolio_beta, portfolioReturn=portfolio_return, snpReturn=snp_change,
                                 highestValue=highest_value, lowestValue=lowest_value)

    def __get_snp_data(self, start_date):
        symbol = "^GSPC"
        return self.dataframe_collector.get(symbol, start=start_date)

    @staticmethod
    def __get_snp_percentage_change(df):
        closing_prices = df['Close']
        initial_price = closing_prices.iloc[0]
        latest_price = closing_prices.iloc[-1]
        price_change = latest_price - initial_price
        return (price_change / initial_price) * 100

    @staticmethod
    def __get_portfolio_beta(portfolio_df, benchmark_df):
        if benchmark_df.shape[0] > portfolio_df.shape[0]:
            benchmark_df.drop(benchmark_df.index[-1], inplace=True)
        portfolio_returns = portfolio_df["Value"].pct_change().dropna()
        benchmark_returns = benchmark_df['Close'].pct_change().dropna()
        covariance_matrix = np.cov(portfolio_returns, benchmark_returns)
        return covariance_matrix[0, 1] / covariance_matrix[1, 1]

    @staticmethod
    def __generateTickerHoldPeriods(transactions: list[Transaction]) -> list[
        HoldPeriod]:  # lets suppose that transactions are sorted by date
        hold_periods_to_return: list[HoldPeriod] = []
        if not transactions[0].is_buy:
            print("Wrong data, there should be a buy first ! WTF")
        ticker: str = transactions[0].ticker
        current_quantity: int = transactions[0].quantity
        last_date: datetime = transactions[0].date
        transactions.remove(transactions[0])
        for transaction in transactions:
            hold_periods_to_return.append(
                HoldPeriod(ticker=ticker, quantity=current_quantity, start_date=last_date, end_date=transaction.date))
            last_date = transaction.date
            if transaction.is_buy:
                current_quantity += transaction.quantity
            else:
                current_quantity -= transaction.quantity
        if current_quantity != 0:
            hold_periods_to_return.append(
                HoldPeriod(ticker=ticker, quantity=current_quantity, start_date=last_date, end_date=None))

        return hold_periods_to_return

    @staticmethod
    def __generateHoldPeriods(transaction_list: list[Transaction]) -> list[HoldPeriod]:
        transaction_dict: dict[str, list[Transaction]] = {}
        for transaction in transaction_list:
            if transaction.ticker not in transaction_dict:
                transaction_dict[transaction.ticker] = [transaction]
            else:
                transaction_dict[transaction.ticker].append(transaction)
        hold_periods_to_return = []
        for ticker in transaction_dict:
            hold_periods_to_return += PortfolioAnalyser.__generateTickerHoldPeriods(transaction_dict[ticker])
        return hold_periods_to_return

    @staticmethod
    def __initDataframeCash(df, transaction_list: list[Transaction]):
        df['Date'] = pd.to_datetime(df['Date'])
        date = None
        cash_before = None
        if len(transaction_list) == 0:
            df["Value"] = INITIAL_MONEY
            return df
        for transaction in transaction_list:
            if date is not None:
                df.loc[
                    (df['Date'] >= date) & (df['Date'] < transaction.date.strftime("%Y-%m-%d")), 'Value'] = cash_before
            else:
                df.loc[df['Date'] < transaction.date.strftime("%Y-%m-%d"), 'Value'] = INITIAL_MONEY
            date = transaction.date.strftime("%Y-%m-%d")
            cash_before = transaction.cash_after_transaction
        df.loc[df['Date'] >= date, 'Value'] = cash_before
        return df
