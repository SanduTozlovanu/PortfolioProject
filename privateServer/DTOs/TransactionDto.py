from datetime import datetime


class TransactionDto:
    def __init__(self, id: int, ticker: str, piece_price: float, quantity: int, date: datetime, is_buy: bool):
        self.id = id
        self.ticker = ticker
        self.piece_price = str(float(round(piece_price, 2))) + "$"
        self.total_price = str(float(round(piece_price * quantity, 2))) + "$"
        self.quantity = quantity
        self.date = date.strftime("%Y-%m-%d")
        if is_buy:
            self.is_buy = "buy"
        else:
            self.is_buy = "sell"
