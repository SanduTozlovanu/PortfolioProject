class ColumnCreator:
    @staticmethod
    def __get_column(field: str, headerName: str, width: int):
        return dict(
            field=field,
            headerName=headerName,
            width=width
        )

    @staticmethod
    def __get_id():
        return ColumnCreator.__get_column("id", "Id", 30)

    @staticmethod
    def __get_ticker():
        return ColumnCreator.__get_column("ticker", "Ticker", 50)

    @staticmethod
    def __get_quantity():
        return ColumnCreator.__get_column("quantity", "Number of Shares", 30)

    @staticmethod
    def __get_market_cap():
        return ColumnCreator.__get_column("marketCap", "Market Cap", 150)

    @staticmethod
    def __get_year_change():
        return ColumnCreator.__get_column("yearChange", "Year change", 50)

    @staticmethod
    def __get_score():
        return ColumnCreator.__get_column("score", "Score", 50)

    @staticmethod
    def __get_ebtPerEbit():
        return ColumnCreator.__get_column("ebtPerEbit", "EBT/EBIT", 50)

    @staticmethod
    def __get_pe_ratio():
        return ColumnCreator.__get_column("peRatio", "P/E", 50)

    @staticmethod
    def __get_price_to_book():
        return ColumnCreator.__get_column("priceToBookRatio", "Price To Book Ratio", 50)

    @staticmethod
    def __get_price_to_sales():
        return ColumnCreator.__get_column("priceToSales", "Price to Sales", 50)

    @staticmethod
    def __get_profit_margin():
        return ColumnCreator.__get_column("profitMargin", "Profit to Margin", 50)

    @staticmethod
    def __get_operating_margin():
        return ColumnCreator.__get_column("operatingMargin", "Operating Margin", 50)

    @staticmethod
    def __get_free_cashflow_yield():
        return ColumnCreator.__get_column("freeCashFlowYield", "Free CashFlow Yield", 50)

    @staticmethod
    def __get_ev_ebitda():
        return ColumnCreator.__get_column("evToEbitdaPercent", "EV/EBITDA", 50)

    @staticmethod
    def __get_base_columns() -> list:
        return [ColumnCreator.__get_id(), ColumnCreator.__get_ticker(), ColumnCreator.__get_quantity()]

    @staticmethod
    def __add_value_columns(columns: list) -> list:
        columns_to_be_added = [ColumnCreator.__get_ebtPerEbit(), ColumnCreator.__get_ev_ebitda(),
                               ColumnCreator.__get_operating_margin(), ColumnCreator.__get_pe_ratio(),
                               ColumnCreator.__get_price_to_book(), ColumnCreator.__get_profit_margin(),
                               ColumnCreator.__get_price_to_sales(), ColumnCreator.__get_free_cashflow_yield(),
                               ColumnCreator.__get_score()]
        return columns + columns_to_be_added

    @staticmethod
    def get_equal_weight_stocks_columns() -> list:
        return ColumnCreator.__get_base_columns()

    @staticmethod
    def get_weighted_stocks_columns() -> list:
        columns = ColumnCreator.__get_base_columns()
        columns.append(ColumnCreator.__get_market_cap())
        return columns

    @staticmethod
    def get_momentum_stocks_columns() -> list:
        columns = ColumnCreator.__get_base_columns()
        columns.append(ColumnCreator.__get_year_change())
        return columns

    @staticmethod
    def get_value_stocks_columns() -> list:
        columns = ColumnCreator.__get_base_columns()
        return ColumnCreator.__add_value_columns(columns)

    @staticmethod
    def get_value_momentum_stocks_columns() -> list:
        columns = ColumnCreator.__get_base_columns()
        columns.append(ColumnCreator.__get_year_change())
        return ColumnCreator.__add_value_columns(columns)
