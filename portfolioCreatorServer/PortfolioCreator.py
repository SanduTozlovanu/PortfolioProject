import pandas as pd
import math
from scipy import stats
from statistics import mean


class PortfolioCreator:
    @staticmethod
    def create_equal_weight_dataframe(stocks_basedata_list, money: float) -> (pd.DataFrame, float):
        columns = ["ticker", "price", "sharesToBuy"]
        df = pd.DataFrame(columns=columns)
        for stock in stocks_basedata_list:
            df.loc[len(df)] = {"ticker": stock["ticker"], "price": stock["price"], "sharesToBuy": 'N/A'}

        return PortfolioCreator.distribute_dataframe_equally(df, money)

    @staticmethod
    def create_weighted_dataframe(stocks_basedata_list, money: float) -> (pd.DataFrame, float):
        columns = ["ticker", "price", "marketCap", "sharesToBuy"]
        df = pd.DataFrame(columns=columns)
        for stock in stocks_basedata_list:
            df.loc[len(df)] = {"ticker": stock["ticker"], "price": stock["price"], "marketCap": stock["marketCap"],
                               "sharesToBuy": 'N/A'}
        total_market_cap = (df['marketCap']).sum()
        for i in range(0, len(df['ticker'])):
            df.loc[i, 'sharesToBuy'] = math.floor(money * (df['marketCap'][i] / total_market_cap) / df['price'][i])
        residual_cash = money - (df['price'] * df['sharesToBuy']).sum()
        return df, residual_cash

    @staticmethod
    def create_filtered_quantitative_momentum_dataframe(stocks_basedata_list, money: float) -> (pd.DataFrame, float):
        df = PortfolioCreator.create_quantitative_momentum_dataframe(stocks_basedata_list)
        df.sort_values('yearChange', ascending=False, inplace=True)
        df = df[:20]
        df.reset_index(drop=True, inplace=True)

        return PortfolioCreator.distribute_dataframe_equally(df, money)

    @staticmethod
    def create_quantitative_momentum_dataframe(stocks_basedata_list) -> (pd.DataFrame, float):
        columns = ['ticker', 'price', 'yearChange', 'sharesToBuy']
        df = pd.DataFrame(columns=columns)
        for stock in stocks_basedata_list:
            df.loc[len(df)] = {"ticker": stock["ticker"], "price": stock["price"], "yearChange": stock["yearChange"],
                               "sharesToBuy": 'N/A'}
        return df

    @staticmethod
    def distribute_dataframe_equally(df: pd.DataFrame, money: float) -> (pd.DataFrame, float):
        for i in range(0, len(df['ticker'])):
            df.loc[i, 'sharesToBuy'] = math.floor(money / len(df.index) / df['price'][i])
        residual_cash = money - (df['price'] * df['sharesToBuy']).sum()
        return df, residual_cash

    @staticmethod
    def create_filtered_quantitative_value_dataframe(stocks_basedata_list, money: float) -> (pd.DataFrame, float):
        df = PortfolioCreator.create_quantitative_value_dataframe(stocks_basedata_list)

        df.sort_values(by='score', inplace=True, ascending=False)
        df = df[:20]
        df.reset_index(drop=True, inplace=True)

        return PortfolioCreator.distribute_dataframe_equally(df, money)

    @staticmethod
    def create_quantitative_value_dataframe(stocks_basedata_list) -> pd.DataFrame:
        columns = ['ticker', 'price', "sharesToBuy", 'ebtPerEbit', 'ebtPerEbitPercent', 'peRatio', 'peRatioPercent',
                   'priceToBookRatio', 'priceToBookRatioPercent', 'priceToSales', 'priceToSalesPercent',
                   'profitMargin', 'profitMarginPercent', 'operatingMargin', 'operatingMarginPercent',
                   'freeCashFlowYield', 'freeCashFlowYieldPercent', 'evToEbitda', 'evToEbitdaPercent', 'score']
        df = pd.DataFrame(columns=columns)
        for stock in stocks_basedata_list:
            df.loc[len(df)] = {"ticker": stock["ticker"], "price": stock["price"], "ebtPerEbit": stock["ebtPerEbit"],
                               "sharesToBuy": 'N/A', "ebtPerEbitPercent": 'N/A', "peRatio": stock['peRatio'],
                               "peRatioPercent": 'N/A', "priceToBookRatio": stock['priceToBookRatio'],
                               'priceToBookRatioPercent': 'N/A', "priceToSales": stock["priceToSales"],
                               "priceToSalesPercent": 'N/A', "profitMargin": stock["profitMargin"],
                               "profitMarginPercent": 'N/A', "operatingMargin": stock['operatingMargin'],
                               'operatingMarginPercent': 'N/A', "freeCashFlowYield": stock["freeCashFlowYield"],
                               "freeCashFlowYieldPercent": "N/A", "evToEbitda": stock["evToEbitda"],
                               "evToEbitdaPercent": "N/A", 'score': "N/A"}
        ratio_percentile_dict = {
            "ebtPerEbit": ["ebtPerEbitPercent", True], "peRatio": ["peRatioPercent", False],
            "evToEbitda": ["evToEbitdaPercent", True],
            "priceToBookRatio": ["priceToBookRatioPercent", False], "priceToSales": ["priceToSalesPercent", False],
            "profitMargin": ["profitMarginPercent", True], "operatingMargin": ["operatingMarginPercent", True],
            "freeCashFlowYield": ["freeCashFlowYieldPercent", True]
        }
        for row in df.index:
            for ratio_percentile in ratio_percentile_dict.keys():
                if ratio_percentile_dict[ratio_percentile][1]:
                    df.loc[row, ratio_percentile_dict[ratio_percentile][0]] = stats.percentileofscore(
                        df[ratio_percentile], df.loc[row, ratio_percentile])
                else:
                    df.loc[row, ratio_percentile_dict[ratio_percentile][0]] = 100 - stats.percentileofscore(
                        df[ratio_percentile], df.loc[row, ratio_percentile])

        for row in df.index:
            value_percents = []
            for ratio_percentile in ratio_percentile_dict.keys():
                value_percents.append(df.loc[row, ratio_percentile_dict[ratio_percentile][0]])
            df.loc[row, 'score'] = mean(value_percents)

        columns_to_delete = ["ebtPerEbitPercent", "evToEbitdaPercent", "peRatioPercent",
                             "priceToBookRatioPercent", "priceToSalesPercent", "profitMarginPercent",
                             "operatingMarginPercent", "freeCashFlowYieldPercent"]

        df = df.drop(columns_to_delete, axis=1)

        return df

    @staticmethod
    def create_quantitative_value_momentum_dataframe(value_basedata_list, momentum_basedata_list) -> (
            pd.DataFrame, float):
        value_df = PortfolioCreator.create_quantitative_value_dataframe(value_basedata_list)
        momentum_df = PortfolioCreator.create_quantitative_momentum_dataframe(momentum_basedata_list)
        momentum_df['momentumPercent'] = "N/A"
        for row in momentum_df.index:
            momentum_df.loc[row, "momentumPercent"] = stats.percentileofscore(
                momentum_df["yearChange"], momentum_df.loc[row, "yearChange"])
        merged_df = pd.merge(value_df, momentum_df, on='ticker')
        merged_df['mean'] = (merged_df['score'] + merged_df['momentumPercent']) / 2

        columns_to_delete = ["score", "sharesToBuy_y", "price_y"]

        merged_df = merged_df.drop(columns_to_delete, axis=1)
        new_columns_names = {"price_x": "price", "sharesToBuy_x": "sharesToBuy", "mean": "score"}
        merged_df = merged_df.rename(columns=new_columns_names)
        return merged_df

    @staticmethod
    def create_filtered_quantitative_value_momentum_dataframe(value_basedata_list, momentum_basedata_list,
                                                              money: float) -> (pd.DataFrame, float):
        df = PortfolioCreator.create_quantitative_value_momentum_dataframe(value_basedata_list, momentum_basedata_list)

        df.sort_values(by='score', inplace=True, ascending=False)
        df = df[:20]
        df.reset_index(drop=True, inplace=True)

        return PortfolioCreator.distribute_dataframe_equally(df, money)
