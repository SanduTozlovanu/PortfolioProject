class WeightedStockDto:
    def __init__(self, id: int, ticker: str, price: float, quantity: str, marketCap: int):
        self.id = id
        self.ticker = ticker
        self.price = price
        self.quantity = quantity
        self.marketCap = int(marketCap)
