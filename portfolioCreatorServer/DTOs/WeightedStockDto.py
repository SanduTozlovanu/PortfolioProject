class WeightedStockDto:
    def __init__(self, id: int, ticker: str, price: float, quantity: str, marketCap: int):
        self.id = id
        self.ticker = ticker
        self.price = price
        self.quantity = quantity
        self.marketCap = WeightedStockDto.number_to_string(int(marketCap))

    @staticmethod
    def number_to_string(number):
        suffixes = ["", "Th", "Ml", "Bl", "Tr", "Qd", "Qt"]

        if number == 0:
            return "Zero"

        # Calculate the magnitude of the number
        magnitude = 0
        while abs(number) >= 1000:
            magnitude += 1
            number /= 1000.0

        # Format the number with the appropriate suffix
        formatted_number = "{:.2f}".format(number).rstrip("0").rstrip(".")
        return f"{formatted_number} {suffixes[magnitude]}"