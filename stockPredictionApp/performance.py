import asyncio
from datetime import datetime

import numpy as np
import pandas as pd
import yfinance as yf
import aiohttp


def example1():
    # First DataFrame
    df1 = pd.DataFrame({
        'date': ['2023-10-01', '2023-10-01', '2023-10-02', '2023-10-03', '2023-10-04'],
        'close': [50.23, 50.50, 51.20, 52.73, 55.66]
    })

    # Second DataFrame
    df2 = pd.DataFrame({
        'date': ['2023-10-02', '2023-10-03'],
        'close': [70.23, 80.50]
    })

    # Merge the DataFrames on 'date' column with 'left' join
    merged_df = pd.merge(df1, df2, on='date', how='left')

    # Multiply 'close_y' values by 3 and fill missing values with 0
    merged_df['close_y_multiplied'] = merged_df['close_y'].fillna(0) * 3

    # Add 'close_x' and 'close_y_multiplied' columns
    merged_df['close_sum'] = merged_df['close_x'] + merged_df['close_y_multiplied']

    # Select only the 'date' and 'close_sum' columns
    result_df = merged_df[['date', 'close_sum']]

    print(result_df)


def example2():
    # Create a DataFrame
    df = pd.DataFrame({
        'date': ['2023-10-01', '2023-10-02', '2023-10-03', '2023-10-04', '2023-10-05'],
        'close': [50.23, 50.50, 51.20, 52.73, 55.66]
    })

    # Convert the 'date' column to datetime type
    df['date'] = pd.to_datetime(df['date'])

    # Set the conditions to update the 'close' column
    conditions = (df['date'] > '2023-10-02') & (df['date'] < '2023-10-04')

    # Update the 'close' column with the specified value
    df.loc[conditions, 'close'] = 25

    print(df)


class Transaction:
    def __init__(self, ticker, piece_price: float, date: datetime, quantity: int, cash_after_transaction: float,
                 is_buy: bool):
        self.ticker = ticker
        self.piece_price = piece_price
        self.date = date
        self.quantity = quantity
        self.cash_after_transaction = cash_after_transaction
        self.is_buy = is_buy


class HoldPeriod:
    def __init__(self, ticker, quantity: int, start_date: datetime, end_date: [datetime, None]):
        self.ticker = ticker
        self.quantity = quantity
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return f"ticker:{self.ticker}, quantity:{self.quantity}, start_date:{self.start_date}, end_date:{self.end_date}"


def getTransactions() -> list[Transaction]:
    trans_list = []
    money = 10000
    money = money - 4 * 106.6
    trans_list.append(Transaction("ADBE", 106.6, datetime.strptime("2022-10-02", "%Y-%m-%d"), is_buy=True, quantity=10,
                                  cash_after_transaction=money))
    money = money - 3 * 430.8
    trans_list.append(Transaction("TSLA", 430.8, datetime.strptime("2022-10-04", "%Y-%m-%d"), is_buy=True, quantity=3,
                                  cash_after_transaction=money))
    money = money - 5 * 23.01
    trans_list.append(Transaction("AMZN", 23.01, datetime.strptime("2022-10-05", "%Y-%m-%d"), is_buy=True, quantity=5,
                                  cash_after_transaction=money))
    money = money + 5 * 24.05
    trans_list.append(Transaction("AMZN", 24.05, datetime.strptime("2022-10-17", "%Y-%m-%d"), is_buy=False, quantity=5,
                                  cash_after_transaction=money))
    money = money + 8 * 50.64
    trans_list.append(Transaction("ADBE", 50.64, datetime.strptime("2022-10-23", "%Y-%m-%d"), is_buy=False, quantity=8,
                                  cash_after_transaction=money))
    money = money + 2 * 50.64
    trans_list.append(Transaction("ADBE", 80.22, datetime.strptime("2022-10-26", "%Y-%m-%d"), is_buy=False, quantity=2,
                                  cash_after_transaction=money))
    return trans_list


def generateTickerHoldPeriods(transactions: list[Transaction]) -> list[
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


def generateHoldPeriods(transactions: list[Transaction]) -> list[HoldPeriod]:
    transaction_dict: dict[str, list[Transaction]] = {}
    for transaction in transactions:
        if transaction.ticker not in transaction_dict:
            transaction_dict[transaction.ticker] = [transaction]
        else:
            transaction_dict[transaction.ticker].append(transaction)
    hold_periods_to_return = []
    for ticker in transaction_dict:
        hold_periods_to_return += generateTickerHoldPeriods(transaction_dict[ticker])
    return hold_periods_to_return


def initDataframeCash(df, transactions: list[Transaction]):
    df['Date'] = pd.to_datetime(df['Date'])
    date = None
    cash_before = None
    for transaction in transactions:
        if date is not None:
            df.loc[(df['Date'] >= date) & (df['Date'] < transaction.date), 'Value'] = cash_before
        else:
            df.loc[df['Date'] < transaction.date, 'Value'] = 10000
        date = transaction.date
        cash_before = transaction.cash_after_transaction
    df.loc[df['Date'] >= date, 'Value'] = cash_before
    return df

transactions = getTransactions()
hold_periods = generateHoldPeriods(transactions)
created_on = datetime.strptime("2022-09-22", "%Y-%m-%d")

df = yf.download("AAPL", start=created_on.strftime("%Y-%m-%d"), end="2023-04-20")
df.reset_index(inplace=True)
df = df.drop(['Open', 'High', 'Adj Close', 'Volume', 'Low'], axis=1)
df["Close"] = np.nan
df = df.rename(columns={'Close': 'Value'})
initDataframeCash(df, transactions)

print(df)
for hold_period in hold_periods:
    if hold_period is None:
        df2 = yf.download(hold_period.ticker, start=hold_period.start_date)
    else:
        df2 = yf.download(hold_period.ticker, start=hold_period.start_date, end=hold_period.end_date)
    df2.reset_index(inplace=True)
    df2 = df2.drop(['Open', 'High', 'Adj Close', 'Volume', 'Low'], axis=1)
    df = pd.merge(df, df2, on='Date', how='left')
    # Multiply 'close_y' values by 3 and fill missing values with 0
    df['Value_multiplied'] = df['Close'].fillna(0) * hold_period.quantity

    # Add 'close_x' and 'close_y_multiplied' columns
    df['Value'] = df['Value'] + df['Value_multiplied']

    # Select only the 'date' and 'close_sum' columns
    df = df[['Date', 'Value']]

print(df)