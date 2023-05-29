class CreatedPortfolioDto:
    def __init__(self, columns, cash: float, data: list):
        self.columns = columns
        self.cash = round(cash, 2)
        self.data = data
