class TickerPriceDto:
    def __init__(self, ticker: str, change: float):
        self.ticker = ticker
        self.change = round(change, 2)
