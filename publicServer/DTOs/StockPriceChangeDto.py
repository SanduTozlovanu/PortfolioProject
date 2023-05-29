class StockPriceChangeDto:
    def __init__(self, ticker: str, price: float, yearChange: float):
        self.ticker = ticker
        self.yearChange = round(yearChange, 2)
        self.price = round(price, 2)
