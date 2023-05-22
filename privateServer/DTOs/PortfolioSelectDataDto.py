class PortfolioSelectDataDto:
    def __init__(self, label: str, value: str, price: float, number: int):
        self.label = label
        self.value = value
        self.price = price
        self.number = number
