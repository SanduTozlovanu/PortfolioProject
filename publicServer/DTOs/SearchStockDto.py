class SearchStockDto:
    def __init__(self, id: int, name: str, ticker:str, marketCap: int, beta: float, price: float, sector: str):
        self.id = id
        self.ticker = ticker
        self.name = name
        self.marketCap = marketCap
        self.beta = beta
        self.price = price
        self.sector = sector

