class ValueStockDto:
    def __init__(self, id: int, ticker: str, price: float, quantity: str, ebtPerEbit: float, peRatio: float,
                 priceToBookRatio: float, priceToSales: float, profitMargin: float, operatingMargin: float,
                 freeCashFlowYield: float, evToEbitda: float, score: float):
        self.id = id
        self.ticker = ticker
        self.price = price
        self.quantity = quantity
        self.ebtPerEbit = ebtPerEbit
        self.peRatio = peRatio
        self.priceToBookRatio = priceToBookRatio
        self.priceToSales = priceToSales
        self.profitMargin = profitMargin
        self.operatingMargin = operatingMargin
        self.freeCashFlowYield = freeCashFlowYield
        self.evToEbitda = evToEbitda
        self.score = round(score, 2)
