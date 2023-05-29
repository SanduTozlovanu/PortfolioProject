class StockBasedataDto:
    def __init__(self, ticker: str, marketCap: int, price: float):
        self.ticker = ticker
        self.marketCap = marketCap
        self.price = price

