class MomentumStockDto:
    def __init__(self, id: int, ticker: str, price: float, quantity: str, yearChange: float):
        self.id = id
        self.ticker = ticker
        self.price = price
        self.quantity = quantity
        self.yearChange = yearChange
